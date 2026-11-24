# Settle-price re-run — 12 Nov 2026 (variant, NOT yet applied to the report)

## What changed vs the canonical real-CTD run
- Futures price: 106-01.5 (106.046875, CME Treasury Analytics snapshot 11 Nov 12:10 CT)
  → **106.25 (106'080, official CME Nov 10 settle for TYZ6)**.
  The snapshot price was intraday Nov 11 futures; the cash yield (4.9023%) is Nov 10
  vintage (no cash trading Nov 11, Veterans Day). The settle makes both legs Nov 10.
- Cash price still DERIVED (94.1427, repriced at CME yield 4.9023%) — the true
  Nov 10 close cash price for 91282CHT1 is still the one number that settles A vs B.
- Everything else identical: CTD 91282CHT1, CF 0.8870, SOFR 3.88%, delivery 1 Dec 2026.

## Results (script checks passed; full JSON in outputs/basis_trade_real_ctd_settle10625_results.json)
- Gross basis: +0.0791 pts → **-0.1011 pts**
- Scenario A total: -$66,561 (-3.5% of equity) → **+$113,610 (+5.98%)**
- Scenario B (CME net basis -0.3539): unchanged **+$368,151 (+19.36%)**
- Stresses unchanged: 50bp yield fall → $2,750,138 VM call (144.6% of equity);
  haircut 2%→4% = 100% of equity; basis widens 0.50pts = $500k; repo +50bp = $25,525.
- Identity gap -$1,731 (residual unhedged $11.3m leg, as in the canonical run).

## Reading
Both scenarios are now positive, so the sign dispute narrows to magnitude
(+$114k vs +$368k) — but the sign is NOT settled: the cash leg is still derived,
not observed. CME's -0.3539 net basis still embeds something beyond price + carry
(it implies cash ~93.71 / yield ~4.97%, vs the Nov 10 par curve interpolation ~4.88%
that leans Scenario A). Re-run again with the true Nov 10 cash close when it is pulled.

## Decision for Jack / the team
Apply the settle (106.25) to the canonical model + report v0.5, or wait for the
true Nov 10 cash close and apply both together? The canonical model and report v0.4
still use the snapshot price 106-01.5 and Scenario A -$66,561 until that call is made.

**DECIDED 2026-11-12 (Jack): wait for the cash close — apply settle + true Nov 10 cash close together.** Canonical model and report v0.4 stay on the snapshot price until then.

**ADOPTED 2026-11-15: the cash close arrived (94.188) and Jack chose "Adopt as v0.5" — settle + cash close are now both in the canonical model and report v0.5 (see data/cash-close-2026-11-14.md).**

**Internal note (do not surface to Jack as a separate item): the variant JSON field is still named `futures_price_106_01_5` but holds 106.25 — rename the field when the variant is adopted into the canonical model.**
