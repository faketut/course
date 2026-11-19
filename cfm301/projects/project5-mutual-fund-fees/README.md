# CFM301 Project 5 — Are the Fees Justified?

Five actively managed US large-cap growth funds (FCNTX, FMAGX, AGTHX,
PRGFX, TRBCX), one flagship retail share class each, 1994-01 to 2024-12
(371 monthly returns). Question: is each fund's fee justified, i.e. is
its gross-of-fee alpha large enough that its net-of-fee alpha is
non-negative? Tests: CAPM / Fama-French 3-factor / Carhart 4-factor
alphas (net and gross), alpha against a constrained index-fund
benchmark (loadings >= 0, sum to 1), fee vs performance, persistence
and flows, sensitivity analysis, and a fee-design recommendation.

## Headline results (net Carhart alpha, %/yr, 1994-2024)

| Fund | Fee | Net alpha (t) | Gross alpha | Benchmark alpha (t) | Verdict |
|------|-----|---------------|-------------|---------------------|---------|
| FCNTX | 0.74% | +2.38 (2.59) | 3.12 | +1.80 (1.56) | justified |
| FMAGX | 0.64% | -0.50 (-0.62) | 0.14 | -0.59 (-0.71) | not justified |
| AGTHX | 0.58% | +1.81 (2.23) | 2.39 | +1.01 (1.07) | justified |
| PRGFX | 0.66% | +1.01 (1.16) | 1.67 | +0.43 (0.41) | borderline |
| TRBCX | 0.70% | +1.83 (2.20) | 2.53 | +1.31 (1.34) | justified |

No fund's benchmark alpha is significant. Every fund's alpha fell from
1994-2009 to 2010-2024 (by 2.0-4.3pp); in 2010-2024 none is significant
and FMAGX is -2.34% (t = -2.49). See report/report.pdf (4 pages) for
the full analysis.

## Data — and the WRDS problem

The brief asks for the CRSP Mutual Fund Database via WRDS. **This WRDS
account is not authorized for the CRSP mutual-fund files**: on
2026-11-19, SAS Studio returned `ERROR: User does not have appropriate
authorization level for file CRSP.FUND_SUMMARY.DATA` (same for
CRSP.FUND_HDR). Sign-in and Duo worked; the code was correct. The
authorization has to be enabled by the professor or a WRDS
administrator. The queries that were run are in `docs/wrds_queries.sql`.

Fallback used instead (all documented in the report):

- **Returns**: Yahoo Finance adjusted closes (distributions reinvested,
  loads excluded, net of expenses), monthly, 1994-01 to 2024-12, all 8
  funds, 0 missing months. Validated against Zacks annual total
  returns: FMAGX 2016-2024 agrees within 0.15pp in every year.
  Files: `data/fund_prices_monthly.csv`, `data/fund_returns_monthly.csv`.
- **Factors**: Ken French Mkt-RF, SMB, HML, UMD, RF (already in
  decimals — do NOT divide by 100; see the bug note below),
  `data/french_factors_monthly.csv` (copied from Project 2).
- **Fees / turnover / TNA**: current prospectus values and fund-company
  fact sheets (Nov 2026), `data/fund_info.csv`. Fees are held constant
  at current values (they do vary: FMAGX 0.49-0.83% over 2016-2026).
- **Fee distribution**: Morningstar 2024 US Fund Fee Study (all funds
  0.34%, active US equity 0.60%, passive 0.11% asset-weighted) and ICI
  (equity mutual funds 0.40% in 2025, index equity ETFs 0.14%).
- **TNA history**: unavailable without CRSP, so **fund flows cannot be
  estimated**. The report discusses Berk & Green (2004) on the
  persistence evidence instead (Section 5).

If WRDS mutual-fund access is enabled later, replace
`data/fund_returns_monthly.csv` with CRSP `mret` (plus `exp_ratio`,
`mtna`, `turn_ratio` from `crsp.fund_summary`), keep the same
tickers/sample, and re-run: the pipeline, report and deck regenerate
unchanged. Flows can then be computed as
flow(t) = TNA(t) - TNA(t-1) x (1 + r(t)).

## How to run

```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy scipy statsmodels matplotlib fpdf2 python-pptx
.venv/bin/python run_project.py            # -> outputs/*.csv
.venv/bin/python report/make_figures.py    # -> outputs/fig_*.png
.venv/bin/python report/make_report.py     # -> report/report.pdf (4 pages)
.venv/bin/python presentation/make_deck.py # -> presentation/deck.pptx (7 slides)
```

Everything runs offline on the files in `data/`; no WRDS login, no
internet. `run_project.py` prints the cleaning counts, the persistence
Spearman rho and the fee/turnover correlations.

## Method (one paragraph)

Excess returns are fund total return minus RF, winsorized at 1/99
(baseline; 8 months clipped per fund; none and 5/95 as sensitivity).
Gross returns add the expense ratio / 12 each month and the
regressions are re-run, so gross alpha is exact. Annualized alpha =
monthly x 12; tracking error = residual std x sqrt(12); information
ratio = alpha / tracking error; OLS t-statistics. The implementable
benchmark regresses each fund's excess returns on the three Vanguard
index funds' excess returns (SLSQP, loadings >= 0, sum to 1); alpha is
the mean return over the replicating portfolio, with a tracking-error
t-statistic. Persistence uses Carhart net alpha in 1994-2009 vs
2010-2024 plus Spearman rank correlation.

## Fee sensitivity (time-varying expense ratios)

The main analysis adds back a constant fee (current prospectus value).
Zacks publishes annual expense ratios back to 2016
(`data/zacks_fees_annual.csv`, read from Zacks /performance pages
2026-11-19; 2016-2026, 55 rows, no gaps). `src/fee_sensitivity.py`
re-runs the gross Carhart alpha with time-varying fees (Zacks annual
fee / 12 for 2016-2024, current fee before 2016; everything else
identical). Result (`outputs/table_fee_sensitivity.csv`): full-sample
gross alpha moves by at most **0.014pp** (FCNTX 3.115% -> 3.104%,
FMAGX 0.136% -> 0.146%, AGTHX 2.393% -> 2.407%, PRGFX 1.674% ->
1.672%, TRBCX 2.527% -> 2.526%); on the 2016-2024 window alone, where
every month uses a Zacks fee, the largest move is **0.047pp**. No
verdict changes. The constant-fee shortcut is harmless because the
five funds' fees barely move (2016-2024 averages 0.63-0.70% vs current
0.58-0.74%) and the sample-average fee is what matters for gross alpha.

## Bug note (do not repeat)

The French factor file is in **decimals** (e.g. Mkt-RF = 0.0508 in
1963-08). An early version of `run_project.py` divided it by 100,
which nearly zeroed RF and inflated every alpha by mean(RF)
(~2.35%/yr): FCNTX's Carhart net alpha printed +4.67% instead of
+2.38%, and VFINX printed +2.92% instead of +0.63%. Caught by the
index-fund check (an S&P 500 fund's alpha must be about minus its
0.14% fee; NAESX and VIVAX now print -0.08% and -0.06%). The fix is
in `run_project.py` with a comment; the corrected tables were
regenerated 2026-11-19.

## Files

- `run_project.py` — full pipeline (data -> outputs/*.csv)
- `src/fund_analysis.py` — factor regression, constrained benchmark, winsorizing
- `data/` — trimmed data only (prices, returns, factors, fund info)
- `outputs/` — all tables + figures (regenerated by run_project.py)
- `report/` — make_report.py, make_figures.py, report.pdf
- `presentation/` — make_deck.py, deck.pptx
- `docs/` — fund_selection.md (fund choice + justification), wrds_queries.sql
