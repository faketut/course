= Case 1
1) The yield-to-maturity (YTM) is the annualized internal rate of return (IRR) that makes the present value of all of the bond's promised future cash flows (coupons and principal) equal to its current full price. It is a _promised_ return calculated under a set of assumptions, not a _guaranteed_ realized return. Therefore, Mrs. Smith will only actually earn 6% per year if all of the following hold:

- She holds the bond to maturity; selling early exposes her to price (interest-rate) risk, so the realized return would differ from 6%.
- The issuer does not default and makes every promised coupon and principal payment in full and on time (no credit risk).
- Every coupon received is reinvested at 6% until maturity (no reinvestment risk).
- The bond is not called/redeemed early and no other embedded option is exercised, so the cash flows occur exactly as scheduled.

If any of these conditions fails, the realized return will differ from the quoted YTM. For example, if market rates fall, coupons are reinvested at less than 6% and the realized return is below 6%; if rates rise, coupons are reinvested at more than 6% but the bond's resale price falls (these two effects only cancel if she holds to maturity and the curve is flat). In practice, the only bond for which YTM is guaranteed regardless of reinvestment is a zero-coupon bond, since it has no intermediate cash flows to reinvest.\
2) Inputs: $N=2(2032-2026)+1=13, c=(9%)/2=4.5%, i=(7.6%)/2=3.8%, f=3/180, P=100, A=(1-(1+i)^(-N))/(i)$\
$"FP"=(1+i)^f (P+P(c-i)A)=107.14$\
3) $"AI"=f C=f P c=0.075, "CP"="FP"-"AI"= 107.07$\
Quoted price (also called clean price) is the value of full price excluding the accrued interest. The difference between the quoted price and the full price on the settlement date is the accrued interest. Dealers quote the clean price so that market price fluctuations aren't distorted by how close the bond is to its next interest payment. However, Mrs. Smith will actually pay the full price because the buyer must compensate the seller for accrued interest.\
4) By $(1+"APR"_12/12)^12=(1+"APR"_2/2)^2$, we have $"APR"_2=8.76%$, which is higher than Heavy Equipment Bond's 7.6%. Thus, the Rock Bond is more attractive.\

= Case 2
1) $N=20, c=(6.5%)/2=3.25%, P=100, i=(9%)/2=4.5%, f=0, A=(1-(1+i)^(-N))/(i)$\
$"FP"=(1+i)^f (P+P(c-i)A)=83.74$\
2) Since 6.5% coupon rate is less than 9% market discount rate (YTM), investors demand a price reduction to compensate for lower interest payment, making it discount bond.\
3) 
- enter the calculated bond purchase price (\$83.74) as the opening carrying value at period 0.\
- for each period, calculate the true economic interest expense by multiplying the opening carrying value by the semi-annual market discount rate (4.5%).\
- subtract the fixed cash coupon payment (\$3.25) from the interest expense. This difference represents the unearned discount that must be added back to the bond's book value.\
- repeat 20 times updating the carrying value by adding the period's discount amortization. By period 20, the carrying value will land on the\$100 par value.


= Case 3
1) By $P_i=C/2 (sum_1^(i-1) d_(0.5 i))+(100+C/2)d_(0.5 i) "and" d_t=1/(1+z_t/2)^t$, we have
- t=0.5 Y (1 period)\
  $P_1=(100+1.875) d_(0.5)=99.177975 arrow.r d_(0.5)=0.973526. z_(0.5)=2(1/d_(0.5) -1)=5.4388%$.
- t=1 Y (2 period)\
  $P_2=2.525 d_0.5 +102.525 d_1=99.399571 arrow.r d_(1)=0.945539. z_(1)=2(d_(1)^(-1/2) -1)=5.6791%$.
- t=1.5 Y (3 period)\
  $P_3=3.195(d_0.5 +d_1)+103.195 d_(1.5)=100.547780 arrow.r d_(1.5)=0.914932. z_(1.5)=2(d_(1.5)^(-1/3) -1)=6.0158%$.\
- t=2 Y (4 period)\
  $P_4=1.22(d_0.5+d_1+d_1.5)+101.22 d_2=94.424926 arrow.r d_2=0.898710. z_2.0=2(d_2^(-1/4)-1)=5.4117%$\
- t=2.5 Y (5 period)
  $P_5=3.65(d_0.5+...+d_2)+103.65 d_2.5=105.038305 arrow.r d_2.5=0.881948. z_2.5=2(d_2.5^(-1/5)-1)=5.0885%$.
- t=3 Y (6 period)
  $P_6=3.235(d_0.5+...+d_2.5)+103.235d_3=104.589915 arrow.r d_3=0.868518. z_3=2(d_3^(-1/6)-1)=4.7545%$\

2) Cash flow happens at t=1,1.5,...,3 from now on and each pay coupon $C/2$. We need to discount $P_0$ forward by $d_0.5$ to get $P_0.5$, thus $P_0.5=(2.5(d_1+d_1.5+d_2+d_2.5)+102.5d_3)/(d_0.5)=100.7944$.\
$100.7944=limits(sum)^5_(k=1) 2.5/(1+r)^k +100/(1+r)^5 arrow.r r approx 2.3298%$. Thus, $"YTM"=2(2.3298%) approx 4.66%$.\
3) The bond pays a semi-annual coupon of $(6%)/2 = 3%$ (on a par value of 100) at $k=1,...,5$ and a final payment of $103$ at $k=6$. A z-spread of 150 bps adds $(1.50%)/2 = 0.75%$ to each semi-annual discount rate; thus by $P = sum_(k=1)^6 ("CF"_k)/(1+z_k/2 + 0.0075)^k$, we have $P = 99.17$.\
4) $95.45=limits(sum)^6_(k=1) 2.675/(1+r)^k+100/(1+r)^6 arrow.r r=3.5297%$.
So $"YTM"=2 r=7.06%$\
$"Nominal Spread"="YTM"-"Benchmark Yield"=7.06%-4.50%=256 "bps"$.\
$95.45=limits(sum)^6_(k=1)2.675/(1+z_k/2 +s)^k +100/(1+z_6/2+s)^6$\
By excel's goal seek function, we have $s=1.1290%$. $Z=2 s=2.2580%=225.80 "bps"$.\

= Case 4
1) Representative dates I pick for the respective periods are: 2008/9/15, 2020/1/31, 2020/4/20, 2022/2/28, 2023/7/3, 2026/9/23.\
Yield curves plot (data source: U.S. Department of the Treasury, _Daily Treasury Par Yield Curve Rates_, retrieved September 2026):
#image("./us_treasury_yield_curves_across_representative_periods.png")
a. GFC (2008): Short rates collapsed 1.02% due to emergency Fed cuts and flight-to-safety, while 10Y rates stayed higher ($3.47\%$) expecting eventual economic recovery.\
b. Pre-COVID (2020): Rates compressed near 1.30%-1.57%, inverting the 10Y-3M spread as late-cycle momentum slowed.\
c. COVID Panic (2020): Emergency rate cuts 0.00%-0.25% and massive QE pushed the entire curve down near historical lows 10Y at 0.63%.\
d. Pre-Hikes (2022): Front-end yields remained anchored near zero, but intermediate/long yields rose 10Y at 1.83% pricing in upcoming anti-inflation hikes.\
e. Deep Inversion (2023): Aggressive Fed tightening raised short rates to 5.44%, while long rates remained lower 3.86% expecting a policy-induced economic slowdown and eventual rate cuts.\
f. Current Period (2026): The curve un-inverted and re-steepened into a normal slope (10Y-2Y = +0.56%) as front-end rates eased while long-end yields rose due to ongoing Treasury issuance. \
2) When the Fed hikes short rates to restrictive levels, markets anticipate an economic contraction that will force future rate cuts. Investors rush to lock in long-term bonds, bidding prices up and driving long-term yields below short-term rates. \ Inversion squeezes bank Net Interest Margins (NIM) by making short-term borrowing costlier than long-term lending returns. Banks restrict credit expansion, suppressing business investment and consumer spending.\
Bull Steepening: Short rates fall rapidly as the central bank cuts rates to cushion a slowing economy.
Bear Steepening: Long rates rise faster than short rates, driven by high inflation, term premium expansion, or heavy government debt issuance.\
Historically, recessions begin not during the deep inversion, but as the curve un-inverts and re-steepens, because lagging credit tightening impacts finally hit corporate refinancings and employment. The recent re-steepening reflects both policy recalibration on the front end and elevated fiscal debt issuance pushing up long-end yields 5.00%+, indicating that macroeconomic risk remains active during this transition window.\

= References
- U.S. Department of the Treasury. _Daily Treasury Par Yield Curve Rates._ https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve
- Federal Reserve Bank of New York. _The Yield Curve as a Leading Indicator (Applied Macroeconomics and Econometrics Center)._ https://www.newyorkfed.org/research/capital_markets/ycfaq
- Federal Reserve Bank of St. Louis. _FRED Economic Data_ (Treasury Constant Maturity and Term Spread series). https://fred.stlouisfed.org
- Estrella, A., and Mishkin, F. S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." _The Review of Economics and Statistics_, 80(1), 45–61.\

