# AI response for Appendix C — run 16 Nov 2026

Prompt (verbatim, as drafted in report/basis-trade-draft.md Appendix C):
> "Explain the Treasury cash-futures basis trade and why it is considered low-risk: a hedge fund buys cash Treasuries, sells Treasury futures, finances the bonds in repo, and earns the basis as it converges to zero at delivery. What are the risks?"

Method: the prompt was given verbatim to a fresh AI assistant (a separate agent)
with no access to the report, the data, or any prior context — the way a
student would get the answer from a general-purpose AI. The response below is
quoted in full, unedited.

## Response (verbatim)

The Treasury cash-futures basis trade is a classic relative-value strategy. A hedge fund buys a cash Treasury bond — usually the cheapest-to-deliver (CTD) bond into the futures contract — and simultaneously sells the matching Treasury futures contract. It finances the cash bond in the repo market, borrowing most of the purchase price against the bond as collateral. The difference between the cash price and the futures price (adjusted by the bond's conversion factor) is called the basis. At futures delivery, the basis must converge to zero, because the futures contract settles by delivery of the bond itself. So if the fund holds the position to delivery, it locks in the basis it bought at entry, plus the difference between the repo rate it pays and the implied repo rate embedded in the futures price. That's the profit.

It's considered low-risk for a few intuitive reasons. First, the position is duration-hedged: the short futures contract offsets the interest-rate risk of the long cash bond, so if yields rise or fall, the gain on one leg roughly cancels the loss on the other. Second, the payoff is anchored by convergence — the basis is a known quantity that mechanically shrinks to zero at delivery, so the trade looks like an arbitrage rather than a directional bet. Third, the collateral is U.S. Treasuries, the most liquid and creditworthy asset in the world, so funding in repo is cheap and readily available, and haircuts are small (often around 2%), which lets the fund run the trade at high leverage — 50x is common — turning a tiny basis of a few basis points into a meaningful return on equity.

But the risks are real, and they're mostly about funding and liquidity rather than interest rates. The main ones:

- **Funding and repo risk.** The trade is financed overnight or very short-term in repo. If repo rates spike or lenders pull back, the fund's carry turns negative and it may have to unwind at a loss.
- **Variation margin.** The futures leg is marked to market daily and settled in cash. If yields fall, the short futures position loses money and the fund must post cash margin immediately, even though the offsetting gain on the cash bond is unrealised — it can't be spent. A large enough yield move can produce a margin call bigger than the fund's equity.
- **Haircut increases.** If repo lenders raise haircuts in volatile markets — say from 2% to 4% — the fund must suddenly double the equity behind the same position or sell bonds to shrink it, which pushes prices down further.
- **Basis widening.** The basis can move against the fund before delivery. In a stress episode like March 2020, the basis widened sharply as funds rushed to sell, and leveraged holders were forced out at the worst moment. Convergence only helps if you can hold to delivery.
- **Cheapest-to-deliver switch.** The futures contract allows delivery of any bond in a basket, and which bond is cheapest can change as yields move. If the CTD switches, the hedge ratio breaks and the position is no longer properly hedged.
- **Rollover risk.** The position must be rolled into the next futures contract each quarter, and the roll is itself a moment when funding and margin can bind.
- **Crowded-trade and correlation risk.** Many funds run the same trade at the same time, so when one fund is forced to sell, they all are — selling into the same market, against the same collateral, from the same lenders. What looks market-neutral for one fund becomes systemic when everyone holds it.

So the trade is low-risk in the narrow sense — it's hedged against yields and its terminal payoff is known — but it's highly exposed to the plumbing: repo funding, margin timing, haircuts, and the fact that the very leverage that makes it profitable also makes it fragile.

## Check against the draft critique (for Appendix C)

Draft predicted four errors; checked against this response:
- "Calls the trade risk-free arbitrage / market-neutral" — NOT supported as written: it says "looks like an arbitrage" and "looks market-neutral", never "risk-free", and concludes the trade is "highly exposed to the plumbing". Corrected in the critique, not repeated.
- "Lists interest-rate risk as the main risk" — WRONG: it says the risks are "mostly about funding and liquidity rather than interest rates". Dropped.
- "Omits the CTD switch" — WRONG: it covers the CTD switch explicitly. Dropped.
- "Treats the $830bn aggregate as measured" — N/A: it makes no aggregate claim at all. Dropped.

Genuine errors found in this response:
1. Leverage as typical: "haircuts are small (often around 2%)" / "50x is common". Verified: haircuts typically around 3% or less; measured leverage of large basis traders in 2019 averaged 21x (median 17.6x) (Barth & Kahn, OFR WP 21-01). 50x is only the leverage at the assumed 2% haircut in our model.
2. Sign condition missing: "earns the basis as it converges to zero" / "locks in the basis it bought at entry", with no condition that convergence only earns when cash is cheap at entry (G < 0). With G = P − CF×F, clean P&L = dG; our model: Nov 10 entry G = −0.0554 earned +$55,425; the par illustration's original +$120,000 had this sign flipped (corrected to −$80,000).

What it gets right: funding/liquidity framing, margin call can exceed equity (our model: 144.7% on a 50 bp fall), haircut channel, March 2020 widening, CTD switch, rollover, crowded-trade correlation. It invents no figures.
