import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_meta import BOOKS, FIRST_PREREQ, ICONS, META, TRACK_LABEL

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "outlines.txt"
TRACKS = {
    "A": "Fondasi",
    "B": "Data Wrangling dan Visualisasi",
    "C": "Statistik dan Inferensi",
    "D": "Machine Learning",
    "E": "Deep Learning, Graph, dan Framework",
    "F": "Data Engineering",
    "G": "Capstone",
    "H": "ML Systems dan MLOps",
    "I": "Elective",
}


def parse():
    courses = []
    current = None
    for raw in SRC.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("@"):
            parts = [p.strip() for p in line[1:].split("|")]
            cid, title, track, level, n, ref = parts
            current = {
                "id": cid,
                "title": title,
                "track": track,
                "track_name": TRACKS[track],
                "level": level,
                "expected_modules": int(n),
                "reference": ref,
                "modules": [],
            }
            courses.append(current)
        else:
            m = re.match(r"(\d+)\s*\|\s*(.+)", line)
            no, title = int(m.group(1)), m.group(2).strip()
            current["modules"].append({"module_no": no, "title": title})
    return courses


def sources(ref):
    out = []
    for m in re.finditer(r"([A-Z]{2,4})\s+bab\s+(.+?)(?=,\s*[A-Z]{2,4}\s+bab|$)", ref):
        b = BOOKS[m.group(1)]
        out.append({"code": m.group(1), "title": b["title"], "author": b["author"], "chapters": "bab " + m.group(2)})
    return out


def main():
    courses = parse()
    total_modules = 0
    for c in courses:
        assert len(c["modules"]) == c["expected_modules"], (c["id"], len(c["modules"]), c["expected_modules"])
        nos = [m["module_no"] for m in c["modules"]]
        assert nos == list(range(1, len(nos) + 1)), c["id"]
        assert c["id"] in META, c["id"]
        assert len(META[c["id"]][1]) <= 20, c["id"]
        total_modules += len(c["modules"])
    cdir = ROOT / "courses"
    index = {"schema_version": 2, "content_version": 2, "curriculum_version": "1.0", "icons": ICONS, "courses": []}
    prev_in_track = {}
    for c in courses:
        d = cdir / c["id"]
        d.mkdir(parents=True, exist_ok=True)
        title_id, short, icon = META[c["id"]]
        modules = []
        done = 0
        minutes = 0
        n_ex = 0
        for m in c["modules"]:
            f = d / ("m%02d.json" % m["module_no"])
            entry = {
                "module_no": m["module_no"],
                "title": m["title"],
                "file": f.name,
                "status": "todo",
                "estimated_minutes": 105,
                "lesson_count": 3,
                "exercise_count": 12,
                "practice_preview": None,
            }
            if f.exists():
                data = json.loads(f.read_text(encoding="utf-8"))
                entry["status"] = "ready"
                entry["estimated_minutes"] = data["estimated_minutes"]
                entry["lesson_count"] = data["lesson_count"]
                entry["exercise_count"] = data["exercise_count"]
                entry["practice_preview"] = data["practice_preview"]
                done += 1
            minutes += entry["estimated_minutes"]
            n_ex += entry["exercise_count"]
            modules.append(entry)
        if c["id"] in FIRST_PREREQ:
            prereq = FIRST_PREREQ[c["id"]]
        elif c["track"] in prev_in_track:
            prereq = [prev_in_track[c["track"]]]
        else:
            prereq = []
        prev_in_track[c["track"]] = c["id"]
        common = {
            "id": c["id"],
            "title": title_id,
            "title_short": short,
            "icon": icon,
            "track": c["track"],
            "track_label": TRACK_LABEL[c["track"]],
            "track_name": c["track_name"],
            "level": c["level"],
            "module_count": len(modules),
            "total_minutes": minutes,
            "exercise_count": n_ex,
            "prerequisites": prereq,
            "lock_policy": "recommended",
        }
        outline = dict(common)
        outline.update(
            {
                "course_id": c["id"],
                "curriculum_version": "1.0",
                "has_certificate": True,
                "certificate": {"title": title_id, "scope": "Modul kurikulum penuh", "id_prefix": "MDS-" + c["id"]},
                "sources": sources(c["reference"]),
                "modules": modules,
            }
        )
        (d / "outline.json").write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")
        item = dict(common)
        item["modules_ready"] = done
        item["url"] = "courses/%s/outline.json" % c["id"]
        index["courses"].append(item)
    (ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    ready = sum(c["modules_ready"] for c in index["courses"])
    lines = ["# Status Konten", "", "Courses: %d. Modul: %d. Siap: %d." % (len(courses), total_modules, ready), ""]
    lines.append("| Kode | Judul | Siap | Total |")
    lines.append("|---|---|---|---|")
    for c in index["courses"]:
        lines.append("| %s | %s | %d | %d |" % (c["id"], c["title"], c["modules_ready"], c["module_count"]))
    (ROOT / "STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("courses", len(courses), "modules", total_modules, "ready", ready)


if __name__ == "__main__":
    sys.exit(main())
