---
name: short-drama-director
description: Convert Chinese short-drama, AI comic-drama, film, web-novel adaptation, dialogue, suspense, action, and emotional scripts into elastic director storyboards with continuous timecodes, dialogue delivery budgets, selective motivated transitions, shot groups, staging, axis control, continuity ledgers, and AI-video-executable action loads. Use when Codex must direct or re-direct a script, decide where to split or combine shots, create a nine-column Markdown storyboard, design sparse transitions at suitable cut boundaries, diagnose directing or timing logic, or produce an SDP-1.0 handoff for a downstream video-prompt skill. Do not use merely to translate an already approved storyboard into model prompts.
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
- Budget audible dialogue before locking timecodes. Visual coverage may change, but the total speaking time may not be compressed below a source-appropriate delivery.
- Design transitions only at motivated boundaries. An unadorned hard cut is the default and needs no decorative effect.
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
| Selective transition types, boundary tests, and appendix format | `references/transition-design.md` |
| Axis, eyeline, direction, prop/crowd/state continuity | `references/continuity-axis.md` |
| Dialogue, emotion, action, sound, flashback, AI action load | `references/dialogue-action-sound.md` |
| Exact table fields, metadata, modes, examples | `references/output-contract.md` |
| Chaining to a downstream prompt skill | `references/interchange-schema.md` |

## Workflow

1. Identify scenes, time changes, characters, objectives, conflict, source dialogue, key props, and irreversible state changes.
2. Mark the source facts and lines that must survive. Separate visible action from psychology.
3. Count audible dialogue and estimate its natural delivery from performance state before assigning shot durations. Reserve additional time for required pauses and simultaneous actions.
4. Estimate natural duration from dialogue and action; compare it with any user-specified duration. If the target is too short, report the conflict instead of compressing speech.
5. Split the story into action, dialogue, reaction, prop, space, and emotional-turn beats.
6. Give every beat one primary audience takeaway.
7. Design a carrying shot first; add inserts only when they reveal necessary information, hide unstable action, or create a motivated cut.
8. Apply the split/combine decision chain in `references/directing-workflow.md`.
9. Design 2-4-shot groups: observation, action, dialogue, suspense, or space.
10. Build an internal axis and continuity ledger for each scene before assigning angles and screen direction.
11. Test every boundary for a transition motive. Record only the suitable designed transitions using `references/transition-design.md`; leave the rest as ordinary hard cuts.
12. Assign shot size, angle, composition, camera movement, duration, sound, and exact timecodes.
13. Run a dialogue-load pass: every audible line must fit its combined assigned duration at the chosen delivery state without deleting words, rushing emotional pauses, or overloading action.
14. Run `scripts/validate_storyboard.py` and review warnings against the source before delivery.

## Elastic splitting rules

- Short insert: normally 0.8-2s.
- Ordinary narrative shot: normally 2-4s.
- Carrying shot: normally 4-6s.
- Emotional hold or continuous blocking: normally 6-8s when visible change continues.
- Above 8s requires a clear continuous-performance reason; above 12s normally requires revision.
- Use a planning baseline of roughly 3.5-4.5 Chinese characters per second for ordinary speech, 2.5-3.5 for crying, hesitation, grief, or heavy emotional pauses, and at most 4.5-5.5 for source-supported urgent/official delivery. These are planning ranges, not targets to fill.
- Multiple coverage shots may carry one continuous line, but their combined timeline must still cover the natural delivery. Do not mistake more cuts for more speaking time.
- When dialogue and visible action compete, either lengthen the beat, distribute the unchanged line across motivated covers, or simplify source-permitted secondary action.
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

When one or more boundaries genuinely benefit from a designed transition, append the optional `## 选择性转场设计` table defined in `references/transition-design.md`. Do not add a transition column to the primary table and do not list ordinary hard cuts merely to fill the appendix.

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
9. Never assign audible dialogue a duration that requires unnatural acceleration. Emotional punctuation and source-required pauses consume time.
10. Keep off-screen speakers out of the `人物` column unless they are visible; identify them in `声音 / 台词`.
11. Do not use text cards such as "翌日" as a substitute for a visual time transition unless the user explicitly requires them.
12. Never add a dissolve, whip pan, flash, occlusion, match cut, or sound bridge without a source-supported exit and entry anchor.

## Validation

Run:

```bash
python scripts/validate_storyboard.py path/to/storyboard.md
```

Treat automated warnings as review cues, not permission to alter source dialogue. A full deliverable is ready only when structural errors are zero and all warnings are either corrected or source-justified.
