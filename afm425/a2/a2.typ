= Problem Solving Case \#1 (25 points)

You are assessing a bond position in a fixed-income portfolio. The bond details
are as follows: a 10-year, 7.5% semiannual-pay corporate bond maturing on
February 15, 2030. The current date is October 20, 2026, and the bond's YTM is
10%, quoted on a street-convention (30/360 day count) semiannual bond basis.

+ Using the provided information and the estimation method, calculate the
  modified duration of the bond position for a 25-bps yield change. (5 marks)\
  $"using the 30/360 day-count convention:"\
  "accrued days (Aug 15 - Oct 20, 2026):" quad (10-8)(30)+(20-15)=65 "days"\
  "fraction of period left to next coupon (Feb 15, 2027):" quad f=(180-65)/180=0.6389\
  "remaining payments (Feb 2027, Aug 2027, ..., Feb 2030):" quad 7\
  "(YTM=10%, i.e. 5% per half-year):"\
  "value at next coupon date:" quad 3.75(1+(1-1.05^(-6))/0.05)+100(1.05)^(-6)=\$97.41\
  "dirty (full) price:" quad 97.41/(1.05)^(0.6389)=\$94.42\
  "accrued interest:" quad (65/180)(3.75)=\$1.35\
  "clean price:" quad V_0=\$94.42-\$1.35=\$93.06\
  "(-25 bp, YTM=9.75%):" quad V_- = 95.08 " dirty," quad 93.73 " clean"\
  "(+25 bp, YTM=10.25%):" quad V_+ = 93.76 " dirty," quad 92.40 " clean"\
  "modified duration" approx (V_- - V_+)/(2 Delta y V_0) = (95.08-93.76)/(2 times 0.0025 times 94.42) approx 2.81 "years"\
  $
  The denominator must be the *full* (dirty) price 94.42: accrued interest does not
  react to the yield, so the position's sensitivity is driven by the full price, and
  the answer is *modified duration $approx 2.81$ years*. (Dividing by the clean price
  93.06 gives $2.85$; that variant understates the sensitivity because the accrued
  interest is part of the value at risk.)

+ Define the concepts of Macaulay duration and modified duration. How are they
  related? Using the bond's modified duration, compute its Macaulay duration.
  (4 marks)\
  *Macaulay duration:* the present-value-weighted average time (in years) until the bond's cash flows are received,
  $"MacDur" = (sum_t t dot "PV"("CF"_t))/V_0$.\
  *Modified duration:* the percentage price change per unit (100%) change in yield,
  $"ModDur" = -(1/V_0)(dif V)/(dif y)$.\
  *Relationship:* $"ModDur" = "MacDur"/(1+"YTM"/k) quad <==> quad "MacDur" = "ModDur"(1+"YTM"/k)$,
  where $k$ is the number of coupon payments per year (here $k = 2$).\
  $"MacDur" = 2.8056(1.05) = 2.95 "years" quad ("built on the full-price modified duration")$
  (The clean-price variant gives 2.8464 × 1.05 = 2.99 years; 2.95 is the consistent value.)

+ While you're evaluating the bond, your supervisor inquires about the
  relationship between time to maturity and bond Macaulay durations for:

  - A zero-coupon bond
  - A fixed-rate premium bond
  - A fixed-rate discount bond

  How would you elucidate these relationships? (6 marks)\

  *Zero-coupon bond.* $"MacDur" = T$ exactly: the only cash flow arrives at maturity,
  so the present-value-weighted average time is the maturity itself. Its modified
  duration is smaller, $T slash (1+y slash k)$.

  *Fixed-rate premium bond* (coupon rate above the YTM). $"MacDur"$ increases as the
  maturity lengthens, but at a decreasing rate: it is always below $T$ and converges
  to the perpetuity limit $(1+k slash y)$. At $y = 0.10$ and $k = 1$ that ceiling is
  11.0 years, so extending maturity keeps adding duration but with diminishing effect.

  *Fixed-rate discount bond.* $"MacDur"$ also generally rises with maturity, but for
  long-term *deep-discount* bonds a duration reversal appears: $"MacDur"$ rises, peaks,
  then declines back towards $(1+k slash y)$ as $T -> infinity$. At $y = 0.10$ a 3%
  coupon bond peaks at 12.68 years ($T = 30$) and falls to 11.67 years at $T = 50$;
  a 1% coupon bond peaks at 17.05 years. In every case $"MacDur" <= T$, with equality
  only for a zero.

+ After assessing the bond's duration, you decide to refine your price movement
  estimate by considering convexity. Using the same bond details, calculate the
  bond's approximate convexity for a 25-bps yield change. (5 marks)\
  $"approximate convexity" approx (V_- + V_+ - 2 V_0)/((Delta y)^2 V_0)$\
  $= (95.08108+93.75662-2(94.41595))/((0.0025)^2 (94.41595)) = 0.00580/0.00059010 approx 9.83$\
  The answer is *convexity $approx 9.8$* (in the annual measure). Keep enough decimals:
  the numerator is a difference of numbers near 188.83, so rounding the prices to two
  decimals gives 0 and to four decimals gives 10 — both are pure rounding artifacts.
  The analytic value, the present-value-weighted second derivative of the full price
  at the 10% yield, is 9.83.

+ The bond position's total principal value is $100,000$. The fixed-income
  portfolio you're reviewing consists solely of this bond and a zero-coupon
  bond valued at $95,000$ with a time to maturity of 4.75 years (hint: assume
  annual compounding for the zero). Using the approximate modified duration
  from the previous question, determine the portfolio's modified duration.
  (5 marks)\

  *The zero's modified duration.* With annual compounding and a face value of
  100,000, the market value 95,000 implies $95,000 = 100,000 slash (1+y_z)^(4.75)$,
  hence $y_z = 0.01086$ (1.086%). Its Macaulay duration is the maturity, 4.75 years,
  so its modified duration is $4.75 slash (1+y_z) = 4.70$ years — not 4.75.

  *Market-value weights (full prices).* bond position:
  $100,000 slash 100 times 94.41595 = \$94,415.95$; zero: $\$95,000$; total
  $\$189,415.95$. Hence $w_"bond" = 49.85$% and $w_"zero" = 50.15$%.\
  $"ModDur"_"portfolio" = w_"bond" "ModDur"_"bond" + w_"zero" "ModDur"_"zero" = 0.4985(2.8056)+0.5015(4.699) approx 3.76 "years"$\
  The weights must be *market-value* weights (weighting by principal, or by par
  value, has no theoretical content). Using clean prices instead changes the answer
  only marginally, to 3.78 years.

= Problem Solving Case \#2 (25 points)

You are evaluating two fixed-income securities. One is a 12.90-year maturity
zero-coupon bond with a yield to maturity of 9%. This zero has modified duration
of 11.83 years and convexity of 150.9. The other is a 30-year maturity,
4%-annual-payment coupon bond trading at the same yield to maturity and with
the same modified duration. However, the coupon bond has higher convexity of
236.4.

+ Suppose unexpectedly positive job market data has been released. Anticipating
  that the central bank will adopt a more cautious approach regarding the timing
  of policy benchmark rate cuts, both short-term and long-term market interest
  rates have risen. As a result, the yields on both zero-coupon and coupon bonds
  increased by 1.5% to 10.50%.

  What is the actual percentage change in bond price? What is the change
  predicted by duration? What is the change predicted by duration plus
  convexity? (9 points)

  There is no change to the term to maturity of either bond. Include your
  calculation steps and summarize your results in the table.\
  $1. "zero-coupon bond:"\
  P_0 = 100/(1.09)^12.9 = 32.90\
  P_1 = 100/(1.105)^12.9 = 27.58\
  "actual" quad %Delta P = (27.58-32.90)/32.90 = -16.16%\
  2. "coupon bond:"\
  P_0 = 4(1-(1.09)^(-30))/0.09 + 100(1.09)^(-30) = 48.63\
  P_1 = 4(1-(1.105)^(-30))/0.105 + 100(1.105)^(-30) = 41.19\
  "actual" quad %Delta P = (41.19-48.63)/48.63 = -15.30%\
  "predicted by duration:" quad %Delta P = -"ModD" times Delta y = -11.83(0.015) = -17.75%\
  "predicted by duration + convexity:" quad %Delta P = -"ModD" Delta y + 1/2 "CX" (Delta y)^2\
  1) "zero:" quad -17.75% + 0.5(150.9)(0.015)^2 = -16.05%\
  2) "coupon:" quad -17.75% + 0.5(236.4)(0.015)^2 = -15.09%\
  $

  #table(
    columns: (1.4fr, 1fr, 1fr, 1.2fr),
    table.header(
      [Bond],
      [Actual % change],
      [Predicted by duration],
      [Predicted by duration + convexity],
    ),
    [Zero-coupon bond (Bond A)], [-16.16%], [-17.75%], [-16.05%],
    [Coupon bond (Bond B)], [-15.30%], [-17.75%], [-15.09%],
  )

+ Suppose the scenario described in question 1 did not occur. Instead, imagine
  there was a spike in unemployment coupled with a sharp decline in the CPI
  data, leading to market concerns that overly aggressive tightening has
  precipitated a recession. In reaction to these market conditions, the central
  bank announced a 50-basis-point (bps) rate cut in its latest rate decision
  meeting. Following this announcement, the yields on both zero-coupon and
  coupon bonds decreased by 1.5% to 7.5%.

  What is the actual percentage change in bond price? What is the change
  predicted by duration? What is the change predicted by duration plus
  convexity? (9 points)\
  $1. "zero-coupon bond:"\
  P_2 = 100/(1.075)^12.9 = 39.34\
  "actual" quad %Delta P = (39.34-32.90)/32.90 = 19.57%\
  2. "coupon bond:"\
  P_2 = 4(1-(1.075)^(-30))/0.075 + 100(1.075)^(-30) = 58.66\
  "actual" quad %Delta P = (58.66-48.63)/48.63 = 20.63%\
  "predicted by duration:" quad %Delta P = -"ModD" times Delta y = -11.83(-0.015) = 17.75%\
  "predicted by duration + convexity:" quad %Delta P = -"ModD" Delta y + 1/2 "CX" (Delta y)^2\
  1) "zero:" quad 17.75% + 0.5(150.9)(0.015)^2 = 19.44%\
  2) "coupon:" quad 17.75% + 0.5(236.4)(0.015)^2 = 20.40%\
  $
  #table(
    columns: (1.4fr, 1fr, 1fr, 1.2fr),
    table.header(
      [Bond],
      [Actual % change],
      [Predicted by duration],
      [Predicted by duration + convexity],
    ),
    [Zero-coupon bond (Bond A)], [19.57%], [17.75%], [19.44%],
    [Coupon bond (Bond B)], [20.63%], [17.75%], [20.40%],
  )

+ Compare the two bonds under both market scenarios. Which bond appears more attractive? Which bond is a "long convexity" trader most likely to favor? (7 points)\
  Bond B (the coupon bond) is consistently more attractive. The two bonds have the
  same modified duration (11.83), so the comparison is driven purely by convexity:
  convexity is always beneficial — it adds price when yields fall and cushions the
  price when yields rise. Bond B therefore loses less in the sell-off (-15.30% vs
  -16.16%) and gains more in the rally (20.63% vs 19.57%). Its cash flows are more
  dispersed (they are spread over 30 years rather than concentrated at one maturity),
  which is exactly what produces the higher convexity (236.4 vs 150.9). A "long
  convexity" trader will favor Bond B: it delivers more convexity per unit of duration
  risk, and here it does so at the same yield.