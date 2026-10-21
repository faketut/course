"""
CFM301 Project 2: end-to-end analysis.

Reads data/monthly_panel.csv, data/ey_panel.csv, data/french_factors_monthly.csv,
data/french_25_size_bm.csv (no downloads) and writes outputs/:
  factor_ey.csv            monthly EY long-short factor + quintile legs
  table_cleaning.csv       cleaning log (observations affected per step)
  table_quintile_rets.csv  EY quintile portfolio summary stats
  table_reg_ey_quintiles.csv  OLS: quintile excess returns on MKT + EY
  table_reg_ff25.csv          OLS: French 25 Size-B/M excess returns on MKT + EY
  table_benchmark.csv         R^2 comparison: CAPM / FF3 / FF5 vs +EY; spanning test
  table_sensitivity.csv       premium & added power under alternative assumptions
  fig_cumret.png, fig_quintile_spread.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.regress import ols_nw, regression_table, factor_premium_stats, spanning_alpha

os.makedirs("outputs", exist_ok=True)
WINSOR = (0.01, 0.99)   # main spec: 1st/99th percentiles


# ---------------------------------------------------------------- data
def norm_date(s):
    """Map any month-end (CRSP last trading day, Yahoo/French calendar month-end,
    possibly tz-aware) to the calendar month-end so all panels join exactly."""
    s = pd.to_datetime(pd.to_datetime(s, utc=True).dt.date)
    return s.dt.to_period("M").dt.to_timestamp("M")


def norm_index(idx):
    return pd.DatetimeIndex(idx).to_period("M").to_timestamp("M")


def load_data():
    px = pd.read_csv("data/monthly_panel.csv", parse_dates=["date"])
    px["date"] = norm_date(px["date"])
    ey = pd.read_csv("data/ey_panel.csv", parse_dates=["date"])
    ey["date"] = norm_date(ey["date"])
    ff = pd.read_csv("data/french_factors_monthly.csv", parse_dates=["date"],
                     index_col="date")
    ff.index = norm_index(ff.index)
    f25 = pd.read_csv("data/french_25_size_bm.csv", parse_dates=["date"],
                      index_col="date")
    f25.index = norm_index(f25.index)
    return px, ey, ff, f25


def cleaning_report(px, ey):
    """Missing values, duplicates, outliers; returns log rows + cleaned frames."""
    log = []
    # duplicates
    dups = int(px.duplicated(subset=["date", "ticker"]).sum())
    log.append(("duplicate (date,ticker) rows dropped", dups,
                f"{len(px)} panel rows"))
    px = px.drop_duplicates(subset=["date", "ticker"])
    # missing returns
    miss_ret = int(px["ret"].isna().sum())
    log.append(("missing monthly returns dropped", miss_ret,
                f"{len(px)} panel rows"))
    px = px.dropna(subset=["ret"]).copy()
    # winsorize returns
    lo, hi = px["ret"].quantile([WINSOR[0], WINSOR[1]])
    n_hit = int(((px["ret"] < lo) | (px["ret"] > hi)).sum())
    log.append((f"returns winsorized at {WINSOR[0]:.0%}/{WINSOR[1]:.0%}",
                n_hit, f"cut-offs [{lo:.4f}, {hi:.4f}]"))
    px["ret"] = px["ret"].clip(lo, hi)
    # EY coverage
    miss_ey = int(ey["ey"].isna().sum())
    log.append(("EY missing (insufficient filing history)", miss_ey,
                f"{len(ey)} ey rows"))
    ey = ey.dropna(subset=["ey"]).copy()
    lo_e, hi_e = ey["ey"].quantile([WINSOR[0], WINSOR[1]])
    n_hit_e = int(((ey["ey"] < lo_e) | (ey["ey"] > hi_e)).sum())
    log.append((f"EY winsorized at {WINSOR[0]:.0%}/{WINSOR[1]:.0%}", n_hit_e,
                f"cut-offs [{lo_e:.4f}, {hi_e:.4f}]"))
    ey["ey"] = ey["ey"].clip(lo_e, hi_e)
    tab = pd.DataFrame(log, columns=["step", "obs_affected", "detail"])
    tab.to_csv("outputs/table_cleaning.csv", index=False)
    return px, ey


# ---------------------------------------------------------------- factor
def form_factor(px, ey, n_groups=5, label="Q", mcap=None, vw=False):
    """Monthly sorts on lagged EY -> group returns + LS factor.

    Sort at month-end t on ey[t]; hold during t+1. Equal-weighted legs by
    default; value-weighted (by month-t market cap) when vw=True. Returns
    factor series (high-EY minus low-EY) and the n_groups leg return series.
    If mcap (DataFrame with date/ticker/mcap, or Series indexed by
    (date, ticker)) is given, also returns the time-series average of each
    quintile's mean market cap (for size-tilt diagnostics).
    """
    ret = px.set_index(["date", "ticker"])["ret"]
    e = ey.set_index(["date", "ticker"])["ey"]
    if mcap is not None:
        mc = (mcap.set_index(["date", "ticker"])["mcap"] if not isinstance(
            mcap, pd.Series) else mcap)
    else:
        mc = None
    if vw and mc is None:
        raise ValueError("vw=True needs mcap")
    common_dates = sorted(set(ret.index.get_level_values("date"))
                          & set(e.index.get_level_values("date")))
    legs = {f"{label}{i+1}": [] for i in range(n_groups)}
    mcs = {f"{label}{i+1}": [] for i in range(n_groups)}
    idx = []
    for t in common_dates[:-1]:
        t1 = common_dates[common_dates.index(t) + 1]
        chars = e.loc[t].dropna()
        r1 = ret.loc[t1].reindex(chars.index).dropna()
        chars = chars.reindex(r1.index)
        if len(chars) < 2 * n_groups:
            continue
        q = pd.qcut(chars, n_groups, labels=False, duplicates="drop")
        row = {}
        for g in range(n_groups):
            members = chars.index[q == g]
            r = r1.reindex(members)
            if vw:
                w = mc.loc[t].reindex(members)
                row[f"{label}{g+1}"] = float((r * w).sum() / w.sum())
            else:
                row[f"{label}{g+1}"] = r.mean()
            if mc is not None:
                mcs[f"{label}{g+1}"].append(
                    mc.loc[t].reindex(members).mean())
        for k, v in row.items():
            legs[k].append(v)
        idx.append(t1)
    legs = pd.DataFrame(legs, index=pd.DatetimeIndex(idx))
    factor = legs[f"{label}{n_groups}"] - legs[f"{label}1"]
    factor.name = "EY"
    avg_mcap = (pd.Series({k: float(np.mean(v)) for k, v in mcs.items()})
                if mc is not None else None)
    return factor, legs, avg_mcap


# ---------------------------------------------------------------- regressions
def regress_test_assets(excess, factors, name):
    """Each test asset on MKT + EY (and CAPM-only for comparison)."""
    rows, rows_capm = [], []
    for col in excess.columns:
        y = excess[col].dropna()
        X = factors.reindex(y.index).dropna()
        y = y.reindex(X.index)
        r = ols_nw(y, X[["Mkt_RF", "EY"]])
        rc = ols_nw(y, X[["Mkt_RF"]])
        rows.append({"asset": col,
                     "alpha": r["params"]["const"],
                     "alpha_t": r["tstats"]["const"],
                     "b_mkt": r["params"]["Mkt_RF"],
                     "b_mkt_t": r["tstats"]["Mkt_RF"],
                     "b_ey": r["params"]["EY"],
                     "b_ey_t": r["tstats"]["EY"],
                     "R2": r["rsquared"],
                     "R2_capm": rc["rsquared"],
                     "nobs": r["nobs"]})
    tab = pd.DataFrame(rows).set_index("asset")
    tab.to_csv(f"outputs/table_reg_{name}.csv")
    return tab


def benchmark_comparison(excess, ff, ey_factor):
    """Does EY add explanatory power beyond CAPM / FF3 / FF5? + spanning test."""
    bench = {
        "CAPM": ["Mkt_RF"],
        "FF3": ["Mkt_RF", "SMB", "HML"],
        "FF5": ["Mkt_RF", "SMB", "HML", "RMW", "CMA"],
    }
    rows = []
    for bname, cols in bench.items():
        d_r2, n_sig = [], 0
        for col in excess.columns:
            y = excess[col].dropna()
            base = ff[cols].reindex(y.index).dropna()
            aug = base.assign(EY=ey_factor).dropna()
            y = y.reindex(aug.index)
            r0 = ols_nw(y, base.reindex(y.index))
            r1 = ols_nw(y, aug.reindex(y.index))
            d_r2.append(r1["rsquared"] - r0["rsquared"])
            if abs(r1["tstats"]["EY"]) > 1.96:
                n_sig += 1
        rows.append({"benchmark": bname,
                     "avg_dR2_add_EY": float(np.mean(d_r2)),
                     "assets_w_sig_EY_loading": f"{n_sig}/{len(excess.columns)}"})
    # spanning: is EY explained by FF5?
    common = pd.concat([ey_factor, ff], axis=1, join="inner").dropna()
    sp = spanning_alpha(common["EY"], common[["Mkt_RF", "SMB", "HML", "RMW", "CMA"]])
    rows.append({"benchmark": "spanning: EY on FF5",
                 "avg_dR2_add_EY":
                     f"alpha={sp['alpha']*12:.4f}/yr, t={sp['alpha_tstat']:.2f}, "
                     f"R2={sp['rsquared']:.3f}",
                 "assets_w_sig_EY_loading": ""})
    tab = pd.DataFrame(rows).set_index("benchmark")
    tab.to_csv("outputs/table_benchmark.csv")
    return tab


def sensitivity(factor, legs, ff, excess_ff25):
    """Premium, significance and added power under alternative assumptions."""
    out = []

    def stats(f, tag):
        s = factor_premium_stats(f)
        out.append({"spec": tag,
                    "mean_ann": s["mean_ann"], "sharpe": s["sharpe"],
                    "tstat_mean": s["tstat_mean"], "nobs": s["nobs"]})

    stats(factor, "main: quintiles, 1/99 winsor")
    # alternative 1: tercile formation
    px = pd.read_csv("data/monthly_panel.csv", parse_dates=["date"])
    px["date"] = norm_date(px["date"])
    ey = pd.read_csv("data/ey_panel.csv", parse_dates=["date"])
    ey["date"] = norm_date(ey["date"])
    f3, _, _ = form_factor(px, ey, n_groups=3, label="T")
    stats(f3, "alt: terciles (instead of quintiles)")
    # alternative 1b: value-weighted legs (is the premium tradable at scale?)
    fvw, _, _ = form_factor(px, ey, n_groups=5, label="Q", mcap=ey, vw=True)
    stats(fvw, "alt: value-weighted legs")
    # alternative 2: subperiods
    for tag, sl in [("alt: 2002-2009", slice("2002", "2009")),
                    ("alt: 2010-2019", slice("2010", "2019")),
                    ("alt: 2020-2024", slice("2020", "2024"))]:
        sub = factor.loc[sl].dropna()
        if len(sub) > 24:
            stats(sub, tag)
    # alternative 3: exclude COVID crash months
    stats(factor.drop(pd.date_range("2020-02-29", "2020-04-30", freq="ME"),
                      errors="ignore"), "alt: excl. Mar-Apr 2020")
    tab = pd.DataFrame(out).set_index("spec")
    tab.to_csv("outputs/table_sensitivity.csv")
    return tab


# ---------------------------------------------------------------- main
def main():
    px, ey, ff, f25 = load_data()
    px, ey = cleaning_report(px, ey)

    # --- factor + quintile test assets (excess over RF) ---
    factor, legs, avg_mcap = form_factor(px, ey, n_groups=5, mcap=ey)
    rf = ff["RF"]
    qx = legs.sub(rf.reindex(legs.index), axis=0).dropna()
    common = pd.concat([factor, ff], axis=1, join="inner").dropna()
    factor, ff_c = common["EY"], common.drop(columns="EY")
    qx = qx.reindex(factor.index).dropna()
    pd.DataFrame({"EY": factor}).to_csv("outputs/factor_ey.csv")
    qstats = pd.DataFrame({c: factor_premium_stats(qx[c].add(
        rf.reindex(qx.index), axis=0)) for c in qx.columns}).T
    qstats["avg_mcap_$mm"] = avg_mcap / 1e6
    qstats.to_csv("outputs/table_quintile_rets.csv")

    # --- regressions ---
    reg_q = regress_test_assets(qx, ff_c[["Mkt_RF"]].assign(EY=factor),
                                "ey_quintiles")
    f25x = f25.sub(ff["RF"], axis=0)
    f25x = f25x.reindex(factor.index).dropna()
    ff25 = ff_c.reindex(f25x.index)
    reg_25 = regress_test_assets(f25x, ff25[["Mkt_RF"]].assign(
        EY=factor.reindex(f25x.index)), "ff25")
    bench = benchmark_comparison(f25x, ff25,
                                 factor.reindex(f25x.index).rename("EY"))

    # --- sensitivity ---
    sens = sensitivity(factor, legs, ff_c, f25x)

    # --- figures ---
    cum = (1 + pd.DataFrame({"EY": factor,
                             "Mkt_RF": ff_c["Mkt_RF"]})).cumprod()
    ax = cum.plot(figsize=(8, 4.5), title="Cumulative returns: EY factor vs market")
    ax.set_ylabel("growth of $1"); ax.figure.tight_layout()
    ax.figure.savefig("outputs/fig_cumret.png", dpi=150)

    spread = qx.mean() * 12 * 100
    market_ann = ff_c.loc[qx.index, "Mkt_RF"].mean() * 12 * 100
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(spread.index, spread, color="steelblue", label="EY quintiles")
    ax.axhline(market_ann, color="#d4a017", linewidth=2,
               label="Mkt_RF")
    ax.set_title("Annualized mean excess return by EY quintile (Q1=low EY)")
    ax.set_ylabel("mean excess return (%/yr)")
    ax.legend()
    fig.tight_layout()
    fig.savefig("outputs/fig_quintile_spread.png", dpi=150)

    prem = factor_premium_stats(factor)
    print(f"EY factor: n={prem['nobs']}, mean={prem['mean_ann']:.4f}/yr, "
          f"Sharpe={prem['sharpe']:.2f}, t={prem['tstat_mean']:.2f}")
    print(f"Quintile R2 (MKT+EY): {reg_q['R2'].mean():.3f} avg; "
          f"FF25 R2 (MKT+EY): {reg_25['R2'].mean():.3f} avg")
    print("Benchmark comparison:\n", bench.to_string())
    print("Sensitivity:\n", sens.round(3).to_string())


if __name__ == "__main__":
    main()
