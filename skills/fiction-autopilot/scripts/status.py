from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_status(project_dir: Path) -> dict[str, Any]:
    project = read_json(project_dir / "project.json")
    state = read_json(project_dir / "state.json")
    return {
        "project_dir": str(project_dir),
        "title": project.get("title"),
        "genre": project.get("genre"),
        "target_chapters": project.get("target_chapters"),
        "chapter_words": project.get("chapter_words"),
        "current_phase": state.get("current_phase"),
        "awaiting_confirmation": state.get("awaiting_confirmation"),
        "pending_artifact": state.get("pending_artifact"),
        "confirmed_stages": state.get("confirmed_stages", []),
        "confirmed_chapter_cards": state.get("confirmed_chapter_cards", []),
        "confirmed_chapters": state.get("confirmed_chapters", []),
        "next_chapter": state.get("next_chapter"),
        "revision_required": state.get("revision_required", False),
        "revision_source": state.get("revision_source"),
        "rejected_artifacts": state.get("rejected_artifacts", []),
        "revision_requests": state.get("revision_requests", []),
        "last_updated": state.get("last_updated"),
    }


def print_text(status: dict[str, Any]) -> None:
    print(f"Project: {status['title']} ({status['project_dir']})")
    print(f"Genre: {status.get('genre')}")
    print(f"Current phase: {status.get('current_phase')}")
    print(f"Awaiting confirmation: {status.get('awaiting_confirmation')}")
    if status.get("pending_artifact"):
        print(f"Pending artifact: {status.get('pending_artifact')}")
    print(f"Confirmed stages: {', '.join(status.get('confirmed_stages') or []) or '-'}")
    print(f"Confirmed chapter cards: {status.get('confirmed_chapter_cards')}")
    print(f"Confirmed chapters: {status.get('confirmed_chapters')}")
    print(f"Next chapter: {status.get('next_chapter')}")
    print(f"Revision required: {status.get('revision_required')}")
    if status.get("revision_source"):
        print(f"Revision source: {status.get('revision_source')}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Show fiction-autopilot project status.")
    parser.add_argument("project_dir")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    status = load_status(Path(args.project_dir))
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print_text(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
