# Distilled Chapter Prompt Cards

Use these cards for chapter planning and prose production. Read confirmed outline, characters, opening/engagement files, latest memory, and previous chapter before generating.

## Chapter Contract Essentials

- Treat the confirmed chapter catalog entry as binding. Chapter cards may enrich, but must not replace, skip, or contradict it.
- Treat `emotion_contract`, `pressure_level`, payoff ledger items, suspense ledger items, previous chapter handoff, and latest memory as the chapter's live control state.
- Ordinary chapter prose must satisfy the script floor: at least `max(1500, 80% of chapter_words)` counted prose characters unless the project target is below 1500 or the user explicitly approves a shorter chapter. `target_words` is the aim; falling below the script floor is a blocking failure.
- Key events are the spine. Preserve order and one-to-one coverage from card -> scenes -> prose -> completed events.
- Do not confuse event coverage with scene quality. Each key event must land inside a scene with pressure, opposition, risky action, consequence, and a changed situation.
- The prose must be readable without the chapter card. It must explain why each action happens now, what blocks it, what choice the character makes, what changes after the choice, and why the next beat follows.
- Never let planning/control language leak into `Prose`: do not write SEG, 伏笔, 兑现, 章末, 本章, 关键事件, 导演卡, 章节卡, or reader-facing analysis inside the chapter text.

## chapter_plan

- `chapter_card_design`: Design a chapter card bound to the catalog entry. Required content: chapter number, title, goal, stage goal, previous state, core conflict, initiator goal, opponent goal, stakes, opening hook, ending hook, pursuit question, key events, twist, payoff, target words, style hint, catalog binding, emotion contract, pressure level.
  - Copy `catalog_binding` from the current catalog context, including entry hash, entry, and segment; do not invent or omit it. If no bound catalog entry exists, stop and ask to repair the outline/catalog before drafting.
  - Define `emotion_contract` as `{from, to}` using states such as repression, anger, anxiety, expectation, despair -> release, reversal, reveal, upgrade, comeback.
  - Set `pressure_level` to `low`, `medium`, `high`, or `critical` from recent pressure/release history. If `critical`, the card must contain a strong payoff release.
- `chapter_card_final_check`: Check catalog binding, conflict, stakes, hook, event coverage, payoff, style hint, and continuity. Pass only when the card can directly guide prose.

## chapter_draft_setup

- `chapter_context_lock`: Lock chapter card, locked facts, continuity state, previous handoff, memory, and draft word target. This is the chapter's contract.
  - If a candidate-competition report exists for this chapter, copy its reader expectations, drop-risk points, must-deliver scenes, pacing advice, and do-not-merge constraints into the chapter contract. Prose generation must obey them.
- `draft_conflict_design`: Convert card conflict into concrete scene pressure: core conflict, stakes, escalation, opposition method, and failure cost.
- `draft_hook_design`: Convert opening hook, ending hook, and pursuit question into prose obligations. Opening must answer or intensify the previous handoff.
- `scene_plan`: Plan scenes by length and event count: about 2-3 scenes for 1000 words, 3-4 for 2000, 4-5 for 3200, 6 for 5000, 8 for 9000, 10 for 12000, then scale carefully. Each scene needs dramatic function, location/time, participants, conflict beat, information gap, micro payoff, emotional shift, last image, and `word_budget_ratio`. Participants must use official names from `characters/characters.md`; do not create new names or aliases unless the chapter card explicitly introduces them.
- `scene_detail_generate`: For each scene, detail scene goal, character actions, opposition, failed or risky attempt, immediate consequence, emotional shift, key information, sensory anchors, and scene-ending change. Every key event needs its own action anchor, information anchor, visible situation change, and closing image; do not merge multiple key events into one summary. Replace "arrive -> see -> open/read -> complete" chains with "observe -> infer wrongly or incompletely -> pressure worsens -> choose cost -> act -> result changes leverage."
- `scene_continuity_check`: Check scene order, causality, escalation, handoff continuity, missing scene details, and whether every planned scene changes the situation. For each scene answer: because of what prior beat, why now, why this character, what alternative was rejected, and what concrete state changed.
- `chapter_director`: Produce the writing director card: emotional throughline, opening bridge, scene brief, character voice brief, pacing warning, quality watchpoints, repetition watchlist, and rewrite strategy. `character_voice_brief` must include `dialogue_examples`, `never_say`, `gesture_habits`, and `conflict_style`. Dialogue examples are examples of rhythm, not fixed lines to repeat. Include rewrite-mode triggers for `voice_rewrite`, `scene_intensity_rewrite`, `hook_rewrite`, `payoff_rewrite`, and `length_expand_rewrite`.

## prose_candidates

- `prose_generation`: Write a complete chapter candidate from the director card. Required content: full prose, prose integrity check, summary, completed events, ending hook. The `Prose` section must contain only the actual chapter正文, not scene plans, commentary, checkmarks, or patch notes. The prose must land each key event in order inside dramatic scenes; `completed_events` must match the chapter card's key events instead of renaming them.
- `prose_integrity_check`: After drafting, audit only the actual `Prose`: cause/effect chain, timeline and space logic, tool or world logic, character motivation, scene-change summary, and meta-language leak. If any answer depends on the outline rather than words on the page, rewrite the prose before quality check.
- `candidate_review`: Compare 2-3 candidates if available. Select one existing candidate; do not merge, rewrite, patch, or synthesize a new version. Prioritize key-event coverage, character voice, scene change, payoff landing, ending hook, hard floor, and locked-fact consistency. Below target but above hard floor is advisory, not failure.
- `reader_reaction_review`: Simulate target readers. Output binge points, drop points, confusion points, payoff landing, and rewrite suggestions. Separate blocking issues from advice.
- `candidate_polish`: For local fixes only, output the complete polished chapter, summary, polish targets, and fixed issues. Preserve effective passages.
- `chapter_quality_check`: Check pass status, final output, issues, blocking issues, advisory notes, next chapter handoff, rewrite instruction, quality scores, editorial scores, editorial notes, rewrite focus, and rewrite mode. Script validation is authoritative: never mark `passed` when prose is below the script floor, key events are missing, scene count is too low, repeated lines dominate voice, meta/control terms appear in `Prose`, the cause/effect chain is unclear, or `blocking_issues` is non-empty. Below target but above the script floor is advisory only.
- `chapter_rewrite`: When blocking issues exist, rewrite the full chapter. Fix the specified issues while preserving locked facts, chapter goal, and effective existing material. Return a complete chapter, not a replacement fragment or explanation.

## candidate_competition

Use before high-risk chapters or when the user wants reader simulation before prose.

- `candidate_inventory`: Summarize chapter card, evaluation dimensions, and baseline requirements.
- `reader_simulation`: Define reader personas, likely reactions, drop points, binge points, and must-deliver scenes.
- `competitive_scoring`: Score pursuit potential, winning edges, dealbreakers, and reasoning.
- `revision_strategy`: Convert simulation into reader expectations, drop-risk points, must-deliver scenes, pacing advice, and do-not-merge constraints.
- `competition_final_check`: Confirm the recommended strategy is usable before drafting.

## Chapter Writing Rules

- Start with pressure, not exposition.
- Every scene must change information, leverage, emotion, or relationship state.
- Every scene must include resistance. A scene where the protagonist simply arrives, reads, opens, agrees, or completes a task without opposition or cost must be rewritten.
- Every action needs visible logic on the page. If the protagonist knows something, show evidence or inference; do not rely on "he knew" as a shortcut.
- Avoid completion language. A chapter should not read like a mission report with "完成第一步", "任务完成", or "继续 SEG"; translate those into in-world stakes, choices, and consequences.
- Dialogue must reveal pressure or conceal intention.
- Do not reuse dialogue examples verbatim more than once. Do not let every character address the same person with the same opener.
- Payoff must land inside the chapter when the card or ledger makes it due, even when larger suspense remains open.
- Ending hook must name a concrete new danger, question, reveal, deadline, or choice.
- Do not let the protagonist wait passively for rescue or rewards when the chapter promises a counterattack or payoff.
- Avoid floating payoff: make the satisfying moment depend on concrete skill, evidence, leverage, choice, or consequence instead of arbitrary money, force, or coincidence.
- If `pressure_level=critical`, the chapter must release pressure through a strong, visible payoff unless the user explicitly chooses a tragic/dark delay.
- If the draft fails hard quality gates, rewrite rather than explain.
