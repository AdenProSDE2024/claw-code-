#!/usr/bin/env python3
"""生成 Mentor 仪表盘(自包含 HTML)。

用法:python3 mentor/dashboard.py <输出路径>
数据来源:TODO.md + mentor/state/。生成后可发布为 Claude Artifact 或直接用浏览器打开。
"""

import html
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mentor import load_config, parse_tasks, today_local  # noqa: E402
from tracker import load_history, parse_iso, now_utc  # noqa: E402

CHECKLIST_URL = "https://github.com/AdenProSDE2024/claw-code-/issues/1"

CSS = """
:root{
  --ground:#F7F6F2; --surface:#FFFFFF; --line:#E4E2DB;
  --ink:#22252A; --ink-2:#5C6066; --ink-3:#8A8E95;
  --accent:#3D51C4; --accent-soft:#E7EAFB;
  --red:#B3372B; --red-soft:#F7E9E7; --amber:#8F6400; --amber-soft:#F6EFDC;
  --green:#2F7D4E; --green-soft:#E5F1EA;
}
@media (prefers-color-scheme: dark){:root{
  --ground:#17181B; --surface:#1F2126; --line:#33363D;
  --ink:#ECEDEF; --ink-2:#A6ABB3; --ink-3:#787D85;
  --accent:#93A2F2; --accent-soft:#2A2F4A;
  --red:#E08578; --red-soft:#3D2724; --amber:#D6A94C; --amber-soft:#3A3121;
  --green:#7CC49A; --green-soft:#24382C;
}}
:root[data-theme="light"]{
  --ground:#F7F6F2; --surface:#FFFFFF; --line:#E4E2DB;
  --ink:#22252A; --ink-2:#5C6066; --ink-3:#8A8E95;
  --accent:#3D51C4; --accent-soft:#E7EAFB;
  --red:#B3372B; --red-soft:#F7E9E7; --amber:#8F6400; --amber-soft:#F6EFDC;
  --green:#2F7D4E; --green-soft:#E5F1EA;
}
:root[data-theme="dark"]{
  --ground:#17181B; --surface:#1F2126; --line:#33363D;
  --ink:#ECEDEF; --ink-2:#A6ABB3; --ink-3:#787D85;
  --accent:#93A2F2; --accent-soft:#2A2F4A;
  --red:#E08578; --red-soft:#3D2724; --amber:#D6A94C; --amber-soft:#3A3121;
  --green:#7CC49A; --green-soft:#24382C;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:ui-sans-serif,system-ui,-apple-system,"PingFang SC","Noto Sans CJK SC",sans-serif;
  line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:680px;margin:0 auto;padding:40px 20px 64px;display:flex;flex-direction:column;gap:28px}
header h1{font-size:26px;font-weight:700;margin:0;letter-spacing:-.01em;text-wrap:balance}
header .date{color:var(--ink-2);font-size:14px;margin-top:4px}
.meter{margin-top:18px}
.meter .nums{display:flex;justify-content:space-between;font-size:13px;color:var(--ink-2);
  font-variant-numeric:tabular-nums;margin-bottom:6px}
.meter .track{height:8px;border-radius:4px;background:var(--line);overflow:hidden}
.meter .fill{height:100%;border-radius:4px;background:var(--accent)}
section h2{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 10px}
ul.tasks{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
li.task{background:var(--surface);border:1px solid var(--line);border-radius:8px;
  padding:12px 14px;display:flex;gap:12px;align-items:baseline}
li.task .box{flex:none;width:15px;height:15px;border:1.5px solid var(--ink-3);
  border-radius:4px;position:relative;top:2px;display:inline-block}
a.box:hover,a.box:focus-visible{border-color:var(--accent);outline:none;
  box-shadow:0 0 0 3px var(--accent-soft)}
.acts{display:flex;gap:6px;flex:none}
.act{font-size:12px;font-weight:600;color:var(--accent);background:var(--accent-soft);
  border:none;border-radius:6px;padding:3px 9px;cursor:pointer;text-decoration:none;
  font-family:inherit;white-space:nowrap}
.act:hover,.act:focus-visible{filter:brightness(.94);outline:none}
li.task.done .box{background:var(--green);border-color:var(--green)}
li.task.done .box::after{content:"✓";position:absolute;inset:-3px 0 0 2px;color:#fff;font-size:11px}
li.task .t{flex:1;min-width:0}
li.task.done .t{color:var(--ink-3);text-decoration:line-through}
.meta{display:flex;gap:8px;flex:none;align-items:center}
.chip{font-size:11.5px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap}
.chip.red{color:var(--red);background:var(--red-soft)}
.chip.amber{color:var(--amber);background:var(--amber-soft)}
.chip.plain{color:var(--ink-2);background:var(--ground);border:1px solid var(--line)}
.chip.green{color:var(--green);background:var(--green-soft)}
.chip.p0{color:var(--accent);background:var(--accent-soft)}
.due{font-size:12.5px;color:var(--ink-3);font-variant-numeric:tabular-nums;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.stat .v{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums}
.stat .k{font-size:12px;color:var(--ink-2);margin-top:2px}
.warn{font-size:13.5px;color:var(--amber);background:var(--amber-soft);
  border-radius:8px;padding:10px 14px}
footer{font-size:12.5px;color:var(--ink-3);border-top:1px solid var(--line);padding-top:14px;
  display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
footer a{color:var(--accent);text-decoration:none}
footer a:hover,footer a:focus-visible{text-decoration:underline}
"""


def read_sections():
    """解析 TODO.md,返回 [(任务dict, 是否每日跟进)]。"""
    cfg = load_config()
    tasks = parse_tasks(cfg)
    lines = (Path(__file__).resolve().parent.parent / "TODO.md").read_text(encoding="utf-8").splitlines()
    daily_lines = set()
    current = ""
    fence = False
    for i, raw in enumerate(lines, 1):
        if raw.lstrip().startswith("```"):
            fence = not fence
        if fence:
            continue
        if raw.startswith("## "):
            current = raw
        elif "每日跟进" in current:
            daily_lines.add(i)
    return [(t, t["line"] in daily_lines) for t in tasks], cfg


def chip_for(t, today):
    if t["done"]:
        return '<span class="chip green">完成</span>'
    if t["days_left"] is None:
        return '<span class="chip plain">无日期</span>'
    if t["days_left"] < 0:
        return f'<span class="chip red">逾期 {-t["days_left"]} 天</span>'
    if t["days_left"] == 0:
        return '<span class="chip amber">今天</span>'
    if t["days_left"] == 1:
        return '<span class="chip plain">明天</span>'
    return f'<span class="chip plain">{t["days_left"]} 天后</span>'


def dispatch_prompt(t):
    due = f",截止 {t['due']}" if t["due"] else ""
    prio = f",优先级 {t['prio']}" if t["prio"] else ""
    return ("你在仓库 AdenProSDE2024/claw-code-(Mentor TODO 系统,规则见 CLAUDE.md;"
            "若当前目录没有这个仓库,先向我确认本地路径或克隆)。"
            f"我要执行任务:「{t['title']}」{due}{prio}。"
            "第一步:先把完成这个任务所需的关键 context 一次性问齐(背景、涉及的人、已有素材、成功标准、格式要求)。"
            "第二步:根据我的回答帮我执行或起草,文字成果放进仓库 drafts/ 目录。"
            "第三步:完成后把 TODO.md 中这条任务标记为 [x],运行 python3 mentor/tracker.py record,commit 并 push。")


def li(t, today):
    prio = f'<span class="chip p0">{t["prio"]}</span>' if t["prio"] == "P0" and not t["done"] else ""
    due = f'<span class="due">{t["due"][5:]}</span>' if t["due"] else ""
    if t["done"]:
        box, acts = '<span class="box"></span>', ""
    else:
        box = (f'<a class="box" href="{CHECKLIST_URL}" target="_blank" rel="noopener"'
               ' title="去 Checklist 勾选完成" aria-label="去 Checklist 勾选完成"></a>')
        p = dispatch_prompt(t)
        link = "claude-cli://open?repo=AdenProSDE2024/claw-code-&q=" + urllib.parse.quote(p)
        acts = (f'<span class="acts"><a class="act" href="{link}" title="在本机 Claude Code 新会话中执行">▶ 派单</a>'
                f'<button class="act copy" data-p="{html.escape(p, quote=True)}"'
                ' title="复制派单提示词,粘贴到 Cowork">⧉ 复制</button></span>')
    return (f'<li class="task{" done" if t["done"] else ""}">{box}'
            f'<span class="t">{html.escape(t["title"])}</span>'
            f'<span class="meta">{prio}{chip_for(t, today)}{due}</span>{acts}</li>')


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dashboard.html")
    pairs, cfg = read_sections()
    today = today_local(cfg)
    tz = timezone(timedelta(hours=cfg["tz_offset_hours"]))
    now = datetime.now(tz)

    tasks = [t for t, _ in pairs]
    open_t = [t for t in tasks if not t["done"]]
    done_t = [t for t in tasks if t["done"]]
    daily = [t for t, d in pairs if d and not t["done"]]
    overdue = [t for t in open_t if t["days_left"] is not None and t["days_left"] < 0]
    today_t = [t for t, d in pairs if not d and not t["done"] and t["days_left"] == 0]
    tomorrow_t = [t for t, d in pairs if not d and not t["done"] and t["days_left"] == 1]
    later_t = [t for t, d in pairs if not d and not t["done"]
               and (t["days_left"] is None or t["days_left"] > 1)]

    history = load_history()
    week_ago = now_utc() - timedelta(days=7)
    completed_7d = [e for e in history if e["event"] == "completed" and parse_iso(e["ts"]) >= week_ago]
    added_7d = [e for e in history if e["event"] == "added" and parse_iso(e["ts"]) >= week_ago]

    total = len(open_t) + len(done_t)
    pct = round(len(done_t) / total * 100) if total else 0

    def section(title, items):
        if not items:
            return ""
        rows = "\n".join(li(t, today) for t in items)
        return f'<section><h2>{title}</h2><ul class="tasks">{rows}</ul></section>'

    warn = ""
    if len(added_7d) > len(completed_7d):
        warn = (f'<div class="warn">⚠ 近 7 天新增 {len(added_7d)} 项 &gt; 完成 {len(completed_7d)} 项,'
                "清单在变长。先收口,再开新任务。</div>")

    body = f"""<title>Mentor 作战板</title>
<style>{CSS}</style>
<div class="wrap">
<header>
  <h1>Mentor 作战板</h1>
  <div class="date">{now.strftime("%Y-%m-%d %H:%M")} · America/Los_Angeles</div>
  <div class="meter">
    <div class="nums"><span>本周完成 {len(done_t)} / {total}</span><span>{pct}%</span></div>
    <div class="track"><div class="fill" style="width:{pct}%"></div></div>
  </div>
</header>
{warn}
{section("🔴 逾期 — 现在就处理", overdue)}
{section("今天", today_t)}
{section("明天", tomorrow_t)}
{section("之后", later_t)}
{section("每日跟进", daily)}
{section("已完成", done_t)}
<section><h2>完成统计</h2><div class="stats">
  <div class="stat"><div class="v">{len(open_t)}</div><div class="k">未完成</div></div>
  <div class="stat"><div class="v">{len(completed_7d)}</div><div class="k">近 7 天完成</div></div>
  <div class="stat"><div class="v">{len(added_7d)}</div><div class="k">近 7 天新增</div></div>
  <div class="stat"><div class="v">{len(done_t)}</div><div class="k">累计完成</div></div>
</div></section>
<footer>
  <span><a href="{CHECKLIST_URL}">✅ 去 Checklist 勾任务</a></span>
  <span>▶ 派单 = 本机 Claude Code · ⧉ 复制 = 粘贴到 Cowork</span>
</footer>
</div>"""
    body += """
<script>
document.querySelectorAll("button.copy").forEach(function(b){
  b.addEventListener("click", async function(){
    try{ await navigator.clipboard.writeText(b.dataset.p); }catch(e){}
    var o=b.textContent; b.textContent="✓ 已复制"; setTimeout(function(){b.textContent=o;},1400);
  });
});
</script>"""
    out.write_text(body, encoding="utf-8")
    print(f"{out} ({len(tasks)} tasks, {pct}% done)")


if __name__ == "__main__":
    main()
