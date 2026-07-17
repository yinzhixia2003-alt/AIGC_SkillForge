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

    count_match = COUNT_RE.search(text)
    if count_match and rows and int(count_match.group(1)) != len(rows):
        findings.append(Finding("ERROR", f"Declared shot count {count_match.group(1)} does not match {len(rows)} table rows."))
    duration_match = DURATION_RE.search(text)
    if duration_match and rows and abs(float(duration_match.group(1)) - rows[-1].end) > 0.01:
        findings.append(Finding("ERROR", f"Declared duration {duration_match.group(1)}s does not match final timecode {rows[-1].end:g}s."))

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

