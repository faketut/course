== mod 1
$"continuous:" 1/e^(0.05 times 0.5)\
"annual effective:" 1/1.05^(0.5)\
"semi-annual APR:" 1/(1+0.05/2)\
i=e^r-1 "where i is annual effective rate and r is continuous compound rate"\
$

== mod 2
general method for margin problems:\
- step1 - find the cushion per contract
- step2 - convert to a price move
- step3 - apply the direction
- step4 - trigger price


for consumption asset (not easily to short) we have the asymmetry between holding an asset and shorting $F<=S(1+r)+U$ (or $F=S(1+r)+U-Y$).\

== mod 3
$h^*= rho (sigma_s/sigma_f)\
N^*=h^*(Q_a/Q_f)$
"perfect hedge" means 0 uncertainty, not guarantee any outcome.\
hedge effectiveness=$rho^2$, the $R^2$ of regression of spot price change on future price change.
perfect hedge requires $rho=1$.\
To move a portfolio's beta from β to a target $β*$, the number of index futures contracts required is: 
$N = (β* − β) times V_A / V_F$ 
where $V_A$ is the value of the portfolio and $V_F$ is the value of one futures contract (futures price × 
multiplier). A negative N means a short position, a positive N a long position.\

$"business gain"="realized sale price"(S_2)-"price locked in"(F_1)$\

== mod 5

#table(
  columns: 3,
  stroke: 0.5pt,
  align: left,
  inset: 6pt,
  table.header(
    [*Position*],
    [*Goal: extra income* \
      (give up big upside; sell options, collect premium)],
    [*Goal: cap maximum loss* \
      (buy insurance; buy options, pay premium)],
  ),
  [Long Stock \
    → profit if the stock rises],
  [*Covered Call* \
    • Sell Call, collect premium \
    • If the stock rallies, you must sell your shares at the fixed strike],
  [*Protective Put* \
    • Buy Put, pay premium \
    • If the stock crashes, you can force-sell your shares at the fixed strike],
  [Short Stock \
    → profit if the stock falls],
  [*Covered Put* \
    • Sell Put, collect premium \
    • If the stock crashes, you must buy back the stock at the fixed strike to close],
  [*Protective Call* \
    • Buy Call, pay premium \
    • If the stock rallies (short squeeze), you can buy back at the fixed strike to cut losses],
)


== mod 6
$"position greek"="single-option greek" times "# of underlying shares"$\



