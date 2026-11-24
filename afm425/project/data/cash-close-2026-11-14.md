# Cash-close re-run — 14 Nov 2026 (variant, NOT yet applied to the report)

## The one number is in: Nov 10 close for 91282CHT1 = 94.188

- Source: Safe Rate Markets security page for the 3.875% note due Aug 15, 2033,
  https://saferate.com/treasury/securities/91282CHT1, read 14 Nov 2026 ~14:55 EST.
  Safe Rate republishes Treasury's own end-of-day prices; the page's price-history
  table gives, for Nov 10, 2026: bid 94.094 / offer 94.125 / **close 94.188**
  (per 100 of face). Neighbouring closes sanity-check the series: Nov 9, 94.906;
  Nov 12, 93.500 — a 72-cent fall on Nov 10, consistent with the 10y par yield
  rising 10 bp that day.
- No API key was needed: the public security page carries the full price history.
  (The API route tried Nov 14 needs a free key and 401s without one; the page is
  the free route that works.)
- Quirk, flagged not hidden: the close sits outside the bid-offer spread on both
  sides of the window (Nov 10 close 94.188 is 6.3c above the offer; Nov 12 close
  93.500 is 15.6c below the bid). The close is Treasury's EOD print, not a mid —
  so the report should quote the close as "the Nov 10 close" and show the
  bid/offer bracket as the sensitivity, not average the three prints.

## Cross-check: the derivation is confirmed, Scenario B is rejected

- The observed close reprices to a yield of 4.894% on the Nov 11 stub — 0.8 bp
  below CME's reported cash yield of 4.9023%. The derived clean price 94.1427
  sits ~1.8c above the Nov 10 offer (94.125) and 4.5c below the close (94.188) —
  outside the bid-offer spread (94.094–94.125), not inside it. The derivation was
  right to within 4.5 cents.
- Scenario B (CME net basis −0.3539) implies a cash price near 93.71 — about
  40–48 cents below every Nov 10 print (bid / offer / close). That is ~8 bp of yield away from the Nov 10 par-curve
  interpolation (~4.88%). Scenario B is now REJECTED on observed prices, not
  just doubted. It stays in the output below only for comparison.
- The sign dispute is SETTLED: the base case is positive. What remains is
  magnitude, and it is print-dependent (see bracket below).

## Results (script checks passed; full JSON in outputs/basis_trade_real_ctd_cashclose10625_results.json)

Variant script: analysis/basis_trade_real_ctd_cashclose.py — a copy of the
canonical script with YTM 0.04894 (reprices to clean 94.1883, i.e. the observed
close to 0.03 cents) and futures at the official Nov 10 settle 106.25, so both
legs are Nov 10 vintage. Canonical model and report v0.4 untouched.

- Gross basis: +0.0791 pts (canonical, snapshot futures) → −0.1011 (settle
  variant, derived cash) → **−0.0554 pts** (this variant, observed cash + settle)
- Scenario A total: −$66,561 (−3.5% of equity) → +$113,610 (settle variant) →
  **+$67,850 (+3.57% of equity)**
- Scenario B: +$368,056 — REJECTED, see above; do not carry it into v0.5
  as a live scenario. If the report keeps it, label it "CME net basis,
  contradicted by the observed Nov 10 close".
- Stresses unchanged: 50 bp yield fall → $2,751,689 VM call (144.7% of
  equity); haircut 2%→4% = 100% of equity; basis widens 0.50 pts = $500k;
  repo +50 bp = $25,538. Identity gap −$1,731 (same residual unhedged
  $11.3m leg as the canonical run).
- DV01 $55.03 vs CME $53.98 (+1.9%); modified duration 5.843 vs CME 5.7838
  (+1.0%) — same cross-check as the canonical run.

## Magnitude bracket across the Nov 10 prints (carry ≈ $14,156 in all cases)

- Close 94.188 → gross basis −0.0554 → total **+$67,850** (primary: this is
  what "Nov 10 close" means; script-exact)
- Offer 94.125 → gross basis −0.1188 → total ≈ +$133,000
- Mid 94.110 → gross basis −0.1343 → total ≈ +$148,000
- Bid 94.094 → gross basis −0.1498 → total ≈ +$164,000
- So: base case +$68k to +$164k, sign positive throughout. The report should
  lead with the close-based +$67,850 and footnote the bracket.

## Decision for Jack / the team

Jack decided 2026-11-12: wait for the cash close, then apply settle + true
Nov 10 cash close together as v0.5. The cash close has now arrived, so v0.5
can be built from this variant: adopt futures 106.25, cash 94.188 (close),
Scenario A +$67,850 as the base case, Scenario B labelled rejected, stresses
unchanged. Canonical v0.4 (−$66,561) stays as-is until that adoption call is made.

**ADOPTED 2026-11-15 (Jack: "Adopt as v0.5").** This variant is now the canonical model: `analysis/basis_trade_real_ctd.py` runs YTM 0.04894 and futures 106.25, its JSON field is renamed `futures_price` (stale `futures_price_106_01_5` name retired), and report v0.5 (draft.md + report.typ + compiled PDF, 8pp: 5pp body + 3pp appendices/references) carries Scenario A +$67,850, gross basis −0.0554, Scenario B labelled rejected. The variant script and this note stay as the audit trail.

**Internal note (do not surface as a separate item): the variant JSON field is
still named `futures_price_106_01_5` but holds 106.25 — rename the field when
the variant is adopted into the canonical model, as already noted for the
settle variant.**
