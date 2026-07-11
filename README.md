# 🧭 Mentor TODO 系统

一个"非常积极主动"的导师系统:定时检查你的 TODO,逾期就催、停滞就问、没日期就逼你定日期、做完了就表扬。

## 它由三部分组成

| 组件 | 作用 |
|------|------|
| [`TODO.md`](TODO.md) | 你的待办清单,唯一需要你维护的文件 |
| [`mentor/mentor.py`](mentor/mentor.py) | 检查引擎(纯 Python 标准库,零依赖) |
| [`mentor/tracker.py`](mentor/tracker.py) | 追踪器:自动记录任务状态变化,统计完成情况 |
| [`mentor/state/`](mentor/state/) | 追踪数据(快照 + 事件日志),提交进仓库即为完整历史 |
| [`.github/workflows/mentor-check.yml`](.github/workflows/mentor-check.yml) | 兜底报告:每天北京时间 09:00 / 20:00 把检查报告 + 完成统计更新到带 `mentor-report` 标签的 Issue |

主循环由 **Claude Routine** 驱动:每小时唤醒一次,自动记录任务变化并主动询问进展(见下文)。

## Mentor 检查什么

- 🔴 **逾期**:`@due` 已过 —— 今天完成,或改期并写明原因
- 🟡 **临期**:3 天内到期 —— 确认它在你今天的计划里
- 🧊 **停滞**:任务行超过 7 天没改动(通过 `git blame` 判断)—— 卡住就写出障碍,不做就删掉
- 📅 **无截止日期**:没有日期的任务永远不会完成
- 🎯 **P0 过多**:进行中的 P0 超过 2 个 —— 全都最重要等于没有最重要
- ✅ **已完成**:给予肯定

阈值都可以在 [`mentor/config.json`](mentor/config.json) 里调整。

## 使用方法

1. 编辑 `TODO.md`,按这个格式写任务:

   ```markdown
   - [ ] 任务描述 @due(2026-07-15) @prio(P0)
   - [x] 已完成的任务 @due(2026-07-10) @prio(P1)
   ```

2. 手动运行检查(可选,定时任务会自动跑):

   ```bash
   python3 mentor/mentor.py            # 健康检查报告
   python3 mentor/mentor.py --json     # JSON 输出
   python3 mentor/mentor.py --strict   # 有逾期任务时退出码为 1,可用于 CI 拦截
   python3 mentor/tracker.py record    # 记录一次检查,输出自上次以来的变化
   python3 mentor/tracker.py report    # 完成情况统计(完成数、平均耗时、新增vs完成)
   ```

3. 定时报告会出现在仓库 Issues 里(标题「🧭 Mentor 督促报告」),Issue 更新时 GitHub 会给你发通知。

## 自动记录 & 追踪

每次检查时 `tracker.py record` 会把 TODO.md 与上次快照对比,自动记录这些事件到 `mentor/state/history.jsonl`:

- ✅ **completed** —— 任务完成(附从首次出现到完成的耗时)
- 🆕 **added** / 🗑️ **removed** / ↩️ **reopened** / 📅 **due_changed**

`tracker.py report` 基于事件日志统计:当前未完成数、累计/近 7 天完成数、平均完成耗时、最老的未完成任务;当近 7 天"新增 > 完成"时会警告清单在膨胀。任务以标题为身份标识,改标题会被记为"移除 + 新增"。

## Claude Routine(主循环)

Claude 会话里配置了每小时一次的 Routine:每次唤醒时拉取最新代码、运行 `tracker.py record` 自动记录变化并提交回仓库,然后像真正的导师一样**主动询问**——挑当前最关键的任务直接问你"进展如何?卡在哪?";有逾期或长期停滞时发推送提醒(深夜静音)。报告是死的,导师是活的。
