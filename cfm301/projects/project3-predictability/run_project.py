"""
CFM301 Project 3: Reproducing the Equity Return Predictability Table.

Pipeline:
  data/predictors_monthly.csv  (FRED + Shiller, via src/build_predictors.py)
  data/french_factors_monthly.csv (Ken French; interim market return = Mkt-RF + RF)
  data/wrds_crsp_msi.csv       (CRSP VWRETD/VWRETX; used when present, else French)

Outputs (outputs/):
  table_cleaning.csv      cleaning log (observations affected per step)
  table_predict.csv       main table: corr + NW t-stat, 1Q/1Y/2Y/5Y, per predictor
  table_predict_excess.csv  same, for excess returns (over monthly RF)
  table_buckets.csv       valuation-quintile future 1Y/5Y returns, mean +- 2 SD
  table_garch.csv         GARCH(1,1) vs realized volatility comparison
  table_sensitivity.csv   subperiods / NW lag / winsor alternatives
  fig_predict.png, fig_buckets.png, fig_garch.png

Returns convention: total returns (VWRETD includes distributions). Monthly
risk-free rate from FRED TB3MS (rf_ann/1200); excess = total - rf.
Horizons are overlapping compounded returns; t-stats are Newey-West with
lag = horizon - 1 months (the MA order of an h-month overlap), via the
standardized-OLS equivalence in src/predict.py.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.predict import future_returns, corr_tstat_nw, winsorize

os.makedirs("outputs", exist_ok=True)
HORIZONS = (3, 12, 24, 60)
HLAB = {3: "1Q", 12: "1Y", 24: "2Y", 60: "5Y"}
PREDICTORS = ["div_yield", "earn_yield", "pe10", "term_spread",
              "credit_spread", "inflation", "ip_growth", "unemp",
              "oil_growth", "vix", "gdp_growth", "rf_level", "past_1y_ret",
              "past_vol", "cay"]
WINSOR = (0.01, 0.99)


def load_returns():
    """Monthly total market return; CRSP VWRETD when present, else French Mkt."""
    msi = "data/wrds_crsp_msi.csv"
    if os.path.exists(msi):
        m = pd.read_csv(msi)
        m["date"] = pd.to_datetime(m["caldt"], format="%Y%m%d")
        m = m.set_index("date").sort_index()
        m.index = m.index.to_period("M").to_timestamp("M")
        src = "CRSP VWRETD"
        return m["vwretd"].rename("ret"), m["ewretd"].rename("ret_ew"), src
    f = pd.read_csv("data/french_factors_monthly.csv", parse_dates=["date"],
                    index_col="date")
    f.index = f.index.to_period("M").to_timestamp("M")
    src = "French Mkt (Mkt-RF + RF; interim until VWRETD arrives)"
    return (f["Mkt_RF"] + f["RF"]).rename("ret"), None, src


def cleaning_report(pred, ret):
    log = []

    def add(step, n, detail):
        log.append({"step": step, "obs_affected": int(n), "detail": detail})

    # duplicates (should be none after month-end normalization)
    add("duplicate months dropped", int(pred.index.duplicated().sum()),
        f"{len(pred)} predictor rows")
    pred = pred[~pred.index.duplicated(keep="last")]
    # missing returns
    miss = int(ret.isna().sum())
    add("missing monthly returns dropped", miss, f"{len(ret)} return rows")
    ret = ret.dropna()
    # predictor missingness (reported, not dropped: pairwise in correlations)
    for c in PREDICTORS:
        add(f"missing {c}", int(pred[c].isna().sum()), f"{len(pred)} rows")
    # winsorize predictors
    for c in PREDICTORS:
        w, lo, hi = winsorize(pred[c].dropna(), *WINSOR)
        n_hit = int(((pred[c] < lo) | (pred[c] > hi)).sum())
        add(f"{c} winsorized at 1%/99%", n_hit, f"cut-offs [{lo:.4g}, {hi:.4g}]")
        pred[c] = pred[c].clip(lo, hi)
    tab = pd.DataFrame(log)
    tab.to_csv("outputs/table_cleaning.csv", index=False)
    return pred, ret


def predict_table(pred, rets, nw_lag_mode="h-1"):
    """Main table: rows = predictors, columns = corr/t per horizon."""
    rows = []
    for c in PREDICTORS:
        row = {"predictor": c}
        for h in HORIZONS:
            lag = h - 1 if nw_lag_mode == "h-1" else 2 * (h - 1)
            rho, t, n = corr_tstat_nw(pred[c], rets[f"R{h}"], lag)
            row[f"corr_{HLAB[h]}"] = rho
            row[f"t_{HLAB[h]}"] = t
            row[f"n_{HLAB[h]}"] = n
        rows.append(row)
    return pd.DataFrame(rows).set_index("predictor")


def main():
    pred = pd.read_csv("data/predictors_monthly.csv", index_col=0,
                       parse_dates=True)
    pred.index = pred.index.to_period("M").to_timestamp("M")
    ret, ret_ew, src = load_returns()
    print(f"return source: {src}")
    # slide predictor: past 1-year (trailing 12M compounded) market return,
    # i.e. the return over months t-11..t, known at time t
    pred["past_1y_ret"] = (np.expm1(np.log1p(ret).rolling(12).sum())
                           .reindex(pred.index))
    # slide predictor: past volatility (last quarter) = std of monthly
    # returns over months t-2..t (correlation is scale-free, so no annualizing)
    pred["past_vol"] = ret.rolling(3).std().reindex(pred.index)
    pred, ret = cleaning_report(pred, ret)
    rf_m = (pred["rf_ann"] / 1200).reindex(ret.index)
    ret_x = ret - rf_m  # excess return

    fut = future_returns(ret)
    fut_x = future_returns(ret_x)
    tab = predict_table(pred, fut)
    tab.to_csv("outputs/table_predict.csv")
    tab_x = predict_table(pred, fut_x)
    tab_x.to_csv("outputs/table_predict_excess.csv")

    # ---- bucket analysis (valuation quintiles) ----
    buck_rows = []
    for val in ["div_yield", "pe10"]:
        x = pred[val].dropna()
        for h, lab in [(12, "1Y"), (60, "5Y")]:
            y = fut[f"R{h}"]
            d = pd.DataFrame({"x": x, "y": y}).dropna()
            if len(d) < 100:
                continue
            q = pd.qcut(d["x"], 5, labels=False, duplicates="drop")
            for g in range(5):
                yy = d["y"][q == g]
                buck_rows.append({
                    "valuation": val, "horizon": lab, "bucket": g + 1,
                    "n": len(yy), "mean": yy.mean(),
                    "sd": yy.std(), "lo_2sd": yy.mean() - 2 * yy.std(),
                    "hi_2sd": yy.mean() + 2 * yy.std()})
    buck = pd.DataFrame(buck_rows)
    buck.to_csv("outputs/table_buckets.csv", index=False)

    # ---- sensitivity ----
    sens_rows = []

    def add_spec(tag, p, r, mode="h-1"):
        f = future_returns(r)
        t = predict_table(p, f, mode)
        for c in PREDICTORS:
            sens_rows.append({"spec": tag, "predictor": c,
                              **{f"{k}_{HLAB[h]}": t.loc[c, f"{k}_{HLAB[h]}"]
                                 for h in HORIZONS for k in ("corr", "t")}})

    add_spec("main: full sample, NW lag h-1", pred, ret)
    # subperiods
    for tag, sl in [("pre-1990", slice(None, "1989-12-31")),
                    ("post-1990", slice("1990-01-31", None)),
                    ("excl. 2008-2009 crisis", None)]:
        if sl is None:
            mask = ~((pred.index >= "2008-01-31") & (pred.index <= "2009-12-31"))
            add_spec(tag, pred[mask], ret.reindex(pred[mask].index).dropna())
        else:
            pp = pred.loc[sl]
            add_spec(tag, pp, ret.reindex(pp.index).dropna())
    # alternative NW lag
    add_spec("alt: NW lag 2(h-1)", pred, ret, mode="2h")
    # alternative winsor 5/95
    pred_w = pred.copy()
    for c in PREDICTORS:
        pred_w[c] = winsorize(pred_w[c].dropna(), 0.05, 0.95)[0].reindex(
            pred_w.index)
    add_spec("alt: winsor 5/95", pred_w, ret)
    # VW vs EW: equal-weighted index as the return series
    if ret_ew is not None:
        add_spec("alt: EW returns (ewretd)", pred, ret_ew)
    sens = pd.DataFrame(sens_rows)
    sens.to_csv("outputs/table_sensitivity.csv", index=False)

    # ---- comparison vs slides (all blocks, excess returns) ----
    slide_tables = [
        ("block1_valuation", "docs/slide_block1_valuation.csv",
         {"Dividend yield": "div_yield", "Earnings yield": "earn_yield"}),
        ("block2_business_cycle", "docs/slide_block2.csv",
         {"Term spread (10y-3m)": "term_spread",
          "Credit spread (BAA-AAA)": "credit_spread",
          "Unemployment rate": "unemp",
          "GDP growth (past year)": "gdp_growth",
          "Industrial production (past year)": "ip_growth",
          "Past 1-year return": "past_1y_ret",
          "Inflation (past year)": "inflation",
          "Oil price (past-year change)": "oil_growth",
          "Risk-free rate": "rf_level"}),
        ("block2_risk", "docs/slide_block2_risk.csv",
         {"VIX": "vix", "Past volatility (last quarter)": "past_vol",
          "Consumption-wealth ratio": "cay"}),
    ]
    for tag, path, smap in slide_tables:
        slide = pd.read_csv(path)
        comp_rows = []
        for _, r in slide.iterrows():
            if r["predictor"] not in smap:
                continue  # e.g. consumption-wealth ratio: no series yet
            c = smap[r["predictor"]]
            comp_rows.append({
                "predictor": r["predictor"], "horizon": r["horizon"],
                "slide_corr": r["corr"], "slide_t": r["tstat"],
                "my_corr_excess": tab_x.loc[c, f"corr_{r['horizon']}"],
                "my_t_excess": tab_x.loc[c, f"t_{r['horizon']}"],
                "my_n_excess": tab_x.loc[c, f"n_{r['horizon']}"]})
        comp = pd.DataFrame(comp_rows)
        comp.to_csv(f"outputs/table_compare_{tag}.csv", index=False)
        print(f"\n{tag} comparison (slide vs extended sample, excess returns):")
        print(comp.round(3).to_string())

    # ---- GARCH(1,1) vs realized volatility (req 11) ----
    from scipy.optimize import minimize
    r_log = np.log1p(ret.dropna())
    y = r_log.values
    mu0 = y.mean()

    def nll(params):
        om, al, be = params
        if om <= 0 or al < 0 or be < 0 or al + be >= 1:
            return 1e10
        sig2 = np.empty_like(y)
        sig2[0] = np.var(y)
        e = y - mu0
        for t in range(1, len(y)):
            sig2[t] = om + al * e[t - 1] ** 2 + be * sig2[t - 1]
        return 0.5 * np.sum(np.log(sig2) + e ** 2 / sig2)

    res = minimize(nll, [np.var(y) * 0.1, 0.1, 0.8],
                   method="Nelder-Mead",
                   options={"maxiter": 20000, "xatol": 1e-8, "fatol": 1e-8})
    om, al, be = res.x
    e = y - mu0
    sig2 = np.empty_like(y)
    sig2[0] = np.var(y)
    for t in range(1, len(y)):
        sig2[t] = om + al * e[t - 1] ** 2 + be * sig2[t - 1]
    garch_vol = pd.Series(np.sqrt(sig2) * np.sqrt(12), index=r_log.index)
    # realized vol: rolling 12M std of monthly log returns, annualized
    real_vol = r_log.rolling(12).std() * np.sqrt(12)
    # future realized vol over next 12M (for predictability comparison)
    fut_real = real_vol.shift(-12)
    d = pd.DataFrame({"garch": garch_vol, "real": real_vol,
                      "fut_real": fut_real}).dropna()
    garch_tab = pd.DataFrame([{
        "omega": om, "alpha": al, "beta": be, "alpha+beta": al + be,
        "corr_garch_realized": d["garch"].corr(d["real"]),
        "corr_garch_future_real": d["garch"].corr(d["fut_real"]),
        "nobs": len(d)}])
    garch_tab.to_csv("outputs/table_garch.csv", index=False)
    print("\nGARCH(1,1):\n", garch_tab.round(4).to_string())

    # ---- sample-split replication check (req 8/12) ----
    # Does the slide's valuation result replicate inside the slide's own era
    # (through 2011), or is it a full-sample artefact? And does it survive
    # after 2011? Quarterly sampling matches the slide's likely construction.
    split_rows = []
    key_preds = ["div_yield", "earn_yield", "cay", "term_spread", "vix"]
    for tag, sl in [("full sample", slice(None, None)),
                    ("through 2011 (slide era)", slice(None, "2011-12-31")),
                    ("1926-1963 (pre-French era)", slice(None, "1963-06-30")),
                    ("post-2011", slice("2012-01-31", None))]:
        pp = pred.loc[sl]
        rr = ret_x.reindex(pp.index).dropna()
        f = future_returns(rr)
        for c in key_preds:
            row = {"spec": tag, "predictor": c}
            for h in HORIZONS:
                rho, t, n = corr_tstat_nw(pp[c], f[f"R{h}"], h - 1)
                row[f"corr_{HLAB[h]}"] = rho
                row[f"t_{HLAB[h]}"] = t
                row[f"n_{HLAB[h]}"] = n
            split_rows.append(row)
    # quarterly sampling: predictor + future returns observed at quarter-ends
    q_idx = pred.index[pred.index.is_quarter_end]
    pq = pred.loc[q_idx]
    rq = ret_x.reindex(q_idx).dropna()
    fq = future_returns(rq)
    for c in key_preds:
        row = {"spec": "quarterly sampling", "predictor": c}
        for h in HORIZONS:
            rho, t, n = corr_tstat_nw(pq[c], fq[f"R{h}"], h - 1)
            row[f"corr_{HLAB[h]}"] = rho
            row[f"t_{HLAB[h]}"] = t
            row[f"n_{HLAB[h]}"] = n
        split_rows.append(row)
    splits = pd.DataFrame(split_rows)
    splits.to_csv("outputs/table_sample_splits.csv", index=False)
    print("\nSample splits (excess returns, key predictors):")
    print(splits.round(3).to_string())

    # ---- quarterly-sampling comparison vs slides (all blocks) ----
    # Quarterly sampling matches the slides' construction better on several
    # cells (oil magnitude, term-spread 1Q sign, 5Y t-stats); kept as a
    # sensitivity, not the main table, to avoid fitting to the answer.
    qtab_rows = []
    for c in PREDICTORS:
        row = {"predictor": c}
        for h in HORIZONS:
            rho, t, n = corr_tstat_nw(pq[c], fq[f"R{h}"], h - 1)
            row[f"corr_{HLAB[h]}"] = rho
            row[f"t_{HLAB[h]}"] = t
            row[f"n_{HLAB[h]}"] = n
        qtab_rows.append(row)
    qtab = pd.DataFrame(qtab_rows).set_index("predictor")
    qtab.to_csv("outputs/table_predict_excess_quarterly.csv")
    for tag, path, smap in slide_tables:
        slide = pd.read_csv(path)
        comp_rows = []
        for _, r in slide.iterrows():
            if r["predictor"] not in smap:
                continue
            c = smap[r["predictor"]]
            comp_rows.append({
                "predictor": r["predictor"], "horizon": r["horizon"],
                "slide_corr": r["corr"], "slide_t": r["tstat"],
                "my_corr_excess": qtab.loc[c, f"corr_{r['horizon']}"],
                "my_t_excess": qtab.loc[c, f"t_{r['horizon']}"],
                "my_n_excess": qtab.loc[c, f"n_{r['horizon']}"]})
        comp = pd.DataFrame(comp_rows)
        comp.to_csv(f"outputs/table_compare_{tag}_quarterly.csv", index=False)
        agree = ((comp["slide_corr"] * comp["my_corr_excess"]) > 0).mean()
        print(f"quarterly {tag} sign agreement: {agree:.0%}")

    # ---- figures ----
    fig, ax = plt.subplots(figsize=(8, 4.5))
    tab[[f"corr_{HLAB[h]}" for h in HORIZONS]].T.plot(ax=ax, marker="o")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title("Predictive correlations by horizon")
    ax.set_ylabel("correlation with future return")
    fig.tight_layout()
    fig.savefig("outputs/fig_predict.png", dpi=150)
    plt.close(fig)

    print(tab.round(3).to_string())
    print("\nBuckets:\n", buck.round(3).to_string())


if __name__ == "__main__":
    main()
