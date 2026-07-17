---
name: mentor-check
description: 执行一轮完整的 Mentor 检查:同步 GitHub Issue #1 勾选状态到 TODO.md、记录任务变化、生成督促报告、按规则推送提醒并主动向用户提问。定时任务和手动 /mentor-check 都用这个。
---

# Mentor 检查流程

按顺序执行以下步骤。用户时区 America/Los_Angeles,先 `TZ=America/Los_Angeles date` 确认当地时间。

## 1. 同步最新状态(含孤立分支检查)

```bash
git pull origin main
git fetch --all
git for-each-ref --format='%(refname:short)' refs/remotes/origin/claude/* \
  | while read b; do
      ahead=$(git rev-list --count main.."$b" 2>/dev/null)
      [ "${ahead:-0}" -gt 0 ] && echo "⚠️ 未合并分支 $b 领先 main $ahead 个提交"
    done
```

**若发现未合并分支**:不要忽略。查看它改了什么(`git log --oneline main..<branch>`、`git diff --stat main <branch>`),
判断是否是某个执行器 session 已交付、但从未合并回 main 的产出——这种情况发生过一次(同一任务被两个 session
各跑一遍研究,结论还互相矛盾)。若确认是有效交付,在报告里点名让用户知道有分支待合并/待裁决,不要自行静默合并
或覆盖,尤其当分支内容与 main 上已有内容冲突时。

## 2. 同步 Checklist 勾选(GitHub Issue #1 ↔ TODO.md)

用 GitHub MCP 的 `issue_read` 读取 AdenProSDE2024/claw-code- 的 Issue #1,按**任务标题**匹配:

- Issue 里新勾选 `[x]` 的任务 → TODO.md 中同样标记 `[x]`
- TODO.md 中新增/完成/改期的任务 → 用 `issue_write` 更新 Issue #1 正文(保留分组格式)

## 3. 记录与检查

```bash
python3 mentor/tracker.py record   # 自动记录变化(完成/新增/移除/改期)
python3 mentor/mentor.py           # 健康检查:逾期/临期/停滞/无日期/P0 过多
```

每日跟进类任务(Monet ×2、STBL):若用户已确认当天跟进过,把该任务的 @due 顺延到下一个跟进日(STBL 为 +2 天,其余 +1 天)。

## 4. 提交记录

TODO.md 或 mentor/state/ 有变化时:

```bash
git add TODO.md mentor/state && git commit -m "chore(mentor): hourly check record" && git push
```

## 5. 推送提醒(PushNotification,先 ToolSearch 加载)

**每日窗口**(每窗口每天最多一次,不受冷却限制):
- 当地 10:00–11:00 → "check Monet deal 配套协议(美国侧)进度";奇数日加"STBL MOU check(每 48 小时)"
- 当地 17:00–18:00 → "跟进 Monet Foundation 亚洲侧 DeFi TVL deal(他们的早上)"

**事件推送**:存在逾期、当天到期、或连续 3 次检查零变化时,推送含具体任务名的提醒。

**静音规则**:当地 22:00–08:00 不推送;距上条推送不足 4 小时或当天已推过相同内容则跳过。

## 6. 刷新仪表盘(若会话有 Artifact 工具)

```bash
python3 mentor/dashboard.py <scratchpad>/mentor-dashboard.html
```

然后用 Artifact 工具发布,**传 url 参数指向固定地址**以更新同一页面:
`https://claude.ai/code/artifact/5b3d650d-b569-47ac-8491-d3e2368264ab`(favicon 🧭)

## 7. 向用户汇报(简短)

- 变化摘要(来自 tracker record 输出)
- 挑 1–2 个最关键任务提**具体**问题,优先级:逾期 > 今天到期 > 停滞 > 进行中 P0
- 新完成的任务明确表扬(用户勾掉任务需要成就感反馈)
- 不写长报告
