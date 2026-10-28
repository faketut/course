-- CFM301 Project 3: CRSP monthly index pull (WRDS SAS Studio)
-- Table: crsp.msi (monthly stock index).
-- NOTE 2026-10-28: the date column is DATE, not caldt (proc contents
-- verified; original caldt version failed). Alias it to caldt on select.
-- vwretd = value-weighted return WITH distributions (total return, per brief)
-- vwretx = value-weighted return EXCLUDING distributions
-- ewretd/ewretx = equal-weighted analogs (for the VW-vs-EW sensitivity)

proc sql;
create table work.msi as
select date as caldt, vwretd, vwretx, ewretd, ewretx
from crsp.msi
where date >= '01JAN1926'd;
quit;

proc export data=work.msi outfile="~/wrds_crsp_msi.csv" dbms=csv replace; run;
