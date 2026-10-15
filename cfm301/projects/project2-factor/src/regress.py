"""
Regression toolkit for CFM301 Project 2.

OLS with Newey-West (HAC) standard errors, factor-premium statistics, and
spanning tests. All t-statistics reported in this project come from here.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm


def ols_nw(y, X, lags=None, add_const=True):
    """OLS with Newey-West standard errors.

    Returns dict with coefficients, HAC standard errors, t-stats, p-values,
    R-squared, adjusted R-squared, and number of observations.
    """
    y = pd.Series(y).dropna()
    X = pd.DataFrame(X).loc[y.index].dropna()
    y = y.loc[X.index]
    if add_const:
        X = sm.add_constant(X, has_constant="add")
    n = len(y)
    if lags is None:
        lags = int(np.floor(4 * (n / 100) ** (2 / 9)))  # Newey-West (1994) rule
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return {
        "params": fit.params,
        "bse": fit.bse,
        "tstats": fit.tvalues,
        "pvalues": fit.pvalues,
        "rsquared": fit.rsquared,
        "rsquared_adj": fit.rsquared_adj,
        "nobs": int(fit.nobs),
        "nw_lags": lags,
    }


def regression_table(results, names=None):
    """Pretty DataFrame: coefficient, t-stat (Newey-West), R^2."""
    idx = results["params"].index
    tab = pd.DataFrame({
        "coef": results["params"],
        "t-stat (NW)": results["tstats"],
    }, index=idx)
    tab.index.name = "variable"
    tab.attrs["rsquared"] = results["rsquared"]
    tab.attrs["rsquared_adj"] = results["rsquared_adj"]
    tab.attrs["nobs"] = results["nobs"]
    if names:
        tab = tab.rename(index=names)
    return tab


def factor_premium_stats(f, freq=12):
    """Annualized mean, vol, Sharpe and t-stat of the mean for a factor."""
    f = pd.Series(f).dropna()
    mu = f.mean() * freq
    vol = f.std() * np.sqrt(freq)
    sharpe = mu / vol if vol > 0 else np.nan
    # t-stat of the mean with Newey-West SEs (regress on constant)
    t = ols_nw(f, pd.DataFrame(index=f.index), lags=None)["tstats"].iloc[0]
    return {"mean_ann": mu, "vol_ann": vol, "sharpe": sharpe,
            "tstat_mean": t, "nobs": len(f)}


def spanning_alpha(candidate, benchmarks, lags=None):
    """Regress candidate factor on benchmark factors.

    A significant intercept means the candidate is not spanned by (adds
    explanatory power beyond) the benchmarks.
    """
    res = ols_nw(candidate, benchmarks, lags=lags)
    return {
        "alpha": res["params"].iloc[0],
        "alpha_tstat": res["tstats"].iloc[0],
        "alpha_pvalue": res["pvalues"].iloc[0],
        "betas": res["params"].iloc[1:],
        "betas_tstats": res["tstats"].iloc[1:],
        "rsquared": res["rsquared"],
        "nobs": res["nobs"],
    }


def winsorize(s, lower=0.01, upper=0.99):
    """Winsorize a Series at the given quantiles; returns (winsorized, n_hit)."""
    lo, hi = s.quantile([lower, upper])
    n_hit = int(((s < lo) | (s > hi)).sum())
    return s.clip(lo, hi), n_hit
