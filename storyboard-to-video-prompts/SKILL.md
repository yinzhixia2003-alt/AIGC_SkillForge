---
name: storyboard-to-video-prompts
description: Translate approved Chinese director storyboards, SDP-1.0 handoffs, storyboard keyframes, and character/location/prop references into one executable AI-video prompt per real shot while preserving shot count, order, duration, shot size, angle, composition, camera movement, dialogue, cut intent, and continuity. Use when Codex must convert a storyboard into generic or platform-specific video-generation prompts, bind assets and A/B/C keyframes, audit prompt fidelity, or return structurally impossible shots to the director. Do not use to re-direct, split, merge, add, delete, or creatively redesign approved shots.
---

# Storyboard to Video Prompts

Translate director intent into model-executable processes. The director decides why and what to shoot; this skill describes how the approved shot unfolds without changing the edit.

## Core contract

- Preserve shot number, count, order, timecode/duration, scene, people, action, shot size, angle, composition, camera movement, sound, and dialogue.
- Do not split, merge, add, delete, reorder, extend, or shorten real shots.
- Do not reveal the next shot's information early or complete its action in the current shot.
- Translate each shot into `start state -> action process -> end state -> camera behavior -> sound -> continuity/risk constraints`.
- Give one primary information target priority over secondary and background information.
- Judge the adjacent-shot relationship before adding any visual anchor, action match, sound bridge, direction carry, or hard cut.
- Keep A/B/C storyboard frames inside one real shot: A=start, B=end, C=necessary intermediate state.
- If a structural conflict cannot be solved without changing directing, output a repair notice for that shot instead of inventing a false prompt.

## Input authority

Resolve conflicts in this order:

1. User's latest approved director storyboard.
2. User's latest approved storyboard/keyframes.
3. Approved character assets.
4. Approved location assets.
5. Approved prop assets.
6. Source script for fidelity checks only.
7. General skill rules.

If two authoritative inputs remain incompatible, stop that shot and return a concrete conflict notice.

## Output modes

- `generic`: Default when no target platform is given. Use portable natural-language prompts without invented platform syntax.
- `platform`: Use only documented/user-supplied platform capabilities, duration limits, references, and syntax.
- `audit`: Compare existing prompts with the approved storyboard; report deviations without rewriting unless asked.

## Resource routing

| Need | Read |
|---|---|
| Per-shot translation process and adjacent relationship types | `references/translation-workflow.md` |
| Assets, A/B/C frames, continuity ledgers, hard cuts | `references/continuity-assets.md` |
| Platform limits, high-risk shots, and return-to-director rules | `references/platform-risk.md` |
| Exact five-block output and prompt line format | `references/output-contract.md` |
| SDP-1.0 upstream handoff | `references/interchange-schema.md` |
| Full author-supplied V2.1 methodology | `references/original-spec-v2.1.md` |

## Workflow

1. Verify that the input is an approved director storyboard or SDP-1.0 handoff.
2. Parse real shots and lock count, order, duration, scale, angle, composition, camera movement, and exact dialogue.
3. Register only supplied character, location, prop, storyboard, and platform references.
4. For each shot, identify the primary information, secondary support, background continuity, start state, end state, and next viewing motive.
5. Classify the relationship to the prior shot: continuous, state-only, information-only, intentional hard cut/new scene, or unclear.
6. Write the start state from the prior end state, new-scene setup, or A frame. Never write `保持上一镜` without concrete facts.
7. Express action in time order and stop exactly at the approved end state.
8. Translate the approved camera behavior with a start, direction, subject, speed character, and stop point; do not replace it.
9. Add only source/director-approved dialogue, sound, or music. Keep off-screen voices off-screen.
10. Add shot-specific negative constraints only for actual risks.
11. Return structurally impossible shots to the director using the repair format.
12. Run `scripts/validate_video_prompts.py prompts.md --storyboard approved-storyboard.md`.

## Adjacent relationship rules

- `连续接续`: Prior end state becomes this start; action, eyeline, direction, and sound may match.
- `状态接续`: Carry only necessary identity, prop, injury, wetness, damage, or emotional result; allow a hard visual cut.
- `信息关联`: Preserve the narrative answer/contrast, not physical space or sound.
- `有意硬切` / `新场景`: Do not carry prior room elements, sound, direction, light, or blocking.
- `关系待确认`: Use only explicit facts and return for confirmation if a choice would alter directing.

## Required output

Use the five blocks in this order:

```text
【人物资产】
【场景资产】
【道具资产】
【故事板参考】
【视频提示词】
```

Each executable shot uses:

```text
分镜01｜4秒｜侧后方平视｜中景｜手持跟拍：画面重点是……。起始时……；随后……；镜头结束时……。摄像机……。同步出现……。连续性要求……；禁止……。
```

When a shot must return to directing:

```text
分镜03｜返修提示：当前2秒镜头同时包含长台词、转身、移动和开门，无法在不改变导演意图的前提下稳定执行。建议返回上游调整时长、动作负载或剪辑点；本技能不擅自拆镜。
```

## Hard rules

1. Never re-direct an approved shot.
2. Never treat A/B/C keyframes as extra video shots.
3. Never write an unspecified platform parameter, focal length, seed, reference syntax, or duration limit.
4. Never make an off-screen caller or narrator appear on screen unless directed.
5. Never invent UI, text, faces, props, injuries, effects, or background events.
6. Never force continuity across a deliberate hard cut or unrelated scene.
7. Never let a close-up erase active off-screen crowds, pursuers, threats, or sounds in a continuous action.
8. Never write vague start/end language; state concrete positions, facing, gaze, hand/prop state, door/damage state, and camera position.
9. Never accelerate, paraphrase, or delete dialogue to make it fit. Return the shot when timing is impossible.
10. Keep negative constraints specific; do not paste a generic prohibition wall into every shot.

## Validation

Run standalone or against the upstream storyboard:

```bash
python scripts/validate_video_prompts.py prompts.md
python scripts/validate_video_prompts.py prompts.md --storyboard approved-storyboard.md
```

A final package requires zero structural errors. Review warnings against the approved director source rather than changing it automatically.

