# Fund selection (Project 5)

Category: US large-cap growth, actively managed. Same category so
performance is comparable and a common factor benchmark applies.

## Active funds (flagship retail share class, identified by ticker)

| Ticker | Fund | Inception |
|---|---|---|
| FCNTX | Fidelity Contrafund | 1967-05-17 |
| FMAGX | Fidelity Magellan | 1963-05-02 |
| AGTHX | American Funds Growth Fund of America (Class A) | 1973-12-01 |
| PRGFX | T. Rowe Price Growth Stock | 1950-04-11 |
| TRBCX | T. Rowe Price Blue Chip Growth | 1993-06-30 |

Sample: 1994-01 to 2024-12 (372 months). 1994 is the first full year
all five funds exist. One share class per fund: the flagship retail
class a retail investor would actually buy, with the longest history.
Fund-level asset-weighted aggregation would mix classes with different
fee structures (A/C/institutional) and is not needed for the question.
Returns are net of expenses and before loads (CRSP convention); loads
do not affect monthly returns.

## Implementable-benchmark index funds (Vanguard, investor shares)

| Ticker | Fund | Inception |
|---|---|---|
| VFINX | Vanguard 500 Index (S&P 500) | 1976-08-31 |
| NAESX | Vanguard Small-Cap Index | 1989-10-03 |
| VIVAX | Vanguard Value Index | 1992-11-02 |

All three exist for the full sample. Loadings constrained to sum to one
and be non-negative (no shorting, no leverage, fully invested).

## Data source

CRSP Mutual Fund Database via WRDS (SAS Studio): monthly fund_summary
(return, TNA, NAV, expense ratio, turnover) by crsp_fundno, looked up
from fund_hdr by ticker. Ken French factors (Mkt-RF, SMB, HML, UMD, RF)
from the project-2 file (1963-07 to 2026-08). Fee distribution: Dec-2024
cross-section of expense ratios for US equity mutual funds.

## Status 2026-11-19

WRDS BLOCKED: the account is not authorized for CRSP mutual-fund files
(CRSP.FUND_SUMMARY / CRSP.FUND_HDR, SAS authorization error 2026-11-19).
Fallback used instead: Yahoo Finance monthly total returns (validated
against Zacks), current prospectus expense ratios / turnover / TNA, and
published Morningstar 2024 / ICI fee benchmarks. TNA history is
unavailable, so fund flows cannot be estimated; the report discusses
Berk & Green (2004) on the persistence evidence. If WRDS access is
enabled, swap in CRSP data per README and re-run.
