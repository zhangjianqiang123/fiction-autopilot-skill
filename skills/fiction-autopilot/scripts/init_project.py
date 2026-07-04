from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


INVALID_PATH_CHARS = r'<>:"/\\|?*'


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(title: str) -> str:
    value = "".join("-" if ch.isspace() else ch for ch in title.strip())
    value = "".join(ch for ch in value if ch not in INVALID_PATH_CHARS)
    value = re.sub(r"-+", "-", value).strip(".-")
    if value:
        return value[:80]
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:10]
    return f"novel-{digest}"


def dump_json(path: Path, data: dict[str, Any], *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_project(args: argparse.Namespace) -> dict[str, Any]:
    missing = []
    for field in ("title", "genre", "chapters", "chapter_words", "audience", "style", "forbidden_content"):
        if getattr(args, field) in (None, ""):
            missing.append(field)
    if missing:
        raise SystemExit(f"Missing required arguments: {', '.join(missing)}")

    root = Path(args.root)
    slug = args.slug or slugify(args.title)
    project_dir = root / slug
    for child in ("stages", "characters", "chapters", "memory", "reports"):
        (project_dir / child).mkdir(parents=True, exist_ok=True)

    project = {
        "title": args.title,
        "slug": slug,
        "genre": args.genre,
        "target_chapters": int(args.chapters),
        "chapter_words": int(args.chapter_words),
        "audience": args.audience,
        "style_reference": args.style,
        "forbidden_content": args.forbidden_content,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    state = {
        "project_slug": slug,
        "current_phase": "market_positioning",
        "awaiting_confirmation": False,
        "pending_artifact": None,
        "confirmed_stages": [],
        "confirmed_chapter_cards": [],
        "confirmed_chapters": [],
        "next_chapter": 1,
        "revision_required": False,
        "revision_source": None,
        "rejected_artifacts": [],
        "revision_requests": [],
        "last_updated": now_iso(),
    }

    dump_json(project_dir / "project.json", project, overwrite=args.force)
    dump_json(project_dir / "state.json", state, overwrite=args.force)

    report = project_dir / "reports" / "quality_report.md"
    if args.force or not report.exists():
        report.write_text("# Quality Report\n\n", encoding="utf-8")

    return {"project_dir": str(project_dir), "project": project, "state": state}


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a file-based fiction-autopilot project.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--genre", required=True)
    parser.add_argument("--chapters", type=int, required=True)
    parser.add_argument("--chapter-words", type=int, required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--style", required=True)
    parser.add_argument("--forbidden-content", required=True)
    parser.add_argument("--root", default="novels")
    parser.add_argument("--slug")
    parser.add_argument("--force", action="store_true", help="Overwrite project.json and state.json if they exist.")
    args = parser.parse_args()

    result = create_project(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
