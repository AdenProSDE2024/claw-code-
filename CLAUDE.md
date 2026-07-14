# claw-code- · Mentor TODO 系统

这个仓库是一套**会话无关**的个人任务督促系统。任何 Claude 会话(云端、本地 CLI、CI)打开本仓库都应能完整接续工作——所有状态和逻辑都在仓库里,不依赖任何对话历史。

## 角色:看板 vs 执行器(先读 `mentor/DISPATCH.md`)

本系统刻意把**调度**和**执行**分离:
- **看板会话**只调度不执行——维护清单、督促、把具体任务派出去;不亲自写 deck/做研究/起草长文(那会烧光它赖以长期在线的上下文)。
- **执行器会话**只执行不留状态——领一条任务做完,产出落到 `drafts/`,更新 TODO/Issue 后推送,做完即弃。

如果你是被"派单提示词"唤起的:你是执行器,读 `TODO.md` 找到你那条任务,按 `mentor/DISPATCH.md` 的流程做完并写回。

## 组件

| 路径 | 作用 |
|------|------|
| `TODO.md` | 任务清单(唯一事实来源),格式:`- [ ] 标题 @due(YYYY-MM-DD) @prio(P0/P1/P2)` |
| GitHub Issue #1 | 用户可勾选的 Checklist 视图,与 TODO.md 双向同步(按标题匹配) |
| `mentor/mentor.py` | 健康检查:逾期/临期/停滞/无日期/P0 过多。`--json` `--strict` |
| `mentor/tracker.py` | `record` 记录状态变化到 `mentor/state/history.jsonl`;`report` 输出完成统计 |
| `mentor/state/` | 快照 + 事件日志,**提交进仓库**(即为持久记忆) |
| `.claude/skills/mentor-check/` | 完整的一轮 Mentor 检查流程,`/mentor-check` 触发 |
| `.github/workflows/mentor-check.yml` | CI 兜底:每天 09:00/20:00 PT 把报告发到 mentor-report Issue |
| `.github/workflows/claude.yml` | Issue 评论 `@claude <任务>` 派单(需 ANTHROPIC_API_KEY secret) |

## 关键约定

- **用户时区:America/Los_Angeles**(`mentor/config.json` 的 tz_offset_hours 对应之)
- 任务身份 = 标题文本。改标题会被记为"移除+新增",同步也会断——改措辞前先在两处同步改
- 用户偏好:任务**尽量往前排**,不堆到周末;导师口吻直接但支持性;完成的任务要明确表扬
- 每日跟进类任务(Monet ×2、STBL 每 48h)不是截止型任务:用户确认当天跟进后,把 @due 顺延到下一个跟进日
- 推送规则:逾期/当天到期/连续 3 次检查零变化时推送;当地 22:00–08:00 静音;4 小时冷却;每日跟进窗口(10-11 点美国侧+奇数日 STBL,17-18 点 Monet 亚洲侧)每天各最多一推

## 常用命令

```bash
python3 mentor/mentor.py            # 健康检查报告
python3 mentor/tracker.py record    # 记录一次检查(自动 diff 上次快照)
python3 mentor/tracker.py report    # 完成统计
```

定时执行一轮完整检查(任何环境):调用 `/mentor-check` skill,或本地 crontab:
`7 * * * * cd /path/to/claw-code- && claude -p "/mentor-check" --dangerously-skip-permissions`
