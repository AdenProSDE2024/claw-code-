# Proposal: A Stablecoin Settlement Layer for AI-Router Payments — CrossMint, Pharos, and OpenRouter

**To:** Head of Partnerships, CrossMint
**From:** [Your Name], [Your Company]
**Date:** July 2026
**Re:** Introduction request — a routed-stablecoin structure connecting CrossMint, Pharos, and OpenRouter

---

## Background

We're a Solana-ecosystem team working at the intersection of stablecoin infrastructure and DeFi, and we've been designing a piece of plumbing that we think sits squarely in CrossMint's lane: routing an AI-infrastructure company's stablecoin payment volume through an emerging L1 in a way that benefits every party in the chain, with CrossMint providing the rails that make it possible.

The short version: **OpenRouter** already accepts USDC and is moving further into crypto-native billing via x402. **Pharos**, an EVM-compatible RealFi chain built with native USDC/CCTP settlement (via a Circle partnership) and backed by a live Model-as-a-Service channel through Ant Digital's ZAN, has an on-chain stablecoin volume KPI it is actively incentivizing. We see an opportunity to route a slice of OpenRouter's stablecoin payment flow through Pharos — helping Pharos hit its liquidity/volume targets, funded in part by a Pharos-side incentive, while OpenRouter's own crypto payment costs move in a favorable direction. **CrossMint is the rail this depends on**: the on/off-ramp and agent-payment infrastructure that would actually move money between these parties.

We're bringing this to you first because CrossMint is the piece we can't build ourselves — and because we think this is a genuinely good match for where CrossMint is headed strategically.

## Why now

Three things have converged in the last few months that make this the right moment to test this structure, not a year from now:

- **OpenRouter is the most crypto-native of the major LLM gateways, and growing fast.** It's the only major router that accepts USDC directly and is actively shifting billing toward x402 pay-per-request settlement — x402 has already processed $50M+ in volume with OpenRouter as a flagship adopter. Its revenue has scaled from ~$1M ARR (end of 2024) to ~$50M ARR (early 2026), on the back of a $113M Series B at a $1.3B valuation. None of its named competitors (Together AI, Fireworks, Requesty, LiteLLM) offer comparable stablecoin support today — this is a live differentiator, not a hypothetical.
- **Pharos has the settlement infrastructure and the incentive, right now, to want exactly this kind of volume.** It has native USDC/CCTP rails live on mainnet via its Circle partnership, and a real, named channel into AI model access through Ant Digital's ZAN — a live MaaS platform where PROS and USDC are the exclusive payment methods for accessing models including Qwen. Pharos is early and needs on-chain stablecoin volume to match its funding and valuation story; that need is a live, current-quarter opportunity, not a future one.
- **Agent-to-agent and AI-to-infrastructure stablecoin payments are becoming a category**, with x402, Skyfire, and Payman all building toward the same primitive: agents and platforms transacting in stablecoins without touching a traditional bank rail. Being the settlement layer that connects an AI-router's payment volume to an emerging chain's liquidity needs is a positioning opportunity that gets more contested, not less, the longer it sits unclaimed.

We think the underlying economics need real diligence before anyone signs anything — and we're doing that work in parallel. But the question of whether the *structure* can be built and whether the *right people* are willing to have the conversation is one we can resolve now, and that's what this note is about.

## How each party's KPI locks together

This only works because each party can point at something they already care about:

- **OpenRouter** cares about processing volume, developer growth, and its own cost of payment acceptance. Routing stablecoin flow in a way that can reduce its effective cost of crypto settlement — while it's already actively investing in crypto-native billing (x402) — is directly aligned with where its payments roadmap is already going.
- **Pharos** cares about on-chain stablecoin volume and liquidity as a direct proof point for its RealFi thesis, its token, and its investors (Sumitomo, Flow Traders, and others backing its $52M in funding to date). Routed volume from a real, high-growth AI-infrastructure company is exactly the kind of organic activity that early-stage L1s struggle to manufacture on their own.
- **CrossMint** cares about transaction volume through its rails, and about being positioned as the default infrastructure layer for a category — AI-agent and AI-infrastructure stablecoin payments — that is visibly forming right now around x402, agent commerce, and multi-protocol wallets. CrossMint already positions itself as protocol-agnostic middleware across x402, AP2, Agent Pay, and Intelligent Commerce; this is a concrete, named use case that fits that positioning exactly.
- **We** care about proving that this kind of multi-party stablecoin routing structure — connect a payments-heavy platform's stablecoin flow to a chain that needs volume, with the right rails in between — actually works end to end. This is deliberately a structure-proof exercise before it's an economics negotiation.

## CrossMint's role and upside

Concretely, we see CrossMint providing:

- **The on-ramp and settlement rails** that move stablecoin value between OpenRouter's payment flow and Pharos's chain — the connective tissue the whole structure depends on.
- **Agent-payments infrastructure** (wallets, multi-protocol support across x402 and others) that OpenRouter and Pharos would otherwise each have to build or separately integrate.
- **A reference case** for CrossMint's stated strategic direction — protocol-agnostic middleware for AI-driven commerce — with a named AI-infrastructure company (not a hypothetical agent use case) and a named L1 partner, at a moment when that category is actively being defined by a handful of infrastructure players.

What's in it for CrossMint specifically: incremental transaction volume through your rails, and a visible, technically credible case study that reinforces the "default stablecoin payment layer for AI-router use cases" position — the kind of story that compounds as more AI platforms look for exactly this kind of settlement infrastructure.

To be direct about scope: **we are not asking CrossMint to commit to economics, volume targets, or a formal partnership at this stage.** This phase is about proving the structure works technically and commercially for all three parties — OpenRouter, Pharos, and CrossMint — not about negotiating anyone's take-rate, including ours. If the structure proves out, the commercial conversation is a separate, later step.

## The ask

We don't have a direct relationship with OpenRouter today, and we understand CrossMint does. Our specific ask is narrow:

**An introduction to the right contact at OpenRouter** — ideally someone on their payments, partnerships, or business development side — to have an exploratory conversation about routing stablecoin volume through Pharos as a way to reduce OpenRouter's cost of crypto payment acceptance, with Pharos providing a volume-based incentive to fund it.

**Proposed next step:** a short introductory call or email thread with OpenRouter, CrossMint, Pharos, and us — framed explicitly as exploratory, no commitments — to test whether the structure holds up from OpenRouter's side before anyone invests further time in it. We're happy to prepare a one-page technical/commercial summary for that conversation, and to loop in Pharos on our side whenever useful.

We think this is a small ask relative to the upside if it works, and we'd welcome the chance to talk through any part of this in more detail before you make the introduction.

Thanks for considering it — happy to jump on a call this week or next.

[Your Name]
[Your Company]
[Contact Information]
