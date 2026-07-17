# Output Contract

## Section order

```text
【人物资产】
【场景资产】
【道具资产】
【故事板参考】
【视频提示词】
```

List each asset once. Do not repeat full static descriptions inside every prompt. If a class is absent, write `无` or a concise placeholder without inventing details.

## Executable shot

```text
分镜01｜4秒｜侧后方平视｜中景｜手持跟拍：画面重点是女孩从正常前行转为发现上方异常。起始时她位于画面中央偏左，朝巷道深处行走；听见上方异响后，她的脚步逐渐放慢并停住，头部沿画面右上方抬高。镜头结束时视线停在画面右上方外，不揭示目标。摄像机保持同侧、同速跟随并停在她侧后方。同步出现短促木板受力声。连续性要求后景同行者保持原位；禁止额外人物进入或提前出现下一镜目标。
```

Each prompt should normally contain:

- `画面重点是...`
- concrete `起始时...`
- ordered process;
- `镜头结束时...`
- inherited camera behavior;
- approved sound/dialogue;
- continuity and only relevant prohibitions.

## Repair shot

```text
分镜03｜返修提示：当前2秒镜头同时包含长台词、转身、移动和开门，无法稳定执行。建议返回上游调整时长、动作负载或剪辑点；本技能不擅自拆镜。
```

Repair notices count as the corresponding real shot; do not add replacement shots.

