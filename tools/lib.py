import ast
import json
import math
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_VERSION = 2
LEVEL_LABEL = {"mudah": "Mudah", "sedang": "Sedang", "menantang": "Tantangan"}
CALLOUT_TITLE = {"tip": "Tips", "note": "Catatan", "warning": "Perhatian", "info": "Info"}


def _c(s):
    return textwrap.dedent(s).strip("\n").rstrip()


def _words(s):
    return len(re.findall(r"\w+", s))


def T(md):
    return {"type": "text", "markdown": _c(md)}


def K(kind, md, title=None):
    return {"type": "callout", "kind": kind, "title": title or CALLOUT_TITLE.get(kind, "Catatan"), "markdown": _c(md)}


def A(title, text, image=None):
    return {"type": "analogy", "title": title, "text": _c(text), "image": image}


def C(code, expected, explanation, filename=None):
    code = _c(code)
    if not filename:
        m = re.search(r"^def\s+([A-Za-z_]\w*)", code, re.M)
        filename = (m.group(1) + ".py") if m else "contoh.py"
    return {
        "type": "code_example",
        "filename": filename,
        "runnable": True,
        "code": code,
        "expected_output_note": _c(expected),
        "explanation": _c(explanation),
    }


def S(code, note):
    return {"type": "code_static", "language": "python", "code": _c(code), "note": _c(note)}


def QC(q, options, answer_index, explanation):
    return {"question": q, "options": list(options), "answer_index": answer_index, "explanation": explanation}


def _split_tests(src, names=None):
    tree = ast.parse(src)
    setup = []
    cases = []
    pending = []
    seen_assert = False

    def seg(node):
        return ast.get_source_segment(src, node)

    def has_assert(node):
        return any(isinstance(n, ast.Assert) for n in ast.walk(node))

    def label_of(node):
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                s = " ".join(seg(n).split())
                return s if len(s) <= 48 else s[:45] + "..."
        return "assert"

    for node in tree.body:
        if not seen_assert and not has_assert(node) and isinstance(node, (ast.Import, ast.ImportFrom)):
            setup.append(seg(node))
            continue
        if has_assert(node):
            seen_assert = True
            code = "\n".join(pending + [seg(node)])
            pending = []
            cases.append({"label": label_of(node), "code": code})
        else:
            pending.append(seg(node))
    if pending:
        if cases:
            cases[-1]["code"] += "\n" + "\n".join(pending)
        else:
            cases.append({"label": "kode", "code": "\n".join(pending)})
    out = []
    for i, c in enumerate(cases, 1):
        nm = None
        if names and i <= len(names):
            nm = names[i - 1]
        name = "Kasus %d" % i
        ok = "Lolos"
        fail = None
        if nm:
            if isinstance(nm, str):
                name = nm
            else:
                name = nm[0]
                ok = nm[1] if len(nm) > 1 and nm[1] else ok
                fail = nm[2] if len(nm) > 2 else None
        out.append(
            {"id": i, "name": name, "label": c["label"], "pass_message": ok, "fail_hint": fail, "code": c["code"]}
        )
    return {"setup": "\n".join(setup), "cases": out}


def _split_instruction(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`])", text, maxsplit=1)
    main = parts[0]
    note = parts[1] if len(parts) > 1 else None
    return main, note


def E(eid, level, instruction, starter, tests, hint, solution, names=None, filename="solution.py"):
    main, note = _split_instruction(_c(instruction))
    return {
        "type": "exercise",
        "id": eid,
        "level": level,
        "level_label": LEVEL_LABEL[level],
        "instruction": main,
        "note": note,
        "filename": filename,
        "starter_code": _c(starter),
        "tests": _split_tests(_c(tests), names),
        "hint": _c(hint),
        "solution": _c(solution),
    }


def _opt(o):
    if isinstance(o, dict):
        return {"label": o["label"], "description": o.get("description", "")}
    if isinstance(o, (tuple, list)):
        return {"label": o[0], "description": o[1] if len(o) > 1 else ""}
    return {"label": o, "description": ""}


def Q(q, options, answer_index, explanation, hint=None, code=None):
    return {
        "q": q,
        "code": code,
        "options": [_opt(o) for o in options],
        "answer_index": answer_index,
        "hint": hint,
        "explanation": explanation,
    }


def M(mistake, fix):
    return {"mistake": mistake, "fix": fix}


def _block_words(b):
    t = b["type"]
    if t in ("text", "callout"):
        return _words(b["markdown"])
    if t == "analogy":
        return _words(b["text"])
    if t == "code_example":
        return _words(b["explanation"]) + 25
    if t == "code_static":
        return _words(b["note"]) + 25
    return 0


def _partition(blocks, n=3):
    total = sum(_block_words(b) for b in blocks)
    parts = [[]]
    cum = 0
    k = 1
    for b in blocks:
        if k < n and cum >= total * k / n and b["type"] == "text" and parts[-1]:
            parts.append([])
            k += 1
        parts[-1].append(b)
        cum += _block_words(b)
    if len(parts) != n:
        idx = [i for i, b in enumerate(blocks) if b["type"] == "text"]
        starts = [0, idx[len(idx) // 3], idx[(2 * len(idx)) // 3]]
        parts = [blocks[starts[0]:starts[1]], blocks[starts[1]:starts[2]], blocks[starts[2]:]]
    return parts


def _part_title(part, no):
    for b in part:
        if b["type"] == "text":
            m = re.search(r"^##\s+(.+)$", b["markdown"], re.M)
            if m:
                return m.group(1).strip()
    return "Bagian %d" % no


def _derive_quick(q, i):
    labels = [o["label"] for o in q["options"]]
    correct = labels[q["answer_index"]]
    wrong = next(l for j, l in enumerate(labels) if j != q["answer_index"])
    if i % 2 == 0:
        opts, ans = [correct, wrong], 0
    else:
        opts, ans = [wrong, correct], 1
    return {
        "question": q["q"],
        "options": opts,
        "answer_index": ans,
        "explanation": q["explanation"],
        "derived_from_quiz": i,
    }


def lesson(lid, title, minutes, objectives, sections, mistakes, quiz, summary, reading, quick_checks=None, catatan=None):
    blocks = [s for s in sections if s["type"] != "exercise"]
    exercises = [s for s in sections if s["type"] == "exercise"]
    for n, ex in enumerate(exercises, 1):
        ex["title"] = "Latihan %d" % n
    parts_blocks = _partition(blocks, 3)
    parts = []
    for i, pb in enumerate(parts_blocks):
        w = sum(_block_words(b) for b in pb)
        if quick_checks and i < len(quick_checks):
            qc = dict(quick_checks[i])
        else:
            qc = _derive_quick(quiz[i], i)
        parts.append(
            {
                "part_no": i + 1,
                "title": _part_title(pb, i + 1),
                "read_minutes": max(1, math.ceil(w / 170)),
                "blocks": pb,
                "quick_check": qc,
            }
        )
    notebook = [{"type": "text", "source": "# " + title}]
    for b in blocks:
        if b["type"] == "code_example":
            notebook.append({"type": "text", "source": b["explanation"]})
            notebook.append({"type": "code", "source": b["code"]})
    if catatan:
        note = {"text": _c(catatan), "source": "author"}
    else:
        m0 = mistakes[0]
        note = {"text": "Hindari: %s Lebih baik: %s" % (m0["mistake"], m0["fix"]), "source": "common_mistake"}
    return {
        "lesson_id": lid,
        "title": title,
        "estimated_minutes": minutes,
        "read_minutes": sum(p["read_minutes"] for p in parts),
        "objectives": objectives,
        "parts": parts,
        "exercises": exercises,
        "quiz": quiz,
        "author_note": note,
        "common_mistakes": mistakes,
        "summary": summary,
        "further_reading": reading,
        "notebook": {"cells": notebook},
    }


def _preview(ex):
    lines = [l for l in ex["starter_code"].splitlines() if l.strip()]
    start = next((i for i, l in enumerate(lines) if l.startswith("def ")), None)
    if start is None:
        keep = [l for l in lines if "TODO" not in l and not l.startswith(("import ", "from "))]
        return "\n".join((keep or lines)[:3])
    out = [lines[start]]
    for l in lines[start + 1:]:
        if not l.startswith((" ", "\t")):
            break
        if "TODO" in l or l.strip() == "pass":
            continue
        out.append(l)
        if len(out) >= 3:
            break
    if len(out) == 1:
        out.append("    ...")
    return "\n".join(out)


def write_module(course_id, module_no, title, minutes, outcomes, lessons, video, references):
    all_ex = [(l["lesson_id"], e) for l in lessons for e in l["exercises"]]
    pick = next((x for x in all_ex if x[1]["level"] == "menantang"), all_ex[-1])
    data = {
        "schema_version": SCHEMA_VERSION,
        "course_id": course_id,
        "module_no": module_no,
        "title": title,
        "estimated_minutes": minutes,
        "learning_outcomes": outcomes,
        "lesson_count": len(lessons),
        "exercise_count": len(all_ex),
        "practice_preview": {
            "lesson_id": pick[0],
            "exercise_id": pick[1]["id"],
            "level_label": pick[1]["level_label"],
            "code_preview": _preview(pick[1]),
        },
        "lessons": lessons,
        "video": video,
        "references": references,
    }
    d = ROOT / "courses" / course_id
    d.mkdir(parents=True, exist_ok=True)
    out = d / ("m%02d.json" % module_no)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out)
