# 行业 Landscape:LLM 中转站 × 稳定币收款 × Agent Payments × On/Off-Ramp

> 研究方法:deep-research 工作流(69 个子 agent、3 票对抗验证)+ 补充 WebSearch,聚焦四个板块。凡标"高置信"为多来源交叉印证;"中置信"为单一权威来源(官网/官方文档)未获二次独立源印证;"未证实/存疑"为检索未找到公开证据或被验证证伪,不代表结论必然为否,只是缺乏支持。

## 1. LLM 中转站/credits 赛道

### OpenRouter(赛道领跑者)
- **商业模式**:市场化 take-rate,不卖算力/席位/订阅,靠"过手资金"抽成。模型本身**不加价**(2025 年起从按 token 抽成转向只在"充值/购买 credits"环节收费),开发者付的每 token 价格与直连模型 API 一致。[Sacra](https://sacra.com/c/openrouter/) [OpenRouter Pricing](https://openrouter.ai/pricing)
- **具体费率**:信用卡充值收 **5.5% + $0.80 floor**;**加密货币(含 USDC)充值收 5%**;BYOK(自带 API key)模式下,超过每月 100 万次免费请求后,按"等效 OpenRouter 调用费用的 5%"收费。[Amnic](https://amnic.com/blogs/openrouter-pricing) [OpenRouter FAQ](https://openrouter.ai/docs/faq)
- **规模**:2026 年 3 月年化收入约 $50M(2025 年底约 $19M);2025 年 5 月年化推理支出已超 $100M。[Sacra](https://sacra.com/c/openrouter/)
- **⚠️ 关键更新(与 brief 假设不同):OpenRouter 已经支持稳定币收款,而非"计划中"。** 已上线 **USDC** 充值(与信用卡、AliPay 并列),并已集成 **Coinbase x402 协议**,支持"agent 直接用 USDC(Base 链)按次付费"的免账户模式;报道称 x402 协议整体已处理超 $50M 的 USDC 支付、集成 2000+ API。PayPal 支持据称也在路上。[Crypto Payments API 公告](https://openrouter.ai/blog/announcements/crypto-payments-api/) [CryptoBriefing](https://cryptobriefing.com/x402-protocol-50m-payments-openrouter/) [MixRoute](https://mixroute.ai/blog/pay-for-ai-apis-with-crypto/)
  - **这对我们的撮合结构是好消息,不是坏消息**:意味着"OpenRouter 用稳定币收款"这一前提已经成立,不需要说服 OpenRouter 从零建设稳定币收款能力——真正的空档在于**它现有的稳定币/加密支付路径(尤其 x402/USDC on Base)有没有做过"链上 volume → 生态激励"的对接**,以及**这笔 5%(crypto)手续费目前算不算"高"、有没有空间被 Pharos volume 补贴覆盖**。这是我们要向 OpenRouter 验证的具体问题,而不是重新推销一个愿景。

### 主要竞对
- **Together AI / Fireworks AI**:两者都是"价差生意"(spread business)——批发买 GPU 算力(自建/CoreWeave/Lambda 等)、零售卖按 token 计费的推理。**毛利率**:Fireworks 约 50%(目标 60%),Together 约 45%。二者货币化靠"算力批零价差 + 工具/生态溢价",不是靠支付通道抽成。目前**未检索到**二者有稳定币收款或 on/off-ramp 相关的公开信息——它们的支付层仍是传统企业计费(合同/信用卡/发票),这与 OpenRouter 的加密原生打法明显不同。[Sacra: Fireworks](https://sacra.com/c/fireworks-ai/) [Sacra: Together](https://sacra.com/c/together-ai/) [ParallelIQ](https://www.paralleliq.ai/blog/two-business-models-running-ai-inference)
- **Portkey**:企业级 AI Gateway,SaaS 订阅制(按日志量阶梯计费,超出后 $9/10万条),目标客户是需要托管、可观测性、护栏(guardrails)的团队,不做加密支付。[TrueFoundry](https://www.truefoundry.com/blog/portkey-pricing-guide)
- **LiteLLM**:开源、自托管网关,免费开源+企业版,面向自己运维基础设施、请求量 500 万+/月的团队,同样无加密支付叙事。
- **Requesty**:纯按量付费,对多数供应商模型统一加价 **5%**(部分供应商如阿里云、Perplexity 不加价直接透传),无订阅/无最低消费,企业功能单独议价——费率结构与 OpenRouter 的 5% 高度接近,可作为"平台抽成 5% 左右是行业常态"的佐证。[Requesty Pricing](https://www.requesty.ai/pricing)
- **结论**:OpenRouter 与 Requesty 代表"加密友好/低门槛市场型网关"一类,~5% 是行业公认的合理 take-rate 区间;Together/Fireworks 是"算力批发商",Portkey/LiteLLM 是"企业网关/自托管工具",都不具备天然的加密收款诉求。**这意味着我们的撮合结构目标客户选 OpenRouter 是对的——它是目前唯一一家在"稳定币收款"和"市场型低摩擦费率"两条线上都成立的头部玩家**,竞对里没有同样合适的替代对象。

## 2. AI × 稳定币支付 / Agent Payments 赛道

行业已经形成清晰的分层("Agent Payments Stack"):协议层、KYA/信任层、SDK/钱包层、支付编排层。[Agent Payments Stack](https://agentpaymentsstack.com/)

| 玩家 | 定位 | 备注 |
|---|---|---|
| **x402(Coinbase 主导的协议)** | 协议层——复活 HTTP 402 状态码,任何 API 可按次索要稳定币微支付,默认结算 USDC on Base | 已被 OpenRouter 采用;2026 年称已处理 $50M+ 支付、集成 2000+ API |
| **Coinbase AgentKit** | SDK/钱包层——给 AI agent 配链上钱包,绕开传统 KYC 摩擦 | 承接 x402 之上的钱包体验 |
| **Skyfire** | KYA(Know Your Agent)验证 + USDC 稳定币支付轨道(KYAPay),定位为"比裸协议更高层"的产品化方案 | 获 Coinbase、a16z 等支持 |
| **Payman** | Agent-to-human 支付基础设施 | 有传统金融机构背景支持 |
| **CrossMint** | Agent 钱包 + 虚拟卡 + 稳定币基础设施一体化平台;内置稳定币 on-ramp(信用卡/借记卡/Apple Pay/Google Pay,覆盖 40+ 链含 Solana/Base/多数 EVM,160+ 国家,轻量 KYC 额度 $1000 以内)及 off-ramp(法币出金) | 已有真实企业级参考案例:**MoneyGram**(用 CrossMint 钱包/稳定币编排基础设施,60 天内上线稳定币支付)、**Western Union**(与 CrossMint 合作支持 USDPT 在 Solana 上结算) |
| **Eco** | 跨链稳定币流动性编排网络,让 agent 看到"单一余额"而无需感知底层多链路由 | 与我们设想的"稳定币经某条链绕一圈"在架构上是同类问题(跨链路由) |

**定位小结**:CrossMint 目前的差异化不在协议层(它不是在跟 x402 竞争协议标准),而在于**一体化的企业级落地能力**(钱包+卡+on/off-ramp 打包,且已有 MoneyGram/Western Union 这类大型金融机构案例)。这正是它能在"帮 OpenRouter 把稳定币收款落地做扎实"这件事上提供真实价值的地方,而不是替代 x402 本身。

## 3. On/Off-Ramp 摩擦点与费率区间

- **典型费率**:零售场景下,出金(off-ramp)费率普遍在 **1%–4%**;信用卡/移动钱包类入金因为即时到账,费率更高,约 **3%–5.5%**;银行转账/ACH 较低,约 **0%–2%**。企业/机构级流量可议价到 **个位数 bps**(如 10bps),显著低于零售费率。[Stablecoin Insider](https://stablecoininsider.org/stablecoin-on-off-ramps/) [Slash](https://www.slash.com/blog/stablecoin-fees)
- **对照 OpenRouter 实际费率**:OpenRouter 自己对加密货币充值收取的 5% 已经处在(甚至高于)零售 on-ramp 费率区间的上沿——这说明它本身也在承担/转嫁 on/off-ramp 摩擦成本,而非只是"钱包里已经躺着 USDC、无摩擦"。
- **"链上 volume 补贴覆盖 conversion fee"这套经济模型是否成立**:本轮检索**未找到任何行业公开的测算案例或基准数据**直接支持或证伪这一具体模式(既没有先例说"某条链靠 volume 补贴帮某支付方 cover 手续费",也没有反例)。这是一个**开放设计问题**,不是已验证的模式。可行的估算思路(供参考,非现成数据):
  1. 先确定"经 Pharos 路由的稳定币 volume"占 OpenRouter 稳定币收款总额的比例 X%;
  2. 确定 Pharos 单位 volume 的补贴强度(即其代币经济学里给生态方的返佣/激励率),得到补贴池规模;
  3 . 补贴池 ÷ OpenRouter 需要覆盖的 on/off-ramp 费用(约当前 5% 加密收款费的一部分)= 覆盖比例。
  只有当 X% 和补贴强度都达到一定量级时,补贴池才可能覆盖有意义比例的手续费——这两个数字目前都不存在,需要与 Pharos、OpenRouter 双方分别核实,**是整个结构里最需要用真实数字验证的一环**。

## 4. Pharos 核实

- **Pharos 是什么(高置信)**:一条追求"超并行"(hyper-parallelism)高吞吐的 Layer 1 公链,定位"web3 SuperApp"生态基础设施。2024 年 11 月完成 **$800万种子轮**,由 **Lightspeed Faction 和 Hack VC** 联合领投,SNZ Capital 为战略锚定方,另有 Reforge、Dispersion Capital、Hash Global 等参投。当时宣称目标 **5万 TPS**,计划 2025 Q1 测试网、2025 年内主网。[The Block](https://www.theblock.co/post/325246/layer-1-blockchain-pharos-seed-funding)
  - **⚠️ 路线图滞后需注意**:实际私有主网延至 **2025年12月**,公开主网约 **2026年4月**;TPS 目标在后续报道中也下修至约 **3万**。官方前瞻性陈述历史上有明显缩水,评估其其他承诺(如流动性激励机制细节)时应打折扣。
- **Pharos 与 Ant Digital 的关系(高置信,但范围有限)**:Pharos 与蚂蚁数科(Ant Digital Technologies)旗下 web3 品牌 **ZAN** 确有公开可查、可技术验证的战略合作(ZAN 的 RPC 服务已集成进 Pharos 官方技术文档,非仅新闻稿),**但合作范围明确限定在节点服务、安全、硬件基础设施**,三方独立来源(The Block 报道、ZAN 官网、Pharos 官方文档)一致印证这一范围。
- **⚠️ "借 Pharos-Ant Digital 关系为 OpenRouter 争取通义千问折扣"——本轮检索未能证实,且具体版本已被证伪**:
  - 已确认 Pharos 有一个 Model-as-a-Service(MaaS)平台,与 ZAN 联合构建,**内置 x402 支付协议**支持 AI agent 支付(中置信,官方文档确认存在该功能页,但抓取受限未能完整核实细节)。[Invezz](https://invezz.com/news/2026/06/15/pharos-network-powers-ai-model-access-with-exclusive-pros-usdc-payment-integration/)
  - 但"该 MaaS 平台提供通义千问(Qwen)折扣接入""$PROS 代币持有者可获千问服务折扣"等具体说法,在 3 票对抗验证中被**明确证伪**(0-3 / 1-2 票),即找不到公开证据支持。
  - **本轮完全没有找到 Ant Digital 与阿里云通义千问团队之间存在任何股权/业务/技术授权关系的公开信息**——这条是评估"千问折扣"设想是否有组织基础的关键缺口,目前是**未知**,不是"已确认为假",但也绝非"已确认为真"。
  - **结论:千问折扣这条杠杆,目前证据强度不足以支撑,不应作为向 OpenRouter/CrossMint 承诺的既定利益,只能作为"内部关系网络下探索中的可能性"提及。** 这与 brief 里"措辞谨慎、标明探索中"的要求一致,proposal draft 已按此口径处理。

## 结论性判断

**① 撮合结构经济上是否讲得通?**
部分成立、部分待验证。好消息:OpenRouter 已经是"稳定币收款 + x402 agent 支付"的活跃玩家,不需要说服它从零建设这个能力,这比 brief 最初设想的"说服 OpenRouter 采用稳定币"要容易得多——**目标客户选对了**。但结构里最核心的两环——(a)"链上 volume 补贴覆盖 conversion fee"的具体数字模型,(b)"Pharos-Ant Digital 关系延伸到千问模型折扣"——目前都缺乏可验证的公开支持,前者是完全开放的设计问题,后者的具体版本已被证伪。**结构的逻辑骨架是通的,但两个关键假设都需要用真实数字/关系去坐实,不能当作既定事实推进。**

**② 对 OpenRouter 的潜在净价值量级?**
- 可量化的部分:OpenRouter 目前加密货币充值收取 **5%** 手续费(接近其信用卡充值 5.5%+$0.80 floor)。如果 Pharos volume 补贴能覆盖其中一部分,净价值上限是"这 5% 手续费 × 经该结构路由的稳定币收款体量"——但目前**没有任何 X%(路由占比)或补贴强度的实际数字**,无法给出可靠的美元量级估算,只能说这是一个"百分之几手续费"级别的成本项,不是数量级巨大的杠杆。
- 千问折扣部分:证据不足,**暂应按"未证实、记为零或高度不确定"处理**,不能计入向 OpenRouter/CrossMint 展示的量化价值。

**③ 最脆弱的前提假设(需要优先验证,按脆弱程度排序):**
1. **Ant Digital 与阿里云通义千问团队之间是否存在任何可授予折扣的实际业务/授权关系**——本轮完全空白,是"千问杠杆"这条故事线能否成立的地基。
2. **"链上 volume 补贴覆盖 on/off-ramp 手续费"缺乏任何行业先例或测算基准**——需要与 Pharos 核实其真实的补贴/返佣机制和强度,与 OpenRouter 核实其愿意/能够路由多少稳定币 volume。
3. **Pharos 官方路线图/技术承诺的历史缩水记录**(TPS 下修、主网延期)——意味着核实 Pharos 侧任何"承诺"都应要求书面/可验证细节,而非仅采信公关表述。

---

## 引用来源
- [Sacra: OpenRouter](https://sacra.com/c/openrouter/)
- [OpenRouter Pricing](https://openrouter.ai/pricing)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq)
- [Amnic: OpenRouter Pricing Explained](https://amnic.com/blogs/openrouter-pricing)
- [OpenRouter Crypto Payments API 公告](https://openrouter.ai/blog/announcements/crypto-payments-api/)
- [CryptoBriefing: x402 $50M OpenRouter](https://cryptobriefing.com/x402-protocol-50m-payments-openrouter/)
- [MixRoute: Pay for AI APIs with Crypto](https://mixroute.ai/blog/pay-for-ai-apis-with-crypto/)
- [Sacra: Fireworks AI](https://sacra.com/c/fireworks-ai/)
- [Sacra: Together AI](https://sacra.com/c/together-ai/)
- [ParallelIQ: Two Business Models Running AI Inference](https://www.paralleliq.ai/blog/two-business-models-running-ai-inference)
- [TrueFoundry: Portkey Pricing Guide](https://www.truefoundry.com/blog/portkey-pricing-guide)
- [TrueFoundry: LiteLLM Pricing Guide](https://www.truefoundry.com/blog/litellm-pricing-guide)
- [Requesty Pricing](https://www.requesty.ai/pricing)
- [Agent Payments Stack](https://agentpaymentsstack.com/)
- [Crossmint: Agentic Payments Infrastructure](https://www.crossmint.com/solutions/agentic-payments)
- [Crossmint: Stablecoin Onramp Docs](https://docs.crossmint.com/onramp/overview)
- [Crossmint: Stablecoin Offramp API](https://www.crossmint.com/products/offramps)
- [OneSafe: Skyfire AI Payment Revolution](https://www.onesafe.io/blog/skyfire-ai-payment-revolution)
- [Businesswire: AI Agents Race to Join Skyfire Payments Network](https://www.businesswire.com/news/home/20241024532897/en/AI-Agents-Race-to-Join-Skyfire-Payments-Network)
- [Stablecoin Insider: Best On/Off-Ramps 2026](https://stablecoininsider.org/stablecoin-on-off-ramps/)
- [Slash: Stablecoin Transaction Fees Guide](https://www.slash.com/blog/stablecoin-fees)
- [The Block: Pharos Seed Funding](https://www.theblock.co/post/325246/layer-1-blockchain-pharos-seed-funding)
- [Invezz: Pharos MaaS x402 USDC](https://invezz.com/news/2026/06/15/pharos-network-powers-ai-model-access-with-exclusive-pros-usdc-payment-integration/)
