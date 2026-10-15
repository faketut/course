# CFM301 Project 2: Finding and Testing a Factor — brief (from course handout)

## Objective
Propose at least one factor — beyond market, size (SMB), value (HML), momentum (UMD) —
that helps explain the cross-section of asset returns, with empirical evidence.
Macro (inflation, growth, volatility) or dynamic/style (quality, illiquidity, low
volatility, credit risk) factor, constructed as a long-short portfolio.

Tests whether the group can correctly apply class tools: constructing returns,
cleaning financial data, building a factor, running/interpreting factor regressions,
sensitivity analysis, and interpreting results under rational vs. behavioral theories
and market-efficiency notions.

## Requirements
1. Propose 1–2 candidate factors + economic rationale (why exposure earns a risk
   premium; how it defines "bad times" in the multifactor framework). Identify the
   intended audience (e.g., quant fund managers, pension funds).
2. Construct or source factor time series + test assets (individual stocks or
   characteristic-sorted portfolios) using CRSP and/or Compustat.
3. Returns must be total returns incl. dividends, split-adjusted (CRSP RET not RETX;
   PRC not split-adjusted — use CFACPR; Compustat: adjustment factor + dividends).
   State variable/formula and frequency.
4. Clean data: missing values, duplicates, outliers. Winsorize returns and sorting
   characteristics (state cut-offs, e.g. 1st/99th pct) or justify not winsorizing.
   Report observation counts affected at each step.
5. OLS: regress test-asset returns on the factor (+ market as control); report
   loadings, t-stats, R².
6. Compare explanatory power vs. a standard benchmark (CAPM or Fama-French style);
   state whether the factor adds explanatory power.
7. Sensitivity: re-run under ≥2 alternative assumptions (different sample/sub-periods;
   terciles vs. quintiles; equal- vs. value-weighted legs; different benchmark;
   different winsorization cut-off). Compact table suffices.
8. Rational vs. behavioral discussion, with evidence (e.g., factor performance in
   recessions/market downturns).
9. Market-efficiency implications: which form (weak/semi-strong/strong) given the
   information used; premium = risk compensation or inefficiency? If inefficiency,
   why not traded away (costly information/trading, capital barriers)? Consistent
   with Grossman-Stiglitz (1980) "near-efficient"? What it means for the audience
   (can they earn the premium after costs — should they?).

## Deliverables
- LEARN Dropbox 2 days before presentation: reproducible code + README; trimmed raw
  data actually used (runs end-to-end, no extra downloads); report ≤4 pages (factor
  definition/construction/rationale/audience; data description incl. return
  construction and cleaning; regression tables; sensitivity analysis; interpretation).
- LEARN Dropbox 1 hour before session: presentation slides.
- In class: 5–6 min presentation, every member present; ≥1 prepared question/comment
  on the paired group's project.

## Grading (15 pts)
Factor definition + rationale + audience: 2 | Data/factor/return construction +
cleaning: 2 | Regressions (coefs, t-stats, R²): 2 | Benchmark comparison: 1 |
Sensitivity (≥2 alternatives): 2 | Interpretation (rational/behavioral, efficiency,
audience): 2 | Reproducibility: 1 | Presentation: 2 | Peer review: 1
