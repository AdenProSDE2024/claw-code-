#!/usr/bin/env python3
"""Tracker —— 自动记录并追踪任务完成情况。

每次运行 `record` 时,把当前 TODO.md 与上次快照对比,
将变化(完成/新增/重开/删除/改期)追加到事件日志,并更新快照。
`report` 基于事件日志输出完成情况统计。

状态文件(全部提交进仓库,即为"记录"本身):
  mentor/state/snapshot.json   上次检查的任务快照(含每个任务首次出现时间)
  mentor/state/history.jsonl   事件日志,一行一个事件

用法:
  python3 mentor/tracker.py record   # 记录一次检查,输出自上次以来的变化
  python3 mentor/tracker.py report   # 输出完成情况统计报告
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mentor import load_config, parse_tasks  # noqa: E402

STATE_DIR = Path(__file__).resolve().parent / "state"
SNAPSHOT_FILE = STATE_DIR / "snapshot.json"
HISTORY_FILE = STATE_DIR / "history.jsonl"


def now_utc():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load_snapshot():
    if SNAPSHOT_FILE.exists():
        return json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
    return {"updated_at": None, "tasks": {}}


def load_history():
    if not HISTORY_FILE.exists():
        return []
    return [json.loads(line) for line in
            HISTORY_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_events(events):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def record():
    cfg = load_config()
    ts = iso(now_utc())
    prev = load_snapshot()
    prev_tasks = prev["tasks"]
    current = parse_tasks(cfg)

    events = []
    new_tasks = {}
    for t in current:
        key = t["title"]
        entry = {
            "done": t["done"], "due": t["due"], "prio": t["prio"],
            "first_seen": prev_tasks.get(key, {}).get("first_seen", ts),
        }
        new_tasks[key] = entry
        old = prev_tasks.get(key)
        if old is None:
            events.append({"ts": ts, "event": "added", "task": key,
                           "due": t["due"], "prio": t["prio"], "done": t["done"]})
        else:
            if not old["done"] and t["done"]:
                days_open = max(0, (parse_iso(ts) - parse_iso(entry["first_seen"])).days)
                events.append({"ts": ts, "event": "completed", "task": key,
                               "days_open": days_open})
            elif old["done"] and not t["done"]:
                events.append({"ts": ts, "event": "reopened", "task": key})
            if old.get("due") != t["due"]:
                events.append({"ts": ts, "event": "due_changed", "task": key,
                               "from": old.get("due"), "to": t["due"]})
    for key, old in prev_tasks.items():
        if key not in new_tasks:
            events.append({"ts": ts, "event": "removed", "task": key,
                           "was_done": old["done"]})

    append_events(events)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(
        json.dumps({"updated_at": ts, "tasks": new_tasks}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    # 输出自上次检查以来的变化摘要
    last = prev["updated_at"]
    since = f"自上次检查({last} 起)" if last else "首次记录"
    print(f"### 📈 {since}的变化\n")
    if not events:
        print("- 没有任何变化。任务不会自己完成——这一小时你在推进哪一项?")
        return
    labels = {
        "completed": ("✅ 完成", lambda e: f"(耗时 {e['days_open']} 天)"),
        "added": ("🆕 新增", lambda e: f"(截止 {e['due']})" if e.get("due") else "(未定截止日期)"),
        "reopened": ("↩️ 重新打开", lambda e: ""),
        "removed": ("🗑️ 移除", lambda e: "(已完成后归档)" if e.get("was_done") else "(未完成即放弃)"),
        "due_changed": ("📅 改期", lambda e: f"({e['from'] or '无'} → {e['to'] or '无'})"),
    }
    for e in events:
        label, extra = labels[e["event"]]
        print(f"- {label}:**{e['task']}** {extra(e)}".rstrip())


def report():
    cfg = load_config()
    tz = timezone(timedelta(hours=cfg["tz_offset_hours"]))
    history = load_history()
    snapshot = load_snapshot()
    now = now_utc()
    week_ago = now - timedelta(days=7)

    completed = [e for e in history if e["event"] == "completed"]
    completed_7d = [e for e in completed if parse_iso(e["ts"]) >= week_ago]
    added_7d = [e for e in history
                if e["event"] == "added" and parse_iso(e["ts"]) >= week_ago]
    open_tasks = {k: v for k, v in snapshot["tasks"].items() if not v["done"]}

    print(f"### 📊 完成情况统计 · {now.astimezone(tz).strftime('%Y-%m-%d %H:%M')}\n")
    print(f"| 指标 | 数值 |")
    print(f"|------|------|")
    print(f"| 当前未完成 | {len(open_tasks)} 项 |")
    print(f"| 历史累计完成 | {len(completed)} 项 |")
    print(f"| 近 7 天完成 | {len(completed_7d)} 项 |")
    print(f"| 近 7 天新增 | {len(added_7d)} 项 |")
    if completed:
        avg = sum(e["days_open"] for e in completed) / len(completed)
        print(f"| 平均完成耗时 | {avg:.1f} 天 |")
    if open_tasks:
        oldest_key = min(open_tasks, key=lambda k: open_tasks[k]["first_seen"])
        age = (now - parse_iso(open_tasks[oldest_key]["first_seen"])).days
        print(f"| 最老的未完成任务 | {oldest_key}(已挂 {age} 天) |")
    if len(added_7d) > len(completed_7d):
        print(f"\n⚠️ 近 7 天新增({len(added_7d)})多于完成({len(completed_7d)}),"
              "清单在变长而不是变短——先收口,再开新任务。")

    recent = history[-8:]
    if recent:
        print(f"\n最近事件:\n")
        for e in recent:
            local = parse_iso(e["ts"]).astimezone(tz).strftime("%m-%d %H:%M")
            print(f"- `{local}` {e['event']}: {e['task']}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "record":
        record()
    elif cmd == "report":
        report()
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
