"""
Earnings-yield factor: SEC EDGAR fundamentals + factor construction.

Characteristic: trailing-twelve-month net income / market cap (E/P), the
trailing analogue of the cfm alphas' forward-estimate/cap sorts
(anl4_fs_detail_estimates_advanced_af_nd_ebit_mean/cap,
 anl4_fs_detail_estimates_advanced_af_nd_ptp_mean/cap).

Point-in-time: quarterly NetIncomeLoss values are used only once their fiscal
period end is at least 90 days before the portfolio formation date (reporting
lag -- no lookahead bias). Market cap uses month-end price times the latest
known shares outstanding.

Stage 1 (fetch_edgar_cache): download per-concept XBRL JSONs (free, no key).
Stage 2 (build_ey_panel): merge with data/monthly_panel.csv -> data/ey_panel.csv.
"""
import json
import os
import time
import pandas as pd
import requests

from data import TICKERS  # noqa: F401  (same universe)

UA = {"User-Agent": "CFM301CourseProject contact@example.com"}
RAW = "data/raw_edgar"
LAG_DAYS = 90  # reporting lag: no lookahead bias


def _get(url, retries=3, timeout=20):
    last = None
    for a in range(retries):
        try:
            r = requests.get(url, headers=UA, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                raise RuntimeError(f"HTTP 404 (no retry): {url}")
            last = f"HTTP {r.status_code}"
        except RuntimeError:
            raise
        except Exception as e:  # noqa: BLE001
            last = repr(e)
        time.sleep(2 * (a + 1))
    raise RuntimeError(f"EDGAR fetch failed: {url} ({last})")


def ticker_cik_map():
    j = _get("https://www.sec.gov/files/company_tickers.json")
    return {v["ticker"]: str(v["cik_str"]).zfill(10) for v in j.values()}


def fetch_edgar_cache(tickers=TICKERS, concepts=(("us-gaap", "NetIncomeLoss"),
                                                 ("dei",
                                                  "EntityCommonStockSharesOutstanding"))):
    """Download per-concept JSONs into data/raw_edgar (gitignored cache)."""
    import concurrent.futures
    os.makedirs(RAW, exist_ok=True)
    cmap = ticker_cik_map()
    missing = [t for t in tickers if t not in cmap]
    if missing:
        print(f"  no CIK for: {missing}")
    jobs = []
    for t in tickers:
        if t not in cmap:
            continue
        for ns, concept in concepts:
            path = f"{RAW}/{t}__{concept}.json"
            if os.path.exists(path):
                continue
            url = (f"https://data.sec.gov/api/xbrl/companyconcept/"
                   f"CIK{cmap[t]}/{ns}/{concept}.json")
            jobs.append((t, concept, url, path))

    def one(job):
        t, concept, url, path = job
        try:
            j = _get(url)
            with open(path, "w") as f:
                json.dump(j, f)
            return (t, concept, "ok")
        except RuntimeError as e:
            return (t, concept, f"FAILED ({e})")

    ok, failed = 0, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for t, concept, res in ex.map(one, jobs):
            if res == "ok":
                ok += 1
            else:
                failed.append(f"{t}/{concept}: {res}")
    print(f"  fetched {ok} new concept files into {RAW}/")
    for f in failed[:20]:
        print("  " + f)
    if len(failed) > 20:
        print(f"  ... +{len(failed) - 20} more failures")


def _quarterly_ttm(ni_df, cutoff):
    """TTM net income from 10-Q quarters with period-end <= cutoff."""
    q = ni_df[(ni_df["form"] == "10-Q") & (ni_df["end"] <= cutoff)]
    q = q.sort_values("end").drop_duplicates("end", keep="last")
    if len(q) < 4:
        return float("nan")
    return float(q["val"].iloc[-4:].sum())


def build_ey_panel(panel_path="data/monthly_panel.csv",
                   out_path="data/ey_panel.csv"):
    """Merge EDGAR fundamentals with the price panel -> EY panel."""
    panel = pd.read_csv(panel_path, parse_dates=["date"])
    # Yahoo-written dates carry a tz suffix that parse_dates may leave as
    # strings -> normalize to tz-naive month-end dates.
    panel["date"] = pd.to_datetime(
        pd.to_datetime(panel["date"], utc=True).dt.date)
    cmap = ticker_cik_map()
    rows = []
    skipped = []
    for t in panel["ticker"].unique():
        if t not in cmap:
            continue
        p_ni, p_sh = f"{RAW}/{t}__NetIncomeLoss.json", \
                     f"{RAW}/{t}__EntityCommonStockSharesOutstanding.json"
        if not (os.path.exists(p_ni) and os.path.exists(p_sh)):
            skipped.append((t, "missing concept file"))
            continue
        ni_units = json.load(open(p_ni)).get("units", {}).get("USD", [])
        if not ni_units:
            skipped.append((t, "empty NetIncomeLoss units"))
            continue
        ni = pd.DataFrame(ni_units)[["end", "val", "form", "fp"]]
        ni["end"] = pd.to_datetime(ni["end"])
        sh = pd.DataFrame(
            json.load(open(p_sh))["units"]["shares"])[["end", "val"]]
        sh["end"] = pd.to_datetime(sh["end"])
        sub = panel[panel["ticker"] == t].sort_values("date")
        for _, r in sub.iterrows():
            cutoff = r["date"] - pd.Timedelta(days=LAG_DAYS)
            ttm = _quarterly_ttm(ni, cutoff)
            known = sh[sh["end"] <= r["date"]]
            shares = float(known.sort_values("end")["val"].iloc[-1]) \
                if len(known) else float("nan")
            mcap = r["price"] * shares
            ey = ttm / mcap if mcap > 0 else float("nan")
            rows.append({"date": r["date"], "ticker": t,
                         "ey": ey, "mcap": mcap, "ttm_ni": ttm})
    ey = pd.DataFrame(rows)
    ey.to_csv(out_path, index=False)
    cov = ey.groupby("date")["ey"].agg(["count", "median"])
    print(f"Wrote {out_path}: {len(ey)} rows; "
          f"avg tickers/month with EY: {cov['count'].mean():.0f}; "
          f"{ey['date'].min().date()} to {ey['date'].max().date()}")
    if skipped:
        print(f"Skipped {len(skipped)} tickers: "
              f"{[t for t, _ in skipped][:12]}")
    return ey


if __name__ == "__main__":
    import sys
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("fetch", "all"):
        fetch_edgar_cache()
    if stage in ("build", "all"):
        build_ey_panel()
