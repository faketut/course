"""
Predictability helpers for Project 3.

- future_returns: overlapping compounded returns over h months.
- corr_tstat_nw: correlation between predictor level at t and future return,
  with a Newey-West t-statistic. Implementation: standardize predictor and
  future return, run OLS; the slope equals the correlation, and the NW
  t-statistic of the slope is the correlation's t-statistic. This is the
  standard way to attach an overlap-robust t-stat to a correlation.
- winsorize: clip to [q_lo, q_hi] quantiles.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm


def future_returns(r, horizons=(3, 12, 24, 60)):
    """Overlapping compounded returns: R(t,h) = prod(1+r_{t+1..t+h}) - 1.

    r: monthly return Series (decimal), month-end indexed.
    Returns DataFrame with columns f"R{h}" (h in months).
    Method: rolling h-month log-return sum is backward-looking
    ([t-h+1, t]); shifting it by -h months gives the forward window
    [t+1, t+h]. (An earlier version reversed the series and shifted by -h,
    which double-shifted the window to [t+h, t+2h-1]; fixed 2026-10-28.)
    """
    out = {}
    logr = np.log1p(r)
    for h in horizons:
        fwd = logr.rolling(h).sum().shift(-h)
        out[f"R{h}"] = np.expm1(fwd)
    return pd.DataFrame(out, index=r.index)


def corr_tstat_nw(x, y, nw_lag):
    """Correlation of x and y with a Newey-West t-statistic.

    Drops pairwise NaN. Standardizes both series, OLS slope (= correlation),
    NW covariance with `nw_lag` lags. Returns (rho, tstat, nobs).
    """
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(d) < 30:
        return np.nan, np.nan, len(d)
    xs = (d["x"] - d["x"].mean()) / d["x"].std()
    ys = (d["y"] - d["y"].mean()) / d["y"].std()
    X = sm.add_constant(xs.values)
    res = sm.OLS(ys.values, X).fit(
        cov_type="HAC", cov_kwds={"maxlags": nw_lag, "use_correction": True})
    return float(d["x"].corr(d["y"])), float(res.tvalues[1]), len(d)


def winsorize(s, lo=0.01, hi=0.99):
    ql, qh = s.quantile([lo, hi])
    return s.clip(ql, qh), ql, qh
