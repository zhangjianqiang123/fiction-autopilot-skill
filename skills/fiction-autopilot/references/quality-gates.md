# Distilled Quality Gates

Use these gates before asking the user to confirm an artifact.

## Universal Gate

Pass only if the artifact:

- Uses the required headings from `schemas.md`.
- Is specific to the project, audience, genre, and style.
- Respects all confirmed locked facts.
- Separates confirmed facts from risks, options, and suggestions.
- Produces downstream-usable decisions, not generic advice.

Fail if the artifact:

- Contradicts confirmed facts without an explicit revision request.
- Omits a required downstream field.
- Replaces story work with meta commentary.
- Invents a new genre, protagonist, core conflict, or chapter direction after those are confirmed.

## Market And Idea Gate

Pass only if:

- The market promise is clear enough to guide title, opening, and chapter rhythm.
- Reader profile names 2-3 core mass emotions and concrete compensation outlets.
- Differentiation preserves the familiar genre promise while adding a usable novelty angle.
- Market fit notes short drama, short video, audio, positive-value, and supporting-character adaptation risks.
- The core seed contains protagonist, event, required action, failure consequence, and hidden crisis.
- Longform engine can support `target_chapters`.
- Locked facts are concrete and limited.

Fail if:

- The protagonist has no agency.
- The conflict is a premise without active opposition.
- The promise cannot be delivered in scenes.

## Outline Gate

Pass only if:

- Main plot, phase structure, conflict escalation, payoff system, twist system, and ending direction align.
- Chapter catalog covers the requested chapter count or defines a clear rolling segment. For projects over 60 chapters, prefer rolling segments: detailed entries for the active 10-20 chapter window and segment-level constraints for later phases.
- Each catalog entry has goal, hook, and payoff/reveal.
- Continuity rules say what future chapters must preserve.

Fail if:

- The story resolves too early.
- Chapter catalog entries are vague labels.
- Turning points do not increase stakes.
- A long project becomes a 100+ chapter task checklist that forces later prose to merely complete catalog items.

## Character Gate

Pass only if:

- Main characters have goals, desires, flaws, fears, secrets, pressure responses, and voice rules.
- Villains can apply pressure across phases.
- Relationships generate conflict, debt, attraction, betrayal risk, or emotional tension.

Fail if characters are decorative, interchangeable, or cannot affect scenes.

## Opening And Engagement Gate

Pass only if:

- First chapter starts with pressure and protagonist action.
- First three chapters satisfy the golden-three rule: chapter 1 identity + core predicament + irreversible trigger; chapter 2 ability/breakout method + cost/boundary + direction; chapter 3 first counterattack/payoff + chapter-4 hook.
- Engagement ledger gives reusable cadence rules for payoffs, suspense, antagonist pressure, emotion, and chapter endings.
- Payoff items and suspense threads use integer chapter numbers for setup and reveal/payoff.
- Payoff ledger maps emotion pressure to payoff release and prevents "only setup, no release."
- Binge pacing identifies drop risks: three chapters without progress, two chapters of explanation/backstory, more than five chapters of antagonist pressure without counterattack, or payoff below promise.

Fail if:

- Opening only explains background.
- Payoff density is delayed without compensation.
- Suspense threads have no reveal schedule.
- The first three chapters lack any local payoff or strong information gap.

## Chapter Card Gate

Pass only if:

- It matches the chapter catalog entry and current chapter number.
- `Catalog Binding` is present and bound; missing binding means repair the outline/catalog before writing.
- Core conflict has opposed goals and stakes.
- Opening hook creates immediate pressure.
- Key events create visible action, turn, and local payoff.
- Ending hook creates a concrete pursuit question.
- `Emotion Contract` has valid from/to states and can be fulfilled by the planned events.
- `Pressure Level` is `low`, `medium`, `high`, or `critical`; `critical` requires a strong payoff release in the card.

Fail if:

- It jumps ahead, repeats without change, or lacks sceneable conflict.
- It ignores previous chapter handoff or memory.
- It treats the catalog entry as optional inspiration instead of a binding source.

## Chapter Draft Gate

Pass only if:

- `Prose` is a complete chapter.
- Ordinary chapters reach the script floor: at least `max(1500, 80% of chapter_words)` counted prose characters unless the project target is below 1500 or the user approved a short chapter. Lower than target but above this floor is advisory only.
- It covers key events one-to-one, in order, with independent action anchors, information anchors, and situation changes.
- It covers core conflict, payoff, and ending hook.
- It has visible action, dialogue or interior pressure, scene change, character voice, and consequence.
- Each ordinary chapter has at least three dramatic scenes. Every scene must contain pressure, opposition, a risky or failed attempt, consequence, and a changed situation; a scene that only transfers information or marks a task complete does not count.
- Character voice rules are varied in execution. Repeated catchphrases, repeated address forms, and repeated inert action beats are blocking voice issues when they dominate dialogue.
- Causality is visible on the page: each major action has a prior cause, evidence or inference, a choice, a result, and a next pressure.
- `Prose Integrity Check` confirms timeline/space logic, tool/world logic, character motivation, scene changes, and absence of production-control language in `Prose`.
- It preserves continuity from memory and confirmed artifacts.
- Candidate review selected a real candidate instead of rewriting, merging, or inventing a new one.

Fail if:

- It is an outline, summary, patch, or mostly exposition.
- It breaks locked facts.
- It has no meaningful ending pursuit question.
- Required key events are missing, merged into summaries, or renamed so they cannot be verified.
- `pressure_level=critical` and the chapter provides no strong release.
- The chapter reads like a checklist of catalog events rather than staged conflict.
- Dialogue repeats the same opener, slogan, address, or sentence pattern enough to collapse distinct character voice.
- `Prose` contains production-control language such as SEG, 伏笔, 兑现, 章末, 本章, 关键事件, 导演卡, or 章节卡.
- The prose relies on "他知道/她知道/某人知道" instead of showing evidence, inference, or pressure.
- Actions happen in a loose sequence without clear because/therefore/choice/consequence logic.

Rewrite only when `blocking_issues` exist or script validation fails. Blocking issues include empty or summary-like prose, required key-event absence, missing ending hook, below script floor, severe voice collapse, no scene change, hard continuity conflict, or severe character drift. Put polish, pacing, below-target-but-above-floor, and future handoff concerns in advisory notes.

## Memory Gate

Pass only if:

- It records events, state changes, relationship changes, world facts, open threads, foreshadowing, and next-chapter bridge.
- Knowledge items are searchable and evidence-backed.
- Speculation is not treated as confirmed fact.
- Short, mid, and long memory responsibilities are separated.
- `Story Control State` contains current arc, active threads, payoff ledger, character states, continuity facts, world rules, resolved/retired items, next-chapter control, and evidence refs.
- Next-chapter control contains bridge, must-continue items, must-not-contradict facts, priority conflicts, pending questions, due payoffs, and focus characters.

Fail if it only summarizes mood or repeats prose without future-useful facts.

## Review Gate

Block forward progress if review finds:

- Script validation failure in the reviewed block.
- Any ordinary chapter below the script prose floor.
- Severe repeated catchphrase, address form, or action beat that collapses character voice.
- Critical continuity contradiction.
- Overdue reveal that damages reader trust.
- Villain pressure collapse.
- Character motivation drift.
- Chapter block with no payoff or scene change.
- Any `problem_chapters` item has severity `critical` or `high`.

Otherwise record advisory notes and continue.
