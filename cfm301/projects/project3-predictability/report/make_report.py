"""Build report/report.pdf from the notebook's results.

The report follows docs/predictors.ipynb (Equity return predictability),
which reproduces the CFM301 Chapter 8 table from local submitted data
only. Its 'Predictor Data' files are not in this repo, so the tables
below are transcribed from the notebook's executed outputs into
outputs/notebook_*.csv (see README); the generator reads those CSVs, and
the slide-comparison tables are computed here from docs/slide_*.csv.
No number in this report comes from the earlier Shiller/FRED pipeline;
that pipeline's outputs (table_predict*.csv, table_compare_*.csv) are
superseded for the report and kept only as a cross-check.
"""
import os
import pandas as pd
from fpdf import FPDF

AUTHOR = "Jian"
OUT = "report/report.pdf"
os.makedirs("report", exist_ok=True)

main = pd.read_csv("outputs/notebook_main_table.csv", index_col=0)
audit = pd.read_csv("outputs/notebook_audit.csv", index_col=0)
missing = pd.read_csv("outputs/notebook_missing.csv", index_col=0)
vol = pd.read_csv("outputs/notebook_vol_predictability.csv")
buck = pd.read_csv("outputs/notebook_buckets.csv")
sub = pd.read_csv("outputs/notebook_sensitivity_subperiod.csv")
lag0 = pd.read_csv("outputs/notebook_sensitivity_lag0.csv", index_col=0)

HORIZONS = ("1Q", "1Y", "2Y", "5Y")
SLIDE_MAPS = [
    ("Valuation ratios", "docs/slide_block1_valuation.csv",
     {"Dividend yield": "Dividend yield",
      "Earnings yield": "Earnings yield"}),
    ("Business cycle and markets", "docs/slide_block2.csv",
     {"Term spread (10y-3m)": "Term spread (10y - 3m)",
      "Credit spread (BAA-AAA)": "Credit spread (BAA - AAA)",
      "Unemployment rate": "Unemployment rate",
      "GDP growth (past year)": "GDP growth (past year)",
      "Industrial production (past year)": "Industrial production (past year)",
      "Past 1-year return": "Past 1-year return",
      "Inflation (past year)": "Inflation (past year)",
      "Oil price (past-year change)": "Oil price (past-year change)",
      "Risk-free rate": "Risk-free rate"}),
    ("Risk and risk aversion", "docs/slide_block2_risk.csv",
     {"VIX": "VIX",
      "Past volatility (last quarter)": "Past volatility (last quarter)",
      "Consumption-wealth ratio": "Consumption-wealth ratio"}),
]


def fmt_corr_t(df, preds):
    """Render corr (t) cells; * marks |t| >= 2."""
    lines = []
    for p in preds:
        cells = []
        for h in HORIZONS:
            c, t = df.loc[p, f"corr_{h}"], df.loc[p, f"t_{h}"]
            star = "*" if abs(t) >= 2 else ""
            cells.append(f"{c:+.2f} ({t:+.2f}){star}")
        lines.append(f"{p:32s} " + "  ".join(cells))
    return lines


class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(110, 110, 110)
            self.cell(0, 6, "CFM301 Project 3: Reproducing the Equity Return "
                            "Predictability Table", align="R")
            self.ln(10)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def h1(self, text):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(31, 78, 121)
        self.cell(0, 8, text)
        self.ln(9)
        self.set_text_color(0, 0, 0)

    def h2(self, text):
        self.set_font("Helvetica", "B", 10.5)
        self.cell(0, 7, text)
        self.ln(8)

    def para(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def mono(self, lines):
        self.set_font("Courier", "", 8)
        for ln in lines:
            self.cell(0, 4.5, ln)
            self.ln()
        self.ln(2)


r = Report()
r.alias_nb_pages()
r.set_auto_page_break(auto=True, margin=15)
r.add_page()
r.set_font("Helvetica", "B", 16)
r.cell(0, 10, "CFM301 Project 3: Reproducing the Equity")
r.ln(11)
r.cell(0, 10, "Return Predictability Table")
r.ln(14)
r.set_font("Helvetica", "", 11)
r.cell(0, 7, f"Author: {AUTHOR}")
r.ln(12)

r.h1("1. Economic question and audience")
r.para("Question: does information available at month-end predict future "
       "market excess returns, and is that predictability still present "
       "after 2011? We reproduce the predictability table of Chapter 8 "
       "(slides 24-25 and the surrounding blocks): correlations and "
       "Newey-West t-statistics between each predictor's level today and "
       "future equity excess returns at 1-quarter, 1-year, 2-year and "
       "5-year horizons, extended to the longest sample the submitted "
       "data allow (1926-01 through 2026-10). The audience is "
       "pension-fund and other long-horizon asset-allocation managers "
       "deciding whether a valuation, business-cycle or risk signal "
       "justifies adjusting equity exposure. The market series is CRSP "
       "value-weighted total return (vwretd), not the ex-dividend "
       "return. Future returns overlap at longer horizons, so "
       "t-statistics use Newey-West/HAC covariance with horizon - 1 lags.")

r.h1("2. Data, construction and cleaning")
r.para("All results come from the submitted data used in "
       "docs/predictors.ipynb. Valuation ratios (annual dividend yield "
       "and earnings yield) come from market_data_full_history_2025.csv; "
       "market returns from Market_Dividends_Returns.csv (CRSP vwretd). "
       "Macro and financial predictors come from FRED files: GS10 and "
       "TB3MS (term spread = 10y - 3m), BAA and AAA (credit spread = "
       "BAA - AAA), CPIAUCSL inflation (past year), INDPRO growth (past "
       "year), UNRATE, GDPC1 growth (past year, quarterly series carried "
       "forward), DCOILWTICO oil-price change (past year), VIXCLS, and "
       "the 3-month T-bill rate. The consumption-wealth ratio is the "
       "Lettau-Ludvigson cay series as supplied (cay_current.csv, "
       "c - 0.218a - 0.801y + 0.441), with the quarterly series carried "
       "forward from the last observed quarter-end. All sources are "
       "converted to month-end dates and duplicate dates are removed "
       "before joining (0 duplicates removed). Excess returns are "
       "geometric: (1 + total return) / (1 + monthly T-bill rate) - 1, "
       "where the monthly rate is (1 + TB3MS/100)^(1/12) - 1. Past "
       "1-year return is the trailing 12-month compounded return; past "
       "volatility (last quarter) is the standard deviation of monthly "
       "returns over the last 3 months, annualized by sqrt(12) "
       "(correlation is scale-free, so annualizing changes nothing). "
       "Predictors are winsorized at the 1st and 99th percentiles "
       "within each usable estimation sample; returns are not "
       "winsorized. Future returns are overlapping compounded returns, "
       "(1 + r) rolled over h months, shifted forward by h months, "
       "minus 1. Each cell is an OLS regression of the future excess "
       "return on the predictor level, with a HAC t-statistic at "
       "horizon - 1 lags; |t| >= 2 is treated as significant.")
r.para("Missing values before estimation (months with no observation): "
       "oil 860, VIX 815, term spread 328, cay 314, unemployment 266, "
       "inflation 266, GDP 264, risk-free rate 97, past 1-year return "
       "33, past volatility 24, industrial production 13, dividend "
       "yield 10, earnings yield 10, credit spread 1. The gaps reflect "
       "series start dates (oil from 1986, VIX from 1990, quarterly "
       "series carried forward) and are handled by pairwise deletion, "
       "so each cell uses only months where both predictor and future "
       "return exist. Estimation sample sizes and winsorized counts:")
r.mono(["predictor                        1Q N/clip  1Y N/clip  "
        "2Y N/clip  5Y N/clip"] +
       [f"{p[:30]:30s} "
        f"{audit.loc[p, 'n_1Q']:>4d}/{audit.loc[p, 'clipped_1Q']:>2d}  "
        f"{audit.loc[p, 'n_1Y']:>4d}/{audit.loc[p, 'clipped_1Y']:>2d}  "
        f"{audit.loc[p, 'n_2Y']:>4d}/{audit.loc[p, 'clipped_2Y']:>2d}  "
        f"{audit.loc[p, 'n_5Y']:>4d}/{audit.loc[p, 'clipped_5Y']:>2d}"
        for p in audit.index])

r.h1("3. Main table: future excess returns (correlation, HAC t)")
r.mono(["predictor                        1Q              1Y              "
        "2Y              5Y"] + fmt_corr_t(main, list(main.index)))
r.para("* marks |t| >= 2. Valuation ratios are positive at every "
       "horizon and grow with horizon: dividend yield 0.11/0.25/0.34/"
       "0.53, earnings yield 0.09/0.21/0.27/0.42. Business-cycle signs "
       "are mostly as the slides predict (term spread and unemployment "
       "positive; GDP growth, industrial production, past return, "
       "inflation, oil and the risk-free rate negative), with oil and "
       "inflation the strongest negatives. Volatility on its own is "
       "weak (VIX 0.13-0.18, past volatility 0.05-0.12, significant only "
       "at 1 quarter for past volatility). cay is positive and "
       "significant from 1 year on (0.19/0.29/0.33, t = 2.01/2.44/2.16) "
       "but not at 1 quarter (0.09, t = 1.72).")

r.h1("4. Comparison with the slides")
for name, path, smap in SLIDE_MAPS:
    slide = pd.read_csv(path)
    lines, agree_n, agree_d = [], 0, 0
    for _, row in slide.iterrows():
        if row["predictor"] not in smap:
            continue
        c = smap[row["predictor"]]
        mc, mt = main.loc[c, f"corr_{row['horizon']}"], main.loc[c, f"t_{row['horizon']}"]
        agree_d += 1
        agree_n += int((row["corr"] * mc) > 0)
        lines.append(f"{row['predictor'][:24]:24s} {row['horizon']:3s} "
                     f"slide {row['corr']:+.2f} ({row['tstat']:+.2f})"
                     f"  vs  notebook {mc:+.2f} ({mt:+.2f})")
    r.h2(f"{name} (sign agreement {agree_n}/{agree_d})")
    r.mono(lines)
r.para("Overall sign agreement is 53 of 56 cells. Magnitudes are close "
       "for dividend yield (5-year 0.53 vs slide 0.49), term spread "
       "(0.38 vs 0.35), unemployment (0.22 vs 0.22) and credit spread at "
       "short horizons. Three gaps stand out. First, earnings yield is "
       "about 0.1 lower than the slides at every horizon "
       "(0.09/0.21/0.27/0.42 vs 0.18/0.33/0.41/0.48) -- and this notebook "
       "uses a different earnings source than the earlier Shiller-based "
       "pipeline, which gave nearly the same numbers (0.09/0.20/0.26/"
       "0.38), so the gap is not an artefact of one earnings series. "
       "Second, oil is about twice the slides' magnitude on monthly "
       "data (-0.34/-0.34 vs -0.18/-0.16 at 1Y/2Y); quarterly sampling "
       "closes most of that gap in the earlier pipeline, suggesting "
       "the slides use quarterly observations for this block. Third, "
       "cay is weaker here than in the slides (5-year 0.33 vs 0.53), "
       "the reverse of the earlier DOLS-reconstructed cay (0.67): the "
       "supplied cay series uses fixed Lettau-Ludvigson coefficients "
       "rather than re-estimated ones, and that choice matters for the "
       "level of cay predictability. VIX at 5 years flips sign "
       "(+0.13 vs slide -0.16) but is insignificant in both. The "
       "t-statistics here are generally larger than the slides' (for "
       "example dividend yield 5-year 3.87 vs 1.95), consistent with "
       "the slides using a more conservative standard-error "
       "construction; Section 8 shows how much the overlap correction "
       "itself matters.")

r.h1("5. Interpretation: the dividend discount model")
r.para("From class, P = D / (E(r) - g), so rearranging gives "
       "D/P = E(r) - g. Holding expected dividend growth g approximately "
       "constant, a high dividend yield means investors require a higher "
       "expected return. The same logic applies to the earnings yield: "
       "a high E/P means the price is low relative to the earnings the "
       "market generates, consistent with a higher required and expected "
       "future return. The extended table supports this prediction: "
       "dividend yield and earnings yield have positive correlations "
       "with future excess returns, and the correlations generally "
       "increase from one quarter to five years. Their post-2011 "
       "observations are included in the extended sample through the "
       "latest available market-return date (2026-10). Long-horizon "
       "predictability is stronger because valuation ratios move slowly "
       "while returns compound: a small difference in expected monthly "
       "returns accumulates over 12, 24 or 60 months, whereas one-quarter "
       "returns contain much more noise. The longer-horizon estimates "
       "should still be interpreted cautiously because overlapping "
       "observations reduce the effective sample size; the table "
       "therefore reports HAC t-statistics.")

r.h1("6. Five-bucket valuation analysis")
r.para("Following slides 26-28, observations are sorted into five "
       "equal-count buckets by dividend yield at time t. Q1 is the "
       "lowest-yield (most expensive) group and Q5 the highest-yield "
       "(cheapest) group. The table shows average compounded 1-year "
       "returns and average annualized 5-year returns with +/- 2 "
       "standard-deviation bands. These bands are dispersion bands, not "
       "confidence intervals.")
r.mono(["bucket       avg yield  1Y mean (SD)         5Y ann. mean (SD)   n"] +
       [f"{row['bucket']:11s}  {row['avg_ratio']:>7.2%}  "
        f"{row['r1_mean']:>6.2%} ({row['r1_sd']:>5.2%})  "
        f"{row['r5_mean']:>6.2%} ({row['r5_sd']:>5.2%})  "
        f"{int(row['n']):>3d}"
        for _, row in buck.iterrows()])
r.para("The cheapest bucket beats the most expensive bucket by a wide "
       "margin: 1-year 16.79% vs 3.91%, 5-year annualized 13.27% vs "
       "3.58%. But the middle buckets are not monotonic at 5 years "
       "(Q2 7.10% above Q3 4.70% and Q4 6.73%), and the +/- 2 SD bands "
       "overlap heavily across buckets (for example Q5 1-year 16.79% "
       "with SD 17.39%): even where mean returns differ, the "
       "distribution of outcomes within each bucket is wide. That is "
       "why a statistically visible correlation is still too weak to "
       "trade on aggressively -- the slides' verdict for the "
       "business-cycle block, and it applies to valuation timing too.")

r.h1("7. Returns versus volatility")
r.para("The slides emphasize that volatility is more predictable than "
       "returns. VIX at time t against annualized realized volatility "
       "over the following horizon gives:")
r.mono(["horizon  corr (HAC t)  n"] +
       [f"{row['horizon']:7s}  {row['corr']:+.2f} ({row['t']:+.2f})  "
        f"{int(row['n']):>3d}" for _, row in vol.iterrows()])
r.para("VIX predicts realized volatility up to 2 years (correlations "
       "0.29/0.38/0.30, all significant) but not at 5 years (-0.16, "
       "t = -1.04). A GARCH(1,1) model on monthly total returns tells "
       "the same story from the other side. Estimated by Gaussian "
       "quasi-maximum likelihood (returns x 100), h_t = omega + alpha "
       "r2_{t-1} + beta h_{t-1} gives omega = 0.7153, alpha = 0.1229 "
       "(ARCH response to new shocks) and beta = 0.8538 (GARCH "
       "persistence), persistence alpha + beta = 0.9767. Annualized "
       "GARCH volatility averages 17.09% (SD 7.27%) against next-quarter "
       "realized volatility averaging 13.92% (SD 10.93%), correlation "
       "0.487 over 1,186 months. This is a volatility forecast "
       "comparison, not a claim that volatility forecasts expected "
       "returns: volatility predicts itself, it does not predict "
       "returns, which is exactly the risk block's verdict.")

r.h1("8. Sensitivity analysis")
r.para("Two alternatives are reported. (1) Subperiods: 1926-1989, "
       "1990 onward, and 2012 onward (post-2011), for dividend yield, "
       "earnings yield and past volatility. (2) A less conservative "
       "overlap correction using HAC lag 0 instead of horizon - 1. The "
       "correlation estimates are unchanged by the lag choice; only "
       "inference changes.")
r.mono(["sample / predictor                1Q              1Y              "
        "2Y              5Y"] +
       [f"{row['sample'][:12]:12s} {row['predictor'][:22]:22s} "
        f"{row['corr_1Q']:+.2f} ({row['t_1Q']:+.2f})  "
        f"{row['corr_1Y']:+.2f} ({row['t_1Y']:+.2f})  "
        f"{row['corr_2Y']:+.2f} ({row['t_2Y']:+.2f})  "
        f"{row['corr_5Y']:+.2f} ({row['t_5Y']:+.2f})"
        for _, row in sub.iterrows()])
r.para("Dividend yield is strong in every era, including post-2011 "
       "(5-year 0.78 in 1926-1989, 0.69 in 1990 onward, 0.69 in 2012 "
       "onward, all significant) -- so the answer to the economic "
       "question is yes for dividend yield. Earnings yield is not: it "
       "is strong before 1990 (5-year 0.60, t = 3.17) but dead from "
       "1990 onward (5-year 0.03, t = 0.11) and insignificant post-2011 "
       "(0.29, t = 1.33). Past volatility is mostly insignificant, with "
       "one exception (post-2011 2-year 0.24, t = 2.16). The lag "
       "sensitivity shows why the overlap correction is decisive:")
r.mono(["predictor (HAC lag 0)            1Q              1Y              "
        "2Y              5Y"] +
       [f"{p[:28]:28s} "
        f"{lag0.loc[p, 'corr_1Q']:+.2f} ({lag0.loc[p, 't_1Q']:+.2f})  "
        f"{lag0.loc[p, 'corr_1Y']:+.2f} ({lag0.loc[p, 't_1Y']:+.2f})  "
        f"{lag0.loc[p, 'corr_2Y']:+.2f} ({lag0.loc[p, 't_2Y']:+.2f})  "
        f"{lag0.loc[p, 'corr_5Y']:+.2f} ({lag0.loc[p, 't_5Y']:+.2f})"
        for p in lag0.index])
r.para("With HAC lag 0, dividend yield's 5-year t-statistic is 19.51 "
       "instead of 3.87, and earnings yield's is 12.01 instead of 2.31. "
       "Ignoring the overlap would make nearly everything look "
       "significant; the horizon - 1 correction is what keeps the "
       "inference honest.")

r.h1("9. Conclusion and limitations")
r.para("Answer to the economic question: predictability survives "
       "extension to 2026-10 in the full sample -- the slides' table "
       "replicates at 53 of 56 sign cells. But the two valuation "
       "ratios diverge after 1990: dividend yield stays strong in "
       "every era including post-2011, while earnings yield does not. "
       "A long-horizon investor should therefore not treat 'valuation "
       "predicts returns' as one stable fact; it is a dividend-yield "
       "fact in recent decades, and even that comes with bucket bands "
       "wide enough to make aggressive timing unwise. The signals that "
       "survive every cut are dividend yield first and cay second "
       "(significant from 1 year on in the full sample, though weaker "
       "here than in the slides). Volatility alone fails as a return "
       "predictor in every cut, while predicting realized volatility "
       "itself up to 2 years. Limitations: the underlying 'Predictor "
       "Data' files are not in this repository, so the tables above "
       "are transcribed from the notebook's executed outputs rather "
       "than re-estimated here; the slides' exact sample window and "
       "return series are inferred rather than stated, which leaves "
       "the earnings-yield gap (about 0.1 at every horizon, present "
       "under two different earnings sources) and the oil magnitude "
       "gap unresolved; cay is the supplied fixed-coefficient series, "
       "not a re-estimated cointegrating residual, so its strength "
       "depends on that choice; and post-2011 long-horizon windows are "
       "short (n = 96 for 5-year) and episode-driven.")

r.output(OUT)
print(f"wrote {OUT}")
