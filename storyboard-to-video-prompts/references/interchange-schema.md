# SDP-1.0 Interchange Schema

SDP-1.0 is the shared handoff between `short-drama-director` and `storyboard-to-video-prompts`. It preserves the human-readable nine-column storyboard and adds an optional downstream appendix without changing the primary table.

## Required metadata

Use the metadata block defined in `output-contract.md` with `生成模式：handoff`.

## Optional handoff appendix

```markdown
## 下游交接附录（SDP-1.0）

| 镜号 | 镜头任务 | 主要信息 | 相邻关系 | 起始状态 | 结束状态 | 下一镜观看动机 | 连续性锁定 |
|---|---|---|---|---|---|---|---|
| 01 | 让观众发现门外来人 | 林岚因敲门停步 | 新场景 | 林岚在前景左侧行走，钥匙在桌面 | 林岚停住并看向右侧门口 | 揭示门外目标 | 钥匙仍在桌面；门关闭；轴线左到右 |
```

Allowed `相邻关系`: `连续接续`, `状态接续`, `信息关联`, `有意硬切`, `新场景`, `关系待确认`.

## Authority order

1. User's latest approved storyboard.
2. Latest approved storyboard/keyframes.
3. Approved character assets.
4. Approved location assets.
5. Approved prop assets.
6. Source script for fidelity checks.
7. General skill rules.

When the appendix conflicts with the primary table, stop and return a correction request; do not silently choose.

