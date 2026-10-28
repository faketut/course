# CFM301 Project 3: Reproducing the Equity Return Predictability Table

Reproduce the predictability table on slides 24-25 of Ch. 8 (Equities) --
correlations and t-statistics between each predictor and future equity
returns at 1-quarter, 1-year, 2-year and 5-year horizons -- extended to the
longest sample the data allow, and assess whether the extended-sample
results are consistent with the slides.

## Report basis (rewritten 2026-10-28)

The report (`report/report.pdf`, built by `report/make_report.py`) now
follows `docs/predictors.ipynb`, which reproduces the Chapter 8 table
from local submitted data only: market_data_full_history_2025.csv
(dividend/earnings yields), Market_Dividends_Returns.csv (CRSP vwretd),
FRED files, and cay_current.csv (fixed-coefficient Lettau-Ludvigson
cay), sample 1926-01 through 2026-10, geometric excess returns,
per-sample 1%/99% winsorization, HAC t-statistics at horizon - 1 lags.
The notebook's `Predictor Data` files are not in this repo, so the
report's tables are transcribed from the notebook's executed outputs
into `outputs/notebook_*.csv`.

## Headline result (notebook numbers)

The slides replicate in the full 1926-2026-10 sample (sign agreement
53/56; dividend yield 5-year 0.53 vs slide 0.49; cay 0.33 vs 0.53).
Dividend yield is strong in every era including post-2011 (5-year 0.69),
while earnings yield is strong pre-1990 (0.60) but dead from 1990 onward
(0.03) and insignificant post-2011. Volatility alone fails as a return
predictor while predicting realized volatility itself up to 2 years.
The earlier Shiller/FRED pipeline (below) gave nearly the same numbers
for most predictors -- notably the same earnings-yield gap vs the slides
-- so that gap is not an artefact of one earnings series. The earlier
pipeline's outputs (`outputs/table_predict*.csv`,
`outputs/table_compare_*.csv`) are superseded for the report and kept
only as a cross-check.

## Pipeline

- `src/build_predictors.py` -- FRED macro + Shiller valuation monthly panel
  (all series normalized to calendar month-end)
- `src/build_cay.py` -- Lettau-Ludvigson consumption-wealth ratio
  reconstructed by DOLS cointegration from FRED (PCND+PCES, TNWBSHNO,
  W209RC1, PCEPI, POPTHM)
- `src/predict.py` -- overlapping compounded future returns; correlation
  with Newey-West t-statistic via the standardized-OLS equivalence
- `run_project.py` -- main table (nominal + excess), slide comparisons,
  bucket analysis, GARCH(1,1) vs realized vol, sensitivities
  (subperiods, NW lag, winsor, VW/EW, quarterly sampling)
- `report/make_report.py` -- report PDF (author: Jian)
- `presentation/make_deck.py` -- slide deck

## Data

- Returns: `data/wrds_crsp_msi.csv` (CRSP msi via WRDS SAS Studio;
  vwretd/vwretx/ewretd/ewretx, 1926-01-30 to 2024-12-31). Note: the current
  crsp.msi date column is DATE, not caldt -- see docs/wrds_queries.sql.
- Predictors: FRED downloads in `data/fred_*.csv`, Shiller
  `data/shiller_ie_data.xls`, cay in `data/cay_monthly.csv`.
- Slide tables transcribed to `docs/slide_block1_valuation.csv`,
  `docs/slide_block2.csv` (business cycle), `docs/slide_block2_risk.csv`.

## Reproduce

```
.venv/bin/python src/build_predictors.py
.venv/bin/python src/build_cay.py
.venv/bin/python run_project.py
.venv/bin/python report/make_report.py
.venv/bin/python presentation/make_deck.py
```

## Outputs

`outputs/notebook_*.csv` holds the report's tables (main table, cleaning
audit, missing counts, VIX-to-realized-volatility diagnostic, buckets,
subperiod and HAC-lag-0 sensitivities), transcribed from
`docs/predictors.ipynb`. The earlier pipeline's `outputs/table_*.csv`
(Shiller/FRED, 1926-2024) remain as a cross-check.
`report/report.pdf`, `presentation/deck.pptx` (deck still reflects the
earlier pipeline's numbers).
