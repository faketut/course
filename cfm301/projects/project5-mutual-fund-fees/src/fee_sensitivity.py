"""Fee sensitivity (Project 5): constant vs time-varying expense ratios.

Question: the main analysis adds back a CONSTANT expense ratio
(current prospectus value) to get gross returns. The brief wants
annual expense ratios converted to monthly. This script re-runs the
gross Carhart alpha with TIME-VARYING fees from Zacks annual expense
ratios (data/zacks_fees_annual.csv, 2016-2026, read from Zacks
/performance pages 2026-11-19) and compares it with the constant-fee
gross alpha in outputs/table_alphas.csv.

Design: months in 2016-2024 use that year's Zacks fee / 12; months
before 2016 (no Zacks history) keep the current prospectus fee, as in
the main analysis. 2025-2026 Zacks rows are out of sample and unused.
Everything else mirrors run_project.py exactly: same returns, same
1/99 winsorized excess returns, same Carhart regression. A second
comparison runs both fee schemes on the 2016-2024 window only, where
every month uses a Zacks fee, so the fee effect is undiluted.

Run: .venv/bin/python src/fee_sensitivity.py
  -> outputs/table_fee_sensitivity.csv
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.fund_analysis import winsorize, factor_reg

ACTIVE = ["FCNTX", "FMAGX", "AGTHX", "PRGFX", "TRBCX"]
CARHART = ["Mkt_RF", "SMB", "HML", "UMD"]

rets = pd.read_csv("data/fund_returns_monthly.csv", index_col=0, parse_dates=True)
rets.index = rets.index.to_period("M").to_timestamp("M")
ff = pd.read_csv("data/french_factors_monthly.csv", index_col=0, parse_dates=True)
ff.index = ff.index.to_period("M").to_timestamp("M")
info = pd.read_csv("data/fund_info.csv", index_col="ticker")
zacks = pd.read_csv("data/zacks_fees_annual.csv")
zacks = zacks[zacks["year"] <= 2024].set_index(["ticker", "year"])["expense_ratio_pct"]

rf = ff["RF"]
common = rets.index.intersection(ff.index)
rets, ff, rf = rets.loc[common], ff.loc[common], rf.loc[common]

exc = rets.sub(rf, axis=0)
exc_w, _ = {}, {}
for t in rets.columns:
    exc_w[t], _ = winsorize(exc[t], 0.01, 0.99)
exc_w = pd.DataFrame(exc_w)

rows = []
for t in ACTIVE:
    fee_const_m = info.loc[t, "fee_pct"] / 100.0 / 12.0
    # monthly fee series: Zacks annual fee / 12 for 2016-2024, else constant
    fee_tv_m = pd.Series(fee_const_m, index=rets.index)
    for y in range(2016, 2025):
        mask = fee_tv_m.index.year == y
        fee_tv_m.loc[mask] = zacks.loc[(t, y)] / 100.0 / 12.0

    gross_const = exc_w[t] + fee_const_m
    gross_tv = exc_w[t] + fee_tv_m
    rc = factor_reg(gross_const, ff[CARHART])
    rt = factor_reg(gross_tv, ff[CARHART])

    w = (exc_w.index >= "2016-01-31") & (exc_w.index <= "2024-12-31")
    rwc = factor_reg(gross_const[w], ff[CARHART])
    rwt = factor_reg(gross_tv[w], ff[CARHART])

    rows.append({
        "ticker": t,
        "avg_fee_const_pct": fee_const_m * 12 * 100,
        "avg_fee_tv_pct": float(fee_tv_m.mean() * 12 * 100),
        "gross_carhart_const_pct": rc["alpha_ann"] * 100,
        "t_const": rc["t_alpha"],
        "gross_carhart_tv_pct": rt["alpha_ann"] * 100,
        "t_tv": rt["t_alpha"],
        "diff_pct": (rt["alpha_ann"] - rc["alpha_ann"]) * 100,
        "window_gross_const_pct": rwc["alpha_ann"] * 100,
        "window_t_const": rwc["t_alpha"],
        "window_gross_tv_pct": rwt["alpha_ann"] * 100,
        "window_t_tv": rwt["t_alpha"],
        "window_diff_pct": (rwt["alpha_ann"] - rwc["alpha_ann"]) * 100,
    })

df = pd.DataFrame(rows)
df.to_csv("outputs/table_fee_sensitivity.csv", index=False)
pd.set_option("display.width", 200)
print(df.round(3).to_string(index=False))
print("\nmax |full-sample diff| =", round(df["diff_pct"].abs().max(), 3), "pp")
print("max |2016-2024 window diff| =", round(df["window_diff_pct"].abs().max(), 3), "pp")
