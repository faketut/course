"""Build report/report.pdf (max 4 pages) for CFM301 Project 5.

Reads outputs/*.csv produced by run_project.py; no number is typed
by hand into the tables below - every cell comes from the CSVs.
"""
import os
import pandas as pd
from fpdf import FPDF

AUTHOR = "Jian"
OUT = "report/report.pdf"
os.makedirs("report", exist_ok=True)

facts = pd.read_csv("outputs/table_fund_facts.csv")
alphas = pd.read_csv("outputs/table_alphas.csv")
bench = pd.read_csv("outputs/table_benchmark.csv")
pers = pd.read_csv("outputs/table_persistence.csv")
subs = pd.read_csv("outputs/table_subperiods.csv")
wins = pd.read_csv("outputs/table_winsor.csv")
roll = pd.read_csv("outputs/table_rolling_summary.csv", index_col=0)
feep = pd.read_csv("outputs/table_fee_perf.csv")
info = pd.read_csv("data/fund_info.csv", index_col="ticker")

ACTIVE = ["FCNTX", "FMAGX", "AGTHX", "PRGFX", "TRBCX"]


def a4(ticker, model, basis):
    r = alphas[(alphas.ticker == ticker) & (alphas.model == model)
               & (alphas.basis == basis)].iloc[0]
    return r["alpha_ann_pct"], r["t_alpha"], r["te_ann_pct"], r["ir"], r["r2"]


class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(110, 110, 110)
            self.cell(0, 6, "CFM301 Project 5: Are the Fees Justified?", align="R")
            self.ln(10)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def h1(self, text):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, text)
        self.ln(9)

    def h2(self, text):
        self.set_font("Helvetica", "B", 10.5)
        self.cell(0, 7, text)
        self.ln(8)

    def para(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def mono(self, lines):
        self.set_font("Courier", "", 7.8)
        for ln in lines:
            self.cell(0, 4.15, ln)
            self.ln()
        self.ln(1)


r = Report()
r.alias_nb_pages()
r.set_auto_page_break(auto=True, margin=15)
r.set_margins(19, 15, 19)
r.add_page()

r.set_font("Helvetica", "B", 16)
r.cell(0, 10, "CFM301 Project 5: Are the Fees Justified?")
r.ln(11)
r.set_font("Helvetica", "", 11)
r.cell(0, 7, f"Author: {AUTHOR}    Sample: January 1994 - December 2024 (371 months)")
r.ln(9)

r.h1("1.  Question and audience")
r.para("A retail investor choosing a US large-cap growth fund pays 0.58-0.74% a year "
       "for active management against about 0.14% for an index fund. Is the fee "
       "justified? Following Wermers (2000) and Fama and French (2010), a fee is "
       "justified if the fund's gross-of-fee alpha is large enough that its "
       "net-of-fee alpha is non-negative - that is, if the manager's skill, "
       "measured against factor benchmarks and against a portfolio of cheap "
       "index funds an investor could actually buy, covers what the manager "
       "charges. This report is written for that investor and for advisers who "
       "recommend these funds.")

r.h1("2.  Data and sample")
r.para("Five actively managed US large-cap growth funds, one flagship retail "
       "share class each (the class a retail investor actually buys; "
       "fund-level asset-weighting would mix A, C and institutional fee "
       "structures), plus three Vanguard index funds used as the implementable "
       "benchmark. The sample starts in January 1994, the first full year all "
       "eight funds exist, and ends in December 2024 (372 months of prices, "
       "371 monthly returns).")
lines = ["Ticker  Fund                                        Fee%  Turn%  TNA$b  AnnRet% AnnVol% Sharpe",
         "------  ------------------------------------------  ----  -----  -----  ------- ------- ------"]
for _, row in facts.iterrows():
    lines.append(f"{row['ticker']:<7} {row['fund'][:42]:<42}  {row['fee_pct']:4.2f}  "
                 f"{row['turnover_pct']:5.1f}  {row['tna_usd_bn']:5.1f}  "
                 f"{row['ann_ret_pct']:7.2f} {row['ann_vol_pct']:7.2f} {row['sharpe']:6.2f}")
lines.append("Fees, turnover and TNA are current (prospectuses / fund-company fact")
lines.append("sheets, Nov 2026). AnnRet/AnnVol/Sharpe are 1994-2024, total returns.")
r.mono(lines)
r.para("Data sources and the WRDS problem. The brief asks for the CRSP Mutual "
       "Fund Database via WRDS. This account is not authorized for the CRSP "
       "mutual-fund files (CRSP.FUND_SUMMARY / CRSP.FUND_HDR return an SAS "
       "authorization error; the CRSP stock files work, the fund files do not), "
       "and the authorization has to be enabled by the professor or WRDS "
       "administrator. Returns therefore come from Yahoo Finance adjusted "
       "closes (distributions reinvested, loads excluded, net of expenses). "
       "They were validated against Zacks annual total returns: for FMAGX, "
       "2016-2024 agree within 0.15 percentage points in every year. Factor "
       "returns are Ken French's Mkt-RF, SMB, HML, UMD and RF. Expense ratios "
       "are treated as constant at their current prospectus values (they do "
       "vary: FMAGX ran 0.49-0.83% over 2016-2026, TRBCX 0.68-0.72%), so gross "
       "alpha uses the current fee. A time-varying-fee check (Zacks annual "
       "fees, 2016-2024) moves gross alphas by at most 0.014pp, and no verdict "
       "changes. TNA history is "
       "unavailable without CRSP, so fund flows cannot be estimated (Section 5).")
r.para("Cleaning. No missing months and no duplicates in any fund (372 of 372 "
       "months). Monthly fund excess returns are winsorized at the 1st/99th "
       "percentiles as the baseline, which clips 8 months per fund (2.2%); "
       "Section 5 shows the no-winsorize and 5/95 alternatives. Excess returns "
       "are fund total return minus RF; gross returns add the expense ratio / 12 "
       "each month and the regressions are re-run, so gross alpha is exact, not "
       "net alpha plus the fee.")

r.h1("3.  Factor alphas: skill exists, but it is not large")
r.para("Table 1 reports annualized alpha (OLS t-statistic), tracking error "
       "(residual standard deviation) and information ratio under CAPM, the "
       "Fama-French 3-factor model and Carhart 4-factor model, net and gross "
       "of fees.")
lines = ["Table 1. Annualized alpha (%/yr), t in parentheses; TE = tracking error (%/yr).",
         "        CAPM net      FF3 net       Carhart net   Carhart gross  TE    IR    R2",
         "        alpha (t)     alpha (t)     alpha (t)     alpha (t)"]
for t in ACTIVE:
    c = a4(t, "CAPM", "net"); f = a4(t, "FF3", "net"); k = a4(t, "Carhart", "net")
    g = a4(t, "Carhart", "gross")
    lines.append(f"{t:<7} {c[0]:5.2f} ({c[1]:5.2f})  {f[0]:5.2f} ({f[1]:5.2f})  "
                 f"{k[0]:5.2f} ({k[1]:5.2f})  {g[0]:5.2f} ({g[1]:5.2f})  "
                 f"{k[2]:4.2f}  {k[3]:4.2f}  {k[4]:.2f}")
r.mono(lines)
r.image("outputs/fig_alpha_net_gross.png", x=19, w=172)
r.para("Four of the five funds earn a positive net Carhart alpha over the full "
       "31 years, three of them significant: FCNTX +2.38% (t = 2.59), AGTHX "
       "+1.81% (t = 2.23) and TRBCX +1.83% (t = 2.20); PRGFX +1.01% (t = 1.16) "
       "is positive but insignificant, and FMAGX -0.50% (t = -0.62) is negative. "
       "Gross alphas are 0.14-3.12%: every fund except FMAGX more than covers "
       "its fee before fees, and FMAGX barely breaks even gross (0.14%). "
       "Tracking errors are 4.4-5.0%/yr, so information ratios are 0.41-0.48 "
       "for the three significant funds - real but modest skill, not the "
       "1.0+ of a great hedge fund. R2 of 0.87-0.93 shows the factors explain "
       "most of the variation; the alpha is not a disguised beta.")
r.para("Why alpha changes as factors are added. Adding SMB and HML raises "
       "alpha for every fund except FMAGX (FCNTX 3.45% to 3.71%, AGTHX 1.32% "
       "to 1.75%): these are growth funds with negative HML loadings (-0.08 "
       "to -0.22), and value earned a positive premium over the sample "
       "(HML 1.35%/yr), so the growth tilt was a headwind the CAPM ignores. "
       "Adding momentum lowers FCNTX's alpha from 3.71% to 2.38% - its UMD "
       "loading is 0.16 against a 4.43%/yr momentum premium, and the other "
       "loadings shift as well - and leaves the others almost unchanged "
       "(UMD loadings near zero). The factor model matters: "
       "a CAPM-only verdict would overstate FCNTX's skill by half.")
r.para("One check on the machinery: the three index funds' own Carhart alphas "
       "are NAESX -0.08% and VIVAX -0.06% (both insignificant, close to minus "
       "their 0.17% fees), as they should be. VFINX is +0.63% (t = 1.88): the "
       "S&P 500 is a committee-selected, profitability-tilted 500 stocks, not "
       "the whole market, and Carhart has no profitability factor, so part of "
       "every fund's alpha is this same tilt. Read the alphas against that "
       "0.63% benchmark, not against zero.")

r.h1("4.  Against a portfolio an investor could actually buy")
r.para("Factor alpha is not the whole test: an investor can buy the factors "
       "cheaply. Table 2 regresses each fund's excess returns on the three "
       "Vanguard index funds with loadings constrained to be non-negative and "
       "to sum to one, so the benchmark is a portfolio the investor could hold. "
       "Alpha is the mean return over that replicating portfolio.")
lines = ["Table 2. Implementable index-fund benchmark (weights sum to 1, >= 0).",
         "        Bench alpha   t     TE    R2    w500  wSmall wValue BenchFee FeeGap",
         "        (%/yr)              (%/yr)"]
for _, row in bench.iterrows():
    lines.append(f"{row['ticker']:<7} {row['alpha_ann_pct']:6.2f}  {row['t_alpha']:5.2f}  "
                 f"{row['te_ann_pct']:4.2f}  {row['r2']:.2f}  {row['w_VFINX']:.2f}  "
                 f"{row['w_NAESX']:.2f}   {row['w_VIVAX']:.2f}   {row['bench_fee_pct']:.2f}   "
                 f"{row['fee_gap_pct']:.2f}")
r.mono(lines)
r.para("The replicating portfolio is 70-95% S&P 500 plus 5-30% small-cap and "
       "no value fund at all - exactly the growth tilt these funds hold - and "
       "it costs 0.14-0.15%/yr against the active funds' 0.58-0.74%. Against "
       "it, no fund's alpha is significant: FCNTX +1.80% (t = 1.56), AGTHX "
       "+1.01% (t = 1.07), TRBCX +1.31% (t = 1.34), PRGFX +0.43% (t = 0.41) "
       "and FMAGX -0.59% (t = -0.71). The point estimates cover the 0.43-0.60pp "
       "fee gap for four funds, but the tracking errors (4.6-6.4%/yr) are too "
       "large for 31 years to certify that. This is the honest headline: the "
       "managers beat the factor model, but they do not significantly beat a "
       "cheap portfolio that copies their style.")
r.para("Fees in context. Morningstar's 2024 US Fund Fee Study puts the "
       "asset-weighted average expense ratio at 0.34% for all funds, 0.60% "
       "for active US equity funds and 0.11% for passive funds (ICI, March "
       "2026: equity mutual funds 0.40%, index equity ETFs 0.14%). Our five "
       "funds (0.58-0.74%) sit at or just above the active average and 4-5 "
       "times the passive average - but below the large-growth category "
       "average of about 0.80-0.89%. They are expensive funds only relative "
       "to index funds, not relative to their peers. Across the five funds, "
       "the fee is not what predicts performance: corr(fee, gross alpha) = "
       "0.42, while corr(turnover, gross alpha) = -0.82. FMAGX trades the "
       "most (54% turnover) and has the worst alpha; TRBCX trades the least "
       "(18%) and has one of the best. With n = 5 this is descriptive, not a "
       "regression result, but it points the same way Carhart (1997) did: "
       "trading costs, not the headline fee, are where the money leaks.")
r.para("Verdicts. FCNTX: justified - net alpha +2.38%, significant, and the "
       "largest gross alpha (3.12%). AGTHX: justified on the full sample "
       "(+1.81%, significant) with the lowest fee (0.58%). TRBCX: justified "
       "(+1.83%, significant; lowest turnover). PRGFX: borderline - positive "
       "but insignificant on every test. FMAGX: not justified - negative net "
       "alpha, the only negative benchmark alpha, and the highest turnover. "
       "Every verdict is a full-sample verdict; Section 5 shows they do not "
       "all survive the second half of the sample.")

r.h1("5.  Persistence, sensitivity and flows")
r.para("Persistence. Splitting the sample in half, every fund's Carhart net "
       "alpha falls, by 2.0-4.3pp. In 1994-2009 all five are positive "
       "(AGTHX +3.64%, t = 2.75; TRBCX +2.33%, t = 2.57) and in 2010-2024 "
       "none is: FCNTX +0.44% (t = 0.45), FMAGX -2.34% (t = -2.49, "
       "significantly negative), AGTHX -0.64%, PRGFX -0.96%, TRBCX -0.23%. "
       "The Spearman rank correlation of the five alphas across halves is "
       "0.70 (p = 0.19, n = 5): the ranking mostly survives, the level does "
       "not. The same decay shows in thirds (2015-2024 alphas: +0.95, -1.37, "
       "+0.04, -0.40, +0.39%, none significant) and in rolling 36-month "
       "alphas, which are significant in only 6-15% of windows and end the "
       "sample at +2.50, -1.67, -0.02, -1.60 and +1.58%.")
r.image("outputs/fig_rolling_alpha.png", x=19, w=172)
r.para("Sensitivity. Winsorizing matters for magnitudes but not for the "
       "story, with one exception. Net Carhart alpha under no winsorizing / "
       "1-99 / 5-95: FCNTX 1.83 / 2.38 / 3.87, FMAGX -1.35 / -0.50 / +0.61, "
       "AGTHX 1.35 / 1.81 / 2.69, PRGFX 0.52 / 1.01 / 1.57, TRBCX 1.13 / 1.83 / "
       "2.38. Clipping crash months (2008, 2020, 2022) lifts every alpha, and "
       "at 5/95 FMAGX flips sign - its 'not justified' verdict is the only "
       "one that is not robust to the cleaning choice, because its worst "
       "months are also its most informative ones.")
r.para("Flows and Berk and Green (2004). The brief asks for flows from TNA: "
       "flow(t) = TNA(t) - TNA(t-1) x (1 + r(t)), related to past 1-year "
       "returns. This cannot be done here: TNA history exists only in the "
       "CRSP mutual-fund files this account cannot access, and no public "
       "source carries 31 years of monthly TNA for these funds. What can be "
       "said is the Berk and Green mechanism, and the data fit it: the "
       "five funds' early alphas are exactly what attracts flows, all five "
       "are now giants ($34bn to $351bn), and their alphas have decayed to "
       "zero or below as assets grew - decreasing returns to scale doing "
       "its work. The persistence result is the flow result, seen from the "
       "other side: investors chased the past returns, and the past returns "
       "stopped repeating. With TNA data, the next step would be to test "
       "whether flows respond to past 12-month returns and whether the "
       "largest inflows precede the largest alpha declines.")
r.para("Fee design. The results argue against paying for stock selection at "
       "these fees and against rewarding trading: the fee that survives is a "
       "low flat fee, or a fulcrum (symmetric performance) fee measured "
       "against a factor benchmark rather than a raw index - the 1940 Act "
       "requires symmetry, and a raw-index fulcrum would pay the manager for "
       "the growth tilt, which the investor can buy for 0.14%. Contrafund "
       "already has a performance-adjusted management fee (plus or minus "
       "0.20% against its index); the evidence here says the adjustment "
       "should be larger and benchmarked on the replicating portfolio in "
       "Table 2, not on the S&P 500. For the investor, the default should be "
       "the replicating portfolio itself: 85% S&P 500 plus 15% small-cap "
       "buys the style these funds hold, at 0.14%, and four of five managers "
       "could not significantly beat it in 31 years.")
r.para("Caveats. First and largest: survivorship and selection. These are "
       "five of the most famous surviving funds in the industry, picked "
       "because they are still alive and well known in 2024; Fama and "
       "French (2010) find the average fund's net alpha is about minus its "
       "fee, and these results say nothing about the average fund. Second, "
       "fees are held constant at current values and loads are excluded - "
       "AGTHX's 5.75% front load would cut a lump-sum investor's return "
       "further. Third, returns are Yahoo adjusted closes, not CRSP; they "
       "were validated, but a CRSP pull would still be the first robustness "
       "check if WRDS access is enabled. Fourth, the 1994 start conditions "
       "on 31 years of survival; a fund that died in 2008 is not in the "
       "sample, by construction.")
r.para("References. Berk, J. and R. Green (2004), Mutual fund flows and "
       "performance in rational markets, Journal of Political Economy 112. "
       "Carhart, M. (1997), On persistence in mutual fund performance, "
       "Journal of Finance 52. Fama, E. and K. French (2010), Luck versus "
       "skill in the cross-section of mutual fund returns, Journal of "
       "Finance 65. Wermers, R. (2000), Mutual fund performance, Journal of "
       "Finance 55. Morningstar (2025), US Fund Fee Study 2024. Investment "
       "Company Institute (2026), Mutual fund and ETF fees remained near "
       "historic lows in 2025. French, K., Data Library (factors). "
       "CFM301 Chapter 15 slides.")
r.para("Reproducibility. run_project.py (Python 3.12, pandas / numpy / "
       "scipy / statsmodels) reads only files in data/ and writes every "
       "number in this report to outputs/*.csv; report/make_report.py builds "
       "this PDF from those CSVs. Data files are trimmed to 1994-2024 and "
       "included in the submission.")

r.output(OUT)
print(f"pages: {r.pages_count}, wrote {OUT}")
