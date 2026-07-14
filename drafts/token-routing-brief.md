# 尽调任务 Brief:OpenRouter × Pharos × CrossMint 撮合

> **给执行器 session 的交接文件。** 你被派来执行这个尽调 + proposal 任务。先读本文件,再读仓库 `CLAUDE.md`。
> 产出落到 `drafts/`,做完更新 `TODO.md`(标 [x])、`python3 mentor/tracker.py record`、commit & push。
> ⚠️ 交易结构是**发起人口述的意图**,涉及各方能力/费率/机制的部分需你调研核实,拿不准的标注出来,不要编造。

## 一句话目标

搞清楚"LLM token 中转站(OpenRouter 这类)用稳定币收款"这个赛道的玩法,并据此给我们的支付合作方 **CrossMint** 出一份 proposal——让双方都看清各自如何切入这个撮合结构、能得到什么,并**请 CrossMint 把我们引荐给 OpenRouter**(我们不直接认识 OpenRouter 的人)。
**当前阶段的重点不是谈钱,而是把整件事跑通、确认各方都能插进去——事情成立了才谈抽成。** 今天要交付,好去推进。

## 撮合结构(发起人口述)

参与方与各自的 KPI/动机:

| 方 | 是谁 | 在这局里做什么 / 要什么 |
|----|------|------------------------|
| **OpenRouter** | LLM API 聚合/中转站,按 token/credits 计费,**用稳定币收钱** | 得到两重好处:① on/off-ramp 的 **conversion fee 被 cover**;② 有机会拿到**打折的模型/推理源**(见 Ant Digital/千问那条线) |
| **Pharos** | 我们的生态合作伙伴(链) | 要**链上稳定币 volume / 流动性 KPI**;补贴**按我们 route 到其链上的稳定币 volume 计**。另:Pharos 与 **Ant Digital** 有 connection,内部**可能促成千问(通义千问)提供打折模型/source** |
| **CrossMint** | 我们的 **on-ramp / agent 支付**合作方 | 提供实际 on/off-ramp + agent 支付通道;**对方向感兴趣**;关键:**能把我们引荐给 OpenRouter**。对接人=他们的 **Head of Partnership** |
| **我们** | 撮合方 / orchestrator | 设计并串起整个 flow;**抽成模型待定,本阶段先不谈钱,先把结构跑通** |

**资金/价值流(意图):**
1. OpenRouter 用稳定币收款。
2. 这笔稳定币**在链上经 Pharos 走一圈** → 贡献 Pharos 的链上稳定币 volume。
3. Pharos **按 routed volume 出补贴**。
4. 补贴去 **cover OpenRouter 的 on/off-ramp conversion fees**。
5. **额外杠杆**:借 Pharos↔Ant Digital 的关系,争取让**千问**给 OpenRouter 提供打折模型/推理源——给 OpenRouter 的第二重甜头。
6. CrossMint 提供 on/off-ramp 与 agent 支付轨道。
7. 我们做撮合方串起全链路(抽成后谈)。
8. 本质:**我们帮 OpenRouter 省钱(手续费)+ 可能给它更便宜的模型源;省的钱/资源来自 Pharos 的 volume 补贴与 Ant/千问关系;各方各拿各的 KPI。**

## 两份交付物

### 交付物 1:行业 Landscape(research)
- **LLM 中转站/credits 赛道**:OpenRouter(商业模式、收款方式、是否已/将用稳定币、credits 机制、费率结构、模型采购/成本结构)+ 主要竞对(Together、Fireworks、Requesty、AI gateway 类;各家钱怎么收、模型成本、on/off-ramp 现状)。
- **AI × 稳定币支付 / agent payments 赛道**:谁在做 agentic payments / 稳定币结算 AI 用量(CrossMint、Skyfire、Payman、Coinbase agent 支付、x402 等),定位与费率逻辑。
- **on/off-ramp + conversion fee 结构**:摩擦在哪、典型费率区间;"用 volume 补贴 cover conversion fee"在经济上是否成立、量级如何。
- **Pharos 侧**:Pharos 是什么(核实是否 Pharos Network L1)、其流动性/volume 激励怎么运作、补贴来源;**Pharos↔Ant Digital↔千问**这条关系链的真实性与可操作性。
- 结论要回答:**这个结构经济上跑得通吗?对 OpenRouter 的净价值(省的手续费 + 可能的模型折扣)大概多少?最脆弱的前提是什么?**

### 交付物 2:CrossMint Proposal(draft,主交付物)
面向 CrossMint 的 **Head of Partnership**,目的有二:
1. **讲清 CrossMint 的角色与收益**:在 flow 里 CrossMint 提供什么(on/off-ramp + agent 支付轨道)、因此得到什么(交易量、成为 OpenRouter 这类 AI 中转站的默认稳定币支付层的战略卡位)。
2. **明确请求引荐**:通过 CrossMint 被引荐给 OpenRouter 对接人;把"引荐我们 = 帮 CrossMint 自己拿下一个旗舰 AI 支付场景"讲透。
- 篇幅 1–2 页;结构:背景 → 机会(为什么现在、为什么是 AI×稳定币)→ 各方与 KPI 如何咬合(用上面那张表和 value flow)→ CrossMint 的角色与收益 → 具体请求(引荐 OpenRouter + 下一步)。
- **本阶段不写具体抽成/费率**,强调"先跑通、双方都能切入";语气=合作方商务提案,利益对齐导向。

## 发起人已确认的关键事实(执行时直接采用)
1. **补贴口径**:按我们 route 到 Pharos 链上的**稳定币 volume** 计。
2. **CrossMint 对接人**:Head of Partnership。
3. **抽成**:本阶段不谈,先把结构跑通、确认双方能切入。
4. **已有资源**:Pharos 与 Ant Digital 有 connection,内部或可让**千问**提供打折模型/source——作为给 OpenRouter 的额外价值杠杆,请在 landscape 里评估其可行性、在 proposal 里酌情作为亮点(措辞谨慎,标明"探索中")。
5. 我们是 Solana 生态 DeFi + 稳定币背景的撮合发起方。

## 仍需留意 / 边做边标注的不确定点
- Pharos 的确切身份与 volume 补贴机制(去核实)。
- "稳定币经 Pharos 绕一圈"在技术与合规上如何实现(跨链?目标链是 Pharos 还是 Solana?稳定币品种 USDC?)——landscape 里给出可行路径与风险。
- 千问/Ant 折扣这条线的真实性(可能是内部意向,勿夸大)。

## 派单提示词(粘到新 Cowork / Code session)
```
你在仓库 AdenProSDE2024/claw-code-,先 git pull origin main,读 CLAUDE.md 和 drafts/token-routing-brief.md。
执行该 brief 的两份交付物:① 行业 landscape(充分 web 检索、给出处),② 给 CrossMint 的 proposal(1–2 页可直接发,面向其 Head of Partnership,本阶段不写抽成)。
brief 里"发起人已确认的关键事实"直接采用,无需再问;只有遇到会改变结论的硬缺口才回来问我。
产出写到 drafts/token-landscape.md 和 drafts/crossmint-proposal.md;
完成后在 TODO.md 标 [x]、运行 python3 mentor/tracker.py record、commit 并 push origin main。
```
