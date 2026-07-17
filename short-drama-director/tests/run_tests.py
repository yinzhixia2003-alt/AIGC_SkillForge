#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("director_validator", ROOT / "scripts" / "validate_storyboard.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


VALID = """交接协议：SDP-1.0
预计自然时长：6秒
采用总时长：6秒
生成模式：handoff
画幅：9:16
整体风格：【待用户补充】
实际镜头数：2
拆镜策略说明：发现与回应。

| 镜号+时间 | 场景 | 人物 | 动作描述 | 景别 | 拍摄角度 | 主画面描述 | 镜头运动 | 声音 / 台词 |
|---|---|---|---|---|---|---|---|---|
| 01｜00–03s | 卧室·夜内 | 林岚 | 脚步停住，抬眼看向右侧门口。 | 中近景 | 斜侧面平视 | 林岚在前景左侧，门口位于中景右侧。 | 定镜 | 门外两下敲门声。 |
| 02｜03–06s | 卧室·夜内 | 林岚 | 保持停步，视线锁住门口。 | 近景 | 正面平视 | 门框保留在右侧边缘，桌上钥匙未动。 | 轻推 | 林岚：“谁？” |

## 选择性转场设计

| 转场位置 | 类型 | 出点 | 入点 | 动机 | 执行说明 | 禁止 |
|---|---|---|---|---|---|---|
| 01→02 | 视线匹配切 | 林岚看向门口 | 门框进入近景边缘 | 保持注意方向 | 同轴直接切入 | 不显示门外人物 |

## 下游交接附录（SDP-1.0）

| 镜号 | 镜头任务 | 主要信息 | 相邻关系 | 起始状态 | 结束状态 | 下一镜观看动机 | 连续性锁定 |
|---|---|---|---|---|---|---|---|
| 01 | 发现声音 | 林岚停步 | 新场景 | 行走 | 停步看门 | 反应 | 门关闭 |
| 02 | 询问 | 林岚发问 | 连续接续 | 看门 | 保持视线 | 门外回应 | 钥匙未动 |
"""


def main() -> int:
    assert not [f for f in MODULE.validate(VALID) if f.level == "ERROR"]
    broken = VALID.replace("| 02｜03–06s", "| 03｜04–06s")
    errors = [f for f in MODULE.validate(broken) if f.level == "ERROR"]
    assert errors, "broken numbering/timecode should fail"
    overloaded = VALID.replace('林岚：“谁？”', '林岚（痛苦）：“我真的不知道为什么所有事情都会在今天突然变成这个样子。”')
    overload_errors = [f for f in MODULE.validate(overloaded) if f.level == "ERROR" and "delivery budget" in f.message]
    assert overload_errors, "overloaded emotional dialogue should fail"
    bad_transition = VALID.replace("| 01→02 |", "| 01→03 |")
    transition_errors = [f for f in MODULE.validate(bad_transition) if f.level == "ERROR" and "adjacent" in f.message]
    assert transition_errors, "non-adjacent transition boundary should fail"
    print("All short-drama-director tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
