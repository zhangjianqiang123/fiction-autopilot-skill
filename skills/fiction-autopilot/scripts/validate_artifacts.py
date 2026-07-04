from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


MIN_PROSE_CHARS = 1500
MIN_PROSE_TARGET_RATIO = 0.8
MIN_SCENES_FOR_ORDINARY_CHAPTER = 3
MIN_CAUSAL_CONNECTORS = 3

PROSE_FORBIDDEN_TERMS = (
    "SEG-",
    "SEG_",
    "本章",
    "章末",
    "章节",
    "章节卡",
    "导演卡",
    "关键事件",
    "伏笔",
    "兑现",
    "读者",
)

CAUSAL_CONNECTORS = (
    "因为",
    "所以",
    "但",
    "但是",
    "却",
    "可",
    "可是",
    "然而",
    "于是",
    "因此",
    "否则",
    "如果",
    "只要",
    "直到",
    "反而",
    "偏偏",
)

REQUIRED_PROJECT_FIELDS = (
    "title",
    "genre",
    "target_chapters",
    "chapter_words",
    "audience",
    "style_reference",
    "forbidden_content",
)

REQUIRED_STATE_FIELDS = (
    "current_phase",
    "awaiting_confirmation",
    "pending_artifact",
    "confirmed_stages",
    "confirmed_chapter_cards",
    "confirmed_chapters",
    "next_chapter",
)

STAGE_ARTIFACTS = {
    "market_positioning": "stages/01_market_positioning.md",
    "idea_incubation": "stages/02_idea_incubation.md",
    "story_outline": "stages/03_story_outline.md",
    "character_design": "characters/characters.md",
    "opening_hook": "stages/05_opening_hook.md",
    "opening_polish": "stages/05b_opening_polish.md",
    "reader_engagement": "stages/06_reader_engagement.md",
}

KNOWN_PHASES = {
    *STAGE_ARTIFACTS,
    "chapter_card",
    "chapter_draft",
    "memory_update",
    "chapter_block_review",
    "candidate_competition",
    "consistency_review",
    "revision_required",
    "complete",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def has_heading(text: str, heading: str) -> bool:
    pattern = rf"^#+\s+{re.escape(heading)}\s*$"
    return re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE) is not None


def has_any_heading(text: str, headings: tuple[str, ...]) -> bool:
    return any(has_heading(text, heading) for heading in headings)


def section_text(text: str, heading: str) -> str:
    pattern = rf"^(#+)\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    level = len(match.group(1))
    next_heading = re.search(rf"^#{{1,{level}}}\s+\S.*$", text[match.end() :], flags=re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end].strip()


def visible_char_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def prose_char_count(text: str) -> int:
    # Count body content, not Markdown headings, punctuation, or spacing.
    return len(re.findall(r"[\u3400-\u9fffA-Za-z0-9]", text))


def first_field_line(value: str) -> str:
    return value.strip().splitlines()[0].strip() if value.strip() else ""


def field_block(text: str, field: str) -> str:
    pattern = rf"^[ \t]*{re.escape(field)}[ \t]*:[ \t]*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    lines = [match.group(1).strip()]
    tail = text[match.end() :].splitlines()
    for line in tail:
        if re.match(r"^#+\s+", line):
            break
        if re.match(r"^[A-Za-z_][\w -]*\s*:", line):
            break
        lines.append(line.rstrip())
    return "\n".join(line for line in lines if line.strip()).strip()


def empty_field(value: str) -> bool:
    normalized = re.sub(r"^[\s\-*+]+", "", value.strip()).strip().lower()
    return normalized in {"", "[]", "none", "null", "n/a", "无", "无。", "没有", "未发现"}


def positive_int(value: Any) -> int | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def chapter_number_from_name(value: Path | str) -> int | None:
    digits = "".join(ch for ch in Path(value).stem if ch.isdigit())
    return int(digits[:3]) if digits else None


def prose_floor(project: dict[str, Any], chapter_text: str = "") -> int:
    target = first_int(section_text(chapter_text, "Target Words")) if chapter_text else None
    target = target or positive_int(project.get("chapter_words")) or MIN_PROSE_CHARS
    if target < MIN_PROSE_CHARS:
        return target
    return max(MIN_PROSE_CHARS, int(target * MIN_PROSE_TARGET_RATIO))


def normalize_value(value: str) -> str:
    value = re.sub(r"^[\s\-*+0-9.、:：]+", "", value.strip())
    return re.sub(r"[\s\W_]+", "", value, flags=re.UNICODE).lower()


def section_items(text: str, heading: str) -> list[str]:
    section = section_text(text, heading)
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^[-*+]\s+", stripped) or re.match(r"^\d+[.、]\s+", stripped):
            items.append(re.sub(r"^([-*+]\s+|\d+[.、]\s+)", "", stripped).strip())
    if items:
        return items
    return [line.strip() for line in section.splitlines() if line.strip()]


def first_int(value: str) -> int | None:
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else None


def require_heading(errors: list[str], path: Path, text: str, heading: str) -> None:
    if not has_heading(text, heading):
        errors.append(f"{path} missing heading: {heading}")


def validate_completed_events(errors: list[str], card: Path, chapter: Path) -> None:
    card_text = card.read_text(encoding="utf-8", errors="replace")
    chapter_text = chapter.read_text(encoding="utf-8", errors="replace")
    key_events = [normalize_value(item) for item in section_items(card_text, "Key Events")]
    completed_text = normalize_value(section_text(chapter_text, "Completed Events"))
    missing = [item for item in key_events if item and item not in completed_text]
    if missing:
        errors.append(f"{chapter} Completed Events do not cover chapter card Key Events from {card}")


def has_problem_chapter_shape(text: str) -> bool:
    problem_text = section_text(text, "Problem Chapters")
    if not problem_text or problem_text in {"[]", "- []"}:
        return True
    required_patterns = (
        r"chapter_number\s*:",
        r"issues\s*:",
        r"fix_instruction\s*:",
        r"severity\s*:\s*(critical|high|medium|low)",
    )
    return all(re.search(pattern, problem_text, flags=re.IGNORECASE) for pattern in required_patterns)


def validate_stage_artifact(errors: list[str], artifact: Path, text: str) -> None:
    if not text.strip():
        errors.append(f"{artifact} is empty")
    if re.search(r"<[^>\n]+>", text):
        errors.append(f"{artifact} still contains template placeholders")
    for required in ("project:", "unit:", "status:", "source:"):
        if required not in text:
            errors.append(f"{artifact} missing common header field: {required}")


def validate_chapter_card_artifact(errors: list[str], card: Path, project: dict[str, Any]) -> None:
    text = card.read_text(encoding="utf-8", errors="replace")
    validate_stage_artifact(errors, card, text)
    required_headings = (
        "Chapter Number",
        "Title",
        "Catalog Binding",
        "Goal",
        "Core Conflict",
        "Initiator Goal",
        "Opponent Goal",
        "Stakes",
        "Opening Hook",
        "Ending Hook",
        "Pursuit Question",
        "Key Events",
        "Payoff",
        "Target Words",
        "Emotion Contract",
        "Pressure Level",
        "Final Check",
    )
    for heading in required_headings:
        require_heading(errors, card, text, heading)

    file_number = chapter_number_from_name(card)
    chapter_number = first_int(section_text(text, "Chapter Number"))
    if file_number is not None and chapter_number is not None and file_number != chapter_number:
        errors.append(f"{card} Chapter Number does not match filename number {file_number}")

    binding_text = section_text(text, "Catalog Binding")
    if binding_text and not re.search(r"status\s*:\s*bound\b", binding_text, flags=re.IGNORECASE):
        errors.append(f"{card} Catalog Binding must include status: bound")

    pressure_text = section_text(text, "Pressure Level").strip().lower()
    if pressure_text and not re.fullmatch(r"(low|medium|high|critical)", first_field_line(pressure_text)):
        errors.append(f"{card} Pressure Level must be exactly one of low, medium, high, or critical")

    emotion_text = section_text(text, "Emotion Contract")
    allowed_from = {"压抑", "愤怒", "焦虑", "期待", "绝望"}
    allowed_to = {"释放", "反转", "揭秘", "升级", "翻盘"}
    from_state = first_field_line(field_block(emotion_text, "from"))
    to_state = first_field_line(field_block(emotion_text, "to"))
    if emotion_text and from_state not in allowed_from:
        errors.append(f"{card} Emotion Contract from must be one of: {', '.join(sorted(allowed_from))}")
    if emotion_text and to_state not in allowed_to:
        errors.append(f"{card} Emotion Contract to must be one of: {', '.join(sorted(allowed_to))}")

    key_events = section_items(text, "Key Events")
    if len(key_events) < 3:
        errors.append(f"{card} Key Events must contain at least 3 sceneable events")

    target_words = positive_int(first_int(section_text(text, "Target Words"))) or positive_int(project.get("chapter_words"))
    if not target_words:
        errors.append(f"{card} Target Words must be a positive integer")

    conflict_text = section_text(text, "Core Conflict")
    if conflict_text and not re.search(r"(vs|对抗|冲突|失败代价)", conflict_text, flags=re.IGNORECASE):
        errors.append(f"{card} Core Conflict must include opposed goals and failure stakes")


def validate_scene_contract(errors: list[str], chapter: Path, text: str, floor: int) -> None:
    scene_plan = section_text(text, "Scene Plan")
    scene_count = len(re.findall(r"(?im)^\s*[-*]?\s*scene_key\s*:", scene_plan))
    minimum = MIN_SCENES_FOR_ORDINARY_CHAPTER if floor >= MIN_PROSE_CHARS else 2
    if scene_count < minimum:
        errors.append(f"{chapter} Scene Plan must contain at least {minimum} scenes")

    ratio_values: list[float] = []
    for match in re.finditer(r"word_budget_ratio\s*:\s*([0-9.]+)", scene_plan, flags=re.IGNORECASE):
        try:
            ratio_values.append(float(match.group(1)))
        except ValueError:
            continue
    if scene_count and len(ratio_values) < scene_count:
        errors.append(f"{chapter} every Scene Plan item must include word_budget_ratio")
    if ratio_values and len(ratio_values) >= scene_count:
        total = sum(ratio_values)
        if not 0.85 <= total <= 1.15:
            errors.append(f"{chapter} Scene Plan word_budget_ratio should total about 1.0, got {total:.2f}")

    scene_details = section_text(text, "Scene Details")
    if scene_count and len(re.findall(r"(?im)^#+\s*scene[_ -]?\d+", scene_details)) < min(scene_count, 2):
        errors.append(f"{chapter} Scene Details must detail the planned scenes, not only summarize them")


def validate_repetition(errors: list[str], chapter: Path, prose: str) -> None:
    phrase_limits = {
        "按匠人协议": 5,
        "陆沉没动": 2,
        "声音不高": 3,
        "每个字都按得很实": 2,
        "他知道": 4,
        "她知道": 4,
        "陆沉知道": 2,
        "金文一共": 2,
        "主任务完成": 1,
        "完成第一步": 0,
        "完成第二步": 0,
    }
    for phrase, limit in phrase_limits.items():
        count = prose.count(phrase)
        if count > limit:
            errors.append(f"{chapter} repeated phrase '{phrase}' {count} times; limit is {limit}")

    dialogue_openers = re.findall(r"[“\"]([^“”\"\n]{1,6})[。.!！?？][”\"]", prose)
    for opener, count in Counter(dialogue_openers).items():
        if count > 6:
            errors.append(f"{chapter} repeats dialogue opener '{opener}' {count} times; rewrite character voice")

    sentences = [
        normalize_value(item)
        for item in re.split(r"[。！？!?]\s*", prose)
        if 4 <= len(normalize_value(item)) <= 40
    ]
    for sentence, count in Counter(sentences).items():
        if count > 3:
            errors.append(f"{chapter} repeats the same sentence/beat {count} times; rewrite for variation")


def prose_sentences(prose: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"[。！？!?]\s*", prose) if sentence.strip()]


def validate_prose_integrity(errors: list[str], chapter: Path, text: str, prose: str, floor: int) -> None:
    integrity = section_text(text, "Prose Integrity Check")
    if not integrity:
        errors.append(f"{chapter} missing heading: Prose Integrity Check")
    else:
        required_fields = (
            "cause_effect_chain",
            "timeline_and_space_logic",
            "tool_or_world_logic",
            "character_motivation",
            "scene_change_summary",
            "meta_language_check",
        )
        for field in required_fields:
            value = field_block(integrity, field)
            if empty_field(value):
                errors.append(f"{chapter} Prose Integrity Check missing or empty: {field}")

    forbidden_hits = [term for term in PROSE_FORBIDDEN_TERMS if term in prose]
    if forbidden_hits:
        errors.append(f"{chapter} Prose contains production/meta terms: {', '.join(forbidden_hits)}")

    sentences = prose_sentences(prose)
    if floor >= MIN_PROSE_CHARS and len(sentences) >= 25:
        connector_count = sum(prose.count(connector) for connector in CAUSAL_CONNECTORS)
        if connector_count < MIN_CAUSAL_CONNECTORS:
            errors.append(
                f"{chapter} Prose has weak explicit causality: {connector_count} causal/contrast connectors; minimum is {MIN_CAUSAL_CONNECTORS}"
            )

    lead_counts: Counter[str] = Counter()
    for sentence in sentences:
        stripped = re.sub(r'^[\s"“”\'‘’]+', "", sentence)
        lead = stripped[:2]
        if lead:
            lead_counts[lead] += 1
    for lead, count in lead_counts.items():
        if lead in {"他", "她", "这", "那"}:
            continue
        if len(sentences) >= 30 and count > max(12, int(len(sentences) * 0.28)):
            errors.append(f"{chapter} Prose starts too many sentences with '{lead}': {count}/{len(sentences)}")

    completion_terms = ("完成", "第一步", "第二步", "任务完成", "继续 SEG", "入口开启")
    completion_count = sum(prose.count(term) for term in completion_terms)
    if completion_count >= 4:
        errors.append(f"{chapter} Prose uses checklist/completion language too often: {completion_count} hits")


def validate_chapter_draft_artifact(errors: list[str], chapter: Path, project: dict[str, Any]) -> None:
    text = chapter.read_text(encoding="utf-8", errors="replace")
    validate_stage_artifact(errors, chapter, text)
    required_headings = (
        "Chapter Number",
        "Title",
        "Context Lock",
        "Conflict Design",
        "Hook Design",
        "Scene Plan",
        "Scene Details",
        "Director Card",
        "Prose",
        "Quality Check",
        "Summary",
        "Completed Events",
        "Ending Hook",
        "Next Chapter Handoff",
    )
    for heading in required_headings:
        require_heading(errors, chapter, text, heading)

    floor = prose_floor(project, text)
    prose = section_text(text, "Prose")
    prose_count = prose_char_count(prose)
    if prose and prose_count < floor:
        errors.append(f"{chapter} Prose section is below required counted prose characters: {prose_count} < {floor}")
    if re.search(r"(?m)^\s*[-*]\s+", prose):
        errors.append(f"{chapter} Prose section must be prose paragraphs, not bullet points")
    if prose and not re.search(r"[“\"].+?[”\"]|：", prose):
        errors.append(f"{chapter} Prose section needs dialogue or explicit interior pressure")

    validate_scene_contract(errors, chapter, text, floor)
    validate_repetition(errors, chapter, prose)
    validate_prose_integrity(errors, chapter, text, prose, floor)

    director = section_text(text, "Director Card")
    for field in ("dialogue_examples", "never_say", "gesture_habits", "conflict_style"):
        if field not in director:
            errors.append(f"{chapter} Director Card character_voice_brief missing: {field}")

    quality = section_text(text, "Quality Check")
    pass_status = first_field_line(field_block(quality, "pass_status")).lower()
    if not pass_status:
        errors.append(f"{chapter} Quality Check missing pass_status")
    elif pass_status in {"fail", "rewrite_needed"}:
        errors.append(f"{chapter} Quality Check pass_status is {pass_status}")
    blocking = field_block(quality, "blocking_issues")
    if not empty_field(blocking):
        errors.append(f"{chapter} Quality Check blocking_issues is not empty")

    ending_hook = section_text(text, "Ending Hook")
    if ending_hook and prose_char_count(ending_hook) < 20:
        errors.append(f"{chapter} Ending Hook is too vague")

    card = chapter.with_name(f"{chapter.stem}_card.md")
    if card.exists():
        card_text = card.read_text(encoding="utf-8", errors="replace")
        card_number = first_int(section_text(card_text, "Chapter Number"))
        chapter_number = first_int(section_text(text, "Chapter Number"))
        file_number = chapter_number_from_name(chapter)
        if file_number is not None and chapter_number is not None and chapter_number != file_number:
            errors.append(f"{chapter} Chapter Number does not match filename number {file_number}")
        if card_number is not None and chapter_number is not None and card_number != chapter_number:
            errors.append(f"{chapter} Chapter Number does not match {card}")
        card_title = normalize_value(section_text(card_text, "Title"))
        chapter_title = normalize_value(section_text(text, "Title"))
        if card_title and chapter_title and card_title != chapter_title:
            errors.append(f"{chapter} Title does not match {card}")
        validate_completed_events(errors, card, chapter)
    else:
        errors.append(f"{chapter} matching chapter card missing: {card}")


def validate_memory_artifact(errors: list[str], memory: Path) -> None:
    text = memory.read_text(encoding="utf-8", errors="replace")
    validate_stage_artifact(errors, memory, text)
    required_memory_headings = (
        ("Source Chapter",),
        ("Chapter Summary",),
        ("Character State Deltas", "Character State Changes"),
        ("Unresolved Threads",),
        ("Next Chapter Bridge",),
        ("Story Control State",),
        ("Knowledge Items",),
        ("Retrieval Queries",),
    )
    for headings in required_memory_headings:
        if not has_any_heading(text, headings):
            label = " or ".join(headings)
            errors.append(f"{memory} missing heading: {label}")

    control = section_text(text, "Story Control State")
    for field in (
        "current_arc",
        "active_threads",
        "payoff_ledger",
        "character_states",
        "continuity_facts",
        "world_rules",
        "next_chapter_control",
        "evidence_refs",
    ):
        if field not in control:
            errors.append(f"{memory} Story Control State missing: {field}")

    knowledge = section_text(text, "Knowledge Items")
    if knowledge and not all(token in knowledge for token in ("item_type:", "subject:", "evidence:", "status:")):
        errors.append(f"{memory} Knowledge Items must include item_type, subject, evidence, and status")
    if empty_field(section_text(text, "Retrieval Queries")):
        errors.append(f"{memory} Retrieval Queries must not be empty")


def validate_block_review_artifact(errors: list[str], report: Path) -> None:
    text = report.read_text(encoding="utf-8", errors="replace")
    validate_stage_artifact(errors, report, text)
    if not has_heading(text, "Mechanical Quality Audit"):
        errors.append(f"{report} missing heading: Mechanical Quality Audit")
    if not has_heading(text, "Problem Chapters"):
        errors.append(f"{report} missing heading: Problem Chapters")
    elif not has_problem_chapter_shape(text):
        errors.append(f"{report} Problem Chapters must include chapter_number, issues, fix_instruction, and severity")


def validate_artifact(project_dir: Path, artifact: str | Path, project: dict[str, Any] | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    project = project if project is not None else read_json(project_dir / "project.json")
    artifact_path = Path(artifact)
    if artifact_path.is_absolute():
        try:
            rel = artifact_path.resolve().relative_to(project_dir.resolve()).as_posix()
        except ValueError:
            errors.append(f"artifact is outside project_dir: {artifact_path}")
            return {"ok": False, "errors": errors, "warnings": warnings}
    else:
        rel = artifact_path.as_posix()
        artifact_path = project_dir / rel

    if not artifact_path.exists():
        errors.append(f"artifact does not exist: {rel}")
        return {"ok": False, "errors": errors, "warnings": warnings}

    if rel in STAGE_ARTIFACTS.values():
        validate_stage_artifact(errors, artifact_path, artifact_path.read_text(encoding="utf-8", errors="replace"))
    elif rel.startswith("chapters/") and rel.endswith("_card.md"):
        validate_chapter_card_artifact(errors, artifact_path, project)
    elif rel.startswith("chapters/") and rel.endswith(".md"):
        validate_chapter_draft_artifact(errors, artifact_path, project)
    elif rel.startswith("memory/") and rel.endswith(".md"):
        validate_memory_artifact(errors, artifact_path)
    elif rel.startswith("reports/block_review_") and rel.endswith(".md"):
        validate_block_review_artifact(errors, artifact_path)
    elif rel.startswith("reports/candidate_competition_") or rel.startswith("reports/consistency_review"):
        validate_stage_artifact(errors, artifact_path, artifact_path.read_text(encoding="utf-8", errors="replace"))
    else:
        warnings.append(f"no specialized validator for artifact: {rel}")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def validate(project_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    project_path = project_dir / "project.json"
    state_path = project_dir / "state.json"
    if not project_path.exists():
        errors.append("project.json missing")
        project = {}
    else:
        project = read_json(project_path)
    if not state_path.exists():
        errors.append("state.json missing")
        state = {}
    else:
        state = read_json(state_path)

    for field in REQUIRED_PROJECT_FIELDS:
        if not project.get(field):
            errors.append(f"project.json missing required field: {field}")
    for field in ("target_chapters", "chapter_words"):
        try:
            if int(project.get(field) or 0) <= 0:
                errors.append(f"project.json field must be positive: {field}")
        except (TypeError, ValueError):
            errors.append(f"project.json field must be integer: {field}")
    for field in REQUIRED_STATE_FIELDS:
        if field not in state:
            errors.append(f"state.json missing required field: {field}")
    current_phase = state.get("current_phase")
    if current_phase and current_phase not in KNOWN_PHASES:
        errors.append(f"state.json current_phase is unknown: {current_phase}")
    target_chapters = 0
    try:
        target_chapters = int(project.get("target_chapters") or 0)
    except (TypeError, ValueError):
        target_chapters = 0
    try:
        next_chapter = int(state.get("next_chapter") or 0)
        if target_chapters and next_chapter > target_chapters + 1:
            errors.append(f"state.json next_chapter exceeds target_chapters+1: {next_chapter}")
    except (TypeError, ValueError):
        errors.append("state.json next_chapter must be integer")
    if state.get("awaiting_confirmation"):
        pending = state.get("pending_artifact")
        if not pending:
            errors.append("state.json awaiting_confirmation=true but pending_artifact is empty")
        elif not (project_dir / str(pending)).exists():
            errors.append(f"pending_artifact does not exist: {pending}")

    for directory in ("stages", "characters", "chapters", "memory", "reports"):
        if not (project_dir / directory).is_dir():
            errors.append(f"directory missing: {directory}")

    for stage in state.get("confirmed_stages", []):
        if stage not in STAGE_ARTIFACTS:
            warnings.append(f"confirmed stage has no standard artifact mapping: {stage}")
            continue
        artifact = project_dir / STAGE_ARTIFACTS[stage]
        if not artifact.exists():
            errors.append(f"confirmed stage artifact missing: {artifact}")

    confirmed_cards = [int(item) for item in state.get("confirmed_chapter_cards", []) if str(item).isdigit()]
    confirmed_chapters = [int(item) for item in state.get("confirmed_chapters", []) if str(item).isdigit()]
    if len(confirmed_cards) != len(state.get("confirmed_chapter_cards", [])):
        errors.append("confirmed_chapter_cards must contain only integers")
    if len(confirmed_chapters) != len(state.get("confirmed_chapters", [])):
        errors.append("confirmed_chapters must contain only integers")

    for number in confirmed_cards:
        card = project_dir / "chapters" / f"chapter_{number:03d}_card.md"
        if not card.exists():
            errors.append(f"confirmed chapter card missing: {card}")
            continue
        validate_chapter_card_artifact(errors, card, project)

    for number in confirmed_chapters:
        chapter = project_dir / "chapters" / f"chapter_{number:03d}.md"
        memory = project_dir / "memory" / f"memory_{number:03d}.md"
        if not chapter.exists():
            errors.append(f"confirmed chapter missing: {chapter}")
            continue
        validate_chapter_draft_artifact(errors, chapter, project)
        if not memory.exists():
            try:
                current_next_chapter = int(state.get("next_chapter") or 0)
            except (TypeError, ValueError):
                current_next_chapter = 0
            memory_is_current_todo = current_phase == "memory_update" and number == current_next_chapter
            if memory_is_current_todo:
                warnings.append(f"memory pending for current memory_update chapter {number}: {memory}")
            else:
                errors.append(f"memory missing for confirmed chapter {number}: {memory}")
        else:
            validate_memory_artifact(errors, memory)

    for report in sorted((project_dir / "reports").glob("block_review_*.md")):
        validate_block_review_artifact(errors, report)

    if confirmed_chapters:
        expected = list(range(1, max(confirmed_chapters) + 1))
        if confirmed_chapters != expected:
            errors.append(f"confirmed_chapters not continuous from 1: {confirmed_chapters}")
    if confirmed_cards:
        expected_cards = list(range(1, max(confirmed_cards) + 1))
        if confirmed_cards != expected_cards:
            errors.append(f"confirmed_chapter_cards not continuous from 1: {confirmed_cards}")
    for number in confirmed_chapters:
        if number not in confirmed_cards:
            errors.append(f"chapter {number} confirmed but its chapter card is not confirmed")
    if target_chapters and len(confirmed_chapters) >= target_chapters and current_phase not in {"complete", "chapter_block_review", "consistency_review", "revision_required"}:
        errors.append("target_chapters reached but current_phase is not complete or final review")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a fiction-autopilot project.")
    parser.add_argument("project_dir")
    parser.add_argument("--artifact", help="Validate one artifact path relative to project_dir or absolute path.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if args.artifact:
        result = validate_artifact(project_dir, args.artifact)
    else:
        result = validate(project_dir)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("OK" if result["ok"] else "FAILED")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
