# 尽调任务 Brief:OpenRouter × Pharos × CrossMint 撮合

> **给执行器 session 的交接文件。** 你被派来执行这个尽调 + proposal 任务。先读本文件,再读仓库 `CLAUDE.md`。
> 产出落到 `drafts/`,做完更新 `TODO.md`(标 [x])、`python3 mentor/tracker.py record`、commit & push。
> ⚠️ 下面的交易结构是**发起人口述的意图/假设**,不是已核实事实——涉及各方能力/费率/KPI 的部分需要你调研核实,拿不准的地方标注出来,不要编造。

## 一句话目标

搞清楚"LLM token 中转站(OpenRouter 这类)用稳定币收款"这个赛道的玩法,并据此给我们的支付合作方 **CrossMint** 出一份 proposal——让他们明白自己在这个撮合结构里的角色、如何参与,并**请他们把我们引荐给 OpenRouter**(我们不直接认识 OpenRouter 的人)。今天要交付,好去推进。

## 撮合结构(发起人口述的 high-level idea)

参与方与各自的 KPI/动机:

| 方 | 是谁 | 在这局里做什么 / 要什么 |
|----|------|------------------------|
| **OpenRouter** | LLM API 聚合/中转站,按 token/credits 计费,**用稳定币收钱** | 痛点:on-ramp/off-ramp 的 **conversion fees(法币↔稳定币兑换成本)**。我们帮它省这笔钱 |
| **Pharos** | 我们的生态合作伙伴(链 / 生态) | 有**链上流动性 KPI**要完成;愿意出**补贴**换取稳定币在其链上"走一圈"带来的流动性指标 |
| **CrossMint** | 我们的 **on-ramp / agent 支付**合作方 | 提供实际的 on/off-ramp + agent 支付通道;**对方向感兴趣**;关键:**能把我们引荐给 OpenRouter** |
| **我们** | 撮合方 / orchestrator | 设计并串起整个 flow,**从中收一道费**(创收) |

**资金/价值流(意图):**
1. OpenRouter 用稳定币收款。
2. 这笔稳定币不直接兑换,而是**在链上经 Pharos 绕一圈** → Pharos 拿到链上流动性/TVL 指标。
3. Pharos 因达成 KPI 而**出补贴**。
4. 用这笔补贴去 **cover OpenRouter 的 on/off-ramp conversion fees** → OpenRouter 净省成本。
5. CrossMint 提供 on/off-ramp 与 agent 支付轨道。
6. 我们做撮合方,在中间**抽一道**。
7. 本质:**我们帮 OpenRouter 省成本,省的钱来自 Pharos 的流动性补贴,各方各拿各的 KPI,我们赚撮合费。**

## 两份交付物

### 交付物 1:行业 Landscape(research)
- **LLM 中转站/credits 赛道**:OpenRouter 本身(商业模式、收款方式、是否已用/计划用稳定币、credits 机制、费率结构)+ 主要竞对(如 Together、Fireworks、Requesty、AI gateway 类,以及各家钱怎么收、on/off-ramp 现状)。
- **AI × 稳定币支付/agent payments 赛道**:谁在做 agentic payments、x402、稳定币结算 AI 用量(CrossMint、Skyfire、Payman、Coinbase 的 agent 支付等),各自定位与费率逻辑。
- **on/off-ramp + conversion fee 结构**:这条链路里钱通常在哪儿产生摩擦、典型费率区间,"补贴 cover 掉 conversion fee"在经济上是否成立、大概量级。
- **Pharos 侧**:Pharos 的流动性/TVL 激励机制到底怎么运作(据此判断"绕一圈"能否真的计入其 KPI、补贴从哪来)。
- 结论要能回答:**这个撮合结构在经济上跑得通吗?我们的抽成从哪一段最合理?最大风险/不成立的前提是什么?**

### 交付物 2:CrossMint Proposal(draft)
面向 CrossMint,目的有二:
1. **讲清他们的角色与收益**:在上述 flow 里 CrossMint 提供什么(on/off-ramp、agent 支付轨道)、因此能拿到什么(交易量、费率、成为 OpenRouter 这类 AI 中转站的默认支付层的战略卡位)。
2. **明确请求引荐**:我们想通过 CrossMint 被引荐给 OpenRouter 的对接人;proposal 要让 CrossMint 觉得"引荐我们=帮自己拿下一个大客户场景",而不是单纯帮忙。
- 篇幅:1–2 页,结构清晰(背景 → 机会 → 你(CrossMint)的角色 → 各方 KPI 如何咬合 → 具体请求:引荐 + 下一步)。
- 语气:合作方之间的商务提案,直接、利益对齐导向。

## 需要发起人补充的已知空白(执行时若缺,先标注,能做的先做)
1. **我们自己的项目/产品**是什么(Solana 生态 DeFi + 稳定币),在 flow 里除了撮合是否还提供链上组件?
2. **Pharos** 到底是什么(是不是 Pharos Network 那条 L1?)、补贴规模/形式。
3. **CrossMint 现有关系**:我们和 CrossMint 的接触到了哪一步、对接人是谁。
4. **抽成模型**:我们想按哪一段收费(bps? 补贴分成? 固定撮合费?)——有初步想法就写进去。
5. **稳定币品种**(USDC?)与目标链(Solana? Pharos?)。

## 派单提示词(粘到新 session)
```
你在仓库 AdenProSDE2024/claw-code-,读 CLAUDE.md 和 drafts/token-routing-brief.md。
执行该 brief 的两份交付物:① 行业 landscape,② 给 CrossMint 的 proposal。
先把 brief 末尾"需要补充的已知空白"里你答不了的问题一次性问我;能先做的部分直接开工。
landscape 用充分的 web 检索并给出处;proposal 写成 1–2 页可直接发的商务提案。
产出分别写到 drafts/token-landscape.md 和 drafts/crossmint-proposal.md,
完成后在 TODO.md 标 [x]、运行 tracker record、commit 并 push。
```
