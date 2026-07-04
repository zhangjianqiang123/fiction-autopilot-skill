from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_artifacts import validate_artifact


KNOWN_PHASES = {
    "market_positioning",
    "idea_incubation",
    "story_outline",
    "character_design",
    "opening_hook",
    "opening_polish",
    "reader_engagement",
    "chapter_card",
    "chapter_draft",
    "memory_update",
    "chapter_block_review",
    "candidate_competition",
    "consistency_review",
}


STAGE_PHASES = {
    "stages/01_market_positioning.md": "market_positioning",
    "stages/02_idea_incubation.md": "idea_incubation",
    "stages/03_story_outline.md": "story_outline",
    "characters/characters.md": "character_design",
    "stages/05_opening_hook.md": "opening_hook",
    "stages/05b_opening_polish.md": "opening_polish",
    "stages/06_reader_engagement.md": "reader_engagement",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_rel(project_dir: Path, artifact: str) -> str:
    path = Path(artifact)
    if path.is_absolute():
        return path.resolve().relative_to(project_dir.resolve()).as_posix()
    return path.as_posix()


def infer_phase(rel: str) -> str:
    if rel in STAGE_PHASES:
        return STAGE_PHASES[rel]
    if rel.startswith("chapters/") and rel.endswith("_card.md"):
        return "chapter_card"
    if rel.startswith("chapters/") and rel.endswith(".md"):
        return "chapter_draft"
    if rel.startswith("memory/") and rel.endswith(".md"):
        return "memory_update"
    if rel.startswith("reports/block_review_") and rel.endswith(".md"):
        return "chapter_block_review"
    if rel.startswith("reports/candidate_competition_") and rel.endswith(".md"):
        return "candidate_competition"
    if rel.startswith("reports/consistency_review") and rel.endswith(".md"):
        return "consistency_review"
    raise SystemExit(f"Cannot infer phase from artifact path: {rel}. Pass --phase explicitly.")


def assert_valid_artifact(project_dir: Path, rel: str) -> dict[str, Any]:
    result = validate_artifact(project_dir, rel)
    if not result["ok"]:
        message = "\n".join(result["errors"])
        raise SystemExit(f"Artifact validation failed before setting pending:\n{message}")
    return result


def set_pending(
    project_dir: Path,
    artifact: str,
    phase: str | None = None,
    *,
    force: bool = False,
    skip_validation: bool = False,
) -> dict[str, Any]:
    state_path = project_dir / "state.json"
    state = read_json(state_path)
    rel = normalize_rel(project_dir, artifact)
    artifact_path = project_dir / rel
    if not artifact_path.exists():
        raise SystemExit(f"Artifact not found: {rel}")

    next_phase = phase or infer_phase(rel)
    if next_phase not in KNOWN_PHASES:
        raise SystemExit(f"Unknown phase: {next_phase}")
    if state.get("awaiting_confirmation") and not force:
        pending = state.get("pending_artifact")
        raise SystemExit(f"Project is already awaiting confirmation for {pending}. Use --force to replace it.")

    validation = {"ok": True, "errors": [], "warnings": []}
    if not skip_validation:
        validation = assert_valid_artifact(project_dir, rel)

    state["current_phase"] = next_phase
    state["awaiting_confirmation"] = True
    state["pending_artifact"] = rel
    state["last_updated"] = now_iso()
    write_json(state_path, state)
    return {"pending_artifact": rel, "validation": validation, "state": state}


def main() -> int:
    parser = argparse.ArgumentParser(description="Mark a fiction-autopilot artifact as pending confirmation.")
    parser.add_argument("project_dir")
    parser.add_argument("artifact")
    parser.add_argument("--phase", choices=sorted(KNOWN_PHASES))
    parser.add_argument("--force", action="store_true", help="Replace an existing pending artifact.")
    parser.add_argument("--skip-validation", action="store_true", help="Emergency escape hatch; use only with explicit user approval.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = set_pending(
        Path(args.project_dir),
        args.artifact,
        args.phase,
        force=args.force,
        skip_validation=args.skip_validation,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Pending artifact: {result['pending_artifact']}")
        print(f"Current phase: {result['state'].get('current_phase')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
