# Output Contract

## Modes

- `review`: metadata + primary nine-column table.
- `handoff`: review output + SDP-1.0 handoff appendix.
- `diagnose`: findings grouped by severity and shot number; do not silently rewrite.

## Required metadata

```text
交接协议：SDP-1.0
预计自然时长：约XX秒
采用总时长：XX秒
生成模式：review / handoff
画幅：9:16 / 16:9 / 用户指定
整体风格：【用户提供】或【待用户补充】
实际镜头数：XX
拆镜策略说明：一句到三句
```

## Primary table

```markdown
| 镜号+时间 | 场景 | 人物 | 动作描述 | 景别 | 拍摄角度 | 主画面描述 | 镜头运动 | 声音 / 台词 |
|---|---|---|---|---|---|---|---|---|
| 01｜00–03s | 卧室·夜内 | 林岚 | 脚步停住，抬眼看向画面右侧门口。 | 中近景 | 斜侧面平视 | 林岚位于前景左侧，门口在中景右侧，桌上钥匙保持原位。 | 定镜 | 门外两下短促敲门声。 |
```

## Column boundaries

- `镜号+时间`: sequential number and continuous time.
- `场景`: location + time/interior-exterior only.
- `人物`: visible actors; use `无` for an empty/object shot.
- `动作描述`: performance and physical action; no camera/light language.
- `景别`: one readable scale.
- `拍摄角度`: viewpoint and elevation.
- `主画面描述`: light, blocking, composition, space, prop/state continuity; not the full action process.
- `镜头运动`: one principal camera behavior; default to `定镜`.
- `声音 / 台词`: exact dialogue, OS/VO/phone/off-screen labels, environment, and necessary effects; use `无` when absent.

