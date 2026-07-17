#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("prompt_validator", ROOT / "scripts" / "validate_video_prompts.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


STORYBOARD = """| 镜号+时间 | 场景 | 人物 | 动作描述 | 景别 | 拍摄角度 | 主画面描述 | 镜头运动 | 声音 / 台词 |
|---|---|---|---|---|---|---|---|---|
| 01｜00–03s | 卧室·夜内 | 林岚 | 停步看门。 | 中近景 | 斜侧面平视 | 人物左，门右。 | 定镜 | 敲门声。 |
| 02｜03–06s | 卧室·夜内 | 林岚 | 保持视线并发问。 | 近景 | 正面平视 | 门框在右侧。 | 轻推 | 林岚：“谁？” |
"""

PROMPTS = """【人物资产】
林岚：严格参考已提供人物资产。

【场景资产】
卧室：严格参考已提供场景结构。

【道具资产】
无

【故事板参考】
无

【视频提示词】
分镜01｜3秒｜斜侧面平视｜中近景｜定镜：画面重点是林岚因敲门停步。起始时她在前景左侧行走；敲门声出现后脚步停止并看向右侧。镜头结束时她保持看门姿态。摄像机固定。同步出现两下敲门声。禁止门提前打开。
分镜02｜3秒｜正面平视｜近景｜轻推：画面重点是林岚向门外发问。起始时她停在前景左侧并看向右侧门口；短暂停顿后说“谁？”。镜头结束时视线仍锁住门口。摄像机轻推后停止。同步出现原台词。禁止新增门外人物。
"""


def main() -> int:
    assert not [f for f in MODULE.validate(PROMPTS, STORYBOARD) if f.level == "ERROR"]
    broken = PROMPTS.replace("分镜02｜3秒", "分镜02｜4秒")
    errors = [f for f in MODULE.validate(broken, STORYBOARD) if f.level == "ERROR"]
    assert errors, "duration mismatch should fail"
    print("All storyboard-to-video-prompts tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

