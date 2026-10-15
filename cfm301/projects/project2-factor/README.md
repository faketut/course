# CFM301 Project 2: Finding and Testing a Factor — Earnings Yield

**Economic question:** Does a trailing earnings-yield (E/P) factor earn a
premium beyond the market, SMB, HML and UMD — and does it survive the
Fama-French five-factor model?

**Headline result:** On CRSP/Compustat (2001–2024, n = 289 months), an
equal-weighted long-short EY factor (Q5 − Q1) earns **18.68%/yr**
(Sharpe 1.03, Newey-West t = 4.13). Spanning it on FF5 leaves
α = 14.90%/yr (t = 5.11, R² = 0.50): half its variance is orthogonal to
the standard factors. The premium is concentrated in small caps —
value-weighting cuts it to 9.5%/yr (t = 1.80).

## Reproduce end-to-end

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Build panels from the WRDS pulls -> data/monthly_panel.csv, data/ey_panel.csv
python src/wrds_build.py

# 2. Factor, regressions, benchmarks, sensitivity -> outputs/
python run_project.py

# 3. Build the report PDF -> report/report.pdf
python report/make_report.py

# 4. Build the presentation deck -> presentation/deck.pptx
python presentation/make_deck.py
```

Steps 2–4 run **without any downloads**: they read only the trimmed
`data/monthly_panel.csv` and `data/ey_panel.csv` checked into this repo.
Step 1 needs the three WRDS CSVs (`data/wrds_crsp_msf.csv`,
`data/wrds_comp_fundaq.csv`, `data/wrds_ccm_link.csv`); the SAS code that
produced them is in `docs/wrds_queries.sql`.

## Layout

| Path | Contents |
|---|---|
| `src/wrds_build.py` | CRSP/Compustat → monthly return + EY panels (point-in-time) |
| `src/regress.py` | OLS with Newey-West, premium stats, spanning test, winsorize |
| `run_project.py` | End-to-end analysis; writes `outputs/` |
| `docs/wrds_queries.sql` | SAS/SQL used on WRDS SAS Studio for the three pulls |
| `docs/project_brief.md` | Original project brief / design notes |
| `data/monthly_panel.csv` | Trimmed panel: date, permno ("ticker"), ret, price |
| `data/ey_panel.csv` | Trimmed panel: date, permno, ey, mcap, ttm_ni |
| `data/french_*.csv` | Ken French factors + 25 Size-B/M portfolios (public) |
| `outputs/` | Factor series, tables, figures (generated) |
| `report/report.pdf` | 4-page project report (generated) |
| `presentation/deck.pptx` | 5–6 minute presentation deck (generated) |

## Method (summary)

- **Factor:** at each month-end t, sort stocks into quintiles on trailing
  EY[t] = TTM net income / market cap; hold equal-weighted legs during t+1;
  factor = Q5 (high EY) − Q1 (low EY).
- **Point-in-time:** TTM NI sums the latest four quarters with report date
  `rdq ≤ t`; market cap = |PRC| × SHROUT × 1000 at t. `"ticker"` holds the
  CRSP PERMNO (unique per date, unlike recycled exchange tickers).
- **Test assets:** (i) the five EY quintiles, (ii) French 25 Size-B/M.
  Benchmarks: Mkt-RF, SMB, HML, RMW, CMA, UMD; models CAPM / FF3 / FF5 +
  spanning regression of EY on FF5. All t-stats Newey-West.
- **Sensitivity:** tercile sorts; value-weighted legs; subperiods
  2002–09 / 2010–19 / 2020–24; excluding Mar–Apr 2020.
- **Motivation:** five of the author's own WorldQuant BRAIN alphas
  (in-sample Sharpe 2.17–2.59) trade *forward* earnings yield
  (analyst EBIT/PTP estimates ÷ market cap); this project tests the
  *trailing* accounting analog.

## Data notes

- The WRDS CRSP vintage available ends **December 2024**, so the sample is
  2000–2024 (factor from 2001, n = 289), not 2000–2026.
- Delisting returns (`crsp.msedelist`) were not pulled: firms delisting
  during the holding month are excluded. Distressed delisters cluster in the
  low-EY leg, so this *understates* the short leg's losses and the reported
  premium is conservative on this dimension — before trading costs, which
  would erode the microcap-tilted paper premium substantially.
- `docs/wrds_queries.sql` also records two schema lessons: `crsp.msf` has no
  ticker/shrcd/exchcd (join `crsp.msenames` on name effective dates), and the
  quarterly file is `comp.fundq` (not `comp.fundaq`).
- An earlier Yahoo Finance / SEC EDGAR proxy pipeline (`src/data.py`,
  `src/factors.py`) validated the code end-to-end before WRDS access; the
  WRDS panels supersede it.
