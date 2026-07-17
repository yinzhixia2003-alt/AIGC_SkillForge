#!/usr/bin/env python3
"""Validate video prompts and optionally compare them with an SDP-1.0 storyboard."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SECTIONS = ["【人物资产】", "【场景资产】", "【道具资产】", "【故事板参考】", "【视频提示词】"]
PROMPT_RE = re.compile(
    r"(?m)^分镜(\d+)\s*[｜|]\s*([0-9]+(?:\.[0-9]+)?)秒\s*[｜|]\s*([^｜|\r\n]+)\s*[｜|]\s*([^｜|\r\n]+)\s*[｜|]\s*([^：:\r\n]+)[：:]\s*(.+)$"
)
REPAIR_RE = re.compile(r"(?m)^分镜(\d+)\s*[｜|]\s*返修提示[：:]\s*(.+)$")
STORYBOARD_ROW_RE = re.compile(
    r"(?m)^\|\s*(\d+)\s*[｜|]\s*([0-9]+(?:\.[0-9]+)?)\s*[–—-]\s*([0-9]+(?:\.[0-9]+)?)s\s*\|"
)
VAGUE_TERMS = ("自然开始", "自然结束", "保持上一镜", "承接上一镜", "延续上一镜")


@dataclass
class Finding:
    level: str
    message: str


@dataclass
class Prompt:
    number: int
    duration: float | None
    line: str
    repair: bool = False


def parse_prompts(text: str) -> list[Prompt]:
    prompts = [Prompt(int(m.group(1)), float(m.group(2)), m.group(0)) for m in PROMPT_RE.finditer(text)]
    prompts.extend(Prompt(int(m.group(1)), None, m.group(0), True) for m in REPAIR_RE.finditer(text))
    return sorted(prompts, key=lambda item: (item.number, item.repair))


def parse_storyboard(text: str) -> list[tuple[int, float]]:
    return [(int(m.group(1)), float(m.group(3)) - float(m.group(2))) for m in STORYBOARD_ROW_RE.finditer(text)]


def validate(text: str, storyboard_text: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    positions: list[int] = []
    for section in SECTIONS:
        index = text.find(section)
        if index < 0:
            findings.append(Finding("ERROR", f"Missing section `{section}`."))
        else:
            positions.append(index)
    if len(positions) == len(SECTIONS) and positions != sorted(positions):
        findings.append(Finding("ERROR", "Output sections are not in the required order."))

    prompts = parse_prompts(text)
    if not prompts:
        findings.append(Finding("ERROR", "No executable prompt or repair notice found."))
        return findings

    numbers = [prompt.number for prompt in prompts]
    if len(numbers) != len(set(numbers)):
        findings.append(Finding("ERROR", "Duplicate real shot numbers found."))
    for expected, prompt in enumerate(prompts, 1):
        if prompt.number != expected:
            findings.append(Finding("ERROR", f"Expected shot {expected:02d}, found {prompt.number:02d}."))
        if prompt.repair:
            if "本技能不擅自拆镜" not in prompt.line and "返回" not in prompt.line:
                findings.append(Finding("WARN", f"Shot {prompt.number:02d}: repair notice should identify the upstream return boundary."))
            continue
        if prompt.duration is None or prompt.duration <= 0:
            findings.append(Finding("ERROR", f"Shot {prompt.number:02d}: invalid duration."))
        for phrase in ("画面重点是", "起始时", "镜头结束时"):
            if phrase not in prompt.line:
                findings.append(Finding("ERROR", f"Shot {prompt.number:02d}: missing `{phrase}`."))
        for term in VAGUE_TERMS:
            if term in prompt.line:
                findings.append(Finding("WARN", f"Shot {prompt.number:02d}: vague continuity phrase `{term}`; restate concrete facts."))

    if storyboard_text is not None:
        source = parse_storyboard(storyboard_text)
        if not source:
            findings.append(Finding("ERROR", "Upstream storyboard contains no parseable shot rows."))
        elif len(source) != len(prompts):
            findings.append(Finding("ERROR", f"Prompt count {len(prompts)} does not match storyboard count {len(source)}."))
        source_map = dict(source)
        for prompt in prompts:
            if prompt.number not in source_map:
                findings.append(Finding("ERROR", f"Shot {prompt.number:02d} does not exist in the upstream storyboard."))
            elif not prompt.repair and prompt.duration is not None and abs(prompt.duration - source_map[prompt.number]) > 0.01:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Shot {prompt.number:02d}: prompt duration {prompt.duration:g}s does not match storyboard duration {source_map[prompt.number]:g}s.",
                    )
                )
    return findings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompts", type=Path)
    parser.add_argument("--storyboard", type=Path)
    args = parser.parse_args()
    text = args.prompts.read_text(encoding="utf-8")
    storyboard = args.storyboard.read_text(encoding="utf-8") if args.storyboard else None
    findings = validate(text, storyboard)
    for finding in findings:
        print(f"{finding.level}: {finding.message}")
    errors = sum(f.level == "ERROR" for f in findings)
    warnings = sum(f.level == "WARN" for f in findings)
    print(f"Summary: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

