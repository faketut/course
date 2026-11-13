== mod 1
$"continuous discount factor (0.5y):" 1/e^(0.05 times 0.5)\
"6-month discount factor:" 1/1.05^(0.5)\
"semiannual discount factor:" 1/(1+0.05/2)\
i = e^r - 1 "where " i "is the annual effective rate and " r "is the continuously compounded annual rate."\
$

== mod 2
general method for margin problems:
- step 1 - find the cushion per contract
- step 2 - convert to a price move
- step 3 - apply the direction
- step 4 - trigger price

for consumption assets (not easily to short), there is an asymmetry between holding the asset and shorting it:
$F <= S(1+r) + U - Y$
where $U$ is the storage/carrying cost and $Y$ is the convenience yield.
If the no-arbitrage condition binds, this is often written as:
$F = S(1+r) + U - Y$
\
== mod 3
$h^* = rho (sigma_s / sigma_f)\
N^* = h^* (Q_a / Q_f)$
"perfect hedge" means 0 uncertainty, not a guarantee of any specific outcome.\\
hedge effectiveness = $rho^2$, the $R^2$ from regressing spot price changes on futures price changes.
perfect hedge requires $rho = 1$.\\
To move a portfolio's beta from $beta$ to a target $beta^*$, the number of index futures contracts required is:
$N = (beta^* - beta) times V_A / V_F$
where $V_A$ is the value of the portfolio and $V_F$ is the value of one futures contract (futures price × multiplier). A negative $N$ means a short position; a positive $N$ means a long position.\

$"business gain" = "realized sale price"(S_2) - "price locked in"(F_1)$\\

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
position greek = single-option greek times \# of underlying shares\
portfolio excess return = market excess return times beta\
market total return = risk-free rate + market excess return\
index capital return = index total return - dividend yield\
call delta = $e^(-q T)$ times N(d1)\
put delta = $-e^(-q T)$ times N(-d1) = call delta - $e^(-q T)$\
future/forward delta = $e^((r-q) T)$\

== mod 7
52 weeks per year, 12 months per year, 365 calendar days per year;
for volatility, we use 252 trading days per year.\
#table(
  columns: (auto, 1.5fr, 1.5fr, 1fr),
  align: (left, left, left, center),
  stroke: 0.5pt + luma(120),
  fill: (col, row) => if row == 0 { luma(240) } else { none },
  
  [#table.header([*期权类型*], [*对冲组合 (Hedging Portfolio)* \ _创造无风险资产_], [*复制组合 (Replicating Portfolio)* \ _创造等效期权资产_], [*Delta ($Delta$) 的正负*])],
  
  [看涨期权 (Call)], [Top Pick: *Long Stock* + Short Call], [*Long Stock* + Borrow Cash], [$Delta > 0$ \ (正数)],
  [看跌期权 (Put)], [Top Pick: *Short Stock* + Long Put], [*Short Stock* + Lend Cash], [$Delta < 0$ \ (负数)],
)
up factor in binomial model: $u=s_u/s_0$ or $u=e^(r T+sigma sqrt(T))$\
$delta = (f_u - f_d) / (S_u - S_d)$\
volatility $sigma$ over period T = $sqrt(T) times sigma_"annual"$\
for stock underlying, $d_1 = [ln(S_0/K) + (r-q+sigma^2/2)T] / (sigma sqrt(T))$\ 
for future underlying (no r,q drift), $d_1 = [ln(F_0/K) + (sigma^2/2)T] / (sigma sqrt(T))$\
As T goes to infinity, the call price approaches the stock price and the put price approaches zero.\
With a dividend yield, the call/put price rise, peak, and falls. 虽然它们都会在时间过长时发生价格崩溃（下滑），但Call 崩溃是因为股票被红利薅秃了，而 Put 崩溃是因为未来的现金被时间折现榨干了.\

== mod 8
bear spread: long put at higher strike, short put at lower strike; bull spread: long call at lower strike, short call at higher strike\
aggressive bear/bull spread: both strikes are in-the-money; conservative bear/bull spread: both strikes are out-of-the-money\
straddle: long call and long put at same strike; strangle: long call and long put at different strikes\
butterfly spread: long call at lower strike, short 2 calls at middle strike, long call at higher strike\
syntheic long forward: long call and short put at same strike; synthetic short forward: short call and long put at same strike\

