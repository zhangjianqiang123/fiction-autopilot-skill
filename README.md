<div align="center">

# Fiction Autopilot Skill

### 让 Codex 按“定位 → 大纲 → 角色 → 章节卡 → 正文 → 记忆 → 复盘”写完中文小说

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](skills/fiction-autopilot/SKILL.md)
[![Workflow](https://img.shields.io/badge/workflow-file--based-blue)](skills/fiction-autopilot/references/flows.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> 一个面向 Codex 的中文小说全流程 Skill。
>
> 从书名或简短设定启动，把小说创作拆成可确认、可续跑、可校验的文件化流程，避免一口气生成后逻辑断裂、章节重复、人物跑偏、记忆丢失。

</div>

## ✨ 为什么用这个？

AI 写长篇小说最容易翻车的地方，不是“不会写”，而是**写着写着失控**：前后设定冲突、章节像流水账、爽点不兑现、角色台词重复、伏笔没人记。

`fiction-autopilot` 专门解决这些问题：

- **先问清楚再开写**：只给书名时，会先补齐题材、章数、字数、受众、风格和禁写内容。
- **阶段确认**：市场定位、大纲、角色、开局、章节卡都要确认后才继续。
- **章节卡驱动正文**：每章先锁定冲突、事件、爽点、追问和结尾钩子，再写正文。
- **文件化记忆**：每章后生成记忆文件，记录事件、人物变化、世界事实、未解悬念和下一章承接。
- **断点续跑**：`state.json` 记录当前阶段，中断后可以从上次位置继续。
- **脚本校验**：用脚本检查缺字段、章节连续性、正文长度、事件覆盖、记忆结构和复盘阻断项。
- **长篇友好**：滚动细化当前章节窗口，避免几百章目录把正文压成机械任务清单。

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zhangjianqiang123/fiction-autopilot-skill.git
cd fiction-autopilot-skill
```

### 2. 安装到 Codex skills 目录

Windows PowerShell:

```powershell
$dest = "$env:USERPROFILE\.codex\skills\fiction-autopilot"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item -Recurse -Force ".\skills\fiction-autopilot\*" $dest
```

macOS / Linux:

```bash
mkdir -p ~/.codex/skills/fiction-autopilot
cp -R ./skills/fiction-autopilot/. ~/.codex/skills/fiction-autopilot/
```

### 3. 重启 Codex

安装后重启 Codex，让它重新发现 `fiction-autopilot`。

### 4. 输入指令

```text
用 fiction-autopilot 写一本小说，书名《归墟回声》。
```

如果你只输入书名，Skill 会先追问必要参数，不会直接开写。

## 🖼️ 使用过程

<table>
  <tr>
    <td align="center"><b>Phase 1 — 参数补齐</b></td>
    <td align="center"><b>Phase 2 — 规划确认</b></td>
  </tr>
  <tr>
    <td>确认书名、题材、目标章数、每章字数、目标读者、风格偏好和禁写内容。</td>
    <td>生成市场定位、创意孵化、大纲、角色、开局钩子和读者参与账本。</td>
  </tr>
  <tr>
    <td align="center"><b>Phase 3 — 逐章创作</b></td>
    <td align="center"><b>Phase 4 — 复盘修订</b></td>
  </tr>
  <tr>
    <td>每章先出章节卡，确认后写正文，正文确认后更新记忆。</td>
    <td>每 5 章做一次章节块复盘；严重问题会阻断继续生成，先修再写。</td>
  </tr>
</table>

## 📊 创作流程

```text
用户输入
                      ↓
┌────────────────────────────────────────────┐
│ Phase 0 项目初始化                         │
│ ·补齐必填参数                              │
│ ·创建 project/state                        │
│ ·检测断点状态                              │
└────────────────────────────────────────────┘
                      ↓
┌────────────────────────────────────────────┐
│ Phase 1-2 故事规划                         │
│ 市场定位 → 创意孵化 → 大纲 → 角色          │
│ 开局钩子 → 读者爽点账本                    │
└────────────────────────────────────────────┘
                      ↓
┌────────────────────────────────────────────┐
│ Phase 3 章节循环                           │
│ 章节卡 → 用户确认 → 正文 → 用户确认        │
│ → 记忆更新 → 下一章                        │
└────────────────────────────────────────────┘
                      ↓
┌────────────────────────────────────────────┐
│ Phase 4 质量复盘                           │
│ 每 5 章检查节奏、兑现、伏笔、人物和逻辑    │
│ critical/high 问题会进入 revision 状态     │
└────────────────────────────────────────────┘
                      ↓
                   全稿完成
```

## 📖 输出样例

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
│   ├── chapter_001.md
│   ├── chapter_002_card.md
│   └── chapter_002.md
├── memory/
│   ├── memory_001.md
│   └── memory_002.md
└── reports/
    └── block_review_001_005.md
```

## 🎯 核心法则

| 法则 | 说明 |
|------|------|
| **先锁定再生成** | 每个阶段确认后才成为下游事实，未确认内容不能继续推进。 |
| **章节卡约束正文** | 正文必须兑现章节卡里的冲突、事件、爽点、情绪变化和结尾追问。 |
| **展示而非讲述** | 正文要写场景、动作、对话、选择和代价，不能写成摘要或事件清单。 |
| **记忆驱动续写** | 每章完成后把事件、人物状态、世界事实和悬念写入记忆文件。 |
| **严重问题先修复** | 复盘发现 critical/high 问题时，状态会进入修订，不继续往后水。 |

## 🛠️ 常用命令

初始化小说项目：

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

查看当前进度：

```bash
python skills/fiction-autopilot/scripts/status.py novels/<slug>
```

设置待确认产物：

```bash
python skills/fiction-autopilot/scripts/set_pending.py novels/<slug> chapters/chapter_001_card.md
```

确认产物并推进状态：

```bash
python skills/fiction-autopilot/scripts/confirm_artifact.py novels/<slug>
```

拒绝或要求修订：

```bash
python skills/fiction-autopilot/scripts/confirm_artifact.py novels/<slug> --reject --reason "不符合预期"
python skills/fiction-autopilot/scripts/confirm_artifact.py novels/<slug> --revise --reason "正文像流水账，需要加强场景冲突"
```

校验项目或单个文件：

```bash
python skills/fiction-autopilot/scripts/validate_artifacts.py novels/<slug>
python skills/fiction-autopilot/scripts/validate_artifacts.py novels/<slug> --artifact chapters/chapter_001.md
```

## 🔍 质量控制

`validate_artifacts.py` 会做硬性检查，脚本结果高于模型自评。

当前重点检查：

- 阶段产物是否缺失必填标题和结构。
- 章节编号是否连续。
- 章节卡是否包含 `Catalog Binding`、`Emotion Contract`、`Pressure Level`、`Payoff`、`Pursuit Question`。
- 正文是否包含 `Prose`、`Completed Events`、`Ending Hook`、`Quality Check`。
- 正文区块是否达到最低字符数地板。
- 正文是否覆盖章节卡关键事件。
- 正文是否混入 `SEG`、`伏笔`、`章末`、`关键事件`、`章节卡` 等流程词。
- 记忆是否包含 `Story Control State`、`Knowledge Items`、`Retrieval Queries`。
- 五章复盘是否把严重问题写入 `Problem Chapters`。

## 📚 内置参考资料

### 流程文档

| 文件 | 内容 |
|------|------|
| `references/flows.md` | 阶段顺序、产物路径、确认闸门和断点续跑规则。 |
| `references/schemas.md` | 市场定位、大纲、角色、章节卡、正文、记忆、复盘等产物结构。 |
| `references/quality-gates.md` | 每个阶段的通过/失败标准，以及阻断继续生成的条件。 |

### 提示词精炼包

| 文件 | 内容 |
|------|------|
| `references/prompts/design.md` | 市场定位、创意孵化、大纲、角色、开局和读者参与设计。 |
| `references/prompts/chapter.md` | 章节卡、正文场景、导演卡、正文质检和重写规则。 |
| `references/prompts/memory.md` | 记忆更新、候选竞争、连续性检查和五章复盘。 |

### 模板

| 目录 | 内容 |
|------|------|
| `assets/templates/` | 阶段、章节卡、正文、记忆、复盘、候选竞争和连续性检查模板。 |

## 🧩 仓库结构

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

## 🔄 设计取向

这个 Skill 不是“全自动无人值守一路写到完稿”的工具，而是**自动生成 + 人工确认 + 脚本校验 + 断点续跑**的协作流程。

默认不会跨过确认闸门：

- 未确认大纲，不进入角色设计。
- 未确认章节卡，不写正文。
- 未确认正文，不更新记忆。
- 复盘发现严重问题，不继续生成下一章。

这样会慢一点，但更适合长篇小说的可控生产。

## ⚠️ 限制

- 这是 Codex Skill，不依赖原后端服务，也不会调用 FastAPI。
- 它能显著降低长篇失控概率，但不能保证每章都达到出版级质量。
- 高质量长篇仍需要人工确认、阶段性修订和必要的审稿判断。
- 当前版本优先支持 Codex，未提供 Claude Code 专属格式。

## 🔗 相关链接

- 完整小说写作平台：<https://aixiaoshuo.cloud>
- 咨询联系：<985018505@qq.com>

## ⚖️ License

MIT
