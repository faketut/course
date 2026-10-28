"""Block 2 in the Data: Risk and Risk Aversion (standalone).

Reproduces the slide's risk block from the project's already-built data:
  data/predictors_monthly.csv  (FRED + Shiller: vix, cay, rf_ann)
  data/wrds_crsp_msi.csv       (CRSP VWRETD, date column 'caldt')

Prediction: higher volatility or risk aversion -> higher future returns.
Table: correlation of each variable today with future EXCESS stock
returns at 1 quarter / 1 year / 2 years / 5 years; Newey-West t-statistic
in brackets; |t| > 2 is statistically significant.

Self-contained: the three helpers below mirror src/predict.py so this
file can be read and run on its own. It does not modify any existing file.
Run from the project root:  .venv/bin/python src/block2_risk.py
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

HORIZONS = (3, 12, 24, 60)  # months: 1Q, 1Y, 2Y, 5Y
HLAB = {3: "1Q", 12: "1Y", 24: "2Y", 60: "5Y"}

# Slide values: (correlation, t-statistic) per horizon.
SLIDE = {
    "VIX": {3: (0.12, 0.96), 12: (0.10, 0.63), 24: (0.13, 0.75), 60: (-0.16, -0.47)},
    "Past volatility (last quarter)": {3: (0.05, 0.55), 12: (0.09, 0.65), 24: (0.13, 0.78), 60: (0.06, 0.17)},
    "Consumption-wealth ratio": {3: (0.16, 2.92), 12: (0.30, 2.62), 24: (0.42, 2.23), 60: (0.53, 1.34)},
}


def future_returns(r, horizons=HORIZONS):
    """Overlapping compounded returns: R(t,h) = prod(1 + r_{t+1..t+h}) - 1.

    Log-return rolling sum is backward-looking ([t-h+1, t]); shifting by -h
    months gives the forward window [t+1, t+h].
    """
    out = {}
    logr = np.log1p(r)
    for h in horizons:
        out[f"R{h}"] = np.expm1(logr.rolling(h).sum().shift(-h))
    return pd.DataFrame(out, index=r.index)


def corr_tstat_nw(x, y, nw_lag):
    """Correlation of x and y with a Newey-West t-statistic.

    Standardizes both series, OLS slope (= correlation), NW covariance with
    `nw_lag` lags. Returns (rho, tstat, nobs).
    """
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(d) < 30:
        return np.nan, np.nan, len(d)
    xs = (d["x"] - d["x"].mean()) / d["x"].std()
    ys = (d["y"] - d["y"].mean()) / d["y"].std()
    res = sm.OLS(ys.values, sm.add_constant(xs.values)).fit(
        cov_type="HAC", cov_kwds={"maxlags": nw_lag, "use_correction": True})
    return float(d["x"].corr(d["y"])), float(res.tvalues[1]), len(d)


def winsorize(s, lo=0.01, hi=0.99):
    return s.clip(*s.quantile([lo, hi]))


def main():
    pred = pd.read_csv("data/predictors_monthly.csv", index_col=0,
                       parse_dates=True)
    pred.index = pred.index.to_period("M").to_timestamp("M")

    msi = pd.read_csv("data/wrds_crsp_msi.csv")
    msi["date"] = pd.to_datetime(msi["caldt"], format="%Y%m%d")
    msi = msi.set_index("date").sort_index()
    msi.index = msi.index.to_period("M").to_timestamp("M")
    ret = msi["vwretd"]  # CRSP value-weighted total return

    # Slide predictor: past volatility (last quarter) = std of monthly total
    # returns over months t-2..t (correlation is scale-free, no annualizing).
    pred["past_vol"] = ret.rolling(3).std().reindex(pred.index)

    # Future EXCESS returns: total return minus 3-month T-bill rate.
    rf_m = (pred["rf_ann"] / 1200).reindex(ret.index)
    fut_x = future_returns(ret - rf_m)

    block = {"VIX": winsorize(pred["vix"].dropna()),
             "Past volatility (last quarter)": winsorize(pred["past_vol"].dropna()),
             "Consumption-wealth ratio": winsorize(pred["cay"].dropna())}

    print(f"{'Predictor':32s}" + "".join(f"{HLAB[h]:>18s}" for h in HORIZONS))
    for name, x in block.items():
        cells = []
        for h in HORIZONS:
            rho, t, n = corr_tstat_nw(x, fut_x[f"R{h}"], h - 1)
            flag = "*" if abs(t) > 2 else " "
            cells.append(f"{rho:+.2f} ({t:+.2f}){flag} [n={n}]")
        print(f"{name:32s}" + "".join(f"{c:>18s}" for c in cells))
        scells = [f"{SLIDE[name][h][0]:+.2f} ({SLIDE[name][h][1]:+.2f})"
                  for h in HORIZONS]
        print(f"{'  slide':32s}" + "".join(f"{c:>18s}" for c in scells))
    print("\n* = |t| > 2, statistically significant.")


if __name__ == "__main__":
    main()
