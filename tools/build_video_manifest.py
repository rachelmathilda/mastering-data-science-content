import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    items = []
    for f in sorted((ROOT / "courses").glob("*/m[0-9][0-9].json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        v = d["video"]
        if v.get("needed"):
            items.append(
                {
                    "course_id": d["course_id"],
                    "module_no": d["module_no"],
                    "module_title": d["title"],
                    "kind": v["kind"],
                    "reason": v["reason"],
                    "brief": v["brief"],
                    "status": "todo",
                }
            )
    out = {"note": "kind: ai_slides dibuat dari brief oleh generator video AI, screen_record direkam dari layar, shoot direkam langsung", "items": items}
    (ROOT / "video_manifest.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("video items", len(items))


if __name__ == "__main__":
    main()
