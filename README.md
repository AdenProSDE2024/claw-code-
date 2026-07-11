# 🧭 Mentor TODO 系统

一个"非常积极主动"的导师系统:定时检查你的 TODO,逾期就催、停滞就问、没日期就逼你定日期、做完了就表扬。

## 它由三部分组成

| 组件 | 作用 |
|------|------|
| [`TODO.md`](TODO.md) | 你的待办清单,唯一需要你维护的文件 |
| [`mentor/mentor.py`](mentor/mentor.py) | 检查引擎(纯 Python 标准库,零依赖) |
| [`.github/workflows/mentor-check.yml`](.github/workflows/mentor-check.yml) | 定时任务:每天北京时间 09:00 / 20:00 自动检查,并把报告更新到带 `mentor-report` 标签的 Issue |

另外,Claude 会话中还可以配置 **Routine 定时唤醒**,让 Claude 本人定期读取 TODO 并主动来催你(见下文)。

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
   python3 mentor/mentor.py            # Markdown 报告
   python3 mentor/mentor.py --json     # JSON 输出
   python3 mentor/mentor.py --strict   # 有逾期任务时退出码为 1,可用于 CI 拦截
   ```

3. 定时报告会出现在仓库 Issues 里(标题「🧭 Mentor 督促报告」),Issue 更新时 GitHub 会给你发通知。

## Claude Routine(可选,更主动)

在 Claude Code 会话里可以创建一个定时 Routine,让 Claude 定期读取 `TODO.md`、对比上次的进展,像真正的导师一样主动找你复盘。报告是死的,导师是活的——Routine 版本可以追问"这个任务为什么停了"。
