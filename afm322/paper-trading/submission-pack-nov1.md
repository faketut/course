# AFM 322 Initial Report — Submission pack, Nov 1, 2026 (for team review)

## Deadline
- Due Mon Nov 2, 2026. Recorded due time is "11:59pm" with no timezone stated;
  the tracking record stores 23:59 UTC = 18:59 EST (Toronto is on EST from Nov 1).
- SAFE TARGET: everything ready to submit by ~18:00 EST Mon Nov 2. Do not plan
  on a 23:59 local-time finish unless the assignment text is re-checked.

## Pack contents (all in ~/workspace/afm322-report/)
- initial-report-draft.docx — 5 pages vs 6-page limit. Body draft, prices TBD.
- scenario4-draft.docx — 2 pages vs 3-page limit. Template proposal only, NOT a pick.
- appendices-draft.docx — 3 pages, appendices extra (not counted in the 6-page body):
  A risk table, B likelihood×magnitude graph + research summary, C PowerBI
  dashboard (data/measures/layout), D AI training process, E AI correspondence.
- TDI_trade_log.xlsx — Trade_Log (6 rows, all PLANNED), Dashboard_Data,
  November_Profit_by_Temp (chart), Daily_Brief_Template, Nov2_FillIn checklist.
- risk-graph.png — likelihood×magnitude graph embedded in Appendix B.
- scenario4-pick-sheet-jack.md — Jack's pick sheet. LOCK FIRST.
- wsb-sealed-method.md — WSB method, sealed. Specific WSB pick is revealed
  Nov 2 only after Jack locks, from the Nov 2 IBKR chain.
- nov2-execution-plan-2026-10-31.md — Monday sequence (still current).
- research-notes-2026-10-26.md, rag-test-2026-10-26.md,
  agent-brainstorm-2026-10-26.md, draft-recommendations-2026-10-26.md — evidence.
- RAG index: ~/workspace/afm322-rag/, 592 chunks (Modules 1–8, incl. OCR'd
  Module 8 reading), agent_log.jsonl.

## What is NOT done (honestly, by design)
- No trades placed. No prices filled. No carbon vendor quote yet.
- Risk table column "AI w/o human guidance?" is NO throughout — no blind run
  has been done in a fresh session. Do not flip to YES without that run.
- PowerBI file is a source workbook + measures + layout, not a .pbix file.
  Say that plainly if asked; insert a live dashboard screenshot at submission.
- AI correspondence appendix is an index + the agent log, not a substitute
  for the verbatim chat export the team must append at submission.
- Jack's Scenario #4 pick: not made, not made by the agent. WSB pick: method
  sealed, specific trade pending Nov 2 chain.

## Nov 2 sequence (in order, see execution plan for detail)
1. IBKR paper login (browser secure sign-in; password never in chat).
   Re-verify contract specs + margins before ordering.
2. Steel: LONG 100 x Dec HRC, close Dec 1.
3. FX: LONG CAD Dec futures, contracts = ($5m x Nov 2 spot) / 100,000, close Nov 30.
   Disclose rounding residual; OTC forward stays as disclosure, not the paper trade.
4. Weather: confirm Nov 2 quotes — HDD call struck ~837 (primary) vs scaled futures.
5. Carbon: named Verra/Gold Standard quote, 750t, hold unretired.
6. Jack locks Scenario #4 pick, then WSB pick is revealed and logged.
7. Fill log rows PLANNED → EXECUTED, fill all [TBD] cells, insert screenshots,
   team sign-off, submit by ~18:00 EST.

## IBKR availability check (Nov 1, completed ~17:06 EST, no orders)
- Paper account confirmed (red "Paper Trading account for Simulated Trading"
  banner, Individual Demo, Ontario). Saved login worked, no 2FA code needed,
  Trading Mode set to Paper each time.
- Dec HRC: VISIBLE, no permission error. No bid/ask shown — futures closed Sunday,
  no real-time market-data subscription evident.
- Dec CAD futures (6C): NOT FOUND in order-ticket search across 3 sessions,
  nor in Future Options tab.
- Chicago HDD Nov (H2): NOT FOUND in order-ticket search.
- Caveats: one session showed "logged in without Trading/Market Data
  permissions"; sessions dropped 3x ahead of IBKR maintenance Sun Nov 1
  18:00-18:30 ET; a control ES search worked, so the search itself works.
  Conclusion is NOT "6C/H2 can never trade" — it is "not visible in this paper
  account on Sunday evening, recheck Monday".
- Monday fallback if still missing: Excel-logged OTC trades, allowed by the
  assignment (buy at ask / sell at bid), with terms clearly labelled as
  simulated OTC, NOT claimed as IBKR executions. FX OTC forward (exact $5m,
  Nov 30) is already the real-life perfect hedge in the draft; weather OTC
  terms must be written from Monday's Chicago HDD index, not invented.

## Decision locked Nov 2, 00:09 EST (Jack's pick)
- Steel: IBKR, daytime (not the midnight ask).
- FX + weather: Excel-logged OTC (see otc-term-sheets-nov2.md and the
  OTC_Term_Sheets tab in TDI_trade_log.xlsx). All rows still PLANNED;
  no OTC trade is executed until its daytime market input is filled.

## Nov 2 00:08 EST recheck (no orders)
- 6C: STILL not found (6C, Canadian Dollar, CAD; Future Options tab also no).
- H2: STILL not found (H2, Chicago HDD).
- HRC Dec: visible, delayed quotes Bid 1397 / Ask 1409 / Last 1398 / Open 1403.
  Initial Margin $3,175/contract, Maintenance $2,746/contract, order amount
  $27,940/contract, est. commission $6.86/contract. Spread $12/ton is thin
  overnight — do not lock the midnight ask as the trade price without Jack's
  explicit choice; daytime re-quote preferred.
- Portal again: 'without Trading/Market Data permissions / delayed data',
  warning about submitting without market data. Open Orders 0, Positions 0.

## Nov 2 ~08:23 EST — HRC order placed, PARTIAL fill (paper only)
- Order ID 1117270116 (Ref 76009460), BUY 100 Dec HRC LIMIT 1405 Day.
- Filled 7 @1405.00 at 08:24 EST ($196,700, fees $48.02 on filled part);
  93 still WORKING at 1405, left untouched (Day order).
- Current executed position: 7 contracts = 140 tons (7% of 2,000-ton need).
- Report must state partial fill + working remainder honestly, and recheck
  final fill count before submission. Do NOT write "100 contracts hedged"
  unless the remainder fills.

## Nov 2 morning — decisions locked by Jack
- Team pack SENT by Jack (confirmed Nov 2).
- FX OTC forward LOCKED at 1.3970 (Finnhub/OANDA ~07:27 EST, IBKR spot blank):
  sell USD 5,000,000 / buy CAD 6,985,000, settle Nov 30. Log status EXECUTED (Excel OTC).

## Nov 2 ~16:05-16:13 EST — FINAL HRC check (paper only, no order changes)
- Order 1117270116 no longer in Orders tab ("No Recent Orders").
- Trades tab: 45 fills totalling 100 contracts @1405.00, 08:24-09:39 EST.
- Positions: LONG 100 Dec HRC, last 1406.
- CORRECTION to morning snapshot: 7/93 meant 7 filled + 93 remaining = 100 total.
  The 93 subsequently filled; remainder is 0, not 93 outstanding. An agent
  inference of "100 filled + 93 remaining = 193" is arithmetically impossible
  for a 100-contract order and is rejected here.
- Portal average-price / P&L displays (1405.34, +690.46) do not reconcile
  with 1405.00 fills and are flagged unverified.
- Steel hedge is therefore FULLY executed: 100 contracts = 2,000 tons @1405.

## Nov 2 ~16:22 EST — CORRECTION to avg/P&L flag above
- Verified by arithmetic: avg 1405.34 = (2,810,000 fills + 686 commission) / 2,000
  = 1405.343 -> 1405.34. P&L +690.46 = market value 2,811,376.46 - 2,810,686
  = exactly 690.46. So avg and P&L DO reconcile with fills @1405 once
  commission is included; the earlier "do not reconcile" flag is withdrawn.
- Remaining minor gap only: market-value implied price 1405.688 vs last
  1406.00 (snapshot valuation basis, unverified) - does not contradict fills.

## Nov 2 17:46 EST — Decisions by Jack's delegation to Muse
- Weather: Option B (69-unit OTC linear swap, fixed 690 HDD) — log EXECUTED.
- Carbon: unresolved gap reported honestly, no invented vendor quote.
- Scenario #4: bull call spread structure locked, with authorship disclosure
  (Muse-selected on delegation, NOT Jack's personal pick; Jack-vs-WSB label void).
  Specific strikes/premiums TBD from Nov 2 chain, not invented.
  See decisions-nov2-evening.md.
