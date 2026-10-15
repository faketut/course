-- CFM301 Project 2: WRDS pulls (run in WRDS web Query / cloud PostgreSQL)
-- Sample: 2000-01 to 2026-09. Download each result as CSV.

-- Q1: CRSP monthly stock file (returns are TOTAL returns incl. dividends)
SELECT permno, date, ret, prc, vol, shrout, cfacpr, ticker, shrcd, exchcd
FROM crsp.msf
WHERE date >= '2000-01-01' AND date <= '2026-09-30'
  AND shrcd IN (10, 11) AND exchcd IN (1, 2, 3);
-- -> wrds_crsp_msf.csv

-- Q2: Compustat quarterly fundamentals (rdq = actual report date, for
-- point-in-time alignment; niq = quarterly net income for TTM earnings)
SELECT gvkey, datadate, fyearq, fqtr, rdq, niq, oibdpq, atq, ceqq, cshoq
FROM comp.fundaq
WHERE datadate >= '2000-01-01' AND datadate <= '2026-09-30'
  AND indfmt = 'INDL' AND datafmt = 'STD' AND consol = 'C' AND popsrc = 'D';
-- -> wrds_comp_fundaq.csv

-- Q3: CRSP-Compustat merged link table (gvkey <-> permno)
SELECT gvkey, lpermno AS permno, linkdt, linkenddt, linkprim, linktype
FROM crsp.ccmxpf_linktable
WHERE linkprim IN ('P', 'C') AND linktype IN ('LU', 'LC');
-- -> wrds_ccm_link.csv

-- Notes for the Python build (src/wrds_build.py):
-- * Market cap (month-end) = abs(prc) * shrout  (shrout is in thousands).
-- * EY at month-end t: TTM niq = sum of last 4 quarterly niq with
--   rdq <= t (no lookahead); EY = TTM_niq / mcap_t. Filing currency: niq is
--   in USD millions for US filers.
-- * CRSP delisting returns: merge crsp.msedelist (permno, dlstdt, dlret)
--   if available; else note the omission.

-- ============ SAS Studio version (WRDS web Query tool was retired) ============
-- In SAS Studio: run each block, then download the WORK table as CSV
-- (right-click the table -> Download, or PROC EXPORT below).
proc sql;
create table work.msf as
select permno, date, ret, prc, vol, shrout, cfacpr, ticker, shrcd, exchcd
from crsp.msf
where date >= '01JAN2000'd and date <= '30SEP2026'd
  and shrcd in (10,11) and exchcd in (1,2,3);
quit;

proc sql;
create table work.fundaq as
select gvkey, datadate, fyearq, fqtr, rdq, niq, oibdpq, atq, ceqq, cshoq
from comp.fundaq
where datadate >= '01JAN2000'd and datadate <= '30SEP2026'd
  and indfmt='INDL' and datafmt='STD' and consol='C' and popsrc='D';
quit;

proc sql;
create table work.ccmlink as
select gvkey, lpermno as permno, linkdt, linkenddt, linkprim, linktype
from crsp.ccmxpf_linktable
where linkprim in ('P','C') and linktype in ('LU','LC');
quit;

proc export data=work.msf    outfile="~/wrds_crsp_msf.csv"    dbms=csv replace; run;
proc export data=work.fundaq outfile="~/wrds_comp_fundaq.csv" dbms=csv replace; run;
proc export data=work.ccmlink outfile="~/wrds_ccm_link.csv"  dbms=csv replace; run;
