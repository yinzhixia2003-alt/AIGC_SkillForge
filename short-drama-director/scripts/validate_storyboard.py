#!/usr/bin/env python3
"""Validate the structural contract of a short-drama director storyboard."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


EXPECTED_HEADER = [
    "镜号+时间", "场景", "人物", "动作描述", "景别", "拍摄角度", "主画面描述", "镜头运动", "声音 / 台词",
]
REQUIRED_METADATA = ["交接协议", "预计自然时长", "采用总时长", "生成模式", "画幅", "整体风格", "实际镜头数", "拆镜策略说明"]
TIME_RE = re.compile(r"^(\d+)\s*[｜|]\s*([0-9]+(?:\.[0-9]+)?)\s*[–—-]\s*([0-9]+(?:\.[0-9]+)?)s$")
COUNT_RE = re.compile(r"实际镜头数[：:]\s*(\d+)")
DURATION_RE = re.compile(r"采用总时长[：:]\s*(?:约\s*)?([0-9]+(?:\.[0-9]+)?)\s*(?:秒|s)")
CAMERA_TERMS_IN_ACTION = ("摄影机", "镜头推", "镜头拉", "镜头摇", "镜头移动", "运镜", "定镜", "推镜", "拉镜", "摇镜")
EMOTIONAL_SPEECH_MARKERS = ("哭", "哽咽", "抽泣", "痛苦", "声嘶力竭", "歇斯底里", "迟疑", "犹豫", "悲痛", "崩溃")
TRANSITION_HEADER = ["转场位置", "类型", "出点", "入点", "动机", "执行说明", "禁止"]
TRANSITION_PAIR_RE = re.compile(r"^(\d+)\s*(?:→|->|—>|＞)\s*(\d+)$")


@dataclass
class Finding:
    level: str
    message: str


@dataclass
class Row:
    line_no: int
    cells: list[str]
    number: int
    start: float
    end: float


def split_table_line(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_rows(text: str, findings: list[Finding]) -> list[Row]:
    lines = text.splitlines()
    header_line = None
    for index, line in enumerate(lines):
        if line.strip().startswith("|") and split_table_line(line) == EXPECTED_HEADER:
            header_line = index
            break
    if header_line is None:
        findings.append(Finding("ERROR", "Missing the exact nine-column storyboard header."))
        return []

    rows: list[Row] = []
    for line_no, line in enumerate(lines[header_line + 2 :], header_line + 3):
        if not line.strip().startswith("|"):
            if rows:
                break
            continue
        cells = split_table_line(line)
        if len(cells) != 9:
            findings.append(Finding("ERROR", f"Line {line_no}: expected 9 cells, found {len(cells)}."))
            continue
        match = TIME_RE.match(cells[0])
        if not match:
            findings.append(Finding("ERROR", f"Line {line_no}: invalid shot/time cell `{cells[0]}`."))
            continue
        rows.append(Row(line_no, cells, int(match.group(1)), float(match.group(2)), float(match.group(3))))
    if not rows:
        findings.append(Finding("ERROR", "Storyboard table contains no data rows."))
    return rows


def dialogue_load(sound_cell: str) -> tuple[int, bool] | None:
    """Return audible Han-character count and emotional-state flag."""
    if "：" not in sound_cell and ":" not in sound_cell:
        return None
    prefix, content = re.split(r"[：:]", sound_cell, maxsplit=1)
    if any(label in prefix for label in ("音效", "字幕", "特写")):
        return None
    count = len(re.findall(r"[\u4e00-\u9fff]", content))
    if not count:
        return None
    emotional = any(marker in sound_cell for marker in EMOTIONAL_SPEECH_MARKERS)
    return count, emotional


def validate_transition_appendix(text: str, rows: list[Row], findings: list[Finding]) -> None:
    marker = "## 选择性转场设计"
    if marker not in text:
        return
    section = text.split(marker, 1)[1]
    if "## 下游交接附录（SDP-1.0）" in section:
        section = section.split("## 下游交接附录（SDP-1.0）", 1)[0]
    lines = section.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.strip().startswith("|") and split_table_line(line) == TRANSITION_HEADER),
        None,
    )
    if header_index is None:
        findings.append(Finding("ERROR", "Selective-transition appendix is missing the exact seven-column header."))
        return
    seen: set[tuple[int, int]] = set()
    valid_numbers = {row.number for row in rows}
    transition_count = 0
    for offset, line in enumerate(lines[header_index + 2 :], header_index + 3):
        if not line.strip().startswith("|"):
            if transition_count:
                break
            continue
        cells = split_table_line(line)
        if len(cells) != 7:
            findings.append(Finding("ERROR", f"Transition appendix line {offset}: expected 7 cells, found {len(cells)}."))
            continue
        match = TRANSITION_PAIR_RE.match(cells[0])
        if not match:
            findings.append(Finding("ERROR", f"Transition appendix line {offset}: invalid boundary `{cells[0]}`."))
            continue
        outgoing, incoming = int(match.group(1)), int(match.group(2))
        transition_count += 1
        if outgoing not in valid_numbers or incoming not in valid_numbers:
            findings.append(Finding("ERROR", f"Transition {outgoing:02d}→{incoming:02d} references a missing real shot."))
        if incoming != outgoing + 1:
            findings.append(Finding("ERROR", f"Transition {outgoing:02d}→{incoming:02d} must connect adjacent real shots."))
        if (outgoing, incoming) in seen:
            findings.append(Finding("ERROR", f"Duplicate transition boundary {outgoing:02d}→{incoming:02d}."))
        seen.add((outgoing, incoming))
        for index, value in enumerate(cells[1:], 1):
            if not value:
                findings.append(Finding("ERROR", f"Transition {outgoing:02d}→{incoming:02d}: `{TRANSITION_HEADER[index]}` is empty."))
    if transition_count > max(3, (len(rows) - 1) // 2):
        findings.append(Finding("WARN", "Designed transitions cover more than half of all cuts; confirm that ordinary cuts remain the default."))


def validate(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for field in REQUIRED_METADATA:
        if not re.search(rf"(?m)^{re.escape(field)}[：:]", text):
            findings.append(Finding("ERROR", f"Missing metadata field `{field}`."))
    if not re.search(r"(?m)^交接协议[：:]\s*SDP-1\.0\s*$", text):
        findings.append(Finding("ERROR", "`交接协议` must be `SDP-1.0`."))

    rows = parse_rows(text, findings)
    for expected, row in enumerate(rows, 1):
        if row.number != expected:
            findings.append(Finding("ERROR", f"Line {row.line_no}: expected shot {expected:02d}, found {row.number:02d}."))
        if row.end <= row.start:
            findings.append(Finding("ERROR", f"Shot {row.number:02d}: end time must be after start time."))
        if expected == 1 and abs(row.start) > 0.01:
            findings.append(Finding("ERROR", "First shot must start at 0s."))
        if expected > 1 and abs(row.start - rows[expected - 2].end) > 0.01:
            findings.append(Finding("ERROR", f"Shot {row.number:02d}: timecode is not continuous with the prior shot."))
        for index, value in enumerate(row.cells[1:], 1):
            if not value:
                findings.append(Finding("ERROR", f"Shot {row.number:02d}: `{EXPECTED_HEADER[index]}` is empty."))
        duration = row.end - row.start
        if duration > 12:
            findings.append(Finding("WARN", f"Shot {row.number:02d}: {duration:g}s exceeds 12s; confirm a justified continuous take."))
        elif duration > 8:
            findings.append(Finding("WARN", f"Shot {row.number:02d}: {duration:g}s exceeds 8s; confirm visible internal change."))
        if any(term in row.cells[3] for term in CAMERA_TERMS_IN_ACTION):
            findings.append(Finding("WARN", f"Shot {row.number:02d}: action column appears to contain camera language."))
        if row.cells[2] == "无" and re.search(r"[\u4e00-\u9fff]{2,}(?:走|跑|看|说|拿|推|拉|转身)", row.cells[3]):
            findings.append(Finding("WARN", f"Shot {row.number:02d}: character action appears while the people cell is `无`."))
        speech = dialogue_load(row.cells[8])
        if speech:
            audible_chars, emotional = speech
            rate = audible_chars / duration
            error_limit = 4.2 if emotional else 5.5
            warn_limit = 3.8 if emotional else 5.2
            if rate > error_limit:
                state = "emotional" if emotional else "ordinary"
                findings.append(Finding("ERROR", f"Shot {row.number:02d}: {audible_chars} audible Chinese characters in {duration:g}s ({rate:.2f}/s) exceed the {state} delivery budget."))
            elif rate > warn_limit:
                state = "emotional" if emotional else "ordinary"
                findings.append(Finding("WARN", f"Shot {row.number:02d}: {audible_chars} audible Chinese characters in {duration:g}s ({rate:.2f}/s) approach the {state} delivery limit; confirm source-supported pacing."))

    count_match = COUNT_RE.search(text)
    if count_match and rows and int(count_match.group(1)) != len(rows):
        findings.append(Finding("ERROR", f"Declared shot count {count_match.group(1)} does not match {len(rows)} table rows."))
    duration_match = DURATION_RE.search(text)
    if duration_match and rows and abs(float(duration_match.group(1)) - rows[-1].end) > 0.01:
        findings.append(Finding("ERROR", f"Declared duration {duration_match.group(1)}s does not match final timecode {rows[-1].end:g}s."))

    validate_transition_appendix(text, rows, findings)

    if "## 下游交接附录（SDP-1.0）" in text:
        appendix = text.split("## 下游交接附录（SDP-1.0）", 1)[1]
        appendix_numbers = [int(value) for value in re.findall(r"(?m)^\|\s*(\d+)\s*\|", appendix)]
        expected_numbers = [row.number for row in rows]
        if appendix_numbers != expected_numbers:
            findings.append(Finding("ERROR", "Handoff appendix shot numbers do not match the primary table."))
    return findings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    args = parser.parse_args()
    findings = validate(args.storyboard.read_text(encoding="utf-8"))
    for finding in findings:
        print(f"{finding.level}: {finding.message}")
    errors = sum(f.level == "ERROR" for f in findings)
    warnings = sum(f.level == "WARN" for f in findings)
    print(f"Summary: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
