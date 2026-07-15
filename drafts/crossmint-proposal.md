# Proposal: A Stablecoin Payment Pilot for LLM Inference — with a Warm Introduction to OpenRouter

**To:** Head of Partnership, CrossMint
**From:** [Your name] — Solana ecosystem DeFi & stablecoin partnerships
**Date:** 2026-07-15
**Status:** Early-stage structuring — seeking alignment and an introduction, not a signed deal

---

## 1. Background

We work at the intersection of Solana DeFi, stablecoin liquidity, and ecosystem partnerships. Through a **strategic relationship with Ant Digital**, we're able to bring discounted access to Qwen inference to the right partner — and we want to build a pilot around it.

The pilot: **stand up an end-to-end stablecoin payment flow for LLM inference, starting from a discounted Qwen model collaboration.** The natural first partner is a leading LLM gateway that already prices in tokens and already accepts stablecoins — **OpenRouter** being the obvious candidate. Two things make it attractive for them: a cheaper inference source, and a payment flow where **we cover a meaningful share of their stablecoin conversion cost.**

CrossMint is the piece that makes the payment side real, and the reason we're writing to you.

## 2. Why now — why AI × stablecoins

- **Agentic AI spend is becoming stablecoin-native.** AI agents increasingly pay for their own compute and API calls programmatically, and stablecoins — not cards, not invoicing — are the natural machine-to-machine rail. This is the thesis behind CrossMint's own agent-payment work.
- **The lead partner is already there.** OpenRouter already accepts USDC and has integrated Coinbase's x402 protocol for per-request stablecoin settlement — running at an estimated ~$50M annualized revenue on $100M+ of annualized inference spend. This isn't a "convince them to try stablecoins" pitch; the rail is live. The open lever is **cost** — both model cost and conversion cost — and that's exactly what this pilot improves.

CrossMint sits at the exact junction: an on/off-ramp and agent-payment provider that already speaks both "stablecoin rails" and "AI agent" fluently, with real enterprise proof points (MoneyGram, Western Union).

## 3. How the pilot is structured

| Layer | What happens | Who provides it |
|---|---|---|
| **Model** | Discounted Qwen inference brought in as the pilot's starting point — a cheaper source for the gateway | Us, via our Ant Digital strategic relationship |
| **Payment (on/off-ramp)** | End-to-end fiat ↔ stablecoin conversion so the gateway can be paid in stablecoins with minimal friction | **CrossMint** |
| **Settlement** | The payment flow settles on **Pharos**, routed over our rail | Us (settlement infrastructure) |
| **Economics** | We offset a meaningful share of the gateway's stablecoin conversion cost, sized to volume | Us |

**In one line:** we bring the cheaper models and cover part of the payment cost; CrossMint provides the on/off-ramp that carries the flow; settlement runs across our rail on Pharos.

## 4. The economics (indicative, not a commitment)

The gateway's own stablecoin top-up/conversion cost runs on the order of ~5%, in line with retail on/off-ramp norms. Against a reference volume on the order of **$50M**, we'd expect to be able to **offset roughly 2–3 percentage points of that conversion cost** — i.e. cover a large share of the gateway's payment friction outright. The exact figure scales with volume and is something we'd size together once the structure is agreed; the point of this note is that the coverage is real and material, not the precise number.

## 5. CrossMint's role and upside

- **What you provide:** the end-to-end on/off-ramp — fiat ↔ stablecoin conversion, custody/wallet plumbing, and the agent-payment rails you've already built — that makes stablecoin-denominated inference billing operationally real.
- **What you get:**
  - A **flagship reference deployment** — "the stablecoin payment layer behind a leading LLM gateway" is a marquee case for CrossMint's agent-payments narrative.
  - **Real, recurring transaction volume** at gateway scale, not a pilot-sized integration.
  - **First-mover positioning** as the default settlement layer for AI-usage payments, ahead of Skyfire, Payman, or a raw x402-based flow claiming the spot.
- **What we're asking you to do:** nothing operationally yet — this is a structuring conversation, not an integration request.

## 6. The ask

Two things:

1. **A conversation** to sanity-check the structure and confirm CrossMint's interest in principle.
2. **An introduction to your OpenRouter counterpart.** We don't have an existing relationship there; CrossMint's standing partnership context is the natural door-opener. Put plainly: helping us open this door is CrossMint helping itself land a flagship AI-payments deployment.

## Next steps

- CrossMint: internal read + go/no-go on the introduction.
- Us: happy to join a call with your OpenRouter contact directly, or send a short one-pager they can forward internally first — whichever is easier on your end.

Looking forward to your thoughts.

---

*Note: our own take rate / commercials are deliberately out of scope for this conversation — the goal here is to confirm the structure works and everyone can plug in.*
