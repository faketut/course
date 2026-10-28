# CFM301 Project 3: Reproducing the Equity Return Predictability Table

Reproduce the predictability table on slides 24-25 of Ch. 8 (Equities) --
correlations and t-statistics between each predictor and future equity
returns at 1-quarter, 1-year, 2-year and 5-year horizons -- extended to the
longest sample the data allow (CRSP VWRETD 1926-2024), and assess whether
the extended-sample results are consistent with the slides.

## Headline result

The slides replicate in the full 1926-2024 sample (sign agreement 52/56 =
93%; dividend yield 5-year 0.47 vs slide 0.49; cay 0.67 vs 0.53). The
qualification is stability, not level: valuation predictability is
regime-dependent (dividend yield 5-year: 0.74 pre-1963, 0.18 in 1963-2011,
0.76 post-2011 on a short, episode-driven window). cay is the most robust
predictor; volatility alone fails in both samples, as the slides conclude.

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

`outputs/` holds the predictability tables (nominal + excess), slide
comparisons, bucket table, GARCH table, sensitivity table, sample-split
table and figures. `report/report.pdf`, `presentation/deck.pptx`.
