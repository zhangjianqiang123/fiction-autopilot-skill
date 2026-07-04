# Fiction Autopilot Skill

`fiction-autopilot` 是一个面向 Codex 的中文小说全流程 Skill。它把“写一本小说”这类请求拆成可恢复、可确认、可校验的文件化流程，适合从书名或简短设定开始，逐步生成定位、创意、大纲、角色、章节卡、正文、记忆和复盘报告。

这个 Skill 不依赖原后端服务，不调用 FastAPI。所有产物都会落到本地项目目录里，并通过 `state.json` 记录当前阶段，方便中断后继续。

## 核心能力

- 从书名或小说简介启动完整创作流程。
- 在缺少题材、目标章数、每章字数、目标读者、风格偏好、禁写内容时先追问，不直接开写。
- 按阶段生成：市场定位、创意孵化、故事大纲、角色设计、开局钩子、读者爽点账本、章节卡、章节正文、记忆、五章复盘。
- 每个阶段有确认闸门，确认后才进入下一阶段。
- 每章先生成章节卡，确认章节卡后再写正文。
- 每章正文确认后生成记忆文件，记录事件、人物状态变化、世界事实、未解悬念和下一章承接。
- 支持断点续跑，通过 `state.json` 找回当前阶段和下一步动作。
- 提供脚本校验，不再只依赖模型自评。
- 针对长篇小说采用滚动目录思路，避免一次性细化几百章导致正文变成机械清单。

## 适合场景

- 想用 Codex 生成或续写中文长篇小说。
- 想把小说创作过程拆成可检查的阶段产物。
- 想保留章节卡、正文、记忆、复盘等中间文件。
- 想让 AI 写作过程更可控，而不是一次性生成一大段不可追踪文本。
- 想在质量较差时通过脚本拦截字数不足、事件缺失、重复表达、元叙事词泄漏、记忆缺失等问题。

## 仓库结构

```text
fiction-autopilot-skill/
├── README.md
├── LICENSE
└── skills/
    └── fiction-autopilot/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        │   └── templates/
        ├── references/
        │   ├── flows.md
        │   ├── schemas.md
        │   ├── quality-gates.md
        │   └── prompts/
        └── scripts/
            ├── init_project.py
            ├── status.py
            ├── set_pending.py
            ├── confirm_artifact.py
            └── validate_artifacts.py
```

## 安装方式

### 1. 克隆仓库

```bash
git clone https://github.com/zhangjianqiang123/fiction-autopilot-skill.git
cd fiction-autopilot-skill
```

### 2. 复制 Skill 到 Codex skills 目录

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse ".\skills\fiction-autopilot" "$env:USERPROFILE\.codex\skills\fiction-autopilot" -Force
```

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/fiction-autopilot ~/.codex/skills/fiction-autopilot
```

### 3. 重启 Codex

如果 Codex 已经在运行，安装后建议重启，让 Codex 重新发现这个 Skill。

## 如何使用

在 Codex 中直接提出小说创作请求，例如：

```text
用 fiction-autopilot 写一本小说，书名《归墟回声》。
```

如果只提供书名，Skill 会先追问必要信息：

- 书名
- 题材/类型
- 目标章数
- 每章字数
- 目标读者
- 风格偏好
- 禁写内容

补齐后，Skill 会创建小说项目目录，并按阶段推进。

## 默认项目产物

生成小说时，默认会创建类似下面的文件结构：

```text
novels/<slug>/
├── project.json
├── state.json
├── stages/
│   ├── 01_market_positioning.md
│   ├── 02_idea_incubation.md
│   ├── 03_story_outline.md
│   ├── 05_opening_hook.md
│   └── 06_reader_engagement.md
├── characters/
│   └── characters.md
├── chapters/
│   ├── chapter_001_card.md
│   └── chapter_001.md
├── memory/
│   └── memory_001.md
└── reports/
    └── block_review_001_005.md
```

其中：

- `project.json` 保存项目基础信息。
- `state.json` 保存当前阶段、已确认阶段、已完成章节和下一步动作。
- `stages/` 保存市场定位、创意、大纲、开局、读者爽点账本。
- `characters/` 保存角色表和人物关系。
- `chapters/` 保存章节卡和章节正文。
- `memory/` 保存每章后的记忆控制文件。
- `reports/` 保存周期性复盘和质量报告。

## 执行流程

默认流程如下：

1. 市场定位：确定题材、读者、爽点、差异化和禁区。
2. 创意孵化：生成主角、核心事件、失败代价、隐藏危机和故事种子。
3. 故事大纲：生成阶段目标、冲突系统、爽点系统、反转系统和滚动目录。
4. 角色设计：生成主角、盟友、反派、灰色角色和关系张力。
5. 开局钩子：设计前三章的压力、行动、反转和留钩。
6. 读者参与账本：规划爽点、悬念、压迫、反击窗口和章节结尾问题。
7. 章节循环：
   - 生成章节卡。
   - 用户确认章节卡。
   - 生成正文。
   - 用户确认正文。
   - 生成记忆。
   - 每 5 章做一次章节块复盘。

## 确认闸门

Skill 使用显式确认机制：

- 生成一个阶段产物后，会设置为待确认。
- 未确认前不会继续下一阶段。
- 用户可以确认、拒绝或要求修订。
- 确认时脚本会再次校验，校验失败不会推进状态。

相关脚本：

```bash
python skills/fiction-autopilot/scripts/set_pending.py <project_dir> <artifact_path>
python skills/fiction-autopilot/scripts/confirm_artifact.py <project_dir>
python skills/fiction-autopilot/scripts/confirm_artifact.py <project_dir> --reject --reason "原因"
python skills/fiction-autopilot/scripts/confirm_artifact.py <project_dir> --revise --reason "修改要求"
```

## 质量校验

`validate_artifacts.py` 会检查小说项目或单个产物。

校验整个项目：

```bash
python skills/fiction-autopilot/scripts/validate_artifacts.py novels/<slug>
```

校验单个章节：

```bash
python skills/fiction-autopilot/scripts/validate_artifacts.py novels/<slug> --artifact chapters/chapter_001.md
```

当前校验重点包括：

- 必填字段是否存在。
- 阶段产物是否缺失。
- 章节编号是否连续。
- 章节卡是否绑定目录。
- 章节卡是否包含核心冲突、追问、爽点、情绪契约和压力等级。
- 正文是否低于最低字数地板。
- 正文是否覆盖章节卡关键事件。
- 正文是否混入 `SEG`、`伏笔`、`章末`、`关键事件` 等流程词。
- 正文是否出现严重重复口头禅、称呼或动作句。
- 正文是否缺少显式因果链。
- 记忆文件是否包含人物状态、世界事实、开放悬念和检索项。
- 复盘报告是否把严重问题标记为阻断项。

脚本校验高于模型自评。即使正文里写了 `Quality Check: passed`，只要脚本校验失败，也不能确认通过。

## 正文质量规则

这个 Skill 不只检查字数，也会尽量拦截常见 AI 水稿问题：

- 不能把章节写成事件清单。
- 不能只写“到达、看见、打开、读出、完成”。
- 每个重要动作都应有原因、阻力、选择、代价和结果变化。
- 人物“知道”某事时，应在页面上给出证据或推理。
- 章节正文不能出现面向作者的流程语言。
- 对白例句只能作为语气参考，不能反复复制。
- 长篇只细化当前滚动窗口，避免几百章目录把正文推成打卡式推进。

## 常用脚本

初始化项目：

```bash
python skills/fiction-autopilot/scripts/init_project.py \
  --title "书名" \
  --genre "题材" \
  --chapters 20 \
  --chapter-words 2000 \
  --audience "目标读者" \
  --style "风格偏好" \
  --forbidden-content "禁写内容"
```

查看状态：

```bash
python skills/fiction-autopilot/scripts/status.py novels/<slug>
```

设置待确认：

```bash
python skills/fiction-autopilot/scripts/set_pending.py novels/<slug> chapters/chapter_001.md
```

确认产物：

```bash
python skills/fiction-autopilot/scripts/confirm_artifact.py novels/<slug>
```

请求修订：

```bash
python skills/fiction-autopilot/scripts/confirm_artifact.py novels/<slug> --revise --reason "正文像流水账，需要加强场景冲突"
```

## 开发与校验

校验 Skill 元数据：

```bash
python <skill-creator>/scripts/quick_validate.py skills/fiction-autopilot
```

编译脚本：

```bash
python -m py_compile skills/fiction-autopilot/scripts/*.py
```

发布前建议确认：

- 不包含生成的 `novels/` 项目。
- 不包含 `__pycache__/` 或 `.pyc`。
- 不包含个人书稿、账号凭据、临时目录。
- `README.md`、`LICENSE`、`SKILL.md` 都存在。

## 限制

- 这是文件化 Skill，不是完整小说写作平台。
- 它不会自动调用后端服务。
- 它不能保证每次生成的正文都达到出版级质量，但会通过流程和脚本拦截明显问题。
- 高质量长篇仍需要人工确认、修订和阶段性复盘。

## License

MIT
