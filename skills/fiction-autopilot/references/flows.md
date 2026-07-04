# Distilled Flow Map

This file is the orchestration map for the file-based Codex skill. It distills the original 13 Flow / 86 Skill system into confirmation units and artifact files. Do not use backend routes or JSON FlowLoop protocol.

## Inputs And State

Required project inputs:

- title
- genre
- target_chapters
- chapter_words
- audience
- style_reference
- forbidden_content

Runtime state lives in `state.json`:

- `current_phase`: next action.
- `awaiting_confirmation`: true when Codex must stop.
- `pending_artifact`: candidate path awaiting user confirmation.
- `confirmed_stages`: confirmed design units.
- `confirmed_chapter_cards`: confirmed card numbers.
- `confirmed_chapters`: confirmed prose numbers.
- `next_chapter`: next chapter number.
- `revision_required`: true when a confirmed review found critical/high issues.
- `revision_source`: review artifact that triggered revision.

## Confirmation Rule

Generate one confirmation unit, save it, run `scripts/set_pending.py <project_dir> <artifact_path>`, and stop. Continue only after the user confirms. A confirmed artifact becomes locked context for all downstream work.

When the user confirms, run `scripts/confirm_artifact.py <project_dir>` so `state.json` advances consistently.
When the user rejects or requests revision, run `scripts/confirm_artifact.py <project_dir> --reject --reason "..."` or `--revise --reason "..."`. These commands clear `awaiting_confirmation` without advancing `current_phase`, and record the decision in `state.json`.
If the user passes an explicit artifact to the script while a pending artifact exists, it must match `pending_artifact`.

## Inter-Flow Handoff

Use this handoff chain when deciding what to read for the next artifact:

- `market_positioning` supplies reader promise, mass emotions, taboo misfires, differentiation, opening promise, and adaptation risks to all later design stages.
- `idea_incubation` turns the promise into protagonist, required action, failure consequence, hidden crisis, and locked facts for the outline.
- `story_outline` supplies phase structure, payoff/twist systems, chapter catalog or rolling catalog window, and continuity rules. Chapter cards must bind to the active catalog window; for long projects, later phases stay as segment goals until a rolling outline update expands them.
- `character_design` supplies goals, fears, secrets, voice rules, pressure responses, relationship tensions, and villain pressure tools for scene design.
- `opening_hook` supplies first-three-chapter obligations and opening retention risks. Chapters 1-3 must obey these obligations even when the catalog is less detailed.
- `opening_polish` is an overlay on `opening_hook`, not a parallel replacement. Its `Chapter Targets`, `Rewrite Priorities`, and `Do Not Change` sections override only the specific first-three-chapter pressure/payoff items they name.
- `reader_engagement` supplies the live control ledgers: emotion curve, payoff ledger, antagonist pressure ladder, suspense/reveal schedule, relationship beats, and chapter-ending rules.
- `candidate_competition` supplies reader-preview constraints to `chapter_context_lock`: reader expectations, drop-risk points, must-deliver scenes, pacing advice, and do-not-merge constraints.
- `chapter_card` selects the relevant catalog entry plus the relevant engagement/memory slice for chapter `N`; it writes the contract for prose.
- `chapter_draft` must satisfy the chapter card, locked facts, previous handoff, memory, and due payoff/reveal items.
- `memory_update` converts the confirmed chapter into short, mid, long, searchable, and next-chapter control memory.
- `chapter_block_review` reads the last 5 confirmed chapters plus memory and engagement ledgers, then returns carryovers, debt updates, and problem chapters to the next chapter card or revision.
- `consistency_review` may set `revision_required` when it confirms critical/high continuity, character, or payoff issues.

## Main Production Flow

1. `market_positioning`
   - Artifact: `stages/01_market_positioning.md`
   - Distilled skills: genre_market_scan, reader_profile_define, trope_promise_design, differentiation_angle, title_blurb_hook_pack, market_fit_final_check.
   - Success: clear reader promise, market lane, trope contract, differentiation, and sellable title/blurb options.

2. `idea_incubation`
   - Artifact: `stages/02_idea_incubation.md`
   - Distilled skills: input_analysis, core_seed, longform_viability, story_bible_seed, idea_final_check.
   - Success: story bible seed with protagonist, action pressure, consequence, hidden crisis, locked facts.

3. `story_outline`
   - Artifact: `stages/03_story_outline.md`
   - Distilled skills: story_bible_expand, conflict_system, plot_phases, chapter_blueprint_plan, chapter_blueprint_part2, chapter_blueprint_part3, outline_synthesis, outline_final_check.
   - Success: phase structure, conflict escalation, payoff/twist systems, and a chapter catalog strategy. For projects over 60 chapters, detail only the current 10-20 chapter window plus the next handoff; keep later chapters at segment-goal level unless the user explicitly asks for a full catalog.

4. `character_design`
   - Artifact: `characters/characters.md`
   - Distilled skills: character_role_analysis, protagonist_design, ally_design, villain_design, gray_character_design, relationship_network, character_final_check.
   - Success: usable characters with goals, pressure responses, dialogue voice, behavior patterns, and conflict-bearing relationships.

5. `opening_hook`
   - Artifact: `stages/05_opening_hook.md`
   - Distilled skills: opening_pressure_analysis, first_chapter_hook_design, first_three_chapter_arc, opening_ab_options, opening_payoff_density, opening_retention_risk_check, opening_hook_final_check.
   - Success: first-three-chapter retention plan with immediate pressure, protagonist action, reversals, payoffs, and risk fixes.

6. `opening_polish` optional
   - Artifact: `stages/05b_opening_polish.md`
   - Distilled skills: opening_pressure_reaudit, first_three_chapter_ab_options, opening_payoff_density_check, opening_revision_plan, opening_polish_final_check.
   - Success: concrete revision plan for the first three chapters when opening quality needs another pass.

7. `reader_engagement`
   - Artifact: `stages/06_reader_engagement.md`
   - Distilled skills: emotion_curve_design, payoff_ledger_plan, antagonist_pressure_ladder, suspense_thread_ledger, emotion_line_ledger, binge_reading_pacing, engagement_final_check.
   - Success: reusable ledger for emotion, payoffs, pressure, suspense, relationships, and chapter-end rhythm.

8. Chapter loop for chapter `N`
   - Card artifact: `chapters/chapter_NNN_card.md`
   - Draft artifact: `chapters/chapter_NNN.md`
   - Memory artifact: `memory/memory_NNN.md`
   - Distilled skills: chapter_card_design, chapter_card_final_check, chapter_context_lock, draft_conflict_design, draft_hook_design, scene_plan, scene_detail_generate, scene_continuity_check, chapter_director, prose_generation, candidate_review, reader_reaction_review, candidate_polish, chapter_quality_check, chapter_rewrite, memory_update.
   - Success: confirmed card, full chapter prose, updated memory. After `target_chapters` confirmed chapters, set `current_phase=complete` unless a 5-chapter block review is due.

9. `chapter_block_review`
   - Artifact: `reports/block_review_XXX_YYY.md`
   - Run every 5 confirmed chapters.
   - Distilled skills: block_scope_analysis, stage_goal_review, payoff_debt_audit, foreshadowing_overdue_audit, villain_pressure_audit, relationship_delta_review, engagement_delta_update, chapter_block_revision_plan, chapter_block_final_check.
   - Success: identifies debt, drift, overdue reveals, pressure gaps, and carryovers. If `Problem Chapters` contains `critical` or `high` severity, confirming the report sets `current_phase=revision_required`; otherwise, if the block review follows the final target chapter, confirming it sets `current_phase=complete`; otherwise it returns to `chapter_card`.

## Review Flow

- `candidate_competition`: use before drafting a high-risk chapter. Artifact: `reports/candidate_competition_NNN.md`.
- `consistency_review`: use after several chapters or before revision. Artifact: `reports/consistency_review.md`. Critical/high findings block forward generation through `revision_required`.
- `rolling_outline_update`: when the active catalog window is nearly exhausted, revise `stages/03_story_outline.md` by creating a new suffix file such as `03_story_outline_window_021_040.md`. It must preserve locked phases and only detail the next 10-20 chapters.

## Resume Rule

If `awaiting_confirmation=true`, do not generate the next artifact. Ask the user whether to confirm, revise, or reject `pending_artifact`.
