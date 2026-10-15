# Earnings-yield factor — literature background for the Project 2 report

Prepared 2026-10-14 (background research; use when writing the report, after regressions are done).
Citations verified via web search on 2026-10-14. This is a summary + citation pack, not quoted text.

## 1. The E/P anomaly (economic rationale anchor)

- Basu, S. (1977), "Investment Performance of Common Stocks in Relation to Their
  Price-Earnings Ratios: A Test of the Efficient Market Hypothesis," *Journal of Finance*
  32(3), 663-682. DOI: 10.1111/j.1540-6261.1977.tb01979.x
  - NYSE industrials, 1957-1971. Lowest-P/E quintile earned ~16.3% p.a. vs ~9.3% for the
    highest-P/E quintile; the spread survived CAPM risk adjustment. Earnings yield = 1/(P/E),
    so this is the original high-EY-minus-low-EY result.

## 2. The honest prior for the benchmark comparison (spanning test)

- Fama & French (1992): in cross-sectional regressions, the E/P effect is largely **subsumed
  by size and book-to-market**. Implication for this project: the literature's null is that
  *trailing* EY adds nothing beyond SMB/HML. The FF3/FF5 spanning test is therefore the
  real test of the factor — a significant spanning alpha is the result worth emphasizing;
  an insignificant one is the literature-consistent outcome and should be reported honestly.
- Nuance that favors this project's design: the BRAIN alphas that inspired the factor use
  **forward expected** earnings (analyst-forecast EBIT/PTP divided by cap), a different
  information set from trailing TTM net income. The FF92 subsumption result applies most
  directly to the trailing implementation; the report should state this forward-vs-trailing
  gap explicitly (already planned in the brief).

## 3. Publication decay — for the "widely known" sensitivity + efficiency discussion

- McLean, R.D. & Pontiff, J. (2016), "Does Academic Research Destroy Stock Return
  Predictability?", *Journal of Finance* 71(1), 5-32.
  - Across 97 published return predictors: returns are ~26% lower out-of-sample (upper bound
    on data-mining) and ~58% lower **post-publication**; ~32pp of the decay is attributed to
    publication-informed trading. Post-publication decay is largest in liquid, easy-to-trade
    stocks; the surviving premium concentrates in illiquid / high-idiosyncratic-risk names.
  - Directly motivates the brief's suggested sensitivity variant: split the sample **before
    vs after the E/P effect became widely known** (Basu 1977 / FF 1992 era). It also answers
    "why hasn't it been traded away": (a) part of the in-sample premium was data mining,
    (b) arbitrage compressed what was real, (c) what remains sits where trading is costly —
    check whether the project's premium survives in large caps.

## 4. Rational vs behavioral framing (for the interpretation section)

- Rational (risk-based): high-EY firms are cheap because they carry more distress/earnings
  risk; the premium is compensation for doing badly in bad times. Counterpoint to disclose:
  Ball, R. (1978) argued apparent E/P anomalies can reflect CAPM risk mismeasurement and
  transaction costs rather than mispricing.
- Behavioral: investors extrapolate past growth — overpaying for glamour (low EY) and
  underpricing value (high EY); mispricing corrects slowly because of limits to arbitrage.
  Reference points: De Bondt & Thaler (1985) overreaction; Lakonishok, Shleifer & Vishny
  (1994) contrarian/value explanation.
- Evidence to bring: how the EY factor behaves in recessions/market downturns (bad-times
  performance supports the risk story; no bad-times pattern weakens it).

## 5. Market-efficiency implications (for the report's final section)

- EY is built from **public accounting information** -> a persistent premium speaks to
  **semi-strong** efficiency, not just weak-form.
- Grossman & Stiglitz (1980) near-efficient markets: a small residual premium can persist
  in equilibrium as compensation for information and trading costs — the "can the intended
  audience earn it after costs, and should they?" question should be answered against the
  net-of-cost premium, not the gross one.
- Replication record is mixed (some updates find the P/E effect weaker after the 1980s) —
  which is exactly what the subperiod sensitivity is for; report whichever way it goes.

## Intended-audience line (quant PMs deciding whether to tilt)

Frame the verdict as: (1) does EY span FF5 in *your* sample, (2) does it survive the
post-publication subperiod, (3) is the net-of-cost premium positive in liquid names.
A "yes" to all three is a tilt case; anything less is a "monitor, don't allocate" case.
