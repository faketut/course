"""Project 5: Are mutual fund fees justified? (CFM301)

Data (see README for sources and the WRDS fallback note):
- data/fund_returns_monthly.csv : Yahoo Finance adjusted-close total
  returns, 8 funds, 1994-01..2024-12 (372 months of prices -> 371 returns).
- data/french_factors_monthly.csv : Ken French 5 factors + UMD + RF.
- data/fund_info.csv : current expense ratios / turnover / TNA from
  fund prospectuses and fund-company fact sheets (Nov 2026).

Method
- Excess returns = fund total return - RF. Winsorize monthly fund
  excess returns at the 1st/99th percentiles (baseline); report the
  number of months clipped per fund. Sensitivity: no winsorizing, 5/95.
- Factor alphas: OLS, CAPM / FF3 / Carhart 4, net and gross.
  Gross returns = net returns + expense ratio / 12 (expense ratio
  treated as constant at its current prospectus value; see README).
  Annualized alpha = monthly x 12; tracking error = residual std
  x sqrt(12); information ratio = alpha / tracking error.
- Implementable benchmark: regress each fund's excess returns on the
  three Vanguard index funds' excess returns, loadings >= 0 and
  summing to 1 (SLSQP); alpha = mean return over the replicating
  portfolio, t-statistic from its tracking error.
- Persistence: Carhart net alpha in two halves, 1994-2009 / 2010-2024,
  plus Spearman rank correlation of the five alphas.
- Sensitivity: rolling 36-month Carhart alphas; three sub-periods;
  winsorization cut-offs.
- Flows: TNA history is unavailable without CRSP/WRDS mutual-fund
  authorization (see README); the flow-return relation cannot be
  estimated from available data. This script records the current-TNA
  snapshot only and the report discusses Berk & Green (2004) on the
  persistence evidence plus the published literature.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.fund_analysis import winsorize, factor_reg, constrained_benchmark

ACTIVE = ["FCNTX", "FMAGX", "AGTHX", "PRGFX", "TRBCX"]
INDEX = ["VFINX", "NAESX", "VIVAX"]
MODELS = {
    "CAPM": ["Mkt_RF"],
    "FF3": ["Mkt_RF", "SMB", "HML"],
    "Carhart": ["Mkt_RF", "SMB", "HML", "UMD"],
}

# ---------------------------------------------------------------- load
rets = pd.read_csv("data/fund_returns_monthly.csv", index_col=0, parse_dates=True)
rets.index = rets.index.to_period("M").to_timestamp("M")
ff = pd.read_csv("data/french_factors_monthly.csv", index_col=0, parse_dates=True)
ff.index = ff.index.to_period("M").to_timestamp("M")
info = pd.read_csv("data/fund_info.csv", index_col="ticker")

# French factors are already in decimals (same units as fund returns),
# e.g. Mkt_RF = 0.0508 in 1963-08. Do NOT divide by 100: doing so
# zeroes out RF and inflates every alpha by mean(RF). (Caught 2026-11-19:
# with /100, VFINX's Carhart alpha printed +2.92% instead of ~ -0.14%.)
rf = ff["RF"]
common = rets.index.intersection(ff.index)
rets, ff, rf = rets.loc[common], ff.loc[common], rf.loc[common]
print(f"sample: {rets.index.min():%Y-%m} .. {rets.index.max():%Y-%m}, n={len(rets)}")

# ------------------------------------------------- cleaning: winsorize
win_lo, win_hi = 0.01, 0.99
exc = rets.sub(rf, axis=0)  # excess returns (net of expenses)
exc_w, clipped = {}, {}
for t in rets.columns:
    exc_w[t], clipped[t] = winsorize(exc[t], win_lo, win_hi)
exc_w = pd.DataFrame(exc_w)
print("months clipped by 1/99 winsorizing:", clipped)

# ------------------------------------------------------------- fund facts
facts = []
for t in ACTIVE + INDEX:
    r = rets[t].dropna()
    facts.append({
        "ticker": t, "fund": info.loc[t, "fund_name"], "role": info.loc[t, "role"],
        "fee_pct": info.loc[t, "fee_pct"], "turnover_pct": info.loc[t, "turnover_pct"],
        "tna_usd_bn": info.loc[t, "tna_usd_bn"],
        "ann_ret_pct": r.mean() * 12 * 100, "ann_vol_pct": r.std() * np.sqrt(12) * 100,
        "sharpe": (r.mean() - rf.mean()) / r.std() * np.sqrt(12),
        "n": len(r),
    })
pd.DataFrame(facts).to_csv("outputs/table_fund_facts.csv", index=False)

# ------------------------------------------------- factor alphas net/gross
rows = []
for t in ACTIVE:
    fee_m = info.loc[t, "fee_pct"] / 100.0 / 12.0  # monthly decimal
    for label, y in [("net", exc_w[t]), ("gross", exc_w[t] + fee_m)]:
        for mname, cols in MODELS.items():
            r = factor_reg(y, ff[cols])
            rows.append({
                "ticker": t, "fund": info.loc[t, "fund_name"], "model": mname,
                "basis": label, "alpha_ann_pct": r["alpha_ann"] * 100,
                "t_alpha": r["t_alpha"], "te_ann_pct": r["te_ann"] * 100,
                "ir": r["ir"], "r2": r["r2"], "n": r["n"],
                **{f"beta_{c}": v for c, v in r["betas"].items()},
            })
pd.DataFrame(rows).to_csv("outputs/table_alphas.csv", index=False)

# ------------------------------------------- implementable index benchmark
brows = []
for t in ACTIVE:
    r = constrained_benchmark(exc_w[t], exc_w[INDEX])
    bfee = sum(r["weights"][i] * info.loc[i, "fee_pct"] for i in INDEX)
    brows.append({
        "ticker": t, "fund": info.loc[t, "fund_name"],
        "alpha_ann_pct": r["alpha_ann"] * 100, "t_alpha": r["t_alpha"],
        "te_ann_pct": r["te_ann"] * 100, "ir": r["ir"], "r2": r["r2"], "n": r["n"],
        **{f"w_{i}": v for i, v in r["weights"].items()},
        "bench_fee_pct": bfee, "fee_gap_pct": info.loc[t, "fee_pct"] - bfee,
    })
pd.DataFrame(brows).to_csv("outputs/table_benchmark.csv", index=False)

# ------------------------------------------------------------- persistence
halves = [("1994-2009", "1994-02", "2009-12"), ("2010-2024", "2010-01", "2024-12")]
prows = []
for t in ACTIVE:
    d = {"ticker": t}
    for hname, a, b in halves:
        y = exc_w[t].loc[a:b]
        r = factor_reg(y, ff.loc[a:b, MODELS["Carhart"]])
        d[f"alpha_{hname}_pct"] = r["alpha_ann"] * 100
        d[f"t_{hname}"] = r["t_alpha"]
    d["alpha_change_pct"] = d["alpha_2010-2024_pct"] - d["alpha_1994-2009_pct"]
    prows.append(d)
pers = pd.DataFrame(prows)
sp = spearmanr(pers["alpha_1994-2009_pct"], pers["alpha_2010-2024_pct"])
pers.to_csv("outputs/table_persistence.csv", index=False)
print(f"persistence Spearman rho = {sp.statistic:.3f} (p = {sp.pvalue:.3f}, n = 5)")

# --------------------------------------------------------------- subperiods
subs = [("1994-2004", "1994-02", "2004-12"), ("2005-2014", "2005-01", "2014-12"),
        ("2015-2024", "2015-01", "2024-12")]
srows = []
for t in ACTIVE:
    d = {"ticker": t}
    for sname, a, b in subs:
        r = factor_reg(exc_w[t].loc[a:b], ff.loc[a:b, MODELS["Carhart"]])
        d[f"alpha_{sname}_pct"] = r["alpha_ann"] * 100
        d[f"t_{sname}"] = r["t_alpha"]
    srows.append(d)
pd.DataFrame(srows).to_csv("outputs/table_subperiods.csv", index=False)

# ------------------------------------------------- rolling 36-month alphas
roll = {}
for t in ACTIVE:
    alphas, ts = [], []
    y = exc_w[t]
    X = ff[MODELS["Carhart"]]
    for i in range(35, len(y)):
        r = factor_reg(y.iloc[i - 35:i + 1], X.iloc[i - 35:i + 1])
        alphas.append(r["alpha_ann"] * 100)
        ts.append(r["t_alpha"])
    roll[t] = pd.DataFrame({"alpha_ann_pct": alphas, "t_alpha": ts}, index=y.index[35:])
    roll[t].to_csv(f"outputs/rolling_alpha_{t}.csv")
rollsum = pd.DataFrame({
    t: {"mean_alpha_pct": roll[t]["alpha_ann_pct"].mean(),
        "sd_alpha_pct": roll[t]["alpha_ann_pct"].std(),
        "min_alpha_pct": roll[t]["alpha_ann_pct"].min(),
        "max_alpha_pct": roll[t]["alpha_ann_pct"].max(),
        "share_sig_pct": (roll[t]["t_alpha"].abs() > 2).mean() * 100,
        "last_alpha_pct": roll[t]["alpha_ann_pct"].iloc[-1],
        "last_t": roll[t]["t_alpha"].iloc[-1]}
    for t in ACTIVE
}).T
rollsum.to_csv("outputs/table_rolling_summary.csv")

# ------------------------------------------------- winsorization sensitivity
wrows = []
for t in ACTIVE:
    for wlabel, (lo, hi) in [("none", (0.0, 1.0)), ("1/99", (0.01, 0.99)),
                             ("5/95", (0.05, 0.95))]:
        yw, _ = winsorize(exc[t], lo, hi)
        r = factor_reg(yw, ff[MODELS["Carhart"]])
        wrows.append({"ticker": t, "winsor": wlabel,
                      "alpha_ann_pct": r["alpha_ann"] * 100, "t_alpha": r["t_alpha"]})
pd.DataFrame(wrows).to_csv("outputs/table_winsor.csv", index=False)

# --------------------------------------------------- fee / turnover vs alpha
alphas = pd.read_csv("outputs/table_alphas.csv")
car = alphas[alphas["model"] == "Carhart"].pivot(index="ticker", columns="basis",
                                                values="alpha_ann_pct")
bench = pd.read_csv("outputs/table_benchmark.csv").set_index("ticker")
fp = []
for t in ACTIVE:
    fp.append({
        "ticker": t, "fee_pct": info.loc[t, "fee_pct"],
        "turnover_pct": info.loc[t, "turnover_pct"],
        "gross_alpha_pct": car.loc[t, "gross"],
        "net_alpha_pct": car.loc[t, "net"],
        "bench_alpha_pct": bench.loc[t, "alpha_ann_pct"],
        "verdict": "justified" if car.loc[t, "net"] >= 0 else "not justified",
    })
fp = pd.DataFrame(fp)
fp.to_csv("outputs/table_fee_perf.csv", index=False)
print("corr(fee, gross alpha) =", round(np.corrcoef(fp["fee_pct"], fp["gross_alpha_pct"])[0, 1], 3))
print("corr(turnover, gross alpha) =", round(np.corrcoef(fp["turnover_pct"], fp["gross_alpha_pct"])[0, 1], 3))
print("corr(fee, net alpha) =", round(np.corrcoef(fp["fee_pct"], fp["net_alpha_pct"])[0, 1], 3))
print("\nALL TABLES WRITTEN")
