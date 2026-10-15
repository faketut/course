"""
Data sourcing and cleaning for CFM301 Project 2.

Downloads daily bars (adjusted close + volume) for a fixed universe of liquid
US stocks from Yahoo Finance's v8 chart API, aggregates to a month-end panel,
and writes a trimmed CSV that the analysis reads (no downloads at run time).

Returns are TOTAL returns: computed from adjusted closes, which reinvest
dividends and are split-adjusted -- the CRSP RET analogue (not RETX, not raw
PRC). Dollar volume (volume x adjclose) is used for sorts because it is
robust to stock splits.

Survivorship note: the universe is a fixed list of large-cap stocks with long
histories; delisted stocks are not included. This is disclosed in the report.
"""
import time
import pandas as pd
import requests

# Fixed universe: large-cap US stocks, mostly listed since ~2000.
TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "BRK-B", "JPM", "V",
    "XOM", "UNH", "MA", "PG", "JNJ", "HD", "CVX", "MRK", "LLY", "ABBV",
    "COST", "PEP", "WMT", "BAC", "DIS", "KO", "PFE", "TMO", "CSCO", "ABT",
    "CRM", "LIN", "DHR", "NEE", "TXN", "ORCL", "QCOM", "HON", "AMGN",
    "IBM", "GE", "CAT", "BA", "MMM", "RTX", "LMT", "AXP", "GS", "MS",
    "C", "USB", "PNC", "SCHW", "BLK", "SPGI", "CME", "ICE", "AON",
    "AFL", "MET", "PRU", "AIG", "TRV", "CB", "ADP", "PAYX", "GWW", "EMR",
    "ETN", "PH", "ROK", "ITW", "DOV", "CMI", "DE", "NSC", "UNP", "CSX",
    "FDX", "UPS", "ADBE", "INTU", "AMD", "INTC", "MU", "ADI", "LRCX",
    "AMAT", "KLAC", "NXPI", "AVGO", "TTWO", "NFLX",
    "SBUX", "MCD", "NKE", "TGT", "LOW", "TJX", "ROST", "AZO", "ORLY",
    "CMG", "DRI", "YUM", "MAR", "HLT", "BKNG",
]
PERIOD1 = 946684800            # 2000-01-01
PERIOD2 = 1790625600           # ~2026-09
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def fetch_daily(ticker, retries=6):
    """Daily adjclose + volume via Yahoo v8 chart API, paced + retried."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?interval=1d&period1={PERIOD1}&period2={PERIOD2}")
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code == 200:
                j = r.json()["chart"]["result"][0]
                ts = pd.to_datetime(j["timestamp"], unit="s", utc=True)
                adj = j["indicators"]["adjclose"][0]["adjclose"]
                vol = j["indicators"]["quote"][0].get("volume")
                df = pd.DataFrame({"adjclose": adj, "volume": vol},
                                  index=ts.tz_convert("America/Toronto"))
                df = df.dropna(subset=["adjclose"])
                return df
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001 - transient network errors
            last = repr(e)
        time.sleep(4 * (attempt + 1))
    raise RuntimeError(f"Yahoo download failed for {ticker}: {last}")


def to_monthly_panel(daily):
    """Month-end panel: total return, avg daily dollar volume, month-end price."""
    daily = daily.copy()
    daily["dvol"] = daily["volume"] * daily["adjclose"]  # split-robust
    g = daily.groupby(pd.Grouper(freq="ME"))
    px = g["adjclose"].last()
    ret = px.pct_change()
    out = pd.DataFrame({
        "ret": ret,
        "price": px,
        "dvol_avg": g["dvol"].mean(),
        "n_days": g["adjclose"].size(),
    }).dropna(subset=["ret"])
    # Drop the still-incomplete current month.
    cur = pd.Timestamp.now(tz="America/Toronto").to_period("M")
    out = out[out.index.to_period("M") < cur]
    return out


def build_dataset(out_path="data/monthly_panel.csv"):
    frames = []
    failed = []
    for i, tkr in enumerate(TICKERS):
        try:
            daily = fetch_daily(tkr)
            m = to_monthly_panel(daily)
            m["ticker"] = tkr
            frames.append(m)
            print(f"  {tkr}: OK ({len(m)} months)", flush=True)
        except RuntimeError as e:
            failed.append(tkr)
            print(f"  {tkr}: FAILED ({e})", flush=True)
        if i < len(TICKERS) - 1:
            time.sleep(2)
    panel = pd.concat(frames)
    panel.index.name = "date"
    panel = panel.reset_index().set_index(["date", "ticker"]).sort_index()
    panel.to_csv(out_path)
    print(f"Wrote {out_path}: {panel.shape[0]} rows, "
          f"{panel.index.get_level_values('ticker').nunique()} tickers, "
          f"{panel.index.get_level_values('date').min().date()} to "
          f"{panel.index.get_level_values('date').max().date()}")
    if failed:
        print(f"Failed tickers ({len(failed)}): {failed}")
    return panel


if __name__ == "__main__":
    build_dataset()
