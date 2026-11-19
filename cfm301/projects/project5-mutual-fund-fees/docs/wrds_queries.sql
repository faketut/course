/* Project 5 -- CRSP Mutual Fund Database, WRDS SAS Studio.
   Phase 1: schema check + fund lookup by ticker.
   Run in SAS Studio, then download the printed output / exported files
   from the SAS Studio home folder. */

/* --- variable lists --- */
proc contents data=crsp.fund_summary
  out=work.summ_vars(keep=name type length varnum label) noprint;
run;
proc sort data=work.summ_vars by varnum; run;
proc print data=work.summ_vars label; run;

proc contents data=crsp.fund_hdr
  out=work.hdr_vars(keep=name type length varnum label) noprint;
run;
proc sort data=work.hdr_vars by varnum; run;
proc print data=work.hdr_vars label; run;

/* --- fund lookup: crsp_fundno + inception for our 8 tickers --- */
proc sql;
  select crsp_fundno, fund_name, ticker, first_offer_dt, end_dt,
         crsp_obj_cd, lipper_obj_cd, index_fund_flag
  from crsp.fund_hdr
  where ticker in ('FCNTX','FMAGX','AGTHX','PRGFX','TRBCX',
                   'VFINX','NAESX','VIVAX');
quit;
