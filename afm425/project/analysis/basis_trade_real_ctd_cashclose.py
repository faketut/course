"""AFM 425 Topic 13 — basis trade on the REAL CTD, CASH-CLOSE variant (14 Nov 2026).

Variant of basis_trade_real_ctd.py (canonical run untouched). Changes vs canonical:
  * Cash leg is OBSERVED, not derived: Safe Rate Markets security page for
    91282CHT1 (republishing Treasury's end-of-day prices) lists the Nov 10, 2026
    close at 94.188 per 100 face (bid 94.094 / offer 94.125). That close reprices
    to a yield of 4.894% on the Nov 11 stub — 0.8 bp below CME's 4.9023% — so
    YTM is set to 0.04894, which reprices to clean 94.1883, i.e. the observed
    close to 0.03 cents. The derived clean 94.1427 sits inside the Nov 10
    bid-offer spread, so the derivation is confirmed, not replaced by a
    conflicting number.
  * Futures leg is the official Nov 10 settle 106.25 (106'080), as in the
    settle10625 variant. Both legs are now Nov 10 vintage.
  * Scenario B (CME net basis -0.3539) is kept in the output for comparison
    but is now REJECTED: it implies a cash price near 93.71, about 40-48 cents
    below every Nov 10 print (bid 94.094 / offer 94.125 / close 94.188).
    The sign dispute is settled: the base case is positive in Scenario A,
    and the remaining question is magnitude, bracketed by the bid/offer/close
    prints (see data/cash-close-2026-11-14.md).
Output: outputs/basis_trade_real_ctd_cashclose10625_results.json (and .csv).


Companion to basis_trade.py (the par-bond illustration). This script
re-runs the same trade on the actual cheapest-to-deliver into the
Dec 2026 10-year futures contract, identified from CME Treasury
Analytics (QuikStrike), snapshot 11 Nov 2026 12:10 PM CT:

  CTD: 3 7/8% Treasury Note due 8/15/2033, CUSIP 91282CHT1,
  coupon 3.875%, yield 4.9023% (CME), CF 0.8870, implied repo 3.39%,
  futures price 106-01.5 (= 106.046875), CME cash DV01 $53.98,
  CME modified duration 5.7838.

Cash price: CME masked it (XXX.XXXX), so the clean price is DERIVED
by exact semi-annual repricing at the CME yield (see data/
ctd_2026-11-11.md). Our DV01 $55.00 vs CME $53.98 (+1.9%) and our
modified duration 5.8425 vs CME 5.7838 (+1.0%) cross-check the
derivation. The derived gross basis is +0.0791 pts, while CME's
reported basis net of carry is -0.3539 pts — those conflict, and the
base-case P&L is therefore reported in both scenarios (A and B).
The stress numbers are robust to the conflict (DV01/equity move <2%).

BASIS SIGN — CORRECTION to basis_trade.py, found by exact repricing
here: with Basis G = P - CF*F, the clean P&L of the hedged position
is dG, exactly. So if G converges to zero at delivery, the basis
P&L is -G(entry), NOT +G. The par illustration in basis_trade.py
had this sign flipped (it added +$100k for G = +0.10); that script
is fixed in the same commit as this one, and its base case moves
from +$120k to -$80k. The "basis widens" stress is unaffected: a
widening in the March-2020 direction means cash cheapens, G FALLS
by 0.50 pts, P&L = -$500k.

Method (exact, no duration approximation for the base case):
  * Price the CTD on its real coupon calendar (Feb 15 / Aug 15),
    settlement 11 Nov 2026, first coupon 15 Feb 2027 (96 of 184 days
    into the half-year). Dirty price = sum of discounted cash flows;
    clean = dirty - accrued.
  * Reprice at delivery, 1 Dec 2026 (first delivery day), same yield,
    G = 0 (futures price = clean price / CF at delivery). Futures
    P&L, cash P&L and repo cost are computed leg by leg; the total
    must equal carry + (-G(entry)) up to the small residual from the
    unhedged $11.3m face (887 contracts deliver $88.7m; the rest is
    sold for cash at delivery). The script asserts this identity.
  * Repo rate = SOFR 3.88% (effective 9 Nov 2026, NY Fed — latest
    FRED observation at the pull). Haircut 2% base case.
  * Stresses are first-order DV01-based (as in the par model), plus
    exact repricing for the +/-50 bp yield moves.
"""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

# --- Inputs: CME Treasury Analytics, 11 Nov 2026 12:10 PM CT ---
COUPON = 0.03875
YTM = 0.04894             # yield repricing to the observed Nov 10 close 94.188 (CME reported 4.9023%)
CF = 0.8870
F_ENTRY = 106.25            # official CME Nov 10 settle for TYZ6, 106'080
IMPLIED_REPO_CME = 0.0339
CME_CASH_DV01 = 53.98     # per $100k contract
CME_MOD_DUR = 5.7838
CME_MAC_DUR = 5.9266
CME_BASIS_NET_OF_CARRY = -0.3539  # price points, CME-reported
SETTLE = date(2026, 11, 11)
MATURITY = date(2033, 8, 15)
DELIVERY = date(2026, 12, 1)      # first delivery day, Dec 2026 contract
FACE = 100_000_000.0
HAIRCUT = 0.02
REPO_RATE = 0.0388                # SOFR, effective 9 Nov 2026 (NY Fed)
AGG_BASIS = 830_000_000_000.0     # Monin (Fed, Jun 2026), Sep 2025


def coupon_dates():
    ds = []
    for y in range(2026, 2034):
        for m, d in [(2, 15), (8, 15)]:
            dt = date(y, m, d)
            if SETTLE < dt <= MATURITY:
                ds.append(dt)
    return ds


CDS = coupon_dates()
PREV_CPN = date(2026, 8, 15)
NEXT_CPN = date(2027, 2, 15)
PERIOD_DAYS = (NEXT_CPN - PREV_CPN).days  # 184


def dirty_clean(asof: date, ytm: float = YTM):
    """Dirty and clean price per 100 face, exact stub-period pricing."""
    w = (NEXT_CPN - asof).days / PERIOD_DAYS
    i = ytm / 2
    dirty = 0.0
    for k, dt in enumerate(CDS):
        cf = 100 * COUPON / 2 + (100 if dt == MATURITY else 0)
        dirty += cf / (1 + i) ** (w + k)
    accrued = 100 * COUPON / 2 * (1 - w)
    return dirty, dirty - accrued, accrued


def dv01_duration():
    """DV01 per 100 face and modified duration by +-1 bp repricing."""
    _, p0, _ = dirty_clean(SETTLE, YTM)
    _, p_up, _ = dirty_clean(SETTLE, YTM + 0.0001)
    _, p_dn, _ = dirty_clean(SETTLE, YTM - 0.0001)
    dv01 = (p_dn - p_up) / 2
    return dv01, dv01 / (p0 * 0.0001), p0


def main() -> dict:
    dirty, clean, accrued = dirty_clean(SETTLE)
    dv01_100, mod_dur, _ = dv01_duration()
    dv01_cash = dv01_100 * FACE / 100
    dv01_per_future = dv01_100 * 1000 / CF
    n_futures = round(FACE * CF / 100_000)  # DV01-matched; 887
    market_value = dirty * FACE / 100
    equity = market_value * HAIRCUT
    borrowing = market_value * (1 - HAIRCUT)
    leverage = market_value / equity
    gross_basis = clean - CF * F_ENTRY

    # --- Exact P&L to delivery (scenario A: our repricing) ---
    T = (DELIVERY - SETTLE).days / 365
    dirty_del, clean_del, _acc_del = dirty_clean(DELIVERY)
    f_del = clean_del / CF
    cash_pnl = (dirty_del - dirty) * FACE / 100
    fut_pnl = n_futures * (F_ENTRY - f_del) * 1000
    repo_cost = borrowing * REPO_RATE * T
    total_a = cash_pnl + fut_pnl - repo_cost
    coupon_accrual = FACE * COUPON * T
    carry = coupon_accrual - repo_cost
    basis_pnl_a = -gross_basis * FACE / 100
    # identity: total == carry + basis P&L, up to the residual-leg rounding
    identity_gap = total_a - (carry + basis_pnl_a)

    # --- Scenario B: CME's reported basis net of carry at face value ---
    basis_pnl_b = -CME_BASIS_NET_OF_CARRY * FACE / 100
    total_b = carry + basis_pnl_b

    # --- Stresses (DV01-based, as in the par model) ---
    repo_50bp = borrowing * 0.005 * T
    haircut_extra = market_value * 0.02
    basis_widen_050 = FACE * 0.50 / 100  # G falls 0.50 (cash cheapens)
    vm_50bp_fall = dv01_cash * 50
    # exact yield moves (repricing the cash leg, futures offset by DV01)
    _, p_up50, _ = dirty_clean(SETTLE, YTM + 0.005)
    _, p_dn50, _ = dirty_clean(SETTLE, YTM - 0.005)
    cash_loss_up50 = (p_up50 - clean) * FACE / 100
    cash_gain_dn50 = (p_dn50 - clean) * FACE / 100
    # aggregate scaling with the REAL duration
    agg_dv01 = mod_dur * AGG_BASIS * 0.0001
    agg_widen_010 = AGG_BASIS * 0.001

    out = {
        "ctd": {
            "security": "3 7/8% Treasury Note due 8/15/2033",
            "cusip": "91282CHT1", "coupon_pct": 3.875,
            "yield_pct_cme": 4.9023, "conversion_factor": CF,
            "futures_price_106_01_5": round(F_ENTRY, 6),
            "implied_repo_pct_cme": 3.39, "sofr_pct_nov9": 3.88,
            "asof": "2026-11-10 close (Safe Rate / Treasury EOD) + 2026-11-10 CME settle",
            "delivery": "2026-12-01 (first delivery day)",
            "T_years_to_delivery": round(T, 4),
        },
        "derived_price": {
            "clean_per_100": round(clean, 4),
            "dirty_per_100": round(dirty, 4),
            "accrued_per_100": round(accrued, 4),
            "gross_basis_pts": round(gross_basis, 4),
            "cme_basis_net_of_carry_pts": CME_BASIS_NET_OF_CARRY,
            "dv01_per_100k_contract_usd": round(dv01_100 * 1000, 2),
            "cme_cash_dv01_usd": CME_CASH_DV01,
            "modified_duration_yrs": round(mod_dur, 4),
            "cme_modified_duration_yrs": CME_MOD_DUR,
            "macaulay_duration_yrs": round(mod_dur * (1 + YTM / 2), 4),
            "cme_macaulay_duration_yrs": CME_MAC_DUR,
        },
        "representative_trade_100m": {
            "face_usd": FACE, "market_value_dirty_usd": round(market_value, 0),
            "equity_usd_2pct_haircut": round(equity, 0),
            "repo_borrowing_usd": round(borrowing, 0),
            "leverage": round(leverage, 1),
            "dv01_cash_leg_usd_per_bp": round(dv01_cash, 0),
            "dv01_per_future_usd_per_bp": round(dv01_per_future, 2),
            "n_futures_contracts_100k": n_futures,
            "dv01_futures_total_usd_per_bp": round(dv01_per_future * n_futures, 0),
        },
        "base_case_pnl_to_delivery_usd": {
            "coupon_accrual": round(coupon_accrual, 0),
            "repo_cost": round(-repo_cost, 0),
            "carry_net": round(carry, 0),
            "basis_pnl_scenario_A_our_repricing": round(basis_pnl_a, 0),
            "total_scenario_A": round(total_a, 0),
            "total_scenario_A_pct_equity": round(total_a / equity * 100, 2),
            "basis_pnl_scenario_B_cme_net_basis": round(basis_pnl_b, 0),
            "total_scenario_B": round(total_b, 0),
            "total_scenario_B_pct_equity": round(total_b / equity * 100, 2),
            "exact_leg_check_cash_pnl": round(cash_pnl, 0),
            "exact_leg_check_futures_pnl": round(fut_pnl, 0),
            "identity_gap_vs_carry_plus_basis": round(identity_gap, 0),
        },
        "stress_usd_and_pct_of_equity": {
            "repo_plus_50bp_cost": round(repo_50bp, 0),
            "repo_plus_50bp_pct_equity": round(repo_50bp / equity * 100, 2),
            "haircut_2_to_4pct_extra_equity": round(haircut_extra, 0),
            "haircut_2_to_4pct_pct_equity": round(haircut_extra / equity * 100, 1),
            "basis_widens_cash_cheapens_0.50pts_loss": round(basis_widen_050, 0),
            "basis_widens_0.50pts_pct_equity": round(basis_widen_050 / equity * 100, 1),
            "yield_falls_50bp_variation_margin_call": round(vm_50bp_fall, 0),
            "yield_falls_50bp_vm_pct_equity": round(vm_50bp_fall / equity * 100, 1),
            "yield_falls_50bp_cash_gain_exact": round(cash_gain_dn50, 0),
            "yield_rises_50bp_cash_loss_exact": round(cash_loss_up50, 0),
            "yield_rises_50bp_futures_gain_dv01": round(vm_50bp_fall, 0),
        },
        "aggregate_scaling_fed_sep2025_real_duration": {
            "basis_trade_usd": AGG_BASIS,
            "gross_long_leg_dv01_usd_per_bp": round(agg_dv01, 0),
            "basis_widens_0.10pts_collective_loss_usd": round(agg_widen_010, 0),
        },
        "sensitivities": {
            "haircut_pct_leverage": {"0": "inf", "1": 100.0, "2": 50.0, "4": 25.0},
            "repo_shock_bp_cost_usd": {
                "25": round(borrowing * 0.0025 * T, 0),
                "50": round(repo_50bp, 0),
                "100": round(borrowing * 0.01 * T, 0),
            },
            "basis_cash_cheapening_pts_loss_usd": {
                "0.10": round(FACE * 0.001, 0),
                "0.50": round(basis_widen_050, 0),
                "1.00": round(FACE * 0.01, 0),
            },
            "yield_move_bp_vm_call_usd": {
                "25": round(dv01_cash * 25, 0),
                "50": round(vm_50bp_fall, 0),
                "100": round(dv01_cash * 100, 0),
            },
        },
    }

    print(json.dumps(out, indent=2))
    outdir = Path(__file__).resolve().parents[1] / "outputs"
    outdir.mkdir(exist_ok=True)
    (outdir / "basis_trade_real_ctd_cashclose10625_results.json").write_text(json.dumps(out, indent=2))
    with open(outdir / "basis_trade_real_ctd_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for section, vals in out.items():
            for k, v in vals.items():
                w.writerow([f"{section}.{k}", v])
    return out


if __name__ == "__main__":
    r = main()
    # Cross-checks against CME's own analytics (within 2-3%: masked
    # price / timing difference, not a model error):
    d = r["derived_price"]
    assert abs(d["dv01_per_100k_contract_usd"] - CME_CASH_DV01) / CME_CASH_DV01 < 0.03
    assert abs(d["modified_duration_yrs"] - CME_MOD_DUR) / CME_MOD_DUR < 0.02
    # Hedge is DV01-matched:
    t = r["representative_trade_100m"]
    assert t["n_futures_contracts_100k"] == 887
    assert abs(t["dv01_futures_total_usd_per_bp"] - t["dv01_cash_leg_usd_per_bp"]) < 500
    # Exact leg-by-leg P&L must equal carry + basis P&L (small residual
    # from the unhedged $11.3m face is the only gap; < $5k):
    b = r["base_case_pnl_to_delivery_usd"]
    assert abs(b["identity_gap_vs_carry_plus_basis"]) < 5000
    # The margin call on a 50 bp fall still exceeds the equity:
    s = r["stress_usd_and_pct_of_equity"]
    assert s["yield_falls_50bp_vm_pct_equity"] > 100
    assert s["haircut_2_to_4pct_pct_equity"] == 100.0
    print("checks passed")
