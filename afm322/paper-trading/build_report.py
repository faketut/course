#!/usr/bin/env python3
"""Build the AFM 322 initial report (6pp body) + Scenario #4 doc (3pp body).

Formatting per the brief: single-spaced, 12pt Times New Roman,
1-inch margins. Appendices are separate and not counted here.
Prices, margins and premiums are TRADE-DATE figures, left as
[TBD — trade date] placeholders: the trade date itself (Nov 2 vs.
an earlier date) is still Jack's decision, and the assignment
requires trades to be shown BY Nov 2, not after it. Nothing in
these files is an executed trade.
"""
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def make_doc(title):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1); s.bottom_margin = Inches(1)
        s.left_margin = Inches(1); s.right_margin = Inches(1)
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"; st.font.size = Pt(12)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.0
    return doc

def h(doc, text):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(12)
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
    return p

def p(doc, text):
    return doc.add_paragraph(text)

def table(doc, rows):
    t = doc.add_table(rows=1, cols=len(rows[0])); t.style = "Table Grid"
    for j, v in enumerate(rows[0]):
        c = t.rows[0].cells[j]; c.text = v
        for par in c.paragraphs:
            for r in par.runs: r.bold = True
    for row in rows[1:]:
        cells = t.add_row().cells
        for j, v in enumerate(row): cells[j].text = v
    return t

# ---------------- Initial report (CRO) ----------------
doc = make_doc("initial")
t = doc.add_paragraph(); r = t.add_run("MEMORANDUM"); r.bold = True
p(doc, "To: Chief Risk Officer, Toronto's Dreamworld Inc. (TDI)")
p(doc, "From: Risk Management Department")
p(doc, "Date: [TBD — trade date, on or before November 2, 2026]")
p(doc, "Re: Initial report — risk exposures for November and recommended hedges (Scenarios #1–#3)")
p(doc, "Status: DRAFT — recommendations for team approval. No trade in this report is executed "
        "until its price, margin and order evidence are recorded in the Excel trade log on the trade date. "
        "All prices marked [TBD] are to be filled from the IBKR paper account or a vendor quote on that date.")

h(doc, "1. Executive summary")
p(doc, "TDI faces three distinct November risks, and they should not be hedged with one mindset. "
        "First, a manufacturing contract creates a long commodity exposure and a short US-dollar exposure at the same time. "
        "Second, a public commitment to cut net greenhouse-gas emissions by 10% a year creates a disclosure and reputation "
        "exposure that is only partly a market exposure. Third, a decision to keep the Toronto park open through November "
        "creates a weather-driven operating exposure whose payoff is not linear in temperature. Our recommendations are: "
        "long December hot-rolled coil (HRC) steel futures for the steel need; long Canadian-dollar December futures in the "
        "paper account for the US-dollar receipt, with an over-the-counter (OTC) forward named as the perfect hedge in real life; "
        "purchase of 750 tonnes of verified voluntary carbon offsets, held unretired until disclosure; and, subject to November 2 "
        "option quotes, long Chicago heating-degree-day (HDD) call options struck near the break-even temperature, rather than a "
        "full linear HDD futures position. The reasoning, the alternatives we rejected, and the basis risks that remain are set out below. "
        "Scenario #4, the personal portfolio, is in a separate document and is not part of TDI's hedging book.")

h(doc, "2. Why hedge at all — benefits and drawbacks in general")
p(doc, "Hedging is not free insurance, and it is not speculation. A hedge exchanges an uncertain future price for a known "
        "structure of costs and risks. The benefits to TDI are stability of input costs and of the Canadian-dollar value of a "
        "foreign-currency receipt, protection of the margin on a fixed-price manufacturing contract, and credibility for a public "
        "emissions commitment that will be disclosed in the first fiscal quarter. The drawbacks are equally real. Futures require "
        "daily variation margin, so a hedge can demand cash even when the underlying business has not yet moved; forwards and "
        "futures cap the upside as well as the downside, so TDI gives up favourable moves; options preserve upside but cost a "
        "premium that is lost if the risk does not materialise; and no hedge in this report is perfect, because the traded "
        "contract never exactly matches TDI's grade, location, timing or quantity. That mismatch is basis risk, and it is the "
        "reason every recommendation below states what is left unhedged. A hedge is justified here when the unhedged outcome "
        "could change a business decision — whether to accept a contract, whether to stay open, or what to disclose — and when "
        "the cost of the hedge is small against that decision. That test is met for Scenarios #1 and #3, and it is met differently "
        "for Scenario #2, where the exposure is to a commitment rather than to a price.")

h(doc, "3. Scenario #1 — steel and the US-dollar receipt")
p(doc, "Exposure. TDI has won a contract to manufacture an attraction for a United States theme park. Production begins "
        "December 1 and requires approximately 2,000 short tons of steel, which TDI does not yet own. TDI is therefore long "
        "steel-price risk: every dollar per ton the steel price rises raises the cost of fulfilling a contract whose revenue is "
        "already negotiated. Buying the steel today would avoid that risk but would incur storage of $50,000 per month, because "
        "the production facility is full; over the month to December 1 that is $50,000 of certain cost, plus working capital tied "
        "up in inventory. Separately, the contract is denominated in US dollars and TDI will receive a first instalment of "
        "$5 million on November 30, while TDI's functional currency is Canadian dollars. TDI is therefore short US dollars: if "
        "the US dollar weakens against the Canadian dollar, the Canadian-dollar value of that receipt falls. The two exposures "
        "are independent and must be hedged separately; a steel hedge does nothing for the currency receipt, and vice versa.")
table(doc, [
    ["Instrument (steel)", "Pros", "Cons"],
    ["Long HRC futures (Dec)", "Exact size; exchange liquidity; no storage; no premium", "Daily margin; CRU index basis; monthly-average settlement"],
    ["OTC steel forward", "Exact grade and date", "Counterparty risk; not executable in the paper account"],
    ["Long HRC call options", "Upside-only protection; no margin calls", "Premium lost if prices do not rise; strike choice matters"],
    ["Buy now (cash-and-carry)", "No basis risk", "$50,000/month storage; capital tied up"],
])
p(doc, "Steel — contracts, cost and basis. The CME US Midwest Domestic Hot-Rolled Coil Steel (CRU) Index futures contract is "
        "20 short tons, quoted in US dollars per short ton, with a $1.00 tick worth $20 per contract, and is financially settled "
        "on the CRU index average for the contract month. TDI needs 2,000 / 20 = 100 contracts, with no rounding residue. We "
        "recommend the December contract, closed out on December 1 when the steel is purchased, not held to its termination "
        "on the business day before the last Wednesday of December. A November contract would settle on November 24, before "
        "the purchase, and would leave a worse timing basis. The initial cost is margin, to be recorded from IBKR on the trade "
        "date [TBD]; the futures gain or loss is $2,000 per $1 per ton move on 100 contracts. Basis exposures remain: the CRU "
        "Midwest index against the grade and supplier TDI actually buys, and the futures price on December 1 against the spot "
        "price TDI pays that day. A futures hedge locks in an effective price of F1 + b2, where F1 is the futures price when "
        "the hedge is placed and b2 is the basis when it is closed — it does not lock in today's spot price, and the report's "
        "interim update must show the realised basis rather than assume it away. The non-derivative alternative, buying now "
        "and storing at $50,000 for the month, should be compared on that basis: it removes basis risk entirely but at a certain "
        "$50,000 plus funding cost, against a futures position whose expected basis cost is uncertain but normally far smaller.")
p(doc, "Currency — contracts, cost and basis. The hedge is to buy Canadian dollars, that is, to sell US dollars. CME Canadian-dollar "
        "futures are 100,000 Canadian dollars per contract, quoted in US dollars per Canadian dollar, with a $0.0001 tick worth "
        "$10, and are listed quarterly (March, June, September, December) only. There is no November contract, so the December "
        "contract is used and closed on November 30 when the receipt arrives; its last trading day is the business day before the "
        "third Wednesday of December. The number of contracts is (US$5 million x spot USD/CAD on the trade date) / 100,000, rounded "
        "to the nearest whole contract — for illustration, 70 contracts at a 1.40 spot rate — leaving a rounding residue of up to "
        "about CAD 50,000 unhedged, which must be disclosed. Margin is to be recorded from IBKR on the trade date [TBD]. In real "
        "life, an OTC forward for exactly US$5 million settling November 30 would be the perfect hedge: exact amount, exact date, "
        "no rounding, no daily margin, with the interest-rate differential embedded in the forward points and bank counterparty "
        "risk as its cost. We name it here so the CRO can see what perfection would look like, but we do not recommend it as the "
        "paper trade, because it cannot be executed and evidenced in the IBKR paper account; the futures recommendation is the "
        "one that can be shown, with an order screenshot, in this report's evidence. If the team prefers the OTC route, that "
        "decision and its Excel-only evidence must be recorded explicitly.")

h(doc, "4. Scenario #2 — net greenhouse-gas emissions and carbon offsets")
p(doc, "Exposure. TDI has publicly committed to lower its net greenhouse-gas emissions each year by 10%, with the eventual goal "
        "of neutrality. Its Toronto park emitted 15,000 metric tonnes of CO2 in its last fiscal year. On the CRO's projections, "
        "new efficiencies and investments should cut gross emissions by 5% this year, to 14,250 tonnes. The net target is 13,500 "
        "tonnes (15,000 x 0.90), so the gap is 750 tonnes. The exposure is not a commodity price in the usual sense: if TDI "
        "discloses a net figure above its commitment in its first public disclosure for the fiscal year (October–December), the "
        "cost is reputational and, over time, commercial, even though no regulator will fine it for missing a voluntary target. "
        "That is why the hedge here is a purchase of offsets, not a futures position, and why its quality matters more than its "
        "headline price.")
p(doc, "Compliance or voluntary? TDI is in the voluntary market. Ontario's Emissions Performance Standards program requires "
        "registration for facilities emitting at least 50,000 tonnes of CO2e whose primary activity is a listed Schedule 2 "
        "industrial activity, and allows opt-in at 10,000 tonnes only for such activities. TDI's park emits 15,000 tonnes and a "
        "theme park is not a Schedule 2 industrial activity, so it meets neither the mandatory nor the opt-in test on the facts "
        "given. The federal Output-Based Pricing System uses the same 50,000-tonne threshold and does not apply in Ontario in "
        "any case, since Ontario's program supplanted it. The team should re-check the Schedule 2 list against TDI's "
        "ride-manufacturing arm before final wording, because the 15,000-tonne figure in the case is the park's, but on the "
        "case facts the conclusion is voluntary. Voluntary participation is therefore a choice about credibility, not compliance, "
        "and it must be reported as such.")
p(doc, "Recommendation and tradability. Buy 750 tonnes of offsets verified under Verra's Verified Carbon Standard or Gold "
        "Standard, from a named vendor at a quoted price on the trade date [TBD — vendor, project, standard, vintage]. Do not "
        "budget from a single market average: 2024 voluntary-market averages were about US$6.34 per tonne overall and about "
        "US$15–20 per tonne for nature-based credits, while a Canadian retail vendor example charges $45 per tonne, which would "
        "put 750 tonnes at $4,755, about $11,250–$15,330, or $33,750 respectively. The report's budget must be the vendor quote, "
        "and the choice of project type — for example, forestry or restoration rather than the cheapest avoidance credit — "
        "should be justified on additionality, permanence and verification, not on price alone. On tradability: credits held "
        "in a registry account before retirement are transferable and can be resold if November emissions come in lower than "
        "expected, but at an uncertain resale price and more easily for high-quality credits; once retired, a credit cannot be "
        "resold. TDI should therefore hold the credits unretired and retire them in stages at disclosure — about 187.5 tonnes "
        "pro-rata for the first quarter — so that the first disclosure can state a net figure only for tonnes actually retired, "
        "naming the project and standard. Offsets do not reduce gross emissions, and the disclosure must not claim neutrality "
        "this year: the commitment is a 10% annual reduction, and the honest claim is that TDI met that year's net target by "
        "retiring 750 tonnes against a 750-tonne gap.")

h(doc, "5. Scenario #3 — keeping the park open in November and weather derivatives")
p(doc, "Exposure. The board has decided to keep the park open through November, against the usual end-of-October close. Fixed "
        "costs for November are forecast at $1.75 million, variable costs at $20 per person, and ticket prices at $50 per person, "
        "so each visitor contributes $30. Attendance on an average day is approximated by A(T) = -2(T - 65)^2 + 3,500, where T is "
        "the average temperature in Fahrenheit. At the expected November average of 42°F, attendance is 2,442 per day, or 73,260 "
        "for the month, giving $2,197,800 of contribution and $447,800 of profit after fixed costs. Break-even attendance is "
        "1,944 per day ($1.75 million / 30 days / $30), which the formula reaches at about 37.1°F on the cold side. Below about "
        "37°F, the month loses money. Warm weather up to 65°F helps attendance, so in November the damaging outcome is cold, "
        "not heat — and that asymmetry decides the hedge direction.")
p(doc, "Hedge design. A heating-degree-day (HDD) for a day is max(0, 65 - T), and the November HDD index is the sum over the "
        "month. At 42°F the expected index is (65 - 42) x 30 = 690; at the break-even temperature it is about 837. Sensitivity at "
        "42°F is 92 visitors per °F per day, or $2,760 per °F per day, which is $82,800 per °F of monthly average temperature and "
        "$2,760 per HDD point (since 1°F of monthly average is 30 HDD points). The CME Chicago HDD Monthly futures contract "
        "(code H2) is 20 index points with 1 point worth $20, financially settled, terminating at 9:00 a.m. Central Time on the "
        "second business day after the contract month; CME's maintenance margin for November 2026 was shown at $1,080 per "
        "contract, to be re-verified on the trade date. A full linear hedge would therefore be $2,760 / $20 = 138 contracts, "
        "with maintenance margin of about $149,040 at that figure. We do not recommend 138 contracts as the default. First, that "
        "size is large relative to weather-market liquidity. Second, the attendance curve is quadratic, so sensitivity rises as "
        "it gets colder and a linear future over-hedges near 42°F and under-hedges in the cold tail where TDI actually loses "
        "money. Our primary candidate, subject to November trade-date option quotes, is long Chicago HDD November call options "
        "struck near the break-even index of about 837: they pay only when the month is cold enough to lose money, their maximum "
        "loss is the premium [TBD], and they avoid daily margin calls. The scaled-futures alternative — for example, 69 contracts "
        "for half the linear sensitivity, at about $74,520 maintenance margin — is fully costed in the appendix so the CRO can "
        "see the trade-off between premium cost and margin plus basis. Basis risks for either route are: Chicago temperatures "
        "against Toronto temperatures, since the traded index is Chicago; the HDD 65°F base against the attendance formula; and "
        "the monthly-average simplification against day-to-day attendance variation. Non-derivative alternatives are flexible "
        "staffing and hours, ticket-price flexibility, weather insurance (a different contract with a claims process, not a "
        "derivative), and accepting the risk given $447,800 of expected profit — but acceptance must be quantified against the "
        "loss region below 37°F, not asserted.")
p(doc, "Trade evidence. The Scenario #1 steel and currency trades and the Scenario #3 weather trade are to be shown by IBKR "
        "order screenshots or, where a contract cannot be traded in the paper account, by the Excel log entry with the exchange "
        "or counterparty, bid and ask, contract size, expiry and source for every price. All trades are consolidated in a single "
        "Excel log and carried into a PowerBI dashboard, which is appended. Any trade that cannot be evidenced this way is not "
        "counted as placed.")

h(doc, "6. AI adoption in the risk management department")
p(doc, "The CRO has made this team responsible for AI adoption, and the assignment requires meaningful, not superficial, use. "
        "We have built two agents on a retrieval index over the course readings and problem-set solutions (Modules 1–8, 531 "
        "chunks, hybrid dense and keyword retrieval), validated first on problem-set questions: the minimum-variance hedge ratio "
        "question returns h* = 1.02125 and short 11 contracts, and the basis question returns an effective price of F1 + b2 with "
        "the worked $5.45 per ounce answer. The AI Risk Analyst Agent is used to identify risks, rank them by likelihood and "
        "magnitude, advise on hedges, research contract logistics, and help maintain the Excel log, the PowerBI dashboard and "
        "these reports. The Wall Street Bets Trading Agent, for the personal portfolio only, is described in the separate "
        "Scenario #4 document. Three limits are stated plainly. First, retrieval is not calculation: every TDI number in this "
        "report was computed outside the language model from a retrieved formula and checked by a human. Second, the course "
        "corpus contains no live market fact, so every contract specification, margin and price in this report comes from a "
        "dated external source and must be re-verified on the trade date. Third, the agent advises and the team decides: no "
        "order in this report was placed by an agent, and any disagreement between the agent and the team in the interim report "
        "will be explained rather than hidden. The appendix contains the risk table (including whether each risk was identified "
        "by the agent without human guidance), the agent-generated likelihood-and-magnitude graph with its supporting research, "
        "the PowerBI dashboard, a description of the agent's training process, and, as the last appendix item, all correspondence "
        "with AI. Bonus automation — live Excel updates feeding PowerBI and daily briefs on activity, hedge coverage and "
        "effectiveness, and margin usage — is being built on the same log, and will be evidenced by a working clip in the interim "
        "report rather than described as if it already worked.")
p(doc, "Next steps to the interim report (November 16). On the trade date, freeze prices, place the Scenario #1 and #3 trades, "
        "obtain the carbon vendor quote, and flip the corresponding log rows from PLANNED to EXECUTED with screenshots. Through "
        "November, track each position's derivative gain or loss, underlying gain or loss, basis gain or loss, and margin impact, "
        "and report whether each hedge is working and whether any adjustment is needed, including any case where the agent "
        "and the team disagree. All Scenario #3 and #4 positions are closed by November 30 at the latest.")
doc.save("/home/hatch/workspace/afm322-report/initial-report-draft.docx")
print("saved initial-report-draft.docx")

# ---------------- Scenario #4 doc (separate, personal) ----------------
doc = make_doc("s4")
t = doc.add_paragraph(); r = t.add_run("PERSONAL PORTFOLIO — SCENARIO #4 (separate document, not addressed to the CRO)"); r.bold = True
p(doc, "Status: DRAFT — strategies are proposed, not traded. Underlyings, strikes, premiums and margins are [TBD — trade date] "
        "from the IBKR paper-account option chain. This document must not be read as TDI advice, and its profit or loss must "
        "not be mixed with TDI's hedging book.")
h(doc, "1. The two books and the competition")
p(doc, "Two option strategies are run in November in the personal paper account, each with the same capital allocation stated "
        "below, and each tracked separately in the Excel log. The first is the author's own strategy. The second is the Wall "
        "Street Bets (WSB) Trading Agent's strategy, generated independently. To keep the competition honest, the author's "
        "strategy is locked before the agent's strategy is viewed, and every adjustment during November is logged with its "
        "reason and timestamp. Both strategies are closed by November 30 at the latest. The paper account is $1 million of "
        "fictional capital, which the assignment allows to be treated as $10 million by multiplying trades by ten; the "
        "allocation used here is [TBD — state the split between TDI hedge margin and personal capital on the trade date], "
        "because TDI hedge margin and personal margin draw on the same paper account and must not be double-counted.")
h(doc, "2. Author's strategy — proposed: a defined-risk vertical spread")
p(doc, "Proposed strategy: a vertical spread (a bull call spread if the view is moderately bullish, or a bear put spread if "
        "moderately bearish) on a liquid underlying chosen from the trade-date option chain [underlying TBD]. The choice of a "
        "spread, rather than a naked long or short option, is deliberate: its maximum profit, maximum loss and break-even can "
        "be stated exactly before trading, its margin is bounded, and the final report's questions — Sharpe ratio, maximum "
        "drawdown, and whether the strategy belongs in a real account — can be answered from a position whose worst case was "
        "known in advance. Construction, strikes, net debit or credit, expiry, and transaction costs are [TBD — trade date]. "
        "Maximum profit, maximum loss and break-even(s) including transaction costs are computed from those actual quotes "
        "and shown in the table below before any order is placed; no figure in this draft is a quote. The thesis is [TBD — "
        "author's market view, in one paragraph, locked before the agent's pick is viewed]. If the trade-date chain does not "
        "offer a spread at an acceptable debit or credit, the strategy is not forced: the log will record that no trade was "
        "placed and why, rather than inventing a fill.")
table(doc, [
    ["Item", "Author's strategy"],
    ["Underlying / expiry", "[TBD — trade date]"],
    ["Construction", "[TBD — strikes, long/short legs]"],
    ["Net debit / credit, incl. costs", "[TBD]"],
    ["Maximum profit / loss", "[TBD — from actual quotes]"],
    ["Break-even(s)", "[TBD]"],
    ["Margin requirement", "[TBD — IBKR paper account]"],
])
h(doc, "3. WSB Trading Agent's strategy")
p(doc, "The WSB Trading Agent was trained on the course option materials (Modules 4, 7 and 8) and on online materials, "
        "including the specified social-media sources, and validated on problem-set questions on spreads and straddles "
        "before being asked for a November play. Its recommendation, its stated thesis, and its maximum profit, maximum loss, "
        "break-even(s) including transaction costs, and margin are [TBD — agent output, logged verbatim, on the trade date]. "
        "Social-media sentiment is treated as an idea source, not as evidence for a price or a size: any agent claim about a "
        "market fact must be traceable to a course chunk or a dated external quote, or it is not used. The agent's strategy "
        "is tracked in the same way as the author's, with the same closing deadline, and the interim and final reports will "
        "compare the two on profit or loss, on what went right or wrong, and on whether either belongs in a real account.")
h(doc, "4. How both strategies will be judged")
p(doc, "At the interim report (November 16): profit or loss to date, margin and buying-power impact, whether each strategy "
        "is going as planned, and any adjustments or new trades made, with reasons. At the final presentation (December 7): "
        "final dollar and percentage profit or loss with tracking evidence, Sharpe ratio and maximum drawdown for each "
        "strategy, the practical steps taken to close each position, whether each strategy went as planned and why, whether "
        "either would be used in a real (non-paper) account and why, and what role AI should have in speculative trading. "
        "A paper profit alone will not be presented as evidence that a strategy is sound: leverage, liquidity, transaction "
        "costs, and the fact that November is a single month will be stated alongside any result.")
doc.save("/home/hatch/workspace/afm322-report/scenario4-draft.docx")
print("saved scenario4-draft.docx")
