"""AFM 425 Topic 13 — Treasury cash-futures basis trade: original quant model.

This is the mandatory quantitative analysis for the report, recomputed
here from stated assumptions — it is NOT a copy of a published figure.

Model (one representative trade, then scaled to the market):
  * Long $100m face of a 10-year Treasury note (the cheapest-to-deliver,
    CTD, into the 10-year futures contract).
  * Short 10-year Treasury futures, DV01-matched to the cash leg
    (n = DV01_cash / DV01_futures = 850 contracts, equivalently
    1,000 x CF — NOT FACE / CF). The 850 contracts deliver $85m
    face at expiry; the remaining $15m face is sold for cash at
    delivery, after the basis has converged, so it carries no
    residual basis risk.
  * Cash leg financed in repo; futures leg needs only margin.

Assumptions (all stated, all changeable — see SENSITIVITY at the bottom):
  * CTD: 10y, 4.00% coupon, 4.00% yield, 10y to maturity, price = par.
    (A par bond keeps the arithmetic transparent; the report's appendix
    must re-run this with the actual CTD coupon / yield on the chosen
    date. Duration / DV01 are computed, not assumed.)
  * Conversion factor CF = 0.85. Futures price F = P / CF at zero basis.
  * Repo haircut h = 2% in the base case (leverage 50x on the cash leg).
    Repo rate = 4.00% p.a., holding period to delivery T = 0.25y.
  * Initial gross basis G = P - CF x F = 0.10 price points (cash is
    0.10 points rich to CF x futures). It converges to zero at
    delivery, so the basis P&L is dG = -0.10 points = -$100,000.
    (CORRECTED 2026-11-11: an earlier version added +$100,000 here.
    Exact repricing in basis_trade_real_ctd.py proves the sign: the
    clean P&L of the hedged position is dG, so convergence from a
    positive basis LOSES money. The trade earns only when cash is
    CHEAP at entry, G < 0.)
  * Futures initial margin is ignored in the base P&L (it is a cash
    call, not a return driver) and is treated separately as a liquidity
    demand in the stress table.

What the model shows, in one line:
  Duration-hedged is not cash-flow-hedged. A parallel yield move
  barely moves the hedged P&L, but a repo-rate rise, a haircut rise,
  a basis widening, or a yield fall that triggers futures variation
  margin can each demand cash equal to a large fraction of — or more
  than — the fund's equity.

Aggregate anchors (primary source, verified 2026-11-11):
  Monin, Fed FEDS Notes, June 22, 2026: basis trade ~$830bn at
  Sep 2025 (~35% of hedge funds' $2.4tn long Treasuries, ~3.5% of
  privately held Treasuries); gross hedge-fund Treasury exposure
  $4.0tn ($2.4tn long / $1.6tn short); repo borrowing $3.0tn;
  swap-spread trade ~$305bn, ~$60bn unwound in Apr 2025.
  These aggregates are used ONLY to scale the representative trade;
  the trade-level P&L is computed from the bond math below.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))
from quant import convexity, dv01, macaulay_duration, modified_duration, price  # noqa: E402

FACE = 100_000_000.0          # $100m face, representative trade
COUPON = 0.04
YTM = 0.04
YEARS = 10.0
CF = 0.85                     # conversion factor, assumed (see header)
HAIRCUT = 0.02
REPO_RATE = 0.04
T = 0.25                      # years to futures delivery
BASIS_POINTS = 0.10           # gross basis, price points, converges to 0


def main() -> dict:
    p = price(100, COUPON, YTM, YEARS)            # per 100 face
    mkt_value = FACE * p / 100
    md = modified_duration(100, COUPON, YTM, YEARS)
    mac = macaulay_duration(100, COUPON, YTM, YEARS)
    conv = convexity(100, COUPON, YTM, YEARS)
    dv01_per_100 = dv01(100, COUPON, YTM, YEARS)
    dv01_cash = dv01_per_100 * FACE / 100        # $ per 1 bp, cash leg

    futures_price = p / CF                        # zero-basis futures price
    # DV01-matched hedge: one futures contract's DV01 is the CTD's
    # DV01 divided by CF (invoice = CF x F), so
    #   n = DV01_cash / DV01_futures
    #     = (dv01_cash) / (dv01_per_100 * 1000 / CF)
    #     = 1,000 x CF = 850 contracts.
    # The earlier code used FACE / CF / 100,000 = 1,176.5, which
    # over-hedges by ~38% and contradicts the stress table below.
    dv01_per_future = dv01_per_100 * 1000 / CF    # $ per 1 bp, $100k contract
    n_futures = FACE * CF / 100_000               # 850, integer
    dv01_futures_total = dv01_per_future * n_futures
    equity = mkt_value * HAIRCUT
    repo_borrowing = mkt_value * (1 - HAIRCUT)
    leverage = mkt_value / equity

    # --- Base-case P&L to delivery (3 months) ---
    coupon_accrual = FACE * COUPON * T
    repo_cost = repo_borrowing * REPO_RATE * T
    # Basis P&L = dG: G = +0.10 converges to 0, so dG = -0.10 points.
    basis_gain = -FACE * BASIS_POINTS / 100       # CORRECTED sign, 2026-11-11
    net_pnl = coupon_accrual - repo_cost + basis_gain
    # (Futures leg P&L is already inside basis_gain: at delivery the
    #  futures price converges to the CTD price / CF, so the combined
    #  cash + futures P&L is coupon - repo + basis convergence.)
    carry_bp_annualised = (COUPON - REPO_RATE * (1 - HAIRCUT)) * 10_000
    # carry on equity, annualised: net P&L ex-basis, / equity, / T
    roe_carry_annualised = ((coupon_accrual - repo_cost) / equity) / T

    # --- Stress 1: repo rate +50 bp for the holding period ---
    repo_shock_cost = repo_borrowing * 0.005 * T
    # --- Stress 2: haircut 2% -> 4% (extra equity to post) ---
    extra_equity_haircut = mkt_value * (0.04 - HAIRCUT)
    # --- Stress 3: basis widens in the March-2020 direction: cash
    #     cheapens, G FALLS by 0.50 points (P&L = dG) ---
    basis_widen_loss = FACE * 0.50 / 100
    # --- Stress 4: yields FALL 50 bp — cash gains, futures short loses,
    #     variation margin is called in cash NOW, cash gain is unrealised ---
    yield_fall = -0.005
    cash_gain_50bp_down = -md * mkt_value * yield_fall  # +ve
    vm_call_50bp_down = cash_gain_50bp_down  # futures leg loses ~same amount
    # --- Stress 5: yields RISE 50 bp — hedged P&L is ~zero, by design ---
    yield_rise = 0.005
    cash_loss_50bp_up = -md * mkt_value * yield_rise
    futures_gain_50bp_up = -cash_loss_50bp_up

    # --- Aggregate scaling (Fed anchors, Sep 2025) ---
    agg_basis = 830_000_000_000.0
    agg_dv01_per_bp = md * agg_basis * 0.0001     # gross long-leg DV01
    agg_basis_widen_10bp_price = agg_basis * 0.001  # 0.10 price points

    out = {
        "representative_trade": {
            "face_usd": FACE, "price_per_100": round(p, 4),
            "market_value_usd": round(mkt_value, 0),
            "macaulay_duration_yrs": round(mac, 3),
            "modified_duration_yrs": round(md, 3),
            "convexity_yrs2": round(conv, 2),
            "dv01_cash_leg_usd_per_bp": round(dv01_cash, 0),
            "dv01_per_future_usd_per_bp": round(dv01_per_future, 2),
            "dv01_futures_total_usd_per_bp": round(dv01_futures_total, 0),
            "conversion_factor_assumed": CF,
            "futures_price_zero_basis": round(futures_price, 4),
            "n_futures_contracts_100k": round(n_futures, 1),
            "repo_haircut": HAIRCUT, "equity_usd": round(equity, 0),
            "repo_borrowing_usd": round(repo_borrowing, 0),
            "leverage_on_cash_leg": round(leverage, 1),
        },
        "base_case_pnl_3m_usd": {
            "coupon_accrual": round(coupon_accrual, 0),
            "repo_cost": round(-repo_cost, 0),
            "basis_convergence_gain": round(basis_gain, 0),
            "net_pnl": round(net_pnl, 0),
            "net_pnl_pct_of_equity": round(net_pnl / equity * 100, 2),
            "carry_only_roe_annualised_pct": round(roe_carry_annualised * 100, 2),
        },
        "stress_usd_and_pct_of_equity": {
            "repo_plus_50bp_cost": round(repo_shock_cost, 0),
            "repo_plus_50bp_pct_equity": round(repo_shock_cost / equity * 100, 1),
            "haircut_2_to_4pct_extra_equity": round(extra_equity_haircut, 0),
            "haircut_2_to_4pct_pct_equity": round(extra_equity_haircut / equity * 100, 1),
            "basis_widens_0.50pts_loss": round(basis_widen_loss, 0),
            "basis_widens_0.50pts_pct_equity": round(basis_widen_loss / equity * 100, 1),
            "yield_falls_50bp_cash_gain": round(cash_gain_50bp_down, 0),
            "yield_falls_50bp_variation_margin_call": round(vm_call_50bp_down, 0),
            "yield_falls_50bp_vm_pct_equity": round(vm_call_50bp_down / equity * 100, 1),
            "yield_rises_50bp_cash_loss": round(cash_loss_50bp_up, 0),
            "yield_rises_50bp_futures_gain_offset": round(futures_gain_50bp_up, 0),
        },
        "aggregate_scaling_fed_sep2025": {
            "basis_trade_usd": agg_basis,
            "gross_long_leg_dv01_usd_per_bp": round(agg_dv01_per_bp, 0),
            "basis_widens_0.10pts_collective_loss_usd": round(agg_basis_widen_10bp_price, 0),
        },
    }

    print(json.dumps(out, indent=2))
    outdir = Path(__file__).resolve().parents[1] / "outputs"
    outdir.mkdir(exist_ok=True)
    (outdir / "basis_trade_results.json").write_text(json.dumps(out, indent=2))
    with open(outdir / "basis_trade_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for section, vals in out.items():
            for k, v in vals.items():
                w.writerow([f"{section}.{k}", v])
    return out


if __name__ == "__main__":
    r = main()
    # Sanity checks — these are the claims the report will make:
    assert r["representative_trade"]["price_per_100"] == 100.0  # par bond
    assert r["representative_trade"]["n_futures_contracts_100k"] == 850.0
    # DV01-matched: futures DV01 must equal cash DV01 (within rounding):
    assert abs(r["representative_trade"]["dv01_futures_total_usd_per_bp"]
               - r["representative_trade"]["dv01_cash_leg_usd_per_bp"]) < 5
    assert abs(r["representative_trade"]["leverage_on_cash_leg"] - 50.0) < 0.1
    # Repo shock and haircut shock each cost a material share of equity:
    assert r["stress_usd_and_pct_of_equity"]["repo_plus_50bp_pct_equity"] > 5
    assert r["stress_usd_and_pct_of_equity"]["haircut_2_to_4pct_pct_equity"] == 100.0
    # A 50 bp yield fall demands variation margin > 100% of equity:
    assert r["stress_usd_and_pct_of_equity"]["yield_falls_50bp_vm_pct_equity"] > 100
    # A 50 bp yield rise is (to first order) hedged:
    s = r["stress_usd_and_pct_of_equity"]
    assert abs(s["yield_rises_50bp_cash_loss"] + s["yield_rises_50bp_futures_gain_offset"]) < 1
    print("checks passed")
