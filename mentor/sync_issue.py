#!/usr/bin/env python3
"""把 TODO.md 渲染成 Checklist Issue 正文(供 CI 用 gh 更新 Issue #1)。

用法:python3 mentor/sync_issue.py > issue-body.md
CI 再执行:gh issue edit 1 --body-file issue-body.md

这样 Checklist 的同步走 GitHub Actions 的稳定 token,不依赖聊天会话里的连接器,
从根上避免"作战板已更新、Issue 还是旧版"的漂移。作战板与本 Issue 因此同源自 TODO.md。
"""

import re
from pathlib import Path

TODO = Path(__file__).resolve().parent.parent / "TODO.md"
ART = "https://claude.ai/code/artifact/5b3d650d-b569-47ac-8491-d3e2368264ab"
TASK_RE = re.compile(r"^\s*[-*]\s*\[([ xX])\]\s*(.+)$")
DUE_RE = re.compile(r"@due\(\d{4}-\d{2}-\d{2}\)")
PRIO_RE = re.compile(r"@prio\((P[0-9])\)", re.IGNORECASE)

EMOJI = {"今天": "🔥", "本周": "⚡", "找工": "💼", "每日跟进": "🔁", "已完成": "✅"}


def emoji_for(heading):
    for k, e in EMOJI.items():
        if k in heading:
            return e + " "
    return ""


def main():
    lines = TODO.read_text(encoding="utf-8").splitlines()
    out = [
        "> 直接点击复选框勾掉完成的任务(手机 App 上也可以)。Mentor 每小时会把这里的勾选同步到 `TODO.md` 并记入完成历史。",
        "> ⚠️ 请不要改动任务文字,同步是按标题匹配的。",
        f"> 🧭 作战板(可视化 + 一键派单):{ART}",
        "",
    ]
    fence = False
    printed_any = False
    for raw in lines:
        if raw.lstrip().startswith("```"):
            fence = True if not fence else False
            continue
        if fence:
            continue
        if raw.startswith("## "):
            heading = raw[3:].strip()
            if heading == "格式规范":
                break
            out += ["", f"## {emoji_for(heading)}{heading}", ""]
            continue
        m = TASK_RE.match(raw)
        if not m:
            continue
        done = m.group(1).lower() == "x"
        body = m.group(2)
        prio_m = PRIO_RE.search(body)
        title = DUE_RE.sub("", PRIO_RE.sub("", body)).strip()
        tag = f" `{prio_m.group(1).upper()}`" if prio_m and prio_m.group(1).upper() in ("P0",) and not done else ""
        out.append(f"- [{'x' if done else ' '}] {title}{tag}")
        printed_any = True
    out += ["", "---", "_由 Mentor 系统维护 · 勾选 = 完成 · 每小时同步 · 作战板与本清单同源自 TODO.md_"]
    if printed_any:
        print("\n".join(out))


if __name__ == "__main__":
    main()
