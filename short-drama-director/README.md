# short-drama-director

把中文短剧、AI 漫剧、影视或网文改编剧本转换为具有导演因果、连续时间码、轴线控制和 AI 视频可执行性的导演分镜。

该技能采用“弹性拆镜”：镜头数量服从剧情节拍、信息密度、表演变化和执行稳定性，不强制固定六镜或固定 15 秒。

## 能力

- 提取剧情节拍、人物目标、冲突和关键状态变化
- 判断合镜与拆镜，建立 2-4 镜的小镜头组
- 设计景别、角度、构图、运镜、声音和转场动机
- 在锁定时码前计算台词自然说完所需时长，避免长台词挤入短镜头
- 只在具备出点、入点和叙事动机的边界设计转场，其余保持普通切镜
- 管理轴线、视线、运动方向、道具和画外压力
- 将心理和情绪转为可表演动作
- 输出固定九列表格和 SDP-1.0 下游交接附录
- 自动检查镜号、时间码、字段和交接一致性

## 安装

将本目录复制或克隆到 Codex 技能目录：

```powershell
Copy-Item -Recurse short-drama-director "$HOME\.codex\skills\short-drama-director"
```

重新启动或刷新 Codex 后，可显式调用：

```text
使用 $short-drama-director 将以下剧本生成 handoff 模式导演分镜。
```

## 输出

默认 `review` 模式输出规划信息和固定九列导演分镜。用于下游视频提示词转换时，选择 `handoff` 模式，额外生成 SDP-1.0 交接附录。

当少数镜头边界确实需要设计转场时，可追加 `选择性转场设计` 表；它不增加真实镜头，也不改变九列表格。普通硬切不列入该表。

```markdown
| 镜号+时间 | 场景 | 人物 | 动作描述 | 景别 | 拍摄角度 | 主画面描述 | 镜头运动 | 声音 / 台词 |
|---|---|---|---|---|---|---|---|---|
```

## 与下游技能串联

```text
剧本
  -> short-drama-director（handoff）
  -> SDP-1.0 导演分镜
  -> storyboard-to-video-prompts
  -> 逐镜视频生成提示词
```

下游技能不得改变导演已确认的镜号、时长、景别、角度、构图、运镜和台词。

## 校验与测试

```bash
python scripts/validate_storyboard.py path/to/storyboard.md
python tests/run_tests.py
```

## 目录

```text
short-drama-director/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
│   ├── directing-workflow.md
│   ├── continuity-axis.md
│   ├── dialogue-action-sound.md
│   ├── transition-design.md
│   ├── output-contract.md
│   └── interchange-schema.md
├── scripts/validate_storyboard.py
└── tests/run_tests.py
```

## 方法来源

核心方法整理自仓库维护者提供的《导演分镜脚本生成 Skill（短剧弹性拆镜·导演思维强化版 V4.4）》，并已提炼为本技能所需的工作流、连续性、对白、转场和输出规范。原始方法全文不随开源包发布。

## 开源许可

当前包未预设许可证。发布到 GitHub 前，请由仓库维护者选择并添加 `LICENSE` 文件。
