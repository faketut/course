"""Build report/report.pdf (max 4 pages) from outputs/ tables and figures."""
import os
import pandas as pd
from fpdf import FPDF

AUTHOR = "Jian"
OUT = "report/report.pdf"
os.makedirs("report", exist_ok=True)

clean = pd.read_csv("outputs/table_cleaning.csv", index_col=0)
qrets = pd.read_csv("outputs/table_quintile_rets.csv", index_col=0)
bench = pd.read_csv("outputs/table_benchmark.csv", index_col=0)
sens = pd.read_csv("outputs/table_sensitivity.csv", index_col=0)


class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(110, 110, 110)
            self.cell(0, 6, "CFM301 Project 2: Finding and Testing a Factor -- Earnings Yield",
                      align="R")
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
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4.6, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def table(self, df, col_widths=None, fmt="{:.4f}"):
        self.set_font("Helvetica", "B", 8)
        cols = [""] + list(df.columns)
        if col_widths is None:
            first = 34
            rest = (190 - first) / len(df.columns)
            col_widths = [first] + [rest] * len(df.columns)
        for w, c in zip(col_widths, cols):
            self.cell(w, 5.5, str(c), border=1, align="C")
        self.ln()
        self.set_font("Helvetica", "", 8)
        for idx, row in df.iterrows():
            self.cell(col_widths[0], 5.5, str(idx), border=1)
            for w, v in zip(col_widths[1:], row):
                try:
                    txt = fmt.format(float(v))
                except (ValueError, TypeError):
                    txt = str(v)
                self.cell(w, 5.5, txt, border=1, align="C")
            self.ln()
        self.ln(3)


pdf = Report(format="Letter")
pdf.alias_nb_pages()
pdf.set_margins(12, 12, 12)
pdf.set_auto_page_break(True, margin=15)

# ---------------- Page 1 ----------------
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)
pdf.multi_cell(0, 8, "Testing the Earnings-Yield Factor\nBeyond Market, Size, Value, and Momentum",
               new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
pdf.cell(0, 7, f"CFM301 Project 2  |  {AUTHOR}  |  October 2026")
pdf.ln(10)

pdf.h1("1. Proposed Factor & Motivation")
pdf.para(
    "I propose the earnings yield (E/P) factor: each month, sort stocks on trailing "
    "earnings yield -- TTM net income divided by market capitalization -- and hold "
    "a long-short portfolio that is long high-E/P (cheap) stocks and short low-E/P "
    "(expensive) stocks. The factor goes beyond the market, SMB, HML and UMD: it "
    "combines the value intuition of Basu (1977) with a profitability tilt, since "
    "E/P is high both when prices are depressed and when earnings are strong.")
pdf.para(
    "The idea is not armchair: five of my own WorldQuant BRAIN alphas (in-sample "
    "Sharpe 2.17-2.59, turnover 9-16%) are built on forward earnings yield -- "
    "analyst consensus EBIT / pre-tax-profit estimates scaled by market cap. This "
    "project tests the trailing, accounting-based analog on CRSP/Compustat, where "
    "no analyst-estimate history is publicly available. If the signal survives "
    "with stale accounting data, the economic mechanism is unlikely to be a "
    "data-mining artifact of one estimate vendor.")

pdf.h1("2. Data & Cleaning")
pdf.para(
    "CRSP monthly stock file (via WRDS SAS Studio), January 2000-December 2024: "
    "1,294,973 stock-months on 12,802 PERMNOs (share codes 10/11; NYSE/AMEX/Nasdaq). "
    "RET is the CRSP total return (dividends and splits included). Compustat "
    "quarterly fundamentals (1,247,280 firm-quarters) are linked via the CCM link "
    "table (33,324 links). Note: the WRDS CRSP vintage available ends December "
    "2024, so the sample is 2000-2024, not 2000-2026.")
pdf.para(
    "Point-in-time construction (no lookahead): for formation month-end t, TTM net "
    "income is the sum of niq over the latest four fiscal quarters whose report "
    "date (rdq) is on or before t; market cap is |PRC| x SHROUT x 1000 at t; "
    "EY = TTM net income / market cap. EY covers 86.9% of stock-months (the rest "
    "lack four quarters of filing history). Cleaning log:")
pdf.table(clean.reset_index().rename(columns={"index": "step"}).set_index("step"),
          col_widths=[62, 30, 98], fmt="{:.0f}")

# ---------------- Page 2 ----------------
pdf.add_page()
pdf.h1("3. Factor Construction & Test Assets")
pdf.para(
    "At each month-end t, stocks are sorted into quintiles on EY[t] and held "
    "during t+1; legs are equal-weighted and the factor is Q5 (high EY) minus Q1 "
    "(low EY). Test assets: (i) the five EY quintile portfolios themselves, and "
    "(ii) the Fama-French 25 Size-B/M portfolios. Benchmarks are the French "
    "factors (Mkt-RF, SMB, HML, RMW, CMA, UMD); models are CAPM, FF3 and FF5, "
    "plus a spanning regression of EY on FF5. All t-statistics are Newey-West.")
pdf.h2("EY quintile portfolios (annualized, 2001-2024)")
qt = qrets.rename(columns={"mean_ann": "Mean (%/yr)", "sharpe": "Sharpe",
                           "tstat_mean": "t(mean)",
                           "avg_mcap_$mm": "Avg mcap ($mm)"}).drop(
    columns=["vol_ann", "nobs"])
qt["Mean (%/yr)"] = qt["Mean (%/yr)"] * 100
pdf.table(qt, fmt="{:.2f}")
pdf.h1("4. Main Result")
pdf.para(
    "The EY factor earns 18.68% per year (Sharpe 1.03, Newey-West t = 4.13, "
    "n = 289 months). Returns are monotone in EY: the low-EY quintile earns "
    "-2.02%/yr while the high-EY quintile earns +16.65%/yr. In MKT+EY "
    "regressions the EY loadings are strongly monotone (Q1 beta_EY = -0.96, "
    "t = -19.7, rising through the quintiles) and average R^2 is 0.821 on the "
    "quintiles and 0.766 on the French 25. The cumulative return plot (Figure 1) "
    "shows steady compounding with drawdowns concentrated in recessions -- "
    "first visual evidence on the risk-vs-mispricing question of Section 7.")
pdf.image("outputs/fig_cumret.png", x=28, w=154)
pdf.ln(2)

# ---------------- Page 3 ----------------
pdf.add_page()
pdf.h1("5. Does EY Survive the Standard Benchmarks?")
pdf.para(
    "Adding EY to CAPM / FF3 / FF5 raises average R^2 across the 25 Size-B/M "
    "portfolios by 1.57 / 0.54 / 0.27 percentage points, with 10, 14 and 11 of "
    "25 portfolios showing significant EY loadings (|t| > 1.96). The spanning "
    "test is decisive: regressing EY on the five Fama-French factors leaves an "
    "alpha of 14.90%/yr (t = 5.11, R^2 = 0.50). Half of EY's variance is "
    "orthogonal to FF5 -- it is not repackaged value or profitability.")
pdf.h2("Sensitivity: premium under alternative assumptions")
st = sens.rename(columns={"mean_ann": "Mean (%/yr)", "sharpe": "Sharpe",
                          "tstat_mean": "t(mean)", "nobs": "n"})
st["Mean (%/yr)"] = st["Mean (%/yr)"] * 100
pdf.table(st, col_widths=[72, 28, 28, 30, 28], fmt="{:.2f}")
pdf.para(
    "The premium is robust to the COVID crash and across subperiods (strongest "
    "2010-2019 and 2020-2024), but two alternatives bite. Tercile sorts cut the "
    "premium to 4.2%/yr (t = 0.92, insignificant): the signal lives in the "
    "extremes, consistent with the microcap tilt in the quintile table (Q1 "
    "averages only $409mm market cap). Value-weighting the legs -- the "
    "implementable version -- halves the premium to 9.5%/yr (t = 1.80, "
    "marginally significant). The anomaly is real, but concentrated where "
    "arbitrage is hardest.")
pdf.image("outputs/fig_quintile_spread.png", x=38, w=134)
pdf.ln(2)

# ---------------- Page 4 ----------------
pdf.add_page()
pdf.h1("6. Rational vs. Behavioral Interpretation")
pdf.para(
    "Rational view: EY compensates for distress and earnings risk. High-EY firms "
    "are often cheap for a reason -- depressed prices reflect distress -- and "
    "the factor's drawdowns cluster in recessions (Figure 1), the signature of "
    "a risk premium earned in bad times. Counterpoint: the premium survives "
    "controls for market, size, value, profitability and investment (spanning "
    "alpha t = 5.11), so it is not the standard distress proxies doing the work.")
pdf.para(
    "Behavioral view: investors underreact to earnings information (post-earnings "
    "announcement drift) and overextrapolate past growth, leaving profitable "
    "cheap stocks underpriced -- especially neglected microcaps, where the "
    "premium is strongest and analyst coverage thinnest. The nonlinearity "
    "(quintiles work, terciles do not) fits mispricing better than a linear "
    "risk loading. My reading: both forces operate, with mispricing dominant "
    "in small caps and a distress-risk component in the drawdown pattern.")
pdf.h1("7. Market Efficiency & Takeaway")
pdf.para(
    "The evidence rejects the semi-strong form in its strictest sense -- public "
    "accounting data predicts returns -- but supports Grossman-Stiglitz "
    "near-efficiency: information is costly, so prices need not be perfect. "
    "Exactly where the premium is largest (microcaps, $409mm average in Q1), "
    "trading costs, illiquidity and short-sale constraints make arbitrage "
    "expensive; at implementable scale (value-weighted, t = 1.80) the market "
    "looks much closer to efficient. An anomaly that cannot be arbitraged at "
    "scale is, for most investors, indistinguishable from efficiency.")
pdf.para(
    "Intended audience: quantitative portfolio managers and pension funds "
    "evaluating factor products. The message is two-fold: (i) trailing earnings "
    "yield contains genuine orthogonal information -- it is not subsumed by "
    "FF5; (ii) the harvestable premium is far smaller than the headline "
    "18.7%/yr -- capacity, turnover and microcap costs must be modeled before "
    "allocating. Caveats: CRSP vintage ends 2024-12; delisting returns "
    "(crsp.msedelist) were not pulled, so distressed delisters are excluded -- "
    "this understates the short leg's losses and hence the reported premium; "
    "US equities only; single formation variable.")
pdf.h1("References & Packages")
pdf.set_font("Helvetica", "", 8.5)
for ref in [
    "Basu, S. (1977). Investment performance of common stocks in relation to their price-earnings ratios. Journal of Finance.",
    "Fama, E. and French, K. (2015). A five-factor asset pricing model. J. Financial Economics.",
    "Grossman, S. and Stiglitz, J. (1980). On the impossibility of informationally efficient markets. AER.",
    "Lakonishok, J., Shleifer, A. and Vishny, R. (1994). Contrarian investment, extrapolation, and risk. Journal of Finance.",
    "Python: pandas, numpy, statsmodels (Newey-West), matplotlib; report: fpdf2. Data: WRDS (CRSP/Compustat), Ken French library.",
]:
    pdf.multi_cell(0, 4.5, "- " + ref, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

pdf.output(OUT)
print(f"Wrote {OUT} ({pdf.page_no()} pages)")
