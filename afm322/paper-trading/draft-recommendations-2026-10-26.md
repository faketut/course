# Initial report — draft recommendations (PRELIMINARY, for team review)
# Nothing here is executed. Prices, margins and option premiums are
# Nov 2 figures, to be filled in IBKR on Nov 2. This file is the
# autonomous draft; the team (and Jack, for Scenario #4) must approve
# it before any order is placed.

## General: why hedge at all
Benefits: locks in input cost / receipt value, stabilises cash flow
and margins, protects the November operating decision and the public
net-emissions commitment, and makes TDI's risk visible to the CRO.
Drawbacks: hedges cost (margin funding, option premiums, bid/ask,
basis), cap upside (futures/forwards), can create cash calls
(daily variation margin) even when the underlying has not moved,
and a badly sized hedge adds risk instead of removing it. TDI
hedges to reduce volatility, not to speculate — Scenario #4 is the
only speculative book, and it is kept separate.

## Scenario #1 — RECOMMENDATION
### Steel: LONG December CME HRC futures, 100 contracts
- Why futures over forward/options/cash-and-carry: exact size
  (2,000/20), exchange liquidity and daily transparency, no
  storage cost, no premium bleed. Forward would fix grade/date
  exactly but adds bank counterparty risk and is not executable
  in the IBKR paper account; a call option protects upside only
  but costs a premium for protection TDI needs in full; buying
  now costs $50k/month storage and ties up working capital.
- Trade: long 100 × Dec HRC, close Dec 1 when steel is bought.
  Effective steel cost = F₁ + b₂ (Module 3) — the report must NOT
  claim it locks in today's spot price.
- Basis: CRU Midwest index vs. TDI's actual grade/supplier;
  monthly-average settlement vs. a single Dec 1 purchase.
### FX: LONG CAD December futures in IBKR (primary, paper-executable)
- $5m USD receipt Nov 30 → short USD. In IBKR, buy CAD futures:
  contracts = ($5m × Nov 2 spot USD/CAD) / 100,000, rounded to
  nearest whole contract (at 1.40 → 70). Close Nov 30.
- Disclose the rounding residual (up to ~CAD 50k unhedged) and the
  Dec-contract timing basis (last trading day Dec 15, closed early).
- State explicitly: in real life an OTC forward for exactly $5m
  on Nov 30 would be the perfect hedge; it is not the paper
  recommendation because it cannot be executed / evidenced in
  IBKR, and the report must not present an Excel-only forward
  as if it were a brokered trade. If the team prefers the OTC
  route, flip this recommendation — but then the evidence is
  Excel-only, by the brief's own supplement rule.
- Margin: verify in IBKR Nov 2; futures daily variation margin
  is a cash-flow risk even though total P&L matches a forward
  ignoring funding (Module 3 Q1).

## Scenario #2 — RECOMMENDATION
- Buy **750 tonnes** of Verra VCS or Gold Standard verified
  voluntary offsets, held UNRETIRED in a registry account, and
  retire in stages at disclosure (Q1 ≈ 187.5t pro-rata).
- Why voluntary: Ontario EPS mandatory ≥50,000t + Schedule 2
  activity; TDI park is 15,000t and a theme park is not Schedule 2.
  Federal OBPS is the same 50,000t threshold and does not apply
  in Ontario. (Re-check Schedule 2 against TDI's manufacturing
  arm before final wording.)
- Price: do not use a single average. Budget at nature-based
  rates ($15–20.44/t → $11,250–$15,330 for 750t); get a vendor
  quote Nov 2 and name project / standard / vintage in the report.
  Retail $45/t ($33,750) is an upper bound, not the plan.
- Resale: yes, before retirement, at an uncertain resale price;
  no, after retirement. That staging is the answer to the brief's
  "can TDI resell if November emissions are lower?" question.
- Disclosure honesty: offsets do not cut gross emissions; claim
  "net" only for retired tonnes, name the project, and do not
  over-claim neutrality (the commitment is −10%/yr, not net-zero
  this year).

## Scenario #3 — RECOMMENDATION (to confirm on Nov 2 option quotes)
- Primary candidate: **LONG Chicago HDD November call options
  struck near break-even HDD ≈ 837** ((65 − 37.1) × 30), expiry /
  settlement per CME H2 options, premium TBD Nov 2.
  Rationale: TDI only loses money below ~37.1°F; a call struck
  there pays only in the loss region, costs only its premium,
  and avoids the daily margin and over-hedging of a linear future
  on a quadratic attendance curve.
- Alternative, fully costed in the report: long H2 November
  futures, scaled — full linear = 138 contracts ($2,760/$20),
  maintenance margin ≈ $149k at CME's Nov 2026 $1,080 figure;
  50% = 69 contracts ≈ $74.5k. The report must explain why 138
  is not the default: size vs. weather-market liquidity, and
  sensitivity rising as it gets colder (quadratic), so a linear
  future mis-hedges away from 42°F.
- Expected November HDD at 42°F = 690; break-even HDD ≈ 837;
  November profit at 42°F ≈ $447,800 (73,260 visitors × $30 −
  $1.75m fixed). Basis: Chicago vs. Toronto; HDD 65°F base vs.
  the attendance formula; monthly-average simplification.
- Non-derivative alternatives: flexible staffing / variable
  hours, ticket-price flexibility, weather insurance (not a
  derivative, different counterparty and claims process), and
  simply accepting the risk given $447,800 expected profit —
  with the loss region below 37°F quantified, not waved away.

## Scenario #4 — NOT decided by the agent alone
- Jack's own strategy: PROPOSED for Jack's approval — a defined-
  risk vertical spread (bull call spread or bear put spread,
  Module 8) on a liquid underlying, chosen from the Nov 2 IBKR
  option chain, with max profit/loss/break-even incl. costs
  computed from actual quotes. A spread, not a naked position,
  because the brief's final report asks for Sharpe / drawdown
  and whether the strategy belongs in a real account — a
  defined-risk answer is defensible on both.
- WSB Agent's strategy: to be generated independently (separate
  log, separate prompt) and NOT shown to Jack before he locks
  his own pick, or the competition is meaningless.
- Both: close by Nov 30, track in the personal tab of the log,
  never in the TDI tab.

## What the 6-page body will contain (appendices carry the rest)
p1 memo + general hedging + risk snapshot; p2 S1 exposures +
comparison table; p3 S1 trades; p4 S2; p5 S3; p6 AI, limits,
interim-report plan. Contract specs, full calculations, AI graph,
PowerBI screenshot, training description, and ALL AI correspondence
go in appendices (not counted in the 6 pages).
