# Research plan — Topic 13 (Basis Trade)

## Primary sources — verified / to verify

| # | Source | What it gives | Status |
|---|---|---|---|
| 1 | Monin, "Decomposing Hedge Funds' U.S. Treasury Exposures", Fed FEDS Notes, June 22, 2026 | Basis ~$830bn Sep 2025 (35% of $2.4tn long), gross $4.0tn, repo $3.0tn, swap-spread ~$305bn, ~$60bn unwound Apr 2025, top-50 funds ~90% of exposure | **Read 2026-11-11** (federalreserve.gov) — figures used as aggregate anchors |
| 2 | Chicago Fed Letter No. 516, Jan 2026 (Patel, "How the U.S. Treasury Futures Market and the Basis Trade Could Be Affected by the Treasury Clearing Mandate: Part 1—A Primer") | Futures mechanics, CTD (usually off-the-run), leverage (futures margin 1–3% → 33–99x), leveraged-fund futures >$1tn notional May 2025, clearing deadlines cash Dec 31 2026 / repo Jun 30 2027 | **VERIFIED 2026-11-11** — read in full (cfl516.pdf); [VERIFY] cleared |
| 3 | Barth, Kahn & Mann, "Recent Developments in Hedge Funds' Treasury Futures and Repo Positions: is the Basis Trade 'Back'?", FEDS Notes No. 2023-08-30-2, Aug 30, 2023 (DOI 10.17016/2380-7172.3355) | Mechanics; trade exposed to BOTH futures-margin and repo-spread changes; sponsored repo +$120bn Oct 2022–May 2023; short futures $715bn May 2023 | **VERIFIED 2026-11-11** — read in full; [VERIFY] cleared |
| 4 | Barth & Kahn (2025), J. Monetary Economics vol. 155(C), art. 103823 (DOI 10.1016/j.jmoneco.2025.103823); working paper OFR WP 21-01 (Apr 2021, rev. Jul 2021) | Disconnect = futures-implied yield − T-bill yield; basis traders sold $91–105bn Mar 2020, shorts $659bn → $554bn; unwind a consequence, not the primary cause; haircuts ~3% or less → >30x; measured leverage median 17.6x (2019) | **VERIFIED 2026-11-11** — JME abstract via RePEc + OFR WP read in full (JME full text paywalled); [VERIFY] cleared |
| 4a | Banegas, Monin & Petrasek (2021), "Sizing hedge funds' Treasury market activities and holdings," FEDS Notes, Oct 6, 2021 (DOI 10.17016/2380-7172.2979) | Method: Form PF disaggregation; Mar 2020 hedge funds net-sold ~$173bn, concentrated in likely basis traders; net repo peaked $598bn (2018–19) | **VERIFIED 2026-11-11** — via Fed 2024 FEDS Notes + EconPapers (Banegas page itself failed to load; open it before citing the note directly) |
| 4b | Kruttli, Monin, Petrasek & Watugala (2025), "LTCM Redux?", J. Financial Economics vol. 169, art. 104017 (DOI 10.1016/j.jfineco.2025.104017); WP FEDS 2021-038 | Mar 2020: basis traders cut repo borrowing ~17%, repo terms shortened, collateral ratios rose; unwind an amplifier, not the cause; G-SIB dealers provided 11–13% MORE repo funding | **VERIFIED 2026-11-11** — working paper read in full (JFE published version paywalled) |
| 4c | Kashyap, Stein, Wallen & Younger (2025), "Treasury Market Dysfunction and the Role of the Central Bank," Brookings Papers on Economic Activity, Spring 2025 | "Basis purchase facility" is THEIR proposal (not the Fed's): hedged purchases (long cash + short futures), standing basis cap or auctions of bundled packages, penalty pricing; Fed bought ~$1.6tn Mar–May 2020; basis spiked 9 SD in Mar 2020 | **VERIFIED 2026-11-11** — final draft read in full |
| 5 | BIS Quarterly Review, Sep 2023, Box A ("Margin leverage and vulnerabilities in US Treasury futures") | Margin leverage = contract value / initial margin: pre-pandemic ~175x (5y) / ~120x (10y); since 2021 ~70x / ~50x; leveraged-fund net shorts ~$600bn mid-2023, 40%+ in 2y | **VERIFIED 2026-11-11** — read in full, spot-checked by parent agent; cite BOTH vintages, never 120x as current |
| 6 | FSB, Leverage in Nonbank Financial Intermediation: Final report, Jul 9, 2025 (consultation Dec 18, 2024) | Two channels (position liquidation + counterparty); near-zero haircuts in bilateral repo; Mar 2020 basis unwind tied to rising futures margins AND repo rates; Rec. 4–5: min haircuts in govt-bond repos, enhanced margin, central clearing | **VERIFIED 2026-11-11** — consultation PDF read in full, final-report summary page read (final PDF itself not opened — cite final for recommendations, consultation for episode analysis) |
| 7 | SEC, Standards for Covered Clearing Agencies for U.S. Treasury Securities, Rel. No. 34-99149 (Dec 13, 2023), 89 FR 2714; extension Rel. No. 34-102487 (Feb 25, 2025) | Cash compliance Dec 31, 2026; repo Jun 30, 2027. SCOPE: repo leg in scope (incl. dealer-to-fund repo); hedge-fund cash trades EXCLUDED from adopted cash definition | **VERIFIED 2026-11-11** — adopting release read; re-check SEC implementation page before submission for any extension after Apr 20, 2026 |
| 8 | CME Treasury futures specs (TY contract) | Contract size $100k, conversion-factor method, deliverable basket, delivery months | **DONE 2026-11-11** — CME Treasury Analytics: CTD 3 7/8% 8/15/2033, CF 0.8870, full 6-bond basket in `data/ctd_2026-11-11.md` |
| 9 | FRED: DGS10, SOFR / repo rates (e.g. TGCR / SOFR), DTCC GCF repo | Yield + funding rates for the actual CTD date | **DONE 2026-11-11 (read, date-stamped in `data/ctd_2026-11-11.md`)** — 10y 4.98% Nov 10 (Treasury par curve), SOFR 3.88% eff. Nov 9, TGCR 3.86%; CSV download not done — values recorded with dates in the data file |
| 10 | CFTC Commitments of Traders — leveraged funds, Treasury futures | Net short futures >$1tn (brief) — verify the vintage | **DONE 2026-11-11** — leveraged funds net short 2,262,310 10y contracts as of Tue 3 Nov 2026 (released 6 Nov); asset managers net long 3,030,236; next release Mon 16 Nov |

## Data to pull before the draft is final

- [x] Actual CTD bond for the chosen futures contract (coupon, maturity,
  CUSIP, conversion factor) — re-run done in
  `analysis/basis_trade_real_ctd.py` (887 contracts, CF 0.8870).
  PRICE is derived, not observed (CME masked it) — see open item below.
- [x] Repo rate + SOFR on the same date; implied repo rate for the CTD
  (3.39% CME vs SOFR 3.88% eff. Nov 9).
- [x] CFTC leveraged-fund net short futures, one dated observation
  (2,262,310 contracts, 3 Nov 2026).
- [ ] OPEN: Nov 11 close cash price for 91282CHT1 from an independent
  source — settles Scenario A (-$67k) vs Scenario B (+$368k) in the
  base case. Do not claim the base-case sign until this lands.
- [x] Mar 2020 basis widening: the "14 bp → 142 bp" figure is **NOT VERIFIED and must NOT be used** — found in no primary source checked (OFR WP 21-01 full text, Barth/Kahn/Mann 2023, CFL 516, Schrimpf/Shin/Sushko 2020); only in a secondary blog with no citation. Citable alternatives, each with its own definition (NOT the report's price-points basis G): implied-repo-minus-GC-repo basis grew to hundreds of bp (Schrimpf, Shin & Sushko 2020, via Duffie 2020); implied-vs-actual term repo spread on the June 5-year contract widened 50 bp (Dallas Fed, Jul 15, 2025).
- [ ] Apr 2025: what unwound was swap-spread (~$60bn, Monin), not the
  cash-futures basis — keep the two trades distinct in the report.
- [x] Central-clearing timeline (cash Dec 31, 2026; repo Jun 30, 2027; repo leg in scope, fund cash excluded) + the "basis purchase facility"
  proposal — Kashyap/Stein/Wallen/Younger (Brookings, Spring 2025), hedged purchases, NOT a Fed proposal; see row 4c above.

## Verification checklist (every number in the report must pass this)

- [ ] Every aggregate figure traces to Monin (2026) or another primary
  source, with a date (Sep 2025) — not "currently".
- [x] Model inputs are labelled *assumed* (par bond CF = 0.85) or *observed* (real CTD: CF 0.8870, CME; Fed aggregates) — never mixed. The real-CTD run replaced the assumed CF.
- [ ] No press total is cited where a prospectus / filing / official
  release exists.
- [ ] The AI-critique appendix is run for real (see draft Appendix C).
- [ ] Team review: one member re-runs `basis_trade.py` from scratch
  and reproduces the tables.
