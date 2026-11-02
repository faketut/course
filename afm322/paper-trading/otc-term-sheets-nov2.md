# OTC term sheets — Nov 2, 2026 (Excel-logged, NOT IBKR executions)

Decision locked by Jack Nov 2, 00:09 EST: steel goes to IBKR in daytime;
FX and weather go via Excel-logged OTC. These sheets are PREPARED, not
executed: every market input is TBD until daytime, and no row flips to
EXECUTED until its input is filled from a named source.

## FX — OTC forward, Scenario #1 (second leg)
- Direction: TDI SELLS USD 5,000,000, BUYS CAD.
- Settlement: Nov 30, 2026 (the receipt date, not a futures expiry).
- Rate: Nov 2 daytime USD/CAD spot, source to fill (IBKR FX spot or
  Bank of Canada daily rate, Nov 2) — TBD daytime.
- CAD amount: 5,000,000 x rate = TBD daytime (formula, not a guess).
- Forward points: ASSUMED ZERO in this paper log. This is a disclosed
  simplification: a real Nov 30 forward would differ by the CAD–USD
  interest differential, which is not available in the paper account.
  The report must say so; it must not present the spot rate as a
  market forward rate.
- Margin: none in the OTC paper log (counterparty credit risk disclosed
  in the report, vs futures margin which the futures route would have
  required). No IBKR order, no IBKR screenshot for this leg.
- Why this leg: it is exact — $5m on Nov 30, no 100,000-CAD rounding
  residual, no quarterly-contract mismatch. That is also why it was
  already the real-life perfect hedge in the draft.

## Weather — OTC, Scenario #3 (choose ONE daytime, do not log both)
### Option A (primary, only if a premium quote exists daytime)
- OTC Chicago HDD November call, strike 837 (break-even HDD), $20 per
  index point, settlement on the November HDD index.
- Premium: TBD from a counterparty quote daytime. If no premium quote
  is obtained, DO NOT log this option with an invented premium — use B.
- Payoff at settlement: $20 x max(0, actual Nov HDD - 837) per unit,
  minus premium paid. Number of units: TBD daytime (must be stated
  with the premium, or the payoff cannot be checked).

### Option B (default OTC fallback — fully specified, no premium needed)
- OTC Chicago HDD linear swap, 69 units (50% of the 138-unit full
  linear hedge), $20 per point = $1,380 per HDD point.
- Fixed leg: expected Nov HDD 690 (at 42F: (65-42) x 30).
- Payoff at settlement: 69 x $20 x (actual Nov HDD - 690).
  At break-even HDD 837 this pays 69 x $20 x 147 = $202,860, against a
  November loss at break-even of $0 by definition — i.e. it is a
  partial hedge, and the report must call it partial, not full.
- Full linear (138 units, $2,760/HDD point) is NOT the default: it
  over-hedges the quadratic payoff above break-even and is large for
  a thin weather market, as already flagged in the draft.
- Settlement index: Chicago HDD for November, defined as the sum over
  November days of max(0, 65 - daily average temperature in F), per
  the CME Chicago HDD definition (daily temps from NOAA Chicago
  O'Hare, to be recorded daily in November, not estimated now).

## Daytime checklist (in order)
1. Re-quote HRC Dec in IBKR (daytime bid/ask, margin re-verify), then
   place LONG 100 x Dec HRC at the daytime ask, screenshot the order.
2. Fill the FX spot rate from a named daytime source, compute the CAD
   amount, log the OTC forward.
3. Choose weather A or B (A only with a real premium quote), log ONE.
4. Carbon: named Verra/Gold Standard vendor quote for 750t, unretired.
5. Jack locks Scenario #4, then WSB pick is revealed and logged.
6. Flip log rows PLANNED -> EXECUTED, fill report placeholders,
   team sign-off, submit by ~18:00 EST.

## FX — LOCKED Nov 2 (Jack's confirmation)
- Rate: 1.3970 (Finnhub/OANDA ~07:27 EST Nov 2, 1.39701 rounded to 1.3970).
- CAD amount: 6,985,000. Settle Nov 30, 2026. Status in log: EXECUTED (Excel-logged OTC).
- Team pack: SENT by Jack (confirmed Nov 2 morning).
