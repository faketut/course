# AFM 322 — Research notes (2026-10-26, for the Nov 2 initial report)

Prices are NOT frozen here. Trade prices are Nov 2 prices (Jack's decision).
Contract specs below are the ones to re-verify in IBKR on Nov 2 before
placing anything; margins in particular move.

## Scenario #1 — Steel + FX

### Steel — CME U.S. Midwest Domestic HRC Steel (CRU) Index Futures, code HRC
- Contract: 20 short tons, quoted USD/short ton, tick $1.00 = $20/contract,
  financially settled on the CRU index average for the contract month.
  Termination: business day before the last Wednesday of the contract month.
- TDI need: 2,000 / 20 = **100 contracts exactly** — no rounding basis on size.
- Contract month choice: **December**, closed out Dec 1 when steel is bought
  (do NOT hold to Dec 29 termination). A November contract would settle
  Nov 24 on the November index, before the Dec 1 purchase — worse basis.
- Basis risks to name in the report: (a) CRU Midwest index vs. the grade/
  supplier TDI actually buys, (b) futures-vs-spot on Dec 1, (c) timing:
  futures settle on a monthly average, TDI buys on one day.
- Alternatives to compare: OTC forward (exact grade/date, counterparty risk,
  no daily margin), HRC call options (premium for upside-only protection,
  keep downside), and non-derivative cash-and-carry (buy now + $50k/month
  storage — compare $50k against futures contango/basis + margin funding).
- P&L: $1/ton move = $2,000 on 100 contracts. Margin: verify in IBKR Nov 2.

### FX — $5m USD receipt Nov 30, functional currency CAD
- Exposure is short USD / long CAD: a weaker USD (lower USD/CAD) cuts the
  CAD receipt. Hedge = sell USD, i.e. buy CAD.
- CME CAD futures: 100,000 CAD/contract, quoted USD per CAD,
  tick $0.0001 = $10/contract, quarterly Mar/Jun/Sep/Dec only.
  Last trading day: business day before the third Wednesday
  (Dec 2026: Dec 15) — so close the position Nov 30, do not hold to expiry.
- Contract count formula: CAD receipt = $5m × spot USD/CAD, / 100,000.
  At 1.35 → 68, 1.38 → 69, 1.40 → 70, 1.42 → 71 contracts.
  Futures therefore leave a rounding residual of up to ~CAD 50k.
- OTC forward alternative: exact $5m, exact Nov 30 date, no rounding,
  no daily margin — but bank counterparty risk, credit line, and no
  exchange liquidity. This is the cleanest answer to "why not just futures?"
  and the likely recommended trade if the team wants a perfect hedge.
- Also name: forward points / interest-rate differential is the cost
  embedded in the forward, not a fee on top.

## Scenario #2 — Carbon (voluntary, not compliance — verify wording)

- Arithmetic (from the case, not from a market): target net 13,500t
  (15,000 × 0.90); projected gross 14,250t (15,000 × 0.95);
  **gap = 750 tonnes**.
- Why voluntary: Ontario EPS (O. Reg. 241/19) mandatory registration is
  ≥50,000 tCO2e AND a Schedule 2 industrial activity; opt-in is ≥10,000t
  AND a Schedule 2 activity. TDI's Toronto park at 15,000t fails the
  50,000t test, and a theme park is not a Schedule 2 industrial activity,
  so it is not a compliance obligation. Federal OBPS is the same 50,000t
  threshold and does not apply in Ontario in any case (Ontario EPS
  supplanted it). Check the Schedule 2 list once before writing this
  sentence in the report — TDI's ride-manufacturing arm is a wrinkle to
  rule out, since the case's 15,000t figure is the park's.
- Price range is wide and quality-driven — do NOT quote a single price:
  Ecosystem Marketplace State of the VCM 2025 (2024 trades): market
  average ~US$6.34/t; nature-based ~US$15–20/t; improved forest
  management US$14.97/t; restoration US$20.44/t. Retail Canadian
  vendor example: Sharp Management $45 base / $60 premium per unit.
  For 750t that is $4,755 at $6.34, $11,250 at $15, $15,330 at $20.44,
  $33,750 at $45. The report must pick a vendor + standard (Verra VCS
  or Gold Standard) and get a quote, not an average.
- Tradability: credits held in a registry account are transferable
  BEFORE retirement; once retired they cannot be resold. So the answer
  to "can TDI resell if November emissions are lower?" is: yes, if it
  buys and holds unretired credits and retires only at disclosure —
  but resale price is not guaranteed, and low-quality credits are
  harder to move. Staging retirement quarterly (187.5t/quarter
  pro-rata) matches the Q1 disclosure rhythm.
- Q1 disclosure math (for the final presentation, note now):
  Q1 gross ≈ 3,562.5t (15,000/4 × 0.95); Q1 net target ≈ 3,375t
  (15,000/4 × 0.90); Q1 offset retirement ≈ 187.5t if staged evenly.
- Greenwashing risk: only claim "net" after retirement, name the
  project/standard/vintage, disclose that offsets do not cut gross
  emissions, and do not net against emissions that were never TDI's.

## Scenario #3 — Weather

- Exposure math (case formula A(T) = −2(T−65)² + 3,500 per day):
  at 42°F: 2,442/day → 73,260 in November → $2,197,800 contribution
  at $30/person → **$447,800 profit** after $1.75m fixed.
  Break-even: 1,944/day → T ≈ **37.1°F** (cold side; 92.9°F is irrelevant
  in November). Below ~37°F the month loses money.
- Sensitivity at 42°F: dA/dT = 92 people/°F/day → $2,760/°F/day →
  **$82,800 per °F of monthly average, $2,760 per HDD point**
  (1°F of monthly average = 30 HDD points).
- CME Chicago HDD Monthly Futures, code H2 (CME contract specs page):
  contract unit 20 index points, 1 point = $20, financially settled,
  termination 9:00 a.m. CT on the 2nd business day after the contract
  month. CME margin for Nov 2026 shown as $1,080 maintenance/contract
  (re-verify Nov 2; initial margin is higher).
- Full linear hedge: $2,760 / $20 = **138 contracts**; margin ≈
  $149,040 at the $1,080 maintenance figure. That size is itself a
  finding: it is large relative to weather-market liquidity, and the
  quadratic payoff means a linear future over/under-hedges away from
  42°F (sensitivity rises as it gets colder). Candidates to compare:
  (a) scaled futures (e.g. 50% = 69 contracts), (b) HDD call option
  struck near break-even HDD ≈ 837 ((65−37.1)×30) — pays only in the
  loss region, premium is the cost, (c) OTC Toronto-indexed swap/
  collar — kills Chicago basis but adds counterparty risk and cost.
- Basis risks: Chicago vs. Toronto temperatures; HDD index (65°F
  base, daily (high+low)/2) vs. the attendance formula's T; monthly
  average simplification vs. daily attendance variation; warm days
  above 65°F would also cut attendance but cannot happen materially
  in a November HDD hedge (HDD = 0 above 65°F).
- Expected November HDD at 42°F: (65−42) × 30 = **690**. A futures
  entry near 690 is the "traders expect 42°F" price the case invites
  you to assume when no live quote is visible.

## Scenario #4 — still open
- Own strategy and the WSB Agent's strategy are NOT chosen yet.
  Both need, in the separate 3-page doc: strategy + why, margin,
  max profit / max loss / break-even(s) including transaction costs,
  and the trade evidence (IBKR screenshot or Excel log).
- Capital: IBKR paper account is $1m USD fictional, may be treated
  as $10m (×10). Do not double-count margin: TDI hedge margin and
  personal-strategy margin draw on the same paper account, so the
  report must state the allocation explicitly.

## Sources checked 2026-10-26
- CME Group: HRC steel futures specs; Chicago HDD Monthly futures
  contract specs + margins pages; weather futures/options codes.
- Government of Ontario: EPS program registration page (O. Reg. 241/19).
- Government of Canada / ICAP: federal OBPS 50,000t threshold.
- Ecosystem Marketplace State of the VCM 2025 via secondary reporting
  (2024 transaction averages); Sharp Management Canada retail pricing.
- All of the above to be re-checked in IBKR / vendor quotes on Nov 2.
