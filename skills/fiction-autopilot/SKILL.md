---
name: fiction-autopilot
description: End-to-end file-based Chinese fiction production workflow distilled from a multi-flow novel control system. Use when Codex is asked to create, continue, plan, draft, review, or automate a novel from a title or brief, including staged positioning, story bible, outline, characters, chapter cards, chapter prose, memory updates, quality reports, and checkpointed resume without relying on the backend API.
---

# Fiction Autopilot

Use this skill to run a file-based novel production pipeline distilled from the repository's Flow/Skill system. Do not call the existing FastAPI backend. Use project files, checkpoints, and explicit confirmation gates.

## Required Inputs

Before creating or continuing a project, ensure these fields exist in `project.json` or ask the user for them:

- `title`
- `genre`
- `target_chapters`
- `chapter_words`
- `audience`
- `style_reference`
- `forbidden_content`

If the user only provides a title, ask for the missing fields and stop.

## Project Setup

Create projects under `novels/<slug>/` unless the user gives another directory. Prefer the bundled script:

```bash
python codex-skills/fiction-autopilot/scripts/init_project.py --title "书名" --genre "题材" --chapters 20 --chapter-words 1000 --audience "目标读者" --style "风格" --forbidden-content "禁写内容"
```

The project layout is:

```text
novels/<slug>/
├── project.json
├── state.json
├── stages/
├── characters/
├── chapters/
├── memory/
└── reports/
```

Use `scripts/status.py <project_dir>` to inspect progress and `scripts/validate_artifacts.py <project_dir>` before reporting success.
Use `scripts/set_pending.py <project_dir> <artifact_path>` after creating a candidate artifact; it validates the artifact before opening the confirmation gate. Do not hand-edit `awaiting_confirmation` or `pending_artifact`.
Use `scripts/confirm_artifact.py <project_dir>` after the user confirms a pending artifact; it validates again before advancing state. Do not update confirmation lists by hand unless the script cannot run.
Use `scripts/confirm_artifact.py <project_dir> --reject --reason "..."` when the user rejects a candidate, and `--revise --reason "..."` when the user asks for a revision. These actions clear the pending gate without advancing the phase.
Do not use `--skip-validation` unless the user explicitly approves overriding a known validation failure.

## Execution Workflow

Read `references/flows.md` before running a stage. Read `references/schemas.md` before writing structured artifacts. Read `references/quality-gates.md` before approving any stage or chapter.

Read exactly one distilled prompt pack for the active unit:

- Design and planning stages: `references/prompts/design.md`.
- Chapter card and prose loop: `references/prompts/chapter.md`.
- Memory, block review, candidate competition, and consistency review: `references/prompts/memory.md`.

These distilled prompt packs are the authoritative Skill content for this file-based Codex workflow. They intentionally omit backend API routes, FlowLoop JSON protocol, database terms, and model-routing details.

Run one confirmation unit at a time:

1. Produce the next stage or chapter artifact.
2. Use the closest template from `assets/templates/` when creating structured Markdown artifacts.
3. Run `scripts/set_pending.py <project_dir> <artifact_path>` to validate the artifact and set the confirmation gate. If validation fails, repair or rewrite the artifact before showing it to the user.
4. Show the user the artifact path and ask for confirmation.
5. Only after confirmation, run `confirm_artifact.py` to revalidate, mark the stage, chapter card, or chapter prose as confirmed, and move to the next action.

Do not skip confirmation gates. Do not start a chapter draft until its chapter card is confirmed.
If `current_phase=revision_required`, stop forward generation. Read `revision_source`, the relevant review report, and the affected artifact before producing a revised artifact.
Script validation is authoritative. A model-written `Quality Check: passed` cannot override failed script checks for length, event coverage, missing memory, repetition, or malformed review reports.

## Stage Order

Use this default order:

1. `market_positioning`
2. `idea_incubation`
3. `story_outline`
4. `character_design`
5. `opening_hook`
6. `reader_engagement`
7. Chapter loop:
   - `chapter_card`
   - `chapter_draft`
   - `memory_update`
   - every 5 confirmed chapters, `chapter_block_review`

Optional advanced review stages are `opening_polish`, `candidate_competition`, and `consistency_review`. Use them when the user asks for more control or quality review.

## Writing Rules

- Keep all generated prose and stage outputs in Simplified Chinese unless the user requests otherwise.
- Treat confirmed stage files and memory files as locked facts.
- Never overwrite a confirmed artifact. Create a revised file with a suffix such as `_rev2.md`.
- Before writing a candidate, if `awaiting_confirmation=true`, stop and ask the user to confirm, revise, or reject the pending artifact.
- Keep each artifact self-contained enough to be read after context loss.
- For chapter prose, write an actual chapter, not an outline, summary, or patch note.
- For chapter prose, satisfy the script floor: ordinary chapters must reach at least `max(1500, 80% of chapter_words)` counted Chinese/ASCII characters unless the project target is below 1500 or the user explicitly approves a short chapter.
- Build prose from dramatic scenes, not a task checklist. Each ordinary chapter needs at least three scenes with pressure, opposition, failed or risky action, consequence, and a changed situation.
- Keep production-control language out of `Prose`. Terms such as SEG, 伏笔, 兑现, 章末, 本章, 关键事件, 导演卡, and 章节卡 belong in planning sections only, never in the novel text.
- Make causality visible in prose. Do not use "he knows / she knows / task complete" as a substitute for evidence, inference, decision, cost, and result.
- Avoid repeating character catchphrases, address forms, and action beats. If a line appears to be a voice rule, vary the sentence rather than pasting it repeatedly.
- After every chapter draft, create `memory/memory_NNN.md` with events, character state changes, unresolved threads, foreshadowing, and next-chapter handoff.
- Prefer templates from `assets/templates/` for stage, chapter card, chapter draft, memory, candidate competition, consistency review, and block review artifacts. Fill every placeholder with project-specific content before setting the artifact pending.
- Preserve the source system's intent, but translate all backend-specific ideas into file workflow terms: "locked workflow" means confirmed artifact; "Flow state" means `state.json` plus confirmed files; "memory context" means files in `memory/`.

## Resume Behavior

When continuing an existing project:

1. Read `state.json`.
2. Read only the confirmed upstream artifacts needed for the next action.
3. If `awaiting_confirmation=true`, do not continue production; ask the user to confirm, revise, or reject the pending artifact.
4. If validation fails, repair the current candidate before moving forward.

## Reference Navigation

- `references/flows.md`: stage order, file names, confirmation gates.
- `references/schemas.md`: required artifact sections and JSON-like structures.
- `references/quality-gates.md`: pass/fail criteria.
- `references/prompts/design.md`: prompts for positioning, idea, outline, characters, opening, engagement.
- `references/prompts/chapter.md`: prompts for chapter cards, drafting, review, rewrite.
- `references/prompts/memory.md`: prompts for memory updates, reader simulation, consistency review, and block review.
- `assets/templates/`: Markdown templates for common artifacts.
