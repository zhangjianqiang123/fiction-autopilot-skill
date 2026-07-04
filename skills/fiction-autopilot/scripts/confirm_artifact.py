from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_artifacts import validate_artifact


STAGE_FILES = {
    "stages/01_market_positioning.md": ("stage", "market_positioning", "idea_incubation"),
    "stages/02_idea_incubation.md": ("stage", "idea_incubation", "story_outline"),
    "stages/03_story_outline.md": ("stage", "story_outline", "character_design"),
    "characters/characters.md": ("stage", "character_design", "opening_hook"),
    "stages/05_opening_hook.md": ("stage", "opening_hook", "reader_engagement"),
    "stages/05b_opening_polish.md": ("stage", "opening_polish", "reader_engagement"),
    "stages/06_reader_engagement.md": ("stage", "reader_engagement", "chapter_card"),
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


def add_unique(values: list[Any], value: Any) -> None:
    if value not in values:
        values.append(value)


def section_text(text: str, heading: str) -> str:
    pattern = rf"^(#+)\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    level = len(match.group(1))
    next_heading = re.search(rf"^#{{1,{level}}}\s+\S.*$", text[match.end() :], flags=re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end].strip()


def has_blocking_problem_chapters(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    problem_text = section_text(text, "Problem Chapters")
    return re.search(r"severity\s*:\s*(critical|high)\b", problem_text, flags=re.IGNORECASE) is not None


def has_blocking_review(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    blocking_patterns = (
        r"pass_status\s*:\s*(fail|rewrite_needed)",
        r"severity\s*:\s*(critical|high)\b",
    )
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in blocking_patterns)


def assert_valid_artifact(project_dir: Path, rel: str, project: dict[str, Any]) -> dict[str, Any]:
    result = validate_artifact(project_dir, rel, project=project)
    if not result["ok"]:
        message = "\n".join(result["errors"])
        raise SystemExit(f"Artifact validation failed before confirmation:\n{message}")
    return result


def assert_expected_number(state: dict[str, Any], number: int, artifact_type: str) -> None:
    expected = int(state.get("next_chapter") or 1)
    if number != expected:
        raise SystemExit(f"Cannot confirm {artifact_type} {number}: state.next_chapter is {expected}.")


def resolve_pending(project_dir: Path, state: dict[str, Any], artifact: str | None) -> tuple[str, Path]:
    pending = state.get("pending_artifact")
    raw_artifact = artifact or pending
    if not raw_artifact:
        raise SystemExit("No pending artifact. Provide an artifact path or set state.pending_artifact.")

    rel = normalize_rel(project_dir, str(raw_artifact))
    if state.get("awaiting_confirmation") and pending:
        pending_rel = normalize_rel(project_dir, str(pending))
        if rel != pending_rel:
            raise SystemExit(f"Artifact mismatch: pending_artifact is {pending_rel}, got {rel}.")

    artifact_path = project_dir / rel
    if not artifact_path.exists():
        raise SystemExit(f"Artifact not found: {rel}")
    return rel, artifact_path


def clear_pending(state: dict[str, Any]) -> None:
    state["awaiting_confirmation"] = False
    state["pending_artifact"] = None
    state["last_updated"] = now_iso()


def reject(project_dir: Path, artifact: str | None = None, reason: str = "") -> dict[str, Any]:
    state_path = project_dir / "state.json"
    state = read_json(state_path)
    rel, _artifact_path = resolve_pending(project_dir, state, artifact)
    state.setdefault("rejected_artifacts", []).append(
        {"artifact": rel, "reason": reason, "rejected_at": now_iso()}
    )
    clear_pending(state)
    write_json(state_path, state)
    return {"rejected_artifact": rel, "state": state}


def revise(project_dir: Path, artifact: str | None = None, reason: str = "") -> dict[str, Any]:
    state_path = project_dir / "state.json"
    state = read_json(state_path)
    rel, _artifact_path = resolve_pending(project_dir, state, artifact)
    state.setdefault("revision_requests", []).append(
        {"artifact": rel, "instruction": reason, "requested_at": now_iso()}
    )
    clear_pending(state)
    write_json(state_path, state)
    return {"revision_requested_for": rel, "state": state}


def confirm(project_dir: Path, artifact: str | None = None, *, skip_validation: bool = False) -> dict[str, Any]:
    state_path = project_dir / "state.json"
    state = read_json(state_path)
    project = read_json(project_dir / "project.json")
    target_chapters = int(project.get("target_chapters") or 0)
    rel, artifact_path = resolve_pending(project_dir, state, artifact)
    validation = {"ok": True, "errors": [], "warnings": []}
    if not skip_validation:
        validation = assert_valid_artifact(project_dir, rel, project)

    if rel in STAGE_FILES:
        _kind, stage, next_phase = STAGE_FILES[rel]
        add_unique(state.setdefault("confirmed_stages", []), stage)
        state["current_phase"] = next_phase
    elif rel.startswith("chapters/") and rel.endswith("_card.md"):
        number = chapter_number_from_name(rel)
        assert_expected_number(state, number, "chapter card")
        add_unique(state.setdefault("confirmed_chapter_cards", []), number)
        state["current_phase"] = "chapter_draft"
        state["next_chapter"] = number
    elif rel.startswith("chapters/") and rel.endswith(".md"):
        number = chapter_number_from_name(rel)
        assert_expected_number(state, number, "chapter draft")
        if number not in state.get("confirmed_chapter_cards", []):
            raise SystemExit(f"Cannot confirm chapter {number}: chapter card is not confirmed.")
        add_unique(state.setdefault("confirmed_chapters", []), number)
        state["current_phase"] = "memory_update"
        state["next_chapter"] = number
    elif rel.startswith("memory/") and rel.endswith(".md"):
        number = chapter_number_from_name(rel)
        assert_expected_number(state, number, "memory")
        if number not in state.get("confirmed_chapters", []):
            raise SystemExit(f"Cannot confirm memory {number}: chapter draft is not confirmed.")
        next_chapter = number + 1
        state["next_chapter"] = next_chapter
        if number > 0 and number % 5 == 0:
            state["current_phase"] = "chapter_block_review"
        elif target_chapters and number >= target_chapters:
            state["current_phase"] = "complete"
        else:
            state["current_phase"] = "chapter_card"
    elif rel.startswith("reports/block_review_"):
        next_chapter = int(state.get("next_chapter") or 1)
        if has_blocking_problem_chapters(artifact_path):
            state["current_phase"] = "revision_required"
            state["revision_required"] = True
            state["revision_source"] = rel
        else:
            state["revision_required"] = False
            state["current_phase"] = "complete" if target_chapters and next_chapter > target_chapters else "chapter_card"
    elif rel.startswith("reports/candidate_competition_"):
        state["current_phase"] = "chapter_draft"
    elif rel.startswith("reports/consistency_review"):
        if has_blocking_review(artifact_path):
            state["current_phase"] = "revision_required"
            state["revision_required"] = True
            state["revision_source"] = rel
        else:
            state["revision_required"] = False
            state["current_phase"] = "chapter_card"
    else:
        raise SystemExit(f"Cannot infer confirmation type from artifact path: {rel}")

    clear_pending(state)
    write_json(state_path, state)
    return {"confirmed_artifact": rel, "validation": validation, "state": state}


def chapter_number_from_name(value: str) -> int:
    digits = "".join(ch for ch in Path(value).stem if ch.isdigit())
    if not digits:
        raise SystemExit(f"Cannot infer chapter number from path: {value}")
    return int(digits[:3])


def main() -> int:
    parser = argparse.ArgumentParser(description="Confirm, reject, or request revision for a pending fiction-autopilot artifact.")
    parser.add_argument("project_dir")
    parser.add_argument("artifact", nargs="?")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--reject", action="store_true", help="Reject the pending artifact without advancing current_phase.")
    action.add_argument("--revise", action="store_true", help="Request a revised artifact without advancing current_phase.")
    parser.add_argument("--reason", default="", help="Reason or revision instruction for --reject/--revise.")
    parser.add_argument("--skip-validation", action="store_true", help="Emergency escape hatch; use only with explicit user approval.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if args.reject:
        result = reject(project_dir, args.artifact, args.reason)
    elif args.revise:
        result = revise(project_dir, args.artifact, args.reason)
    else:
        result = confirm(project_dir, args.artifact, skip_validation=args.skip_validation)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if args.reject:
            print(f"Rejected: {result['rejected_artifact']}")
        elif args.revise:
            print(f"Revision requested for: {result['revision_requested_for']}")
        else:
            print(f"Confirmed: {result['confirmed_artifact']}")
        print(f"Next phase: {result['state'].get('current_phase')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
