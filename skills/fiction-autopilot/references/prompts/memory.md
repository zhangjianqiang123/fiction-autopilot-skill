# Distilled Memory And Review Prompt Cards

Use these cards after confirmed prose or during periodic review.

## Memory Contract Essentials

- Memory is not a recap dump. It is the control layer for the next chapter card and later continuity checks.
- Separate short, mid, and long memory. Short memory carries the immediate hook and chapter handoff; mid memory carries the recent arc; long memory carries durable facts, character states, world rules, payoffs, and unresolved threads.
- Never promote suspicion, misdirection, fake-outs, or reader interpretation into confirmed fact. Mark them as open thread or speculation until the prose confirms them.

## memory_update

- `memory_input_analysis`: Extract chapter summary, current events, and ending state from the confirmed chapter.
- `short_memory_update`: Record previous hook resolution, chapter events, chapter summary, and next chapter bridge.
- `mid_memory_update`: Update recent arc summary, active conflicts, unresolved threads, and pacing notes.
- `long_memory_update`: Update global summary delta, character state deltas, world fact deltas, foreshadowing updates, and story control state. `story_control_state` must include current arc, active threads, payoff ledger, character states, continuity facts, world rules, resolved/retired items, next-chapter control, and evidence references.
- `knowledge_extract`: Extract searchable knowledge items with type, subject, predicate, object, content, evidence, importance, visibility, and status. Use only these item types unless the user extends the schema: fact, character_state, relationship, conflict, foreshadowing, open_thread, resolved_thread, world_rule, chapter_event.
- `retrieval_index_plan`: Create retrieval queries and searchable chunks future chapters can use.
- `memory_final_check`: Confirm memory separates fact from speculation and is useful for future chapter cards and prose.

## consistency_review

- `continuity_audit`: Find timeline issues, continuity risks, and locked fact conflicts.
- `character_state_audit`: Find character drift, voice drift, and relationship inconsistencies.
- `foreshadowing_payoff_audit`: Track open threads, payoff gaps, and overdue reveals.
- `revision_priority_plan`: Produce priority fixes, chapter targets, and do-not-change constraints.
- `consistency_final_check`: Confirm whether generation may continue or must stop for revision. If any finding is `critical` or `high`, write a clear `pass_status: fail` or severity line so `confirm_artifact.py` can move state to `revision_required`.

## chapter_block_review

Run every 5 confirmed chapters.

- `block_scope_analysis`: Define chapter range, block goal, and available evidence.
- `mechanical_quality_audit`: Read the actual chapter files, not summaries. Record prose character counts, repeated catchphrases/address forms, production-control terms leaked into `Prose`, weak cause/effect chains, checklist/completion language, key-event coverage gaps, missing memory files, and any script validation failures.
- `stage_goal_review`: Review stage goal alignment, progress gaps, and next-stage pressure.
- `payoff_debt_audit`: List payoff debts, delivered payoffs, and overdue payoffs.
- `foreshadowing_overdue_audit`: List open threads, overdue threads, and reveal priorities.
- `villain_pressure_audit`: Review villain moves, pressure gaps, and counterpressure needed.
- `relationship_delta_review`: Review relationship changes, character state deltas, and voice or motivation drifts.
- `engagement_delta_update`: Update emotion curve, payoff ledger, suspense thread ledger, and pacing adjustments.
- `chapter_block_revision_plan`: Produce revision priorities, do-not-change list, next chapter carryovers, and structured `problem_chapters`. Each problem chapter needs integer `chapter_number`, `issues` with type/detail, concrete `fix_instruction`, and severity `critical`, `high`, `medium`, or `low`. Use `high` for below-floor prose, missing key events, meta/control language in `Prose`, severe repetition, weak cause/effect chain, or a chapter that reads like a checklist; use `critical` when continuity or reader trust is broken.
- `chapter_block_final_check`: Confirm whether the block passes or requires revision before continuing. If any problem chapter is `critical` or `high`, stop forward generation and require revision or user approval to continue despite risk.

## Review Severity

- `critical`: blocks future continuity or reader trust; stop generation.
- `high`: should be fixed before next block; stop if it affects current next chapter.
- `medium`: record in report and address when convenient.
- `low`: advisory note only.

## Memory Writing Rules

- Record state changes, not just events.
- Include evidence for knowledge items.
- Preserve unresolved questions explicitly.
- Convert chapter endings into next-chapter obligations.
- Track payoff debt and reveal debt by chapter number so future chapter cards can call them.
- Keep character state changes causal: who changed, what changed, why, and what source proves it.
- In `next_chapter_control`, always include bridge from previous hook, must-continue items, must-not-contradict facts, priority conflicts, pending questions, due payoffs, and focus characters.
- Do not mark guesses, fake-outs, or suspected motives as confirmed facts.
