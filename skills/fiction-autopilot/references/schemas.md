# Distilled Artifact Schemas

Use stable Markdown headings. These headings are the file-based substitute for the original structured JSON fields.

## Common Header

Every artifact starts with:

```markdown
# <artifact title>

- project: <title>
- unit: <flow_or_chapter_key>
- status: candidate|confirmed
- source: confirmed files used
```

## Market Positioning

Headings:

- Target Channel
- Genre Lane
- Reader Expectations
- Comparable Patterns
- Reader Segments
- Emotional Jobs
- Binge Triggers
- Abandonment Triggers
- Trope Stack
- Promise Statement
- Must Deliver Scenes
- Taboo Misfires
- Familiar Core
- Novelty Angle
- Unfair Advantage
- Positioning Risks
- Title Directions
- Short Blurbs
- Opening Promise
- Cover Keywords
- Final Check

## Idea Incubation

Headings:

- Project Position
- Audience
- Constraints
- Logline Formula
- Protagonist
- Core Event
- Required Action
- Disaster Consequence
- Hidden Crisis
- Longform Engine
- Conflict Escalation
- Episode Hook Pattern
- Title
- Idea Genre
- Story Type
- Worldview
- Logline
- Core Hook
- Main Goal
- Main Conflict
- Drama Hook
- Locked Facts
- Final Check

## Story Outline

Headings:

- Worldview
- Main Goal
- Locked Facts
- Payoff System
- Twist System
- Longform Engine
- Main Conflict
- Stage Conflicts
- Small Payoffs
- Major Reversals
- Stakes Escalation
- Phases
- Global Turning Points
- Foreshadowing Plan
- Catalog Segments
- Chapter Catalog
- Continuity Rules
- Main Plot
- Phase Structure
- Key Turning Points
- Ending Direction
- Final Check

Chapter catalog item format:

```text
chapter_number:
title_hint:
phase:
chapter_goal:
hook:
payoff_or_reveal:
```

## Characters

Headings:

- Role Slots
- Protagonists
- Allies
- Villains
- Gray Characters
- Relationships
- Relationship Tensions
- Betrayal Possibilities
- Final Check

Character item fields:

```text
name:
role:
identity:
external_goal:
inner_desire:
fear:
flaw:
secret:
resources:
weakness:
arc:
function_in_story:
visual_tag:
personality_profile:
dialogue_voice:
behavior_pattern:
emotional_triggers:
moral_boundary:
pressure_response:
relationship_pattern:
```

## Opening Hook And Polish

Opening hook headings:

- Opening Contract
- First Chapter Mission
- First Three Chapter Promise
- Reader Questions
- Opening Image
- Immediate Crisis
- Protagonist Action
- First Reversal
- Chapter End Hook
- First Three Chapter Arc
- AB Options
- Winning Option
- Payoff Density Notes
- Weak Opening Risks
- Fix Suggestions
- Final Check

Opening polish headings:

- Pressure Gaps
- Reader Questions
- Must Intensify
- AB Options
- Payoff Density Notes
- Chapter Targets
- Rewrite Priorities
- Do Not Change
- Final Check

## Reader Engagement

Headings:

- Dominant Emotions
- Emotion Beats
- Pressure Relief Cycle
- Fatigue Risks
- Payoff Items
- Setup Payoff Pairs
- Payoff Cadence
- Must Not Delay
- Antagonist Tiers
- Pressure Escalation
- Counterattack Windows
- Open Threads
- Reveal Schedule
- Misdirection Rules
- Resolution Rules
- Relationship Lines
- Emotional Beats
- Chemistry Moments
- Pacing Rules
- Chapter End Questions
- Cliffhanger Mix
- Micro Payoff Rules
- Fatigue Controls
- Final Check

Payoff item format:

```text
payoff:
type: 智力碾压|身份反转|实力压制|证据反杀|关系背叛揭露|other
setup_chapter: <integer>
due_chapter: <integer>
emotion_trigger: 压抑|愤怒|焦虑|期待|绝望
pressure_threshold:
payoff_description:
status: planned|delivered|delayed|retired
```

Setup/payoff pair format:

```text
setup:
payoff:
setup_chapter: <integer>
payoff_chapter: <integer>
risk_if_delayed:
```

Suspense thread format:

```text
thread:
setup_chapter: <integer>
planned_reveal_chapter: <integer>
status: open|revealed|resolved|retired
```

## Chapter Card

Headings:

- Chapter Number
- Title
- Catalog Binding
- Goal
- Stage Goal
- Previous State
- Core Conflict
- Initiator Goal
- Opponent Goal
- Stakes
- Opening Hook
- Ending Hook
- Pursuit Question
- Key Events
- Twist
- Payoff
- Target Words
- Style Hint
- Emotion Contract
- Pressure Level
- Final Check

Catalog binding format:

```text
mode: required
status: bound|missing
chapter_number:
entry_hash:
entry:
segment:
```

Emotion contract format:

```text
from: 压抑|愤怒|焦虑|期待|绝望
to: 释放|反转|揭秘|升级|翻盘
```

Pressure level must be one of:

```text
low|medium|high|critical
```

## Chapter Draft

Headings:

- Chapter Number
- Title
- Context Lock
- Conflict Design
- Hook Design
- Scene Plan
- Scene Details
- Director Card
- Prose
- Prose Integrity Check
- Candidate Review
- Reader Reaction
- Quality Check
- Summary
- Completed Events
- Ending Hook
- Next Chapter Handoff

The `Prose` section must contain the complete chapter text.

Prose integrity check format:

```text
cause_effect_chain:
  - cause:
    action:
    result:
timeline_and_space_logic:
tool_or_world_logic:
character_motivation:
scene_change_summary:
meta_language_check: no production terms such as SEG, 伏笔, 兑现, 章末, 关键事件, 导演卡, or 章节卡 in Prose
```

This section must be based on the actual `Prose`, not the plan. If any item cannot be answered from the prose itself, rewrite the prose.

Scene plan item format:

```text
scene_key:
purpose:
location:
time:
participants: <official character names only>
conflict_beat:
entry_hook:
opposition:
risky_or_failed_attempt:
consequence:
exit_change:
word_budget_ratio: <number, all scenes should total about 1.0>
```

Director card voice format:

```text
character_name:
dialogue_examples:
never_say:
gesture_habits:
conflict_style:
```

Director card must also include:

```text
repetition_watchlist:
  phrase:
  max_uses:
  substitute_strategy:
```

Quality check fields:

```text
pass_status: passed|rewrite_needed|fail
blocking_issues:
advisory_notes:
next_chapter_handoff:
rewrite_instruction:
quality_scores:
editorial_scores:
editorial_notes:
rewrite_mode: voice_rewrite|scene_intensity_rewrite|hook_rewrite|payoff_rewrite|length_expand_rewrite
```

`pass_status: passed` is invalid when script validation would fail. The `Prose` section must satisfy the script floor, which is `max(1500, 80% of chapter_words)` counted prose characters for ordinary chapters unless the project target is below 1500 or a short chapter was explicitly approved.

Completed events must preserve the chapter card's key-event order and names closely enough for one-to-one verification.

## Memory Update

Headings:

- Source Chapter
- Chapter Summary
- Current Events
- Ending State
- Previous Hook
- Chapter Events
- Next Chapter Bridge
- Recent Arc Summary
- Active Conflicts
- Unresolved Threads
- Pacing Notes
- Global Summary Delta
- Character State Deltas
- World Fact Deltas
- Foreshadowing Updates
- Story Control State
- Knowledge Items
- Retrieval Queries
- Searchable Chunks
- Final Check

Story control state format:

```text
current_arc:
active_threads:
payoff_ledger:
character_states:
continuity_facts:
world_rules:
resolved_or_retired:
next_chapter_control:
  bridge_from_previous_hook:
  must_continue:
  must_not_contradict:
  priority_conflicts:
  pending_questions:
  due_payoffs:
  focus_characters:
evidence_refs:
```

Knowledge item format:

```text
item_type: fact|character_state|relationship|conflict|foreshadowing|open_thread|resolved_thread|world_rule|chapter_event
subject:
predicate:
object:
content:
evidence:
importance: 1-10
visibility:
status: confirmed|open|resolved|retired
```

## Candidate Competition

Headings:

- Chapter Card Summary
- Evaluation Dimensions
- Baseline Requirements
- Reader Personas
- Likely Reactions
- Drop Points
- Binge Points
- Must Deliver Scenes
- Scores
- Winning Edges
- Dealbreakers
- Reader Expectations
- Drop Risk Points
- Pacing Advice
- Do Not Merge
- Revision Strategy
- Final Check

Revision strategy fields:

```text
reader_expectations:
drop_risk_points:
must_deliver_scenes:
pacing_advice:
do_not_merge:
```

## Consistency Review

Headings:

- Timeline Issues
- Continuity Risks
- Locked Fact Conflicts
- Character Drift
- Voice Drift
- Relationship Inconsistencies
- Open Threads
- Payoff Gaps
- Overdue Reveals
- Priority Fixes
- Chapter Targets
- Do Not Change
- pass_status: passed|fail
- severity: critical|high|medium|low
- Final Check

## Chapter Block Review

Headings:

- Chapter Range
- Block Goal
- Available Evidence
- Mechanical Quality Audit
- Stage Goal Alignment
- Progress Gaps
- Next Stage Pressure
- Payoff Debts
- Delivered Payoffs
- Overdue Payoffs
- Open Threads
- Overdue Threads
- Reveal Priorities
- Villain Moves
- Pressure Gaps
- Counterpressure Needed
- Relationship Changes
- Character State Deltas
- Voice Or Motivation Drifts
- Engagement Delta
- Revision Priorities
- Do Not Change
- Next Chapter Carryovers
- Problem Chapters
- Final Check

Problem chapter format:

```text
chapter_number: <integer>
issues:
  - type: payoff_overdue|foreshadowing_open|villain_weak|relationship_drift|pacing|meta_language|weak_causality|checklist_prose|voice_repetition
    detail:
fix_instruction:
severity: critical|high|medium|low
```
