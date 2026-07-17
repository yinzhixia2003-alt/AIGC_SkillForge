# storyboard-to-video-prompts

将已经确认的导演分镜逐镜翻译为 AI 视频模型可执行的生成提示词，同时锁定镜号、数量、时长、景别、角度、构图、运镜、台词和剪辑意图。

该技能不重新导演。若分镜本身无法稳定执行，它会返回明确的上游返修提示，而不是擅自拆镜、改词或补剧情。

## 能力

- 解析九列导演分镜和 SDP-1.0 交接附录
- 将每镜翻译成起始状态、动作过程、结束状态和摄像机行为
- 判断连续接续、状态接续、信息关联、新场景和有意硬切
- 绑定人物、场景、道具和 A/B/C 故事板参考
- 维护人物、道具、轴线、方向、伤势、破坏和画外压力
- 在没有平台信息时生成通用提示词
- 在平台能力明确时进行受控适配
- 自动对照上游分镜检查镜号、数量和时长

## 安装

将本目录复制或克隆到 Codex 技能目录：

```powershell
Copy-Item -Recurse storyboard-to-video-prompts "$HOME\.codex\skills\storyboard-to-video-prompts"
```

显式调用示例：

```text
使用 $storyboard-to-video-prompts 将以下 SDP-1.0 导演分镜转换为通用视频生成提示词。
```

## 输入

必需输入是已经确认的导演分镜。推荐同时提供：

- 人物、场景和道具参考
- 故事板代表帧或 A/B/C 帧
- 目标平台和单次时长限制
- 是否支持首尾帧、音频、口型或参考图

未提供平台信息时，技能不会虚构平台参数或专属语法。

## 输出

默认包含五个区块：

```text
【人物资产】
【场景资产】
【道具资产】
【故事板参考】
【视频提示词】
```

每个真实镜头只对应一个视频提示词；A/B/C 是同一镜头内部状态，不会变成新增镜头。

## 与上游技能串联

```text
剧本
  -> short-drama-director（handoff）
  -> SDP-1.0 导演分镜
  -> storyboard-to-video-prompts
  -> 通用或平台适配视频提示词
```

## 校验与测试

```bash
python scripts/validate_video_prompts.py path/to/prompts.md
python scripts/validate_video_prompts.py path/to/prompts.md --storyboard path/to/storyboard.md
python tests/run_tests.py
```

## 目录

```text
storyboard-to-video-prompts/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
│   ├── translation-workflow.md
│   ├── continuity-assets.md
│   ├── platform-risk.md
│   ├── output-contract.md
│   └── interchange-schema.md
├── scripts/validate_video_prompts.py
└── tests/run_tests.py
```

## 方法来源

核心方法整理自仓库维护者提供的《分镜转视频提示词 Skill（自然成片执行版 V2.1）》，并已提炼为本技能所需的翻译、资产连续性、平台风险和输出规范。原始方法全文不随开源包发布。

## 开源许可

当前包未预设许可证。发布到 GitHub 前，请由仓库维护者选择并添加 `LICENSE` 文件。
