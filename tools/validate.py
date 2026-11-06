import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ALLOWED = {
    "numpy", "pandas", "scipy", "sklearn", "matplotlib", "seaborn", "statsmodels", "networkx", "sqlite3",
    "math", "random", "json", "re", "itertools", "collections", "statistics", "datetime", "io", "csv",
    "string", "functools", "heapq", "bisect", "struct", "hashlib", "time", "textwrap", "dataclasses",
    "typing", "copy", "operator", "decimal", "fractions", "zlib", "base64", "warnings", "enum", "abc",
    "array", "pprint", "contextlib", "uuid", "calendar", "secrets",
}
BLOCK_TYPES = {"text", "code_example", "code_static", "callout", "analogy"}
MIN = {"text": 4, "code_example": 3, "exercise": 4}
MIN_WORDS = 650
TIMEOUT = 40


def words(s):
    return len(re.findall(r"\w+", s))


def check_imports(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return ["syntax error: %s" % e]
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in ALLOWED:
                    bad.append("import %s" % a.name)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED:
                bad.append("import from %s" % node.module)
    return bad


def run(code):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "snippet.py"
        p.write_text(code, encoding="utf-8")
        env = dict(os.environ)
        env["MPLBACKEND"] = "Agg"
        env["PYTHONHASHSEED"] = "0"
        try:
            r = subprocess.run(
                [sys.executable, "-I", str(p)], cwd=d, env=env, capture_output=True, text=True, timeout=TIMEOUT
            )
            return r.returncode, (r.stderr or "")[-600:]
        except subprocess.TimeoutExpired:
            return 124, "timeout"


def validate_module(path):
    errs = []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for k in ("schema_version", "course_id", "module_no", "title", "estimated_minutes", "learning_outcomes", "lesson_count", "exercise_count", "practice_preview", "lessons", "video", "references"):
        if k not in data:
            errs.append("module missing %s" % k)
    if errs:
        return errs
    if data["schema_version"] != 2:
        errs.append("schema_version must be 2")
    if len(data["learning_outcomes"]) < 3:
        errs.append("learning_outcomes < 3")
    v = data["video"]
    if v.get("kind") not in {"ai_slides", "screen_record", "shoot", "none"}:
        errs.append("video.kind invalid")
    if v.get("needed") and not v.get("brief"):
        errs.append("video needed but no brief")
    if not 3 <= len(data["lessons"]) <= 5:
        errs.append("lessons must be 3 to 5, got %d" % len(data["lessons"]))
    pp = data["practice_preview"]
    for k in ("lesson_id", "exercise_id", "level_label", "code_preview"):
        if not pp.get(k):
            errs.append("practice_preview missing %s" % k)
    jobs = []
    ids = set()
    for les in data["lessons"]:
        lid = les.get("lesson_id", "?")
        tag = "%s" % lid
        for k in ("lesson_id", "title", "estimated_minutes", "read_minutes", "objectives", "parts", "exercises", "quiz", "author_note", "common_mistakes", "summary", "further_reading", "notebook"):
            if k not in les:
                errs.append("%s missing %s" % (tag, k))
        if "parts" not in les or "exercises" not in les:
            continue
        if lid in ids:
            errs.append("%s duplicate lesson_id" % tag)
        ids.add(lid)
        if len(les["objectives"]) < 3:
            errs.append("%s objectives < 3" % tag)
        if len(les["summary"]) < 4:
            errs.append("%s summary < 4" % tag)
        if len(les["common_mistakes"]) < 2:
            errs.append("%s common_mistakes < 2" % tag)
        if len(les["quiz"]) < 5:
            errs.append("%s quiz < 5" % tag)
        for qi, q in enumerate(les["quiz"]):
            opts = q.get("options", [])
            if not (0 <= q.get("answer_index", -1) < len(opts)) or len(opts) < 3:
                errs.append("%s quiz %d invalid" % (tag, qi))
            if any(not isinstance(o, dict) or not o.get("label") for o in opts):
                errs.append("%s quiz %d options must be objects with label" % (tag, qi))
            if not q.get("explanation"):
                errs.append("%s quiz %d no explanation" % (tag, qi))
        if len(les["parts"]) != 3:
            errs.append("%s parts must be 3, got %d" % (tag, len(les["parts"])))
        counts = {}
        total_words = 0
        for pi, part in enumerate(les["parts"], 1):
            for k in ("part_no", "title", "read_minutes", "blocks", "quick_check"):
                if k not in part:
                    errs.append("%s part %d missing %s" % (tag, pi, k))
            qc = part.get("quick_check") or {}
            if not (len(qc.get("options", [])) in (2, 3) and 0 <= qc.get("answer_index", -1) < len(qc.get("options", []))):
                errs.append("%s part %d quick_check invalid" % (tag, pi))
            if not part.get("blocks") or part["blocks"][0].get("type") != "text":
                errs.append("%s part %d must start with text" % (tag, pi))
            for s in part.get("blocks", []):
                t = s.get("type")
                if t not in BLOCK_TYPES:
                    errs.append("%s bad block type %s" % (tag, t))
                    continue
                counts[t] = counts.get(t, 0) + 1
                if t in ("text", "callout"):
                    total_words += words(s.get("markdown", ""))
                if t == "analogy":
                    total_words += words(s.get("text", ""))
                if t == "code_example":
                    total_words += words(s.get("explanation", ""))
                    if not s.get("filename"):
                        errs.append("%s code_example no filename" % tag)
                    bad = check_imports(s["code"])
                    if bad:
                        errs.append("%s code_example imports %s" % (tag, bad))
                    else:
                        jobs.append(("%s code_example" % tag, s["code"], 0))
                elif t == "code_static":
                    if not s.get("note"):
                        errs.append("%s code_static no note" % tag)
        ex_ids = set()
        for ex in les["exercises"]:
            for k in ("id", "level", "level_label", "title", "instruction", "filename", "starter_code", "tests", "hint", "solution"):
                if not ex.get(k):
                    errs.append("%s exercise missing %s" % (tag, k))
            if ex.get("id") in ex_ids:
                errs.append("%s duplicate exercise id" % tag)
            ex_ids.add(ex.get("id"))
            tests = ex.get("tests") or {}
            cases = tests.get("cases", [])
            if len(cases) < 3:
                errs.append("%s %s needs >= 3 test cases" % (tag, ex.get("id")))
            if not ex.get("solution") or not cases:
                continue
            body = tests.get("setup", "") + "\n" + "\n".join(c["code"] for c in cases)
            bad = check_imports(ex["solution"]) + check_imports(body) + check_imports(ex["starter_code"])
            if bad:
                errs.append("%s exercise %s imports %s" % (tag, ex.get("id"), bad))
                continue
            jobs.append(("%s %s solution" % (tag, ex["id"]), ex["solution"] + "\n" + body, 0))
            jobs.append(("%s %s starter" % (tag, ex["id"]), ex["starter_code"] + "\n" + body, 1))
        counts["exercise"] = len(les["exercises"])
        for t, n in MIN.items():
            if counts.get(t, 0) < n:
                errs.append("%s %s < %d (got %d)" % (tag, t, n, counts.get(t, 0)))
        if total_words < MIN_WORDS:
            errs.append("%s words %d < %d" % (tag, total_words, MIN_WORDS))
    blob = json.dumps(data, ensure_ascii=False)
    if "\u2014" in blob or "\u2013" in blob:
        errs.append("contains em or en dash")
    if re.search(r"\s--\s", blob):
        errs.append("contains double dash")

    def work(job):
        name, code, expect_fail = job
        rc, err = run(code)
        if expect_fail:
            if rc == 0:
                return "%s: starter passes tests, should fail" % name
            if rc == 124:
                return "%s: starter timeout" % name
            return None
        if rc != 0:
            return "%s: rc=%s %s" % (name, rc, err.strip().splitlines()[-1] if err.strip() else "")
        return None

    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(work, jobs):
            if r:
                errs.append(r)
    return errs


def main():
    paths = sys.argv[1:]
    bad = 0
    for p in paths:
        errs = validate_module(p)
        if errs:
            bad += 1
            print("FAIL", p)
            for e in errs:
                print("  -", e)
        else:
            print("OK  ", p)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
