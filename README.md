# Fiction Autopilot Skill

`fiction-autopilot` is a Codex Skill for file-based Chinese fiction production. It turns a title or brief into a checkpointed novel project with staged planning, chapter cards, chapter prose, memory updates, validation gates, and resumable state.

The skill is designed to run without the original backend service. It stores every artifact as local files and uses explicit confirmation gates before advancing the workflow.

## Features

- End-to-end novel workflow: positioning, idea incubation, outline, characters, opening, reader engagement, chapter cards, prose, memory, and block review.
- File-based project state with `project.json` and `state.json`.
- Validation scripts for required fields, chapter continuity, prose length, event coverage, repetition, meta-language leaks, memory structure, and review blocking.
- Rolling outline guidance for long projects to avoid turning prose into a mechanical checklist.
- Chinese fiction prompts distilled for scene pressure, payoff, continuity, and reader retention.

## Install

Copy the skill folder into your Codex skills directory:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse .\skills\fiction-autopilot "$env:USERPROFILE\.codex\skills\fiction-autopilot" -Force
```

On macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/fiction-autopilot ~/.codex/skills/fiction-autopilot
```

Restart Codex if it was already running.

## Usage

Ask Codex to use the skill, for example:

```text
用 fiction-autopilot 写一本小说，书名《归墟回声》。
```

If required inputs are missing, the skill should ask for:

- title
- genre
- target chapters
- chapter words
- audience
- style reference
- forbidden content

Generated projects are created under `novels/<slug>/` unless another directory is provided.

## Validation

Validate the skill metadata:

```powershell
$env:PYTHONUTF8='1'
python C:/Users/yuanw/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./skills/fiction-autopilot
```

Validate a generated novel project:

```powershell
python ./skills/fiction-autopilot/scripts/validate_artifacts.py ./novels/<slug>
```

Validate one artifact:

```powershell
python ./skills/fiction-autopilot/scripts/validate_artifacts.py ./novels/<slug> --artifact chapters/chapter_001.md
```

## Notes

- The skill does not call the original FastAPI backend.
- Do not commit generated `novels/` projects unless you intentionally want to publish those artifacts.
- Script validation is authoritative. A model-written `Quality Check: passed` cannot override failed script checks.

## License

MIT

