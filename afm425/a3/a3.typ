= Problem Solving Case \#1 (30 points)

+ The three quotations are for the same three-year, €100-par, 2.15% annual-pay, option-free bond. By the law of one price, identical cash flows must have the same present value. Eurex is the most expensive (€102.7962) and Frankfurt the cheapest (€102.3512). (5 points)\
  *Action.* Buy the bond on Frankfurt at €102.3512 and simultaneously sell the same bond on Eurex at €102.7962. The bond bought in Frankfurt is delivered against the short sale on Eurex, so the coupon and principal cash flows cancel. The locked-in profit is
  $ 102.7962 - 102.3512 = €0.4450 "per €100 par." $
  The NYSE Euronext quote (€102.4540) is between the two extremes and is not part of the best pair.

+ The 1-, 2-, and 3-year par rates bootstrap the annual discount factors: (5 points)
  $
    d_1 &= 1/(1+0.015) = 0.9852217, \
    d_2 &= (1-0.0185 d_1)/(1.0185) = 0.9639405, \
    d_3 &= (1-0.0215(d_1+d_2))/(1.0215) = 0.9379276.
  $
  The spot rates are $z_1=1.5000%$, $z_2=1.8532%$, and $z_3=2.1591%$. The arbitrage-free value of the 2.15% three-year bond is
  $
    P^* = 2.15 d_1 + 2.15 d_2 + 102.15 d_3 = 2.1187 + 2.0725 + 95.8088 = €100.0000.
  $
  Because the coupon equals the three-year par rate, the bond is a par bond.

  #table(
    columns: (1.4fr, 1fr, 1fr, 1.2fr),
    table.header([Exchange], [Quote (€)], [Quote $- P^*$ (€)], [Rich / cheap]),
    [Eurex], [102.7962], [+2.7962], [Rich],
    [NYSE Euronext], [102.4540], [+2.4540], [Rich],
    [Frankfurt], [102.3512], [+2.3512], [Rich; closest],
  )

  *Conclusion.* Frankfurt is closest to the arbitrage-free price: its quote is €2.3512 above the fair value of €100.0000, versus €2.4540 for NYSE Euronext and €2.7962 for Eurex. All three quotes are rich, but Frankfurt is the least rich and Eurex the most rich.

+ With a lognormal model, no drift, volatility $sigma=15%$, and $Delta t=1$, adjacent nodes in the same time step satisfy (10 points)
  $
    r_(i,j+1) = r_(i,j)e^(-2 sigma sqrt(Delta t)),
    quad e^(-0.30)=0.740818,
  $
  so each step upward multiplies a rate by $e^(0.30)=1.349859$.

  #table(
    columns: (auto, 1fr),
    table.header([Time], [Short rates, top to bottom]),
    [0], [1.5000%],
    [1], [2.5380%, 1.8800%],
    [2], [3.6680%, *2.7173%*, 2.0130%],
    [3], [4.9440%, *3.6626%*, 2.7130%, *2.0098%*],
    [4], [*6.2890%*, 4.6590%, 3.5410%, 2.5570%, *1.8943%*],
  )

  $
    "Node 2-2" &= 3.6680 e^(-0.30) = 2.7173%, \
    "Node 3-2" &= 4.9440 e^(-0.30) = 3.6626%, \
    "Node 3-4" &= 2.7130 e^(-0.30) = 2.0098%, \
    "Node 4-1" &= 4.6590 e^(0.30) = 6.2890%, \
    "Node 4-5" &= 2.5570 e^(-0.30) = 1.8943%.
  $
  The time-4 endpoints are obtained from the adjacent printed rates 4.6590% and 2.5570%. The printed 3.5410% at time 4 is not exactly on the 15% row, so it is not used to derive those endpoints.

+ For a four-year, 2.85%, annual-pay, option-free bond, the final cash flow at time 4 is $102.85$. Define $V_t$ as the cum-coupon value at time $t$, immediately after the coupon. Backward induction gives (10 points)
  $
    V_3 &= 2.85 + 102.85/(1+r_3), \
    V_2 &= 2.85 + (0.5(V_3^u+V_3^d))/(1+r_2), \
    V_1 &= 2.85 + (0.5(V_2^u+V_2^d))/(1+r_1), \
    V_0 &= (0.5(V_1^u+V_1^d))/(1+r_0).
  $

  #table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr),
    table.header([Time], [Node 1], [Node 2], [Node 3], [Node 4]),
    [3], [100.8547], [102.0661], [102.9834], [103.6736],
    [2], [100.7205], [102.6625], [104.1395], [—],
    [1], [102.0245], [104.3430], [—], [—],
    [0], [*101.6588*], [—], [—], [—],
  )

  *Value.* The tree price is *€101.6588 per €100 par*. The bond is worth more than par because its 2.85% coupon is above the initial one-year rate of 1.50% and above the early forward rates in the lower part of the tree.

= Problem Solving Case \#2 (30 points)

+ The Ho–Lee model is a normal short-rate model with additive drift and constant absolute volatility:
  $
    dif r_t = theta(t) dif t + sigma dif W_t.
  $
  With annual steps, the up and down children of a node are $r + mu_i + sigma$ and $r + mu_i - sigma$. Given $r_0=3.25%$, $sigma=65$ bps, $mu_1=45$ bps, and $mu_2=75$ bps: (6 points)

  #table(
    columns: (auto, 1fr),
    table.header([Time], [Short rates, top to bottom]),
    [0], [3.2500%],
    [1], [4.3500%, 3.0500%],
    [2], [5.7500%, 4.4500%, 3.1500%],
  )

  $
    r_(1,u) &= 3.25% + 0.45% + 0.65% = 4.35%, \
    r_(1,d) &= 3.25% + 0.45% - 0.65% = 3.05%, \
    r_(2,"uu") &= 4.35% + 0.75% + 0.65% = 5.75%, \
    r_(2,"ud") &= 4.35% + 0.75% - 0.65% = 4.45%, \
    r_(2,"dd") &= 3.05% + 0.75% - 0.65% = 3.15%.
  $
  The tree recombines because the up-then-down and down-then-up rates both equal 4.45%.

+ The bond pays €4.25 annually on €100 par and matures at €100 in year 3. It is callable at par at the end of years 1 and 2. At each call date, the issuer compares the ex-coupon continuation value with the €100 call price and calls whenever continuation exceeds €100. The coupon for that date is paid in either case, so the cum-coupon value is (6 points)
  $
    V_t = 4.25 + min(100, "continuation value").
  $
  The final cash flow at time 3 is $104.25$.

  #table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    table.header([Time], [Rate], [Continuation], [Coupon], [Value], [Call?]),
    [2], [5.75%], [98.5816], [4.25], [102.8316], [No],
    [2], [4.45%], [99.8085], [4.25], [104.0585], [No],
    [2], [3.15%], [101.0670], [4.25], [104.2500], [Yes],
    [1], [4.35%], [99.1328], [4.25], [103.3828], [No],
    [1], [3.05%], [101.0731], [4.25], [104.2500], [Yes],
    [0], [3.25%], [—], [—], [*100.5486*], [—],
  )

  *Value.* The callable bond is worth *€100.5486 per €100 par*. The issuer calls at the time-2 node with $r=3.15%$ and at the time-1 node with $r=3.05%$. The corresponding non-callable value is €101.3180, so the embedded call option is worth
  $
    101.3180 - 100.5486 = €0.7695 "per €100 par."
  $
  The call cap reduces the bondholder's upside when rates fall.

+ The z-spread is the constant spread $z$ added to every benchmark spot rate so that the present value of the bond's contractual cash flows equals its market price: (5 points)
  $
    P_"mkt" = sum_(t=1)^T ("CF"_t)/((1+z_t+z)^t).
  $
  It does not adjust the cash flows for embedded options. For a callable bond, the contractual cash flows are not the expected cash flows, so the z-spread absorbs both credit/liquidity compensation and the cost of the issuer's call option.

  The option-adjusted spread (OAS) is the constant spread added to every node of a benchmark rate tree so that the option-adjusted model price equals the market price. The tree explicitly models the issuer's optimal call decision, so the OAS is the spread after removing the value of the embedded option:
  $
    P_"mkt" = P_"model"(z_"OAS"; "optimal exercise").
  $
  It captures credit, liquidity, and other non-option risks, but not option risk itself.

  For a callable bond, the *z-spread is typically higher than the OAS*. The difference $z - "OAS"$ is the option cost: the call option benefits the issuer and hurts the investor, so the raw z-spread must be larger to compensate for it. The OAS strips that option value out and is the cleaner measure of compensation for credit and liquidity risk. For a putable bond the ordering reverses.

+ Both Vasicek and CIR are one-factor, mean-reverting short-rate models. (5 points)

  *Vasicek (1977):*
  $
    dif r_t = kappa(theta - r_t) dif t + sigma dif W_t.
  $
  The drift pulls the rate toward $theta$ at speed $kappa$. The diffusion is additive and constant, so $r_t$ is normally distributed and can become negative. The model has an affine term structure, $P(t,T)=A(t,T)e^(-B(t,T)r_t)$.

  *CIR (1985):*
  $
    dif r_t = kappa(theta - r_t) dif t + sigma sqrt(r_t) dif W_t.
  $
  The diffusion is proportional to $sqrt(r_t)$, so volatility falls as the rate approaches zero. If
  $
    2 kappa theta >= sigma^2
  $
  holds, the origin is inaccessible and the short rate stays strictly positive. The CIR model also has an affine term structure, with different $A(t,T)$ and $B(t,T)$.

  #table(
    columns: (auto, 1.35fr, 2.2fr),
    table.header([Parameter], [Meaning], [Effect]),
    [$r_t$], [Short rate at time $t$], [State variable; starting value $r_0$],
    [$kappa$], [Speed of mean reversion], [Larger $kappa$ means faster pull back to $theta$],
    [$theta$], [Long-run mean of the short rate], [The level the drift pushes toward],
    [$sigma$], [Volatility coefficient], [Larger $sigma$ means more random fluctuation],
    [$W_t$], [Standard Brownian motion], [Source of risk],
  )

  The Vasicek model is analytically convenient but permits negative nominal rates. The CIR model rules out negative rates under Feller and makes volatility level-dependent, at the cost of a more restrictive square-root diffusion.

+ The Black–Derman–Toy model is a lognormal short-rate model. Let $U_i$ be the central level at time $i$ and $sigma_i$ the implied volatility for that step. The nodes are (8 points)
  $
    r_(i,j) = U_i exp[sigma_i (i+1-2j) sqrt(Delta t)],
    quad j=1,...,i+1,
  $
  so adjacent nodes in the same row differ by $e^(2 sigma_i sqrt(Delta t))$. The drift is the change in the central level:
  $
    theta_i = ln(U_i/U_(i-1)), quad U_0 = r_0.
  $
  The market data give
  $
    d_1=1/(1.0525)=0.9501188, quad
    d_2=1/(1.06)^2=0.8899964, quad
    d_3=1/(1.0675)^3=0.8220464.
  $

  With $sigma_1=15%$, write $r_(1,u)=U_1 e^(0.15)$ and $r_(1,d)=U_1 e^(-0.15)$. Calibrating the time-1 row to the two-year zero,
  $
    d_2 = 1/(1.0525) times 1/2(1/(1+r_(1,u))+1/(1+r_(1,d))),
  $
  gives
  $
    U_1=6.6894%, quad r_(1,u)=7.7720%, quad r_(1,d)=5.7577%.
  $

  With $sigma_2=20%$, write $r_(2,1)=U_2 e^(0.40)$, $r_(2,2)=U_2$, and $r_(2,3)=U_2 e^(-0.40)$. Backward induction through the calibrated time-1 row,
  $
    V_(1,u) &= (0.5(1/(1+r_(2,1))+1/(1+r_(2,2))))/(1+r_(1,u)), \
    V_(1,d) &= (0.5(1/(1+r_(2,2))+1/(1+r_(2,3))))/(1+r_(1,d)), \
    d_3 &= (0.5(V_(1,u)+V_(1,d)))/(1.0525),
  $
  gives
  $
    U_2=8.0073%, quad r_(2,1)=11.9454%, quad r_(2,2)=8.0073%, quad r_(2,3)=5.3674%.
  $

  #table(
    columns: (auto, 1fr, 1fr, 1fr, 1.7fr),
    table.header([Period], [$U_(i-1)$], [$U_i$], [Drift $theta_i$], [Calibrated nodes]),
    [1], [5.2500%], [6.6894%], [24.23%], [7.7720%, 5.7577%],
    [2], [6.6894%], [8.0073%], [17.98%], [11.9454%, 8.0073%, 5.3674%],
  )

  *Drift terms.* $theta_1 = ln(6.6894 slash 5.2500) = 24.23%$ and $theta_2 = ln(8.0073 slash 6.6894) = 17.98%$. The cumulative average drift over the two years is $ln(8.0073 slash 5.2500) slash 2 = 21.11%$.

= References

- Black, F., Derman, E., and Toy, W. (1990). “A One-Factor Model of Interest Rates and Its Application to Treasury Bond Options.” _Financial Analysts Journal_, 46(1), 33–39.
- Cox, J. C., Ingersoll, J. E., and Ross, S. A. (1985). “A Theory of the Term Structure of Interest Rates.” _Econometrica_, 53(2), 385–407.
- Ho, T. S. Y., and Lee, S.-B. (1986). “Term Structure Movements and Pricing Interest Rate Contingent Claims.” _Journal of Finance_, 41(5), 1011–1029.
- Vasicek, O. (1977). “An Equilibrium Characterization of the Term Structure.” _Journal of Financial Economics_, 5(2), 177–188.