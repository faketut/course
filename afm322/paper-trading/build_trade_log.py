#!/usr/bin/env python3
"""Build TDI trade log workbook (PowerBI-ready flat tables, no merged cells).

Status discipline: every row starts PLANNED. Nothing here is a trade
until Nov 2 prices are frozen, the order is placed in IBKR, and the
row is flipped to EXECUTED with a screenshot / order ID. That is what
keeps a pre-draft from becoming a false trade record.
"""
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

HEADERS = ["TradeID", "Scenario", "Account", "Date", "Underlying",
           "Instrument", "Exchange_Or_OTC", "Direction", "Contracts",
           "Multiplier", "Entry_Price", "Bid_Ask", "Expiry_CloseDate",
           "Spot_At_Trade", "Margin_USD", "Status", "Source_URL",
           "Screenshot_Ref", "Notes"]

def sheet(name, headers, rows):
    ws = wb.create_sheet(name) if name not in wb.sheetnames else wb[name]
    ws.append(headers)
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True)
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 18
    ws.freeze_panes = "A2"
    return ws

wb.remove(wb.active)
sheet("README", ["Item", "Detail"], [
    ["Purpose", "Single Excel log for AFM 322 TDI paper trading; PowerBI reads Trade_Log directly"],
    ["Price freeze", "Nov 2 prices (Jack decision 2026-10-26). Do not fill Entry_Price before Nov 2."],
    ["Paper capital", "IBKR $1m USD fictional, may be treated as $10m (x10). State allocation in report."],
    ["Old-school rule", "If logged in Excel only: buy at ask, sell at bid."],
    ["Status values", "PLANNED / EXECUTED / CLOSED. Only EXECUTED rows count in interim/final P&L."],
])

planned = [
    ["TDI-S1-STEEL", 1, "TDI", "2026-11-02", "CME HRC Steel",
     "Futures Dec 2026 (HRC)", "CME", "LONG", 100, 20,
     None, "TBD Nov 2", "Close 2026-12-01", None, None, "PLANNED",
     "cmegroup.com HRC specs", "", "2,000 short tons / 20 = 100. Close Dec 1, do not hold to Dec 29 termination."],
    ["TDI-S1-FX", 1, "TDI", "2026-11-02", "USD/CAD",
     "OTC Forward OR CME CAD Futures Dec 2026", "OTC-or-CME", "LONG CAD / SHORT USD", None, 100000,
     None, "TBD Nov 2", "Close/Settle 2026-11-30", None, None, "PLANNED",
     "", "", "Decision pending: OTC exact $5m Nov 30 vs futures rounding (CAD receipt/100k). Fill Nov 2 spot first."],
    ["TDI-S2-CARBON", 2, "TDI", "2026-11-02", "Voluntary carbon offsets",
     "Verra VCS or Gold Standard credits, unretired", "OTC / Registry", "BUY", 750, 1,
     None, "Vendor quote Nov 2", "Retire at disclosure", None, None, "PLANNED",
     "", "", "750t = 14,250 gross - 13,500 target. Hold unretired to stay resellable; retire at disclosure."],
    ["TDI-S3-HDD", 3, "TDI", "2026-11-02", "CME Chicago HDD Nov 2026",
     "HDD Futures Nov 2026 (H2) OR HDD Call strike ~837", "CME", "LONG", None, 20,
     None, "TBD Nov 2", "Close/Settle 2026-11-30", None, None, "PLANNED",
     "cmegroup.com H2 specs", "", "Full linear = 138 contracts ($2,760/$20). Scaled / option alternative to be decided before trading; do not default to 138."],
    ["PER-S4-OWN", 4, "Personal", "2026-11-02", "TBD - Jack's pick",
     "TBD option strategy", "IBKR", "TBD", None, None,
     None, "TBD Nov 2", "Close by 2026-11-30", None, None, "PLANNED",
     "", "", "REQUIRES Jack's pick. Do not fill by agent alone - that would void Jack-vs-WSB competition."],
    ["PER-S4-WSB", 4, "Personal", "2026-11-02", "TBD - WSB Agent pick",
     "TBD option strategy", "IBKR", "TBD", None, None,
     None, "TBD Nov 2", "Close by 2026-11-30", None, None, "PLANNED",
     "", "", "WSB Agent pick, logged independently of Jack's pick."],
]
sheet("Trade_Log", HEADERS, planned)

sheet("Daily_Brief_Template", ["Date", "Scenario", "Hedge_Coverage", "Futures_PL",
                               "Underlying_PL", "Basis_PL", "Margin_Used_USD",
                               "Action_Items"], [
    ["2026-11-02", 1, "", "", "", "", "", "Freeze prices; place S1 trades; screenshot orders"],
    ["2026-11-02", 3, "", "", "", "", "", "Place S3 trade; record Chicago HDD quote"],
])

wb.save("/home/hatch/workspace/afm322-report/TDI_trade_log.xlsx")
print("saved TDI_trade_log.xlsx")
