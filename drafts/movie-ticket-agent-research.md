# 电影票选座 Agent · 市场调研

> 调研日期:2026-08-02 · 触发需求:"不想一个个点进场次看座位,希望有 Agent 在基本条件下替我选座"

---

## 0. 一句话结论

**你的痛点在美国市场确实是个真空,但它不是一个"App 没做好"的问题,而是一个"数据拿不到"的问题。**
座位级实时数据在每条合法通道上都被影院方卡住(MovieGlu 明确不提供选座、Vista 要影院授权、AMC 交易类 API 要签合同),
所以没有任何一家聚合器能做"跨场次座位对比"。
**但**:AMC 一家的座位数据事实上是可拿的,已经有人跑通了完整链路(见 §4)。
所以现实路径是——**先做一个只覆盖你常去的 1~2 家 AMC 的私人 Agent**,而不是做一个通用产品。

---

## 1. 痛点拆解:你说的其实是两件事

| # | 痛点 | 本质 | 市面现状 |
|---|------|------|---------|
| **A** | 要一个个点进场次才知道座位剩什么 | **跨场次的座位可见性**——信息在 N 次点击后面 | ❌ 全球基本没人解决 |
| **B** | 进去之后还要自己在座位图上挑 | **单场次内的选座决策** | ✅ 中国已解决(智能选座),美国没有 |

大部分产品经理只解决了 B,因为 B 是影院自己就能做的 UI 优化。
A 需要**并发拉取一批场次的座位图再做聚合**,对影院自己没有收益(它不希望你比价/比座位,它希望你在这个场次下单),
所以官方产品永远不会做 A。这就是你觉得别扭的根本原因:**这个功能和影院的利益是反的。**

---

## 2. 市场扫描

### 2.1 美国

| 产品 | 跨场次看座位 | 智能/推荐选座 | 备注 |
|------|------------|-------------|------|
| **Fandango** | 半个 —— 有 "Seat Map Preview",宣传语是"check seat availability for all showtimes",但实际交互仍是**逐场次进入预览**,不是一屏聚合;另有 "In Theaters Today" 时间段筛选 | ❌ | 覆盖面最广;⚠️ 具体交互需实机复核(官方页面对爬虫 403,只拿到应用商店文案) |
| **Atom Tickets** | **目前最接近** —— 在 "My Seats" 页可以**直接 toggle 切换不同场次**看座位,不用退回列表 | ❌ | 官方 FAQ 明写这个用法是"handy if you want to see what seats are available for similar showtimes";仍是一次看一个 |
| **AMC 官方 App** | ❌ 逐场次 | ❌ | 但**唯一有公开 API 文档**的连锁(见 §4) |
| **Regal** | ❌ 逐场次;列表只给 "Sold Out" 标签(二值,不告诉你"只剩前三排") | ❌ | |
| **Cinemark** | ❌ 逐场次 | ❌ | |
| **Alamo Drafthouse** | ❌ | ❌ | |
| **Hollywood.com Tickets** | 宣传"one single screen 比较所有组合",2022 上线、只接了 AMC | ❌ | 声量很小,基本没跑起来 |

**关键洞察:** 美国的showtime 列表最多告诉你"Sold Out / 没 Sold Out"。
"这场还剩 40% 但全是第一排" 和 "这场只剩 20% 但正中央有连座" 在列表里长得**一模一样**——
这正是逼你一个个点进去的机制。

### 2.2 中国

| 产品 | 跨场次看座位 | 智能选座 |
|------|------------|---------|
| **淘票票** | ❌ | ✅ **推荐"最佳观影区"**,在推荐区还有空位时能显著砍掉选座时间 |
| **猫眼** | ❌(可在选座页切换当天场次) | 早期只能手动;后来也上了"智能选座" |

中国把 **B** 做透了(还有影院侧动机:降低不合理选座造成的空置率),但 **A** 同样没人做。

> 对你的意义:**"智能选座"这个交互范式在中国已经被验证过用户是买账的**,不用重新验证需求。缺的只是把它从"单场次内"扩展到"跨场次"。

---

## 3. 市场空白(gap)

没有任何一个产品能回答这句话:

> "今天晚上 6-9 点,我家 5 英里内,任何影院任何场次,**只要有 2 个相连的、在最佳观影区的座位**,给我列出来并按座位质量排序。"

这就是你要的东西。它在市面上不存在。

---

## 4. 邻近玩家:有人已经摸到了一半

这三个是最值得研究的先例,**说明技术上跑得通**:

### ① SeatDrop(seatdrop.app)—— 最接近的商业产品
- 监控 **AMC / Cinemark / Alamo** 的座位释放,别人退票时推送给你
- 三种模式:**The Waiter**(想要的场次满了,等空位)/ **The Upgrader**(已有票,盯更好的座位)/ 新片开售提醒
- **免费**,且**不碰支付**——它只做"通知",让你回影院官网自己下单
- ⚠️ 它解决的是"抢到票",不是"减少筛选成本";而且是**你先指定场次+座位**,反过来了

### ② `hxbib/amc-plus`(GitHub,开源)—— 技术可行性的完整证明
一个个人项目,做的事和你想要的**高度重合**:
- 并行扫描多部电影 × 多家 AMC 的所有场次,**逐场次拉座位图**
- 对每个空位跑一套**几何打分模型**(0-100:目标行在 62% 靠后、正中、对前排/后排/边座/无障碍座加权惩罚,连体情侣座加分),分成 ELITE / GREAT / GOOD / OK 四档
- **找"相邻 N 连座"组**,偶数人数 + 躺椅厅时优先真正物理连体的 loveseat 对
- 支持按格式筛(IMAX 70MM / Dolby / Laser)、按座椅类型筛、按 AMC 周二/周三半价日筛
- 与上次扫描 diff → 发现新空位(通常来自退票)→ Discord 推送 → **可选自动通过 GraphQL 下单占座**(约 8 分钟 hold,你去浏览器完成付款)
- 作者动机:抢 Project Hail Mary 的 IMAX 70MM,最后开场前 40 分钟拿到 F24/F25(打分 88.04 / 86.04)

> **这就是你要的 Agent 的 80%。** 它证明了:座位级数据拿得到、评分模型可行、自动占座可行。
> 差的 20% 是:它是"盯着一个目标死等"的狙击模式,不是"给我条件、你帮我筛"的日常模式。

### ③ CinemaView(cinemaview.in)—— 只做评分,不碰票务
浏览器里模拟"从任意座位看屏幕"的效果,对视角/声场/沉浸感打分,一键跳到 "Best Seat"。
**可以直接拿来当你的评分函数的参考基准**,省得从零设计。

---

## 5. 数据从哪来:四条路径

这是整件事的**真正瓶颈**,不是 UI。

| 路径 | 能拿到座位级数据? | 门槛 | 判断 |
|------|-----------------|------|------|
| **MovieGlu API**(90+ 国家场次聚合) | ❌ **明确不支持选座和支付** —— 官方原话:大多数影院不对外开放订票 API | 商务申请 | ⛔ 排除。它只能给你场次表 |
| **AMC 官方 API**(developers.amctheatres.com) | ✅ 有 **Seating API v3** | `X-AMC-Vendor-Key` 请求;**catalog 类欢迎申请,ecommerce/交易类需单独批准 + 签合同** | ✅ **首选**。个人用途走 catalog key,座位读取大概率够用 |
| **Vista OCAPI**(全球大量院线的后台系统) | ✅ `GetSeatAvailabilityForShowtime`(实时,只微缓存几秒)+ `GetSeatLayout` | **要影院方给你授权 token** —— "talk to your local Vista representative" | ⛔ 个人拿不到 |
| **移动 App 私有 GraphQL** | ✅ 最全 | 要伪造 `apollographql-client-name: com.amc` 之类的头,还要用 `curl_cffi` 做 **TLS/JA3 指纹伪装绕 Cloudflare**(amc-plus 就是这么干的,而且作者把真实域名涂掉了) | ⚠️ 灰色。能跑,但违反 ToS、随时会被封 |
| **浏览器 Agent**(Computer Use / Operator 类) | ✅ 看得到就拿得到 | 慢(每场次一次页面加载)、贵、脆 | 🔸 兜底方案,适合覆盖 AMC 以外的院线 |

**结论:合法通道只对 AMC 开放,且只到"读"这一层。**
Fandango / Atom / Regal / Cinemark 没有公开的座位 API,要么爬,要么放弃。

---

## 6. 风险与合规

- **BOTS Act 大概率不适用**:该法覆盖的是"座位数 200 以上场馆的演唱会/戏剧/体育赛事",罚则最高 **$53,088/次**。普通影院厅通常远小于 200 座,且电影不是"event ticket"——但这是**解释空间**,不是保证。
- **真正的红线是"规避购买限制"**:BOTS Act 罚的是绕开限购(假身份、多张卡、多 IP)。**你自用、正常数量、不转售,风险很低。**
- **ToS 违约 ≠ 犯罪**,但会被封号——如果绑的是 AMC Stubs A-List 账号,封号成本不小。
- **建议的安全边界:**
  1. 只读座位数据 + 推送给你,**下单动作留给人**(SeatDrop 就是这个设计,它免费运营了这么久没出事,不是巧合)
  2. 请求频率克制(amc-plus 用了 TTL 缓存 300s、熔断、指数退避、尊重 `Retry-After`——照抄这套)
  3. **不要做成对外产品**,除非你愿意去和 AMC 谈 ecommerce API 合同

---

## 7. 建议方案:MVP(给你自己用,不是做产品)

> 目标:把"点 12 次进 12 个场次"压缩成"看一条推送"。

**Phase 1(1~2 天,价值最高):只读扫描器**
1. 申请 AMC catalog vendor key
2. 配置:常去的 1~3 家 AMC + 你的硬条件(日期/时间窗、人数、格式偏好、最低座位分)
3. 拉该时间窗内**所有场次** → 并发拉每场座位图 → 跑评分 → 找 N 连座
4. 输出**一张跨场次排序表**:

   | 场次 | 影院 | 格式 | 最佳可选连座 | 座位分 |
   |------|------|------|------------|-------|
   | 19:40 | Metreon | IMAX | F12-F13 | 91 |
   | 21:10 | Metreon | Dolby | E9-E10 | 84 |
   | 18:30 | Van Ness | 标准 | 只剩 B 排 | 41 |

   **这一张表就已经 100% 解决了你的痛点 A。** 后面全是锦上添花。
5. 评分函数:直接抄 amc-plus 的几何模型(目标行 ~62% 靠后 + 正中,边座/前排/后排惩罚),或用 CinemaView 的评分做校准

**Phase 2:变成 Agent**
- 接成 MCP server / Claude skill,你直接说:"周六晚上想看 X,两个人,别太靠前" → 它跑完给你排序表 + 直接给下单链接
- 加"退票捡漏"模式(SeatDrop 那套):想要的场次满了就轮询等空位

**Phase 3(可选,谨慎):自动占座**
- AMC GraphQL 下单占座约 8 分钟 hold,你收到推送再去付款
- **只在真的抢不到票的场景开**(热门首映),日常没必要

**明确不做的:**
- ❌ 覆盖所有院线(数据拿不到,ROI 极低)
- ❌ 做成 App 给别人用(合规成本 >> 收益)
- ❌ 全自动付款(风险不对称:省 30 秒,换封号风险)

---

## 8. 如果你在想"这能不能做成产品"

坦白说:**不建议**,理由如下——

- **数据护城河在影院手里,不在你手里。** Vista 要授权、MovieGlu 明说不给、AMC 交易 API 要签合同。你的产品随时可以被一个 header 校验干掉。
- **变现路径被堵死。** 你不能碰支付(SeatDrop 就是被迫"只通知不成交"),所以拿不到票务分成;订阅制卖给"选座强迫症"是个极窄的市场。
- **它和影院的利益是反的**(见 §1),不可能拿到官方合作。
- **对照组 SeatDrop 免费运营** ——一个已经做出来的、覆盖三大连锁的产品选择不收费,这本身就是市场规模的答案。

**但作为个人工具,ROI 极高**:一次性 1~2 天的工作,把你每次看电影的 10 分钟筛选压成 10 秒。

---

## 9. 待你决定 / 待验证

- [ ] **实机复核 Fandango 的 "Seat Map Preview"** —— 它到底是不是"一屏看所有场次的座位",还是仍要逐个点。官方站点挡爬虫,我只拿到应用商店文案,**这条是本报告唯一没验证死的关键事实**。如果它真做到了,你的痛点可能不用写代码就能解决
- [ ] 确认你常去的影院是不是 AMC —— **如果不是 AMC,整个 §7 方案要重估**(Regal/Cinemark 没有公开 API,只能走浏览器 Agent,成本翻几倍)
- [ ] 确认使用场景:**日常"减少筛选"** 还是 **热门片"抢好座"**?这两个的技术方案不一样(前者按需扫描,后者要常驻轮询)

---

## 参考来源

- [Fandango(App Store)](https://apps.apple.com/us/app/fandango-get-movie-tickets/id307906541) · [Fandango(Google Play)](https://play.google.com/store/apps/details?id=com.fandango&hl=en_US)
- [Atom Tickets FAQ:How does Atom work](https://www.atomtickets.com/help/entry/how-does-atom-work) · [Atom:切换日期与地点](https://www.atomtickets.com/help/entry/change-date-and-location)
- [AMC Developer Portal](https://developers.amctheatres.com/) · [Seating API v3](https://developers.amctheatres.com/ApiReference/seating-api-v3) · [API 访问申请](https://developers.amctheatres.com/GettingStarted/NewVendorRequest)
- [Vista for Developers · Seating](https://developer.vista.co/digital-platform/seating)
- [MovieGlu Developer](https://developer.movieglu.com/) · [filmShowTimes](https://developer.movieglu.com/v2/api-index/filmshowtimes/)
- [SeatDrop](https://seatdrop.app/) · [What is SeatDrop](https://seatdrop.app/guide/getting-started/what-is-seatdrop)
- [hxbib/amc-plus(GitHub)](https://github.com/hxbib/amc-plus)
- [CinemaView 座位模拟器](https://www.cinemaview.in/en)
- [竞品分析:猫眼 vs 淘票票购票流程(人人都是产品经理)](https://www.woshipm.com/evaluating/4495716.html) · [智能选座(优设网)](https://www.uisdc.com/hunter/0221284202.html)
- [Better Online Ticket Sales Act(Wikipedia)](https://en.wikipedia.org/wiki/Better_Online_Tickets_Sales_Act) · [FTC:首批 BOTS Act 执法案例](https://www.ftc.gov/news-events/news/press-releases/2021/01/ftc-brings-first-ever-cases-under-bots-act)
- [Regal 帮助中心:购票与取消](https://www.regmovies.com/help/tickets-and-cancellations)
