"""Helpers for Project 5 (mutual fund fees).

- factor_reg: OLS factor regression; annualized alpha, t-stat, betas,
  tracking error (residual std), information ratio, R^2.
- constrained_benchmark: Sharpe-style regression of a fund's excess
  returns on index-fund excess returns, loadings >= 0 and summing to 1;
  alpha is the mean return over the replicating portfolio, with a
  tracking-error-based t-statistic.
- winsorize: clip to [q_lo, q_hi] quantiles, returning (clipped, n_clipped).
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize


def winsorize(s, lo=0.01, hi=0.99):
    s = s.dropna()
    ql, qh = s.quantile([lo, hi])
    clipped = s.clip(ql, qh)
    return clipped, int(((s < ql) | (s > qh)).sum())


def factor_reg(y, X):
    """OLS of y (excess returns) on X (factors, with const added).

    Returns dict with monthly alpha, t-stat, betas, residual std (monthly
    tracking error), R^2 and n. Annualized alpha = monthly x 12,
    annualized tracking error = monthly x sqrt(12).
    """
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    res = sm.OLS(d["y"], sm.add_constant(d[X.columns])).fit()
    resid = res.resid
    te_m = float(resid.std(ddof=1))
    alpha_m = float(res.params["const"])
    return {
        "alpha_m": alpha_m, "alpha_ann": alpha_m * 12,
        "t_alpha": float(res.tvalues["const"]),
        "te_m": te_m, "te_ann": te_m * np.sqrt(12),
        "ir": (alpha_m * 12) / (te_m * np.sqrt(12)),
        "r2": float(res.rsquared), "n": len(d),
        "betas": {c: float(res.params[c]) for c in X.columns},
        "resid": resid,
    }


def constrained_benchmark(y, X):
    """Regress y on index funds X with loadings >= 0, summing to 1.

    Minimizes sum of squared residuals over (alpha, w). Alpha against
    the benchmark is the mean of (y - Xw); its t-statistic uses the
    tracking error of that difference (SE = TE / sqrt(n)).
    Returns dict with weights, alpha_ann, t_alpha, tracking error,
    R^2 and n.
    """
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    yv = d["y"].to_numpy()
    Xv = d[X.columns].to_numpy()
    k = Xv.shape[1]

    def sse(p):
        alpha, w = p[0], p[1:]
        return float(np.sum((yv - alpha - Xv @ w) ** 2))

    cons = [{"type": "eq", "fun": lambda p: np.sum(p[1:]) - 1.0}]
    bounds = [(None, None)] + [(0.0, 1.0)] * k
    p0 = np.concatenate([[0.0], np.full(k, 1.0 / k)])
    sol = minimize(sse, p0, method="SLSQP", bounds=bounds,
                   constraints=cons, options={"maxiter": 1000, "ftol": 1e-12})
    alpha, w = float(sol.x[0]), sol.x[1:]
    diff = yv - Xv @ w
    te_m = float(diff.std(ddof=1))
    n = len(yv)
    return {
        "weights": {c: float(wi) for c, wi in zip(X.columns, w)},
        "alpha_m": alpha, "alpha_ann": alpha * 12,
        "t_alpha": float(alpha / (te_m / np.sqrt(n))),
        "te_m": te_m, "te_ann": te_m * np.sqrt(12),
        "ir": (alpha * 12) / (te_m * np.sqrt(12)),
        "r2": float(1.0 - np.var(diff, ddof=1) / np.var(yv, ddof=1)),
        "n": n,
    }
