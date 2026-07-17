---
name: short-drama-director
description: Convert Chinese short-drama, AI comic-drama, film, web-novel adaptation, dialogue, suspense, action, and emotional scripts into elastic director storyboards with continuous timecodes, motivated cuts, shot groups, staging, axis control, continuity ledgers, and AI-video-executable action loads. Use when Codex must direct or re-direct a script, decide where to split or combine shots, create a nine-column Markdown storyboard, diagnose a storyboard's directing logic, or produce an SDP-1.0 handoff for a downstream video-prompt skill. Do not use merely to translate an already approved storyboard into model prompts.
---

# Short Drama Director

Turn scripts into director decisions. Decide why each shot exists, what the audience must understand, and why the edit moves to the next shot. Do not generate final video-model prompts.

## Core contract

- Preserve core events, relationships, motives, action results, emotional direction, necessary dialogue, and continuity-critical props.
- Do not add new characters, relationships, events, decisive props, clues, screens, text, or plot results.
- Use elastic shot density. Never force a fixed six-shot or fixed-15-second template.
- Give every shot one primary information target, an executable action process, and a verifiable end state.
- Make every cut earn new information, viewpoint, emotional landing, action result, spatial reveal, or execution stability.
- Maintain eyeline, movement, axis, screen direction, prop ownership, doors, damage, crowds, off-screen pressure, and sound continuity.
- Keep source dialogue exact unless the user explicitly authorizes rewriting.
- If the user does not supply a visual style, write `整体风格：【待用户补充】`; do not invent one.

## Output modes

Choose before writing:

- `review`: Default. Output planning metadata and the fixed nine-column director storyboard.
- `handoff`: Output the same storyboard plus the SDP-1.0 downstream handoff appendix from `references/interchange-schema.md`.
- `diagnose`: Review an existing storyboard and report directing, continuity, timing, or executability problems without rewriting unless asked.

## Resource routing

Read only what the task needs:

| Need | Read |
|---|---|
| Beat analysis, elastic splitting, shot groups, transitions | `references/directing-workflow.md` |
| Axis, eyeline, direction, prop/crowd/state continuity | `references/continuity-axis.md` |
| Dialogue, emotion, action, sound, flashback, AI action load | `references/dialogue-action-sound.md` |
| Exact table fields, metadata, modes, examples | `references/output-contract.md` |
| Chaining to a downstream prompt skill | `references/interchange-schema.md` |
| Full author-supplied V4.4 methodology | `references/original-spec-v4.4.md` |

## Workflow

1. Identify scenes, time changes, characters, objectives, conflict, source dialogue, key props, and irreversible state changes.
2. Mark the source facts and lines that must survive. Separate visible action from psychology.
3. Estimate natural duration from dialogue and action; compare it with any user-specified duration.
4. Split the story into action, dialogue, reaction, prop, space, and emotional-turn beats.
5. Give every beat one primary audience takeaway.
6. Design a carrying shot first; add inserts only when they reveal necessary information, hide unstable action, or create a motivated cut.
7. Apply the split/combine decision chain in `references/directing-workflow.md`.
8. Design 2-4-shot groups: observation, action, dialogue, suspense, or space.
9. Build an internal axis and continuity ledger for each scene before assigning angles and screen direction.
10. Create a transition motive before every scene change: decision, action, eyeline, sound, prop, line result, time state, or emotional consequence.
11. Assign shot size, angle, composition, camera movement, duration, sound, and exact timecodes.
12. Run `scripts/validate_storyboard.py` and review warnings against the source before delivery.

## Elastic splitting rules

- Short insert: normally 0.8-2s.
- Ordinary narrative shot: normally 2-4s.
- Carrying shot: normally 4-6s.
- Emotional hold or continuous blocking: normally 6-8s when visible change continues.
- Above 8s requires a clear continuous-performance reason; above 12s normally requires revision.
- Prefer a split when the primary subject, information, emotion, action phase, space, direction, prop state, or sound interpretation changes.
- Prefer a combine when time, space, subject goal, viewing priority, and action result stay unified and the current composition can show them clearly.
- Do not create separate shots for ordinary blinks, breaths, or micro-expressions that do not alter the beat.

## Required output

Before the table, state:

```text
交接协议：SDP-1.0
预计自然时长：
采用总时长：
生成模式：
画幅：
整体风格：
实际镜头数：
拆镜策略说明：
```

Use exactly these columns:

```markdown
| 镜号+时间 | 场景 | 人物 | 动作描述 | 景别 | 拍摄角度 | 主画面描述 | 镜头运动 | 声音 / 台词 |
|---|---|---|---|---|---|---|---|---|
```

Keep timecodes continuous. Put performance and physical action in `动作描述`; put light, blocking, composition, space, and prop state in `主画面描述`; do not mix camera terminology into the action column.

For `handoff` mode, append the handoff table defined in `references/interchange-schema.md`. Do not add columns to the primary storyboard table.

## Hard rules

1. Never summarize a dense scene into a few overloaded long shots.
2. Never cut only for visual variety or "cinematic feel."
3. Never let a shot carry two competing primary information targets.
4. Never restart an action at the next shot; match the same limb, direction, contact point, and progress.
5. Never reverse screen direction or dialogue eyelines without a neutral shot, visible repositioning, camera crossing, POV bridge, occlusion, or scene reset.
6. Never let people, threats, props, open doors, damage, or held objects disappear between continuous shots.
7. Never add an insert whose subject has no source-supported narrative function.
8. Never load strenuous action, fine hand operation, emotional reversal, and long synced dialogue into the same short shot.
9. Keep off-screen speakers out of the `人物` column unless they are visible; identify them in `声音 / 台词`.
10. Do not use text cards such as "翌日" as a substitute for a visual time transition unless the user explicitly requires them.

## Validation

Run:

```bash
python scripts/validate_storyboard.py path/to/storyboard.md
```

Treat automated warnings as review cues, not permission to alter source dialogue. A full deliverable is ready only when structural errors are zero and all warnings are either corrected or source-justified.

