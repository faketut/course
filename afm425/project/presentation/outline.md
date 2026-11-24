# Presentation — Topic 13, Basis Trade (10 min talk + 8 min Q&A)

## Talk plan

| Time | Slides | Content |
|---|---|---|
| 0:00–1:30 | 1–2 | Hook: "$830bn of 'risk-free' arbitrage, levered 50x, in the world's safest market." Thesis: duration-hedged, not cash-flow-hedged. |
| 1:30–3:30 | 3–4 | Mechanics diagram: cash bond + short futures + repo. Basis = P − CF×F; CTD; conversion factor; haircut = leverage. |
| 3:30–6:30 | 5–6 | **Quant (slow down here):** $100m trade, $1.90m equity, 887 DV01-matched contracts, +$67,850 base case (+3.57% of equity, Nov 10 close — print-dependent bracket +$68k–$164k); stress table — repo +50bp, haircut 2→4%, basis +0.50pts, and the 50bp yield-fall VM call of $2.75m (145% of equity). Aggregate scale: $830bn, ~$485m DV01 per bp (real-CTD duration). |
| 6:30–8:30 | 7–8 | Implications: dealers/prime brokers, asset managers (the liquidity the trade provides), public (yields → mortgages), regulators (central clearing, margin floors, basis purchase facility). Mar 2020 vs Apr 2025 — keep basis vs swap-spread distinct. |
| 8:30–10:00 | 9 | Takeaways + one line: "The hedge works on yields; it is the funding that kills you." Handover to Q&A. |

## Q&A prep (backup slides, not presented unless asked)

- Sensitivity: haircut 1% vs 4%; repo +100bp; basis +1.00pts.
- "Isn't the basis guaranteed to converge?" — Yes, at delivery *if*
  you can hold it there; the risk is the cash calls before delivery.
- "Why don't funds just hold more equity?" — That is the trade:
  at 5x leverage the return is ~1% on equity; the business model
  *is* the leverage.
- "Was March 2020 caused by the basis trade?" — OFR evidence:
  likely a consequence as much as a cause; say what the paper
  actually concludes, don't overclaim.
- "What would central clearing change?" — Standardised margin,
  less bilateral repo, but margin is still procyclical.
- Counter-argument to prepare: "The trade adds liquidity and
  the Fed can always intervene" — reply: liquidity that vanishes
  in stress, and intervention is the public paying for private
  leverage.

## Speakers (to assign)

- Speaker 1: overview + securities/mechanics
- Speaker 2: quantitative analysis (must be able to re-derive the
  stress table live from `analysis/basis_trade_real_ctd.py` — the
  canonical v0.5 model, not the par-bond `basis_trade.py`)
- Speaker 3: implications + takeaways
- Q&A lead: fields funding/margin questions.
