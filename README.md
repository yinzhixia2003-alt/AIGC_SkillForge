# AIGC SkillForge

面向 AI 影视创作的 Codex 技能包集合。

本项目目前提供两个可独立使用、也可串联工作的技能包，把中文剧本逐步转换为结构清晰、连续可执行的导演分镜，再转换为逐镜 AI 视频生成提示词。

```text
中文剧本
  ↓
short-drama-director
  ↓  SDP-1.0 导演分镜
storyboard-to-video-prompts
  ↓
逐镜 AI 视频生成提示词
```

项目地址：[yinzhixia2003-alt/AIGC_SkillForge](https://github.com/yinzhixia2003-alt/AIGC_SkillForge)

## 项目目标

AI 视频生产中，剧本、导演分镜和模型提示词属于三个不同层级：

- 剧本负责人物、事件、对白和情绪。
- 导演分镜负责镜头为什么存在、何时切换、观众先看到什么，以及空间和表演如何连续。
- 视频提示词负责把已确认的导演意图翻译成模型能够执行的起始状态、动作过程、结束状态和摄像机行为。

AIGC SkillForge 将“导演决策”和“提示词执行”拆成两个技能，避免一个提示词同时承担改编、拆镜、运镜、连续性和模型适配等过多职责。

## 技能包

| 目录 | 职责 | 主要输入 | 主要输出 |
|---|---|---|---|
| [`short-drama-director`](./short-drama-director/) | 将剧本拆成导演分镜，负责节拍、镜头数量、时长、构图、轴线、声音和选择性转场 | 中文短剧、AI 漫剧、影视或网文改编剧本 | 连续时码九列导演分镜，可选 SDP-1.0 交接附录 |
| [`storyboard-to-video-prompts`](./storyboard-to-video-prompts/) | 将已确认分镜逐镜翻译为 AI 视频提示词，不重新导演 | 已确认导演分镜、SDP-1.0、人物／场景／道具参考 | 通用或平台适配的逐镜视频生成提示词 |

### short-drama-director

这是上游导演技能，负责决定“拍什么、为什么这样拍、在哪里切镜”。

主要能力：

- 从剧本提取动作、对白、反应、道具、空间、情绪和时间节拍。
- 采用弹性拆镜，不强制固定镜头数量或固定单段时长。
- 建立承载镜头与必要插入镜头，组织观察、动作、对白、悬念和空间镜头组。
- 管理轴线、视线、运动方向、人物位置、道具状态和画外压力。
- 在锁定时码前计算台词自然说完所需时长，避免长台词挤入短镜头。
- 只在具备明确出点、入点和叙事动机的位置设计转场，普通切镜不做装饰。
- 输出固定九列 Markdown 分镜，并可生成 SDP-1.0 下游交接信息。
- 自动校验镜号、连续时码、台词负载、转场边界和交接一致性。

详细说明见 [`short-drama-director/README.md`](./short-drama-director/README.md)。

### storyboard-to-video-prompts

这是下游执行翻译技能，负责决定“如何把已经批准的镜头描述成模型可以执行的过程”。

主要能力：

- 锁定上游镜号、数量、顺序、时长、景别、角度、构图、运镜和台词。
- 将每个真实镜头翻译为“起始状态 → 动作过程 → 结束状态 → 摄像机行为 → 声音 → 连续性约束”。
- 判断连续接续、状态接续、信息关联、有意硬切和新场景。
- 绑定人物、场景、道具，以及同一镜头内部的 A/B/C 故事板关键状态。
- 管理人物位置、视线、道具手位、运动方向、伤势、破坏和画外人物压力。
- 未指定目标平台时输出通用自然语言提示词，不虚构平台参数。
- 当上游镜头在结构或时长上无法执行时，返回明确返修提示，不擅自拆镜、改词或补剧情。
- 自动对照上游分镜检查镜头数量、编号和时长。

详细说明见 [`storyboard-to-video-prompts/README.md`](./storyboard-to-video-prompts/README.md)。

## 两个技能为什么分开

两个技能的权限边界不同：

| 决策 | short-drama-director | storyboard-to-video-prompts |
|---|---:|---:|
| 拆分、合并或重新排序镜头 | 可以 | 不可以 |
| 决定镜头时长和剪辑点 | 可以 | 不可以 |
| 设计景别、角度、构图和转场 | 可以 | 只能忠实翻译 |
| 改变已批准对白 | 默认不可以 | 不可以 |
| 描述逐镜动作执行过程 | 提供导演层要求 | 负责完整展开 |
| 发现无法执行的镜头 | 重新设计或报告冲突 | 返回上游返修提示 |

这种分层可以减少提示词阶段擅自改戏、偷改时长、丢失台词或破坏镜头连续性的问题。

## SDP-1.0 交接协议

两个技能通过 SDP-1.0 连接。

上游导演技能输出人类可审阅的九列分镜，并可追加下游交接信息；下游技能以已批准分镜为最高权威，不改变真实镜头结构。

九列导演分镜格式：

```markdown
| 镜号+时间 | 场景 | 人物 | 动作描述 | 景别 | 拍摄角度 | 主画面描述 | 镜头运动 | 声音 / 台词 |
|---|---|---|---|---|---|---|---|---|
```

下游逐镜提示词基本结构：

```text
分镜01｜4秒｜拍摄角度｜景别｜镜头运动：
画面重点是……。起始时……；随后……；镜头结束时……。
摄像机……。同步出现……。连续性要求……；禁止……。
```

## 安装

### 安装整个项目

克隆仓库：

```bash
git clone https://github.com/yinzhixia2003-alt/AIGC_SkillForge.git
cd AIGC_SkillForge
```

将两个技能复制到 Codex 技能目录。

Windows PowerShell：

```powershell
Copy-Item -Recurse -Force .\short-drama-director "$HOME\.codex\skills\short-drama-director"
Copy-Item -Recurse -Force .\storyboard-to-video-prompts "$HOME\.codex\skills\storyboard-to-video-prompts"
```

macOS / Linux：

```bash
cp -R ./short-drama-director "$HOME/.codex/skills/short-drama-director"
cp -R ./storyboard-to-video-prompts "$HOME/.codex/skills/storyboard-to-video-prompts"
```

复制完成后，重新启动或刷新 Codex，使技能被重新发现。

也可以只安装其中一个目录。两个技能没有强制运行时耦合，但串联使用时效果更完整。

## 快速使用

### 第一步：剧本转导演分镜

```text
使用 $short-drama-director，将以下剧本生成 handoff 模式导演分镜。
保持原台词，使用 9:16 画幅；先核算台词时长，只在合适边界设计转场。
```

如果只需要审阅导演方案，可以使用默认的 `review` 模式；需要继续转换视频提示词时，推荐使用 `handoff` 模式。

### 第二步：导演分镜转视频提示词

```text
使用 $storyboard-to-video-prompts，将这份已确认的 SDP-1.0 导演分镜转换为通用视频生成提示词。
保持镜头数量、顺序、时长、景别、角度、运镜和台词不变。
```

如果需要适配特定视频平台，请同时提供平台名称、单次生成时长、参考图能力、首尾帧支持、音频／口型能力和平台提示词限制。没有这些信息时，技能默认输出可迁移的 `generic` 提示词。

## 推荐工作流

1. 提供完整剧本和明确的画幅、视觉风格、目标总时长。
2. 使用 `short-drama-director` 生成 `review` 分镜。
3. 人工审阅剧情忠实度、节奏、台词时长、轴线、连续性和选择性转场。
4. 确认后生成或补齐 `handoff` 信息。
5. 提供人物、场景、道具和故事板参考。
6. 使用 `storyboard-to-video-prompts` 生成逐镜提示词。
7. 运行校验脚本，再进入具体视频平台生成。

## 校验与测试

两个技能都提供仅依赖 Python 标准库的校验器和测试。

```bash
# 导演分镜结构、时码、台词负载和转场边界
python short-drama-director/scripts/validate_storyboard.py path/to/storyboard.md
python short-drama-director/tests/run_tests.py

# 视频提示词结构及与上游分镜的一致性
python storyboard-to-video-prompts/scripts/validate_video_prompts.py path/to/prompts.md
python storyboard-to-video-prompts/scripts/validate_video_prompts.py path/to/prompts.md --storyboard path/to/storyboard.md
python storyboard-to-video-prompts/tests/run_tests.py
```

自动校验主要负责结构完整性。剧情事实、表演合理性、审美风格和平台实际生成效果仍需要人工审阅。

## 项目结构

```text
AIGC_SkillForge/
├── README.md
├── short-drama-director/
│   ├── SKILL.md
│   ├── README.md
│   ├── agents/
│   ├── references/
│   ├── scripts/
│   └── tests/
└── storyboard-to-video-prompts/
    ├── SKILL.md
    ├── README.md
    ├── agents/
    ├── references/
    ├── scripts/
    └── tests/
```

每个子目录都是一个独立、可安装的 Codex 技能包：

- `SKILL.md`：技能入口、触发范围、核心工作流和硬约束。
- `agents/openai.yaml`：技能在 Codex 中的显示信息。
- `references/`：按任务需要加载的方法、格式和原始规范。
- `scripts/`：确定性结构校验工具。
- `tests/`：校验器的基础回归测试。
- 子目录 `README.md`：该技能的单独安装和使用说明。

## 设计原则

- 剧情事实优先，不凭空增加人物、道具、事件、线索或结局。
- 导演决策与模型执行分层，避免下游越权重新拆镜。
- 镜头数量服从剧情和执行需要，不套固定镜头模板。
- 台词按自然表演时长核算，不通过加速、删词或改词硬塞进镜头。
- 连续镜头维护轴线、视线、方向、道具和状态。
- 转场必须有叙事动机和明确出入锚点，不追求镜镜炫技。
- 未确认的平台能力、参考语法、参数或视觉风格一律不虚构。

## 贡献

欢迎通过 Issue 或 Pull Request 提交：

- 更具代表性的短剧、动作、对白、悬念或闪回测试用例。
- 台词时长、连续性和转场边界校验改进。
- 不同 AI 视频平台的受控适配方案。
- 文档修正、错误复现和提示词执行反馈。

提交修改时，建议同时提供最小复现输入、预期结果和对应测试，避免只针对单一样例增加不可迁移的规则。

## 许可

仓库目前未包含统一的开源许可证。正式对外开放使用、修改和再分发权限前，请由仓库维护者选择并添加合适的 `LICENSE` 文件。

## 致谢

两个技能的核心方法分别整理自仓库维护者提供的：

- 《导演分镜脚本生成 Skill（短剧弹性拆镜·导演思维强化版 V4.4）》
- 《分镜转视频提示词 Skill（自然成片执行版 V2.1）》

开源包只提供运行技能所需的提炼版规范，不包含上述原始方法全文。
