#!/usr/bin/env python3
"""Mentor —— 主动督促你的 TODO 检查引擎。

读取仓库根目录的 TODO.md,检查每一项任务的健康状况,
生成一份"导师风格"的督促报告。

检查项:
  - 逾期任务(@due 已过)
  - 临期任务(@due 在 N 天内)
  - 没有截止日期的任务(催你定日期)
  - 长期停滞的任务(通过 git blame 判断该行多久没动过)
  - 同时进行的 P0 太多(提醒聚焦)
  - 已完成任务(给予肯定)

用法:
  python3 mentor/mentor.py               # 输出 Markdown 报告
  python3 mentor/mentor.py --json        # 输出 JSON(供程序消费)
  python3 mentor/mentor.py --strict      # 存在逾期任务时以退出码 1 结束
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TODO_FILE = REPO_ROOT / "TODO.md"
CONFIG_FILE = Path(__file__).resolve().parent / "config.json"

DEFAULT_CONFIG = {
    "tz_offset_hours": 8,      # 报告使用的时区(默认北京时间 UTC+8)
    "due_soon_days": 3,        # 距截止日期 N 天内视为"临期"
    "stale_days": 7,           # 任务行 N 天没改动视为"停滞"
    "max_active_p0": 2,        # 同时进行的 P0 超过该数量时提醒聚焦
}

TASK_RE = re.compile(r"^\s*[-*]\s*\[(?P<done>[ xX])\]\s*(?P<body>.+)$")
DUE_RE = re.compile(r"@due\((\d{4}-\d{2}-\d{2})\)")
PRIO_RE = re.compile(r"@prio\((P[0-9])\)", re.IGNORECASE)


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
    return cfg


def today_local(cfg):
    tz = timezone(timedelta(hours=cfg["tz_offset_hours"]))
    return datetime.now(tz).date()


def blame_line_dates(path):
    """返回 {行号: 该行最后一次改动的日期}。git 不可用时返回空字典。"""
    try:
        out = subprocess.run(
            ["git", "blame", "--line-porcelain", "--", str(path)],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    dates, lineno, ts = {}, None, None
    for line in out.splitlines():
        m = re.match(r"^[0-9a-f]{40} \d+ (\d+)", line)
        if m:
            lineno = int(m.group(1))
        elif line.startswith("committer-time "):
            ts = int(line.split()[1])
        elif line.startswith("\t") and lineno is not None and ts is not None:
            dates[lineno] = datetime.fromtimestamp(ts, tz=timezone.utc).date()
            lineno = ts = None
    return dates


def parse_tasks(cfg):
    if not TODO_FILE.exists():
        return []
    line_dates = blame_line_dates(TODO_FILE)
    today = today_local(cfg)
    tasks = []
    in_fence = False
    for lineno, raw in enumerate(TODO_FILE.read_text(encoding="utf-8").splitlines(), 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        m = TASK_RE.match(raw)
        if in_fence or not m:
            continue
        body = m.group("body").strip()
        due_m = DUE_RE.search(body)
        prio_m = PRIO_RE.search(body)
        title = DUE_RE.sub("", PRIO_RE.sub("", body)).strip()
        due = datetime.strptime(due_m.group(1), "%Y-%m-%d").date() if due_m else None
        last_touched = line_dates.get(lineno)
        tasks.append({
            "line": lineno,
            "title": title,
            "done": m.group("done").lower() == "x",
            "due": due.isoformat() if due else None,
            "days_left": (due - today).days if due else None,
            "prio": prio_m.group(1).upper() if prio_m else None,
            "last_touched": last_touched.isoformat() if last_touched else None,
            "idle_days": (today - last_touched).days if last_touched else None,
        })
    return tasks


def analyze(tasks, cfg):
    open_tasks = [t for t in tasks if not t["done"]]
    findings = {
        "overdue": [t for t in open_tasks if t["days_left"] is not None and t["days_left"] < 0],
        "due_soon": [t for t in open_tasks if t["days_left"] is not None and 0 <= t["days_left"] <= cfg["due_soon_days"]],
        "no_due": [t for t in open_tasks if t["due"] is None],
        "stale": [t for t in open_tasks
                  if t["idle_days"] is not None and t["idle_days"] >= cfg["stale_days"]],
        "done": [t for t in tasks if t["done"]],
        "open_count": len(open_tasks),
    }
    active_p0 = [t for t in open_tasks if t["prio"] == "P0"]
    findings["too_many_p0"] = active_p0 if len(active_p0) > cfg["max_active_p0"] else []
    return findings


def fmt_task(t):
    parts = [f"**{t['title']}**"]
    if t["prio"]:
        parts.append(f"`{t['prio']}`")
    if t["due"]:
        parts.append(f"截止 {t['due']}")
    return " ".join(parts)


def render_markdown(findings, cfg, today):
    lines = [f"## 🧭 Mentor 检查报告 · {today.isoformat()}", ""]

    if not any([findings["overdue"], findings["due_soon"], findings["no_due"],
                findings["stale"], findings["too_many_p0"]]) and findings["open_count"] == 0:
        lines.append("清单是空的。没有任务不等于没有目标——现在就写下你接下来最重要的一件事。")
        return "\n".join(lines)

    if findings["overdue"]:
        lines += ["### 🔴 已经逾期(现在就处理)", ""]
        for t in findings["overdue"]:
            lines.append(f"- {fmt_task(t)} —— 已逾期 **{-t['days_left']} 天**。"
                         "要么今天完成,要么改期并写清楚原因,不要让它继续挂着。")
        lines.append("")

    if findings["due_soon"]:
        lines += [f"### 🟡 {cfg['due_soon_days']} 天内到期", ""]
        for t in findings["due_soon"]:
            when = "今天" if t["days_left"] == 0 else f"{t['days_left']} 天后"
            lines.append(f"- {fmt_task(t)} —— {when}到期,请确认它在你今天的计划里。")
        lines.append("")

    if findings["stale"]:
        lines += [f"### 🧊 超过 {cfg['stale_days']} 天没动静", ""]
        for t in findings["stale"]:
            lines.append(f"- {fmt_task(t)} —— 已停滞 **{t['idle_days']} 天**。"
                         "卡住了就把障碍写出来;不做了就删掉,别让它占据注意力。")
        lines.append("")

    if findings["no_due"]:
        lines += ["### 📅 没有截止日期", ""]
        for t in findings["no_due"]:
            lines.append(f"- {fmt_task(t)} —— 没有日期的任务永远不会完成,给它一个 `@due(...)`。")
        lines.append("")

    if findings["too_many_p0"]:
        n = len(findings["too_many_p0"])
        lines += [f"### 🎯 聚焦提醒", "",
                  f"- 你同时有 **{n} 个进行中的 P0**(建议不超过 {cfg['max_active_p0']} 个)。"
                  "全都最重要,等于没有最重要。挑一个先做完。", ""]

    if findings["done"]:
        lines += [f"### ✅ 已完成 {len(findings['done'])} 项,做得好", ""]
        for t in findings["done"]:
            lines.append(f"- ~~{t['title']}~~")
        lines.append("")

    lines.append(f"---\n📊 当前未完成任务:**{findings['open_count']}** 项。"
                 "记住:清单的意义不是记录,而是完成。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Mentor TODO 检查器")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    ap.add_argument("--strict", action="store_true", help="存在逾期任务时退出码为 1")
    args = ap.parse_args()

    cfg = load_config()
    tasks = parse_tasks(cfg)
    findings = analyze(tasks, cfg)

    if args.json:
        print(json.dumps({"tasks": tasks, "findings": {
            k: v for k, v in findings.items() if k != "open_count"
        }, "open_count": findings["open_count"]}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(findings, cfg, today_local(cfg)))

    if args.strict and findings["overdue"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
