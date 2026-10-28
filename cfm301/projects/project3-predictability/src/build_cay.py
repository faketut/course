"""
Reconstruct the Lettau-Ludvigson (2001) consumption-wealth ratio (cay).

cay is NOT a published series; it is the cointegrating residual of
  c_t = const + beta_a * a_t + beta_y * y_t + residual
where c = log real per-capita consumption (nondurables + services),
a = log real per-capita asset wealth (household net worth),
y = log real per-capita labor income (compensation of employees).

Method (following Lettau-Ludvigson 2001): Stock-Watson DOLS with 8 leads
and lags of (da, dy) to estimate (const, beta_a, beta_y) on the interior
sample; the residual series is then computed for ALL quarters from those
coefficients (leads/lags are only needed for estimation, not for the
residual itself). Quarterly cay is forward-filled to month-ends for the
monthly panel.

FRED sources (all downloaded to data/):
  PCND, PCES  : PCE nondurable goods / services, nominal, monthly
  PCEPI       : PCE price index, monthly (deflator)
  TNWBSHNO    : households net worth, nominal, quarterly
  W209RC1     : compensation of employees, nominal, monthly
  POPTHM      : population, thousands, monthly
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))


def fred(name):
    df = pd.read_csv(os.path.join(DATA, f"fred_{name}.csv"))
    df.columns = ["date", name]
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date").sort_index()[name]


def to_quarter(s):
    return s.resample("QE").mean()


def main():
    pcnd = to_quarter(fred("PCND"))
    pces = to_quarter(fred("PCES"))
    pcepi = to_quarter(fred("PCEPI"))
    wealth = fred("TNWBSHNO").resample("QE").last()
    comp = to_quarter(fred("W209RC1"))
    pop = to_quarter(fred("POPTHM"))

    q = pd.DataFrame({
        "c_nom": pcnd + pces,
        "p": pcepi,
        "a_nom": wealth,
        "y_nom": comp,
        "pop": pop,
    }).dropna()
    # real per-capita levels (deflate by PCE price index, divide by pop)
    q["c"] = np.log((q["c_nom"] / q["p"]) / q["pop"])
    q["a"] = np.log((q["a_nom"] / q["p"]) / q["pop"])
    q["y"] = np.log((q["y_nom"] / q["p"]) / q["pop"])
    q = q[["c", "a", "y"]].dropna()

    # DOLS: c ~ const + a + y + leads/lags of da, dy (8 each side)
    K = 8
    da, dy = q["a"].diff(), q["y"].diff()
    X = pd.DataFrame({"const": 1.0, "a": q["a"], "y": q["y"]})
    for k in range(-K, K + 1):
        if k == 0:
            continue
        X[f"da_{k:+d}"] = da.shift(-k)  # lead/lag: shift(-k) = value k ahead
        X[f"dy_{k:+d}"] = dy.shift(-k)
    d = pd.concat([q["c"], X], axis=1).dropna()
    res = sm.OLS(d["c"].values, d[[c for c in X.columns]].values).fit()
    names = list(X.columns)
    beta = dict(zip(names, res.params))
    print(f"DOLS on {len(d)} quarters "
          f"({d.index.min().date()} -> {d.index.max().date()}): "
          f"const={beta['const']:.4f}, beta_a={beta['a']:.4f}, "
          f"beta_y={beta['y']:.4f}")
    print(f"(Lettau-Ludvigson 2001 published: beta_a ~ 0.30, beta_y ~ 0.60)")

    cay_q = q["c"] - beta["const"] - beta["a"] * q["a"] - beta["y"] * q["y"]
    cay_q = cay_q.rename("cay")
    # quarter-end -> month-end panel (forward-fill within the quarter)
    monthly = pd.DataFrame(index=pd.date_range(
        cay_q.index.min(), pd.Timestamp("2026-10-31"), freq="ME"))
    monthly["cay"] = cay_q.reindex(monthly.index, method="ffill")
    monthly.to_csv(os.path.join(DATA, "cay_monthly.csv"))
    print(f"cay_monthly.csv: {len(monthly)} months, "
          f"{monthly['cay'].count()} non-null, "
          f"{monthly.index.min().date()} -> {monthly.index.max().date()}")


if __name__ == "__main__":
    main()
