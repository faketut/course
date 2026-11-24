// AFM 425, Group 8, Presentation deck, Topic 13: Hedge-Fund Treasury Basis Trade
// 9 slides for the 10-minute talk + 6 backup slides for Q&A.
// All numbers from analysis/basis_trade_real_ctd.py (canonical v0.5, Nov 10 legs).
// Compile: ~/workspace/exam_prep/bin/typst compile presentation.typ "AFM425 Presentation Group 8.pdf"

#set page(
  width: 33.867cm,
  height: 19.05cm,
  margin: (x: 2cm, y: 1.5cm),
  footer: context [
    #grid(
      columns: (1fr, auto),
      text(size: 11pt, fill: rgb("#666666"))[AFM 425 · Group 8 · Topic 13 · Hedge-Fund Treasury Basis Trade],
      text(size: 11pt, fill: rgb("#666666"))[Slide #counter(page).display()],
    )
  ],
)
#set text(font: ("Liberation Sans", "DejaVu Sans"), size: 18pt)
#set par(leading: 0.55em, spacing: 0.7em)

#let slide(title, time: none, body) = {
  pagebreak(weak: true)
  grid(
    columns: (1fr, auto),
    align: (left, right),
    text(size: 27pt, weight: "bold", fill: rgb("#1a3a5c"))[#title],
    if time != none { text(size: 13pt, fill: rgb("#666666"))[#time] },
  )
  v(0.35em)
  line(length: 100%, stroke: 1.5pt + rgb("#1a3a5c"))
  v(0.7em)
  body
}

#let backup(title, body) = {
  pagebreak(weak: true)
  grid(
    columns: (1fr, auto),
    align: (left, right),
    text(size: 27pt, weight: "bold", fill: rgb("#1a3a5c"))[#title],
    text(size: 13pt, fill: rgb("#666666"))[Backup · Q&A only],
  )
  v(0.35em)
  line(length: 100%, stroke: 1.5pt + rgb("#1a3a5c"))
  v(0.7em)
  body
}

// ---- Slide 1: title ----
#align(center + horizon)[
  #text(size: 34pt, weight: "bold", fill: rgb("#1a3a5c"))[The Hedge-Fund Treasury Basis Trade and Systemic Risk (2024–2026)]
  #v(0.8em)
  #text(size: 20pt)[AFM 425 · Group Assignment · Topic 13]
  #v(0.5em)
  #text(size: 18pt)[Group 8 · Jian Feng · Wenzheng An · David Jiang · Johnson Xu · Zhaozhen Xi]
  #v(0.4em)
  #text(size: 16pt, fill: rgb("#666666"))[November 2026]
  #v(1.2em)
  #text(size: 18pt, style: "italic")[Duration-hedged, not cash-flow-hedged.]
]

#slide("The hook: 'risk-free' arbitrage at scale", time: "0:00–1:30")[
  #text(size: 22pt)[*\$830bn of "risk-free" arbitrage, levered 50x, in the world's safest market.*]
  #v(0.5em)
  - The trade in one line: buy cash Treasuries, sell futures, finance in repo, earn the basis as it converges to zero.
  - Scale: ~\$830bn by September 2025: about 35% of hedge funds' \$2.4tn long Treasury exposure, 3.5% of privately held Treasuries (Monin, Federal Reserve FEDS Notes, June 2026).
  - *Thesis:* the position is duration-hedged, not cash-flow-hedged. The risk is funding, not yields.
]

#slide("Mechanics: three legs, one basis", time: "1:30–3:30")[
  #table(
    columns: (1fr, 1fr, 1fr),
    align: left,
    stroke: 0.5pt + rgb("#999999"),
    inset: 10pt,
    [*1. Buy cash*], [*2. Sell futures*], [*3. Finance in repo*],
    [Own the cheapest-to-deliver bond], [Short the matching 10y futures], [Borrow ~98%, post ~2% equity],
  )
  #v(0.5em)
  - Basis *G = P(cash) − CF × F(futures)*; at delivery, G → 0.
  - The *conversion factor (CF)* makes different bonds comparable: invoice = CF × futures price + accrued.
  - *Haircut = leverage:* a 2% haircut is 50x leverage. The funding terms are the trade.
  - Note: 50x is our model's leverage at the assumed 2% haircut; measured fund leverage averaged 21x in 2019 (Barth & Kahn, OFR WP 21-01).
]

#slide("The real cheapest-to-deliver", time: "1:30–3:30")[
  - CTD into the December 2026 10y futures: *3 7/8% note due 15 August 2033, CUSIP 91282CHT1.*
  - Coupon 3.875%, conversion factor *0.8870*, implied repo *3.39%* (highest in the basket), yield 4.894%.
  - Observed Nov 10 close *94.188* (bid 94.094 / offer 94.125); futures at the official Nov 10 settle *106.25*.
  - The CTD is only 111bp of implied repo ahead of the next bond (4.5% 11/15/2033, 2.28%). *The CTD can switch, breaking the hedge ratio.*
]

#slide("Quant: the trade", time: "3:30–6:30 · slow down here")[
  - Representative trade: *\$100m face*, 20 days to delivery (1 December 2026).
  - Equity *\$1.90m* (2% haircut); repo borrowing *\$93.21m*; leverage 50x; *887 DV01-matched contracts* (DV01 \$55,034/bp).
  - Coupon +\$212,329; repo cost −\$198,173; carry +\$14,156.
  - Basis at entry *−0.0554 pts* (cash cheap) → basis P&L +\$55,425.
  - *Base case: +\$67,850 (+3.57% of equity).* Bracket across the Nov 10 prints: +\$68k–\$164k; sign positive throughout.
  - The sign lesson: clean P&L = dG. Convergence only earns when cash is *cheap* at entry.
]

#slide("Quant: the stress table", time: "3:30–6:30 · slow down here")[
  #table(
    columns: (1fr, auto, auto),
    align: (left, right, right),
    stroke: 0.5pt + rgb("#999999"),
    inset: (x: 12pt, y: 8pt),
    [*Shock*], [*Cash cost*], [*% of equity*],
    [Repo +50bp], [\$25,538], [1.34%],
    [Haircut 2% → 4%], [\$1,902,299], [100.0%],
    [Basis +0.50 pts], [\$500,000], [26.3%],
    [Yields fall 50bp], [\$2,751,689 VM call], [144.7%],
    [Yields rise 50bp], [~\$0 net], [~0%],
  )
  #v(0.5em)
  - Read the row that matters: a 50bp fall demands *145% of equity in cash*, while the offsetting cash gain is unrealised.
  - Aggregate: at \$830bn, a 0.10-pt widening is an ~\$830m collective loss; gross long-leg DV01 ~\$485m per bp.
]

#slide("Implications I: who bears it", time: "6:30–8:30")[
  - *Dealers and prime brokers:* raise haircuts and margin fund by fund; collectively they create the fire sale.
  - *Asset managers:* their long futures demand is what the trade turns into cash-market liquidity: genuine value, provided by the most fragile holders.
  - *The public:* Treasury yields set mortgage rates and borrowing costs; in March 2020 only ~\$1.6tn of Fed purchases stopped the rout.
]

#slide("Implications II: regulators", time: "6:30–8:30")[
  - *Central clearing* (SEC 34-99149): cash by 31 Dec 2026, repo by 30 Jun 2027. It reaches the funding leg, not hedge-fund cash trades.
  - *FSB* (final report, 9 July 2025, Rec. 4–5): minimum haircuts in government-bond repos, enhanced margin, central clearing.
  - *Basis purchase facility* (Kashyap et al., Brookings Spring 2025, *not* a Fed proposal): hedged purchases, duration-neutral, penalty pricing against moral hazard.
  - *March 2020 vs April 2025:* keep the basis trade and the swap-spread trade distinct: the documented April 2025 unwind (~\$60bn) was swap-spread.
]

#slide("Takeaways", time: "8:30–10:00")[
  - A hedge is not a hedge against everything: hedged on yields, exposed on funding, haircuts and margin timing.
  - Leverage is not a footnote: at 50x, the funding terms are the trade; a 2pp haircut change is a 100% capital call.
  - Individually rational trades can be collectively catastrophic.
  #v(0.8em)
  #text(size: 22pt)[*"The hedge works on yields; it is the funding that kills you."*]
  #v(0.5em)
  #text(size: 16pt, fill: rgb("#666666"))[Thank you. Questions?]
]

#backup("Sensitivity")[
  - Haircut: 0% → ∞, 1% → 100x, 2% → 50x, 4% → 25x.
  - Repo: +25bp \$12,769 / +50bp \$25,538 / +100bp \$51,075.
  - Basis: +0.10 pts \$100,000 / +0.50 \$500,000 / +1.00 \$1,000,000.
  - Variation margin call: ±25bp \$1,375,844 (72%) / ±50bp \$2,751,689 (145%) / ±100bp \$5,503,377 (289%).
]

#backup("“Isn't the basis guaranteed to converge?”")[
  - Yes, at delivery, *if you can hold it there.*
  - The risk is the cash calls before delivery: repo, haircuts, margin.
  - March 2020 is the example: the basis widened for weeks before it converged.
]

#backup("“Why don't funds just hold more equity?”")[
  - At 5x instead of 50x, the same trade earns roughly a tenth as much on equity: under 0.4% over 20 days, against 3.57% at 50x.
  - *The business model is the leverage.*
]

#backup("“Was March 2020 caused by the basis trade?”")[
  - OFR evidence (Barth & Kahn): the unwind was likely *a consequence as much as a cause*; the shock was the flight to cash.
  - Dealers provided 11–13% *more* repo funding, not less (Kruttli et al. 2025).
  - Don't overclaim: the trade amplified the shock; it was not the shock.
]

#backup("“What would central clearing change?”")[
  - Standardised margin, less bilateral repo, more transparent exposures.
  - Margin is still procyclical: the call can still arrive faster than the cash.
]

#backup("Counter-argument: liquidity and the Fed")[
  - *"The trade adds liquidity, and the Fed can always intervene."*
  - Liquidity that vanishes in stress is not liquidity.
  - Intervention is the public paying for private leverage.
]
