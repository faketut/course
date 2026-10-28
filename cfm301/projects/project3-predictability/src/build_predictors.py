"""
Build the monthly predictor panel for Project 3 from FRED + Shiller downloads.

Sources (all files already in data/):
  FRED (fredgraph.csv downloads, no key):
    DGS10, DGS3MO  -> term spread (month-end, pp)
    BAA, AAA       -> credit spread (monthly, pp)
    CPIAUCSL       -> CPI inflation, y/y % (monthly)
    INDPRO         -> industrial production growth, y/y %
    UNRATE         -> unemployment rate, % (level)
    DCOILWTICO     -> WTI oil price, month-end $; growth y/y %
    VIXCLS         -> VIX, month-end
    TB3MS          -> 3-month T-bill, % ann. (risk-free rate for excess returns)
  Shiller (ie_data.xls, Yale):
    P, D, E, CAPE  -> dividend yield D/P, earnings yield E/P, P/E10 = CAPE

Output: data/predictors_monthly.csv, monthly, calendar month-end index.
Daily FRED series are aggregated to month-end values.
"""
import os
import numpy as np
import pandas as pd

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))


def fred(name):
    df = pd.read_csv(os.path.join(DATA, f"fred_{name}.csv"))
    df.columns = ["date", name]
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    df = df[~df.index.duplicated(keep="last")]
    # FRED monthly series are dated the 1st; daily series any day.
    # Normalize everything to calendar month-end for exact joins.
    return df[name].resample("ME").last()


def yoy_pct(s):
    return s.pct_change(12) * 100


def main():
    # ---- FRED ----
    dgs10 = fred("DGS10")
    dgs3mo = fred("DGS3MO")
    baa = fred("BAA")
    aaa = fred("AAA")
    cpi = fred("CPIAUCSL")
    indpro = fred("INDPRO")
    unrate = fred("UNRATE")
    oil = fred("DCOILWTICO")
    vix = fred("VIXCLS")
    tb3ms = fred("TB3MS")

    panel = pd.DataFrame({
        "term_spread": dgs10 - dgs3mo,
        "credit_spread": baa - aaa,
        "inflation": yoy_pct(cpi),
        "ip_growth": yoy_pct(indpro),
        "unemp": unrate,
        "oil": oil,
        "oil_growth": yoy_pct(oil),
        "vix": vix,
        "rf_ann": tb3ms,  # % per year; monthly rf = rf_ann / 1200
        "rf_level": tb3ms,  # slide predictor: risk-free rate level
    })

    # ---- GDP: quarterly real GDP (GDPC1) -> past-year growth, ffill to months
    # Read raw (do NOT use fred(), which resamples to month-end): FRED dates
    # GDPC1 at the 1st of each quarter's first month.
    gdp_raw = pd.read_csv(os.path.join(DATA, "fred_GDPC1.csv"))
    gdp_raw.columns = ["date", "GDPC1"]
    gdp_raw["date"] = pd.to_datetime(gdp_raw["date"])
    gdp_raw = gdp_raw.set_index("date").sort_index()["GDPC1"]
    gdp_yoy = gdp_raw.pct_change(4) * 100  # y/y %, quarterly
    # quarter-end month for each observation, then forward-fill across months
    gdp_yoy.index = gdp_yoy.index.to_period("Q").to_timestamp("Q")
    panel["gdp_growth"] = gdp_yoy.reindex(panel.index, method="ffill")

    # ---- cay (Lettau-Ludvigson reconstruction, see src/build_cay.py) ----
    cay_path = os.path.join(DATA, "cay_monthly.csv")
    if os.path.exists(cay_path):
        cay = pd.read_csv(cay_path, index_col=0, parse_dates=True)["cay"]
        panel = panel.join(cay, how="outer")

    # ---- Shiller ----
    sh = pd.read_excel(os.path.join(DATA, "shiller_ie_data.xls"),
                       sheet_name="Data", header=7, engine="xlrd")
    sh = sh[["Date", "P", "D", "E", "CAPE"]].copy()
    sh = sh[pd.to_numeric(sh["Date"], errors="coerce").notna()]
    sh["Date"] = sh["Date"].astype(float)
    year = sh["Date"].astype(int)
    month = np.round((sh["Date"] - year) * 100).astype(int)
    # Shiller Date YYYY.MM = that calendar month -> map to month-end so it
    # joins exactly with the FRED month-end panel
    sh["date"] = pd.to_datetime(year * 10000 + month * 100 + 1,
                                format="%Y%m%d") + pd.offsets.MonthEnd(0)
    sh = sh.set_index("date").sort_index()
    sh = sh[["P", "D", "E", "CAPE"]].apply(pd.to_numeric, errors="coerce")
    # Shiller P/D/E are real (CPI-deflated) levels; ratios are unit-free
    sh["div_yield"] = sh["D"] / sh["P"] * 100  # %
    sh["earn_yield"] = sh["E"] / sh["P"] * 100  # %
    sh["pe10"] = sh["CAPE"]
    panel = panel.join(sh[["div_yield", "earn_yield", "pe10"]], how="outer")
    panel = panel.sort_index()

    panel.to_csv(os.path.join(DATA, "predictors_monthly.csv"))
    print(f"predictors_monthly.csv: {len(panel)} months, "
          f"{panel.index.min().date()} -> {panel.index.max().date()}")
    print(panel.count().to_string())


if __name__ == "__main__":
    main()
