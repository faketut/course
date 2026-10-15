"""
Build CRSP/Compustat panels for Project 2 from the WRDS CSV pulls.

Reads
  data/wrds_crsp_msf.csv      (PERMNO,DATE,RET,PRC,VOL,SHROUT,CFACPR,TICKER,SHRCD,EXCHCD)
  data/wrds_comp_fundaq.csv   (gvkey,datadate,fyearq,fqtr,rdq,niq,oibdpq,atq,ceqq,cshoq)
  data/wrds_ccm_link.csv      (gvkey,permno,linkdt,linkenddt,linkprim,linktype)

Writes (same schema as the Yahoo/EDGAR proxy pipeline)
  data/monthly_panel.csv  date,ticker,ret,price,dvol_avg,n_days
  data/ey_panel.csv       date,ticker,ey,mcap,ttm_ni
Existing proxy files are backed up to monthly_panel_yahoo.csv / ey_panel_edgar.csv.

Notes
- "ticker" holds the CRSP PERMNO (as string): unique per (date, id), unlike
  exchange tickers which can be recycled across firms.
- RET is the CRSP total return (dividends + splits included); PRC is the
  month-end closing price (abs() undoes the bid/ask-average sign convention).
- Point-in-time: TTM net income = sum of niq over the latest 4 fiscal quarters
  whose report date rdq <= formation month-end (no lookahead).
  Market cap = |PRC| * SHROUT * 1000  (SHROUT is in thousands of shares).
- price = |PRC|; dvol_avg ~= VOL*|PRC|/21 (approx. avg daily dollar volume);
  n_days is NaN (a monthly file has no daily counts). These three columns are
  unused by run_project.py; they exist for schema compatibility with the proxy.
"""
import os
import shutil
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
DATA = os.path.abspath(DATA)


def ymd(s):
    return pd.to_datetime(s, format="%Y%m%d")


def load_msf():
    m = pd.read_csv(os.path.join(DATA, "wrds_crsp_msf.csv"),
                    usecols=["PERMNO", "DATE", "RET", "PRC", "VOL", "SHROUT"],
                    dtype={"RET": str})
    # RET="C" (first sample month of a permno, no prior price) or "" -> NaN
    m["RET"] = pd.to_numeric(m["RET"], errors="coerce")
    m["date"] = ymd(m["DATE"])
    m["permno"] = m["PERMNO"].astype(int)
    m["prc_abs"] = m["PRC"].abs()
    # monthly panel; keep raw RET (NaN where CRSP has none -- dropped later)
    px = pd.DataFrame({
        "date": m["date"],
        "ticker": m["permno"].astype(str),
        "ret": m["RET"],
        "price": m["prc_abs"],
        "dvol_avg": m["VOL"] * m["prc_abs"] / 21.0,
        "n_days": np.nan,
        "permno": m["permno"],
        "mcap": m["prc_abs"] * m["SHROUT"] * 1000.0,
    })
    px = px.sort_values(["permno", "date"]).reset_index(drop=True)
    return px


def load_link():
    l = pd.read_csv(os.path.join(DATA, "wrds_ccm_link.csv"),
                    dtype={"gvkey": str})
    l["permno"] = l["permno"].astype(int)
    l["linkdt"] = ymd(l["linkdt"])
    # missing linkenddt -> still linked
    l["linkenddt"] = pd.to_datetime(l["linkenddt"], format="%Y%m%d",
                                    errors="coerce").fillna(pd.Timestamp("2099-12-31"))
    return l[["gvkey", "permno", "linkdt", "linkenddt"]]


def load_fundaq(link):
    q = pd.read_csv(os.path.join(DATA, "wrds_comp_fundaq.csv"),
                    dtype={"gvkey": str},
                    usecols=["gvkey", "datadate", "rdq", "niq"])
    q = q.dropna(subset=["niq", "rdq"]).copy()
    q["datadate"] = ymd(q["datadate"].astype(int))
    q["rdq"] = ymd(q["rdq"].astype(int))
    q = q.merge(link, on="gvkey", how="inner")
    q = q[(q["datadate"] >= q["linkdt"]) & (q["datadate"] <= q["linkenddt"])]
    q = q.drop_duplicates(subset=["permno", "datadate"])
    q = q.sort_values(["permno", "datadate"]).reset_index(drop=True)
    # TTM net income: rolling sum of the latest 4 quarters, known at rdq
    roll = q.groupby("permno")["niq"].rolling(4, min_periods=4).sum()
    q["ttm"] = roll.reset_index(level=0, drop=True).values
    ttm = (q.dropna(subset=["ttm"])
             .sort_values(["permno", "rdq", "datadate"])
             .drop_duplicates(subset=["permno", "rdq"], keep="last")
             [["permno", "rdq", "ttm"]]
             .rename(columns={"rdq": "known"}))
    return ttm.sort_values("known").reset_index(drop=True)


def main():
    px = load_msf()
    print(f"msf panel: {len(px)} rows, {px['permno'].nunique()} permnos, "
          f"{px['date'].min().date()} -> {px['date'].max().date()}")

    link = load_link()
    ttm = load_fundaq(link)
    print(f"ttm quarters: {len(ttm)} rows, {ttm['permno'].nunique()} permnos")

    # point-in-time asof: latest quarter with rdq <= month-end, per permno
    left = px[["permno", "date"]].sort_values("date")
    panel = pd.merge_asof(left, ttm, left_on="date", right_on="known",
                          by="permno", direction="backward")
    px = px.merge(panel[["permno", "date", "ttm"]], on=["permno", "date"],
                  how="left")
    # niq is in $millions (Compustat); mcap in $ -> convert
    px["ttm_ni"] = px["ttm"] * 1e6
    px["ey"] = px["ttm_ni"] / px["mcap"]

    cov = px["ey"].notna().mean()
    print(f"EY coverage: {cov:.1%} of permno-months")

    # back up the Yahoo/EDGAR proxy files once (never overwrite a backup)
    for name, backup in [("monthly_panel.csv", "monthly_panel_yahoo.csv"),
                         ("ey_panel.csv", "ey_panel_edgar.csv")]:
        src = os.path.join(DATA, name)
        dst = os.path.join(DATA, backup)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"backed up {name} -> {backup}")

    monthly = px[["date", "ticker", "ret", "price", "dvol_avg", "n_days"]]
    monthly.to_csv(os.path.join(DATA, "monthly_panel.csv"), index=False)
    ey = px[["date", "ticker", "ey", "mcap", "ttm_ni"]].rename(
        columns={"mcap": "mcap"})
    ey.to_csv(os.path.join(DATA, "ey_panel.csv"), index=False)
    print("wrote data/monthly_panel.csv and data/ey_panel.csv (WRDS)")


if __name__ == "__main__":
    main()
