# How the two agents should work — brainstorm, grounded in the RAG test

The RAG skeleton is a retrieval layer, not an agent. An agent =
LLM + system prompt + this retrieval + a calculator + a verbatim log.
Two agents, one retrieval core, different prompts, corpora filters,
and money. Never merge them: the CRO report must never contain
personal speculative P&L, and the WSB log must never touch TDI hedges.

## 0. Sequencing rule that matters most
Run the Risk Analyst's **unguided** risk identification FIRST, before
any human-guided discussion of TDI risks. The appendix table has a
column "Identified by AI Agent (w/o human guidance)?" — if we chat
about steel/FX/weather/carbon with the agent first, that column can
never honestly be "yes". So: blind prompt (case facts only) →
save output verbatim → only then start guided work. Do this before
drafting anything else.

## 1. AI Risk Analyst Agent (TDI)
- Corpus: Modules 1–8 (readings + solutions) via query.py top-5,
  the TDI case facts as a structured file, and an external layer
  (CME specs, Ontario EPS, carbon standards/vendors) tagged with
  source + retrieval date, re-verified Nov 2.
- Jobs, in the brief's own order:
  1. Identify TDI risks, rank by likelihood × magnitude, graph them.
     Human challenges the ranking with real volatilities (steel,
     USD/CAD, Toronto November temperatures, carbon prices) — the
     graph stays agent-generated, human-approved.
  2. Recommend hedges per scenario, with retrieved course support
     (Module 3: long hedge + basis F₁+b₂; Module 5: futures vs.
     options trade-offs; Module 1 solutions: long HDD when cold).
  3. Logistical steps: IBKR ticker, contract month, size, margin,
     close-out date, Excel log entry — checked by a human in IBKR,
     never taken from the agent alone.
  4. Excel log + PowerBI help, and the written reports.
- Calculator rule: every TDI number is computed outside the LLM
  (script or spreadsheet) from a formula the agent retrieved.
  E.g. steel 2,000/20 = 100; HDD $2,760/$20 = 138; carbon
  14,250 − 13,500 = 750. The agent shows the formula + the
  retrieved chunk; a human signs the arithmetic.
- Validation (brief's gate): the PSET tests in rag-test-2026-10-26.md
  pass — Q2 hedge ratio, Q3 effective price, weather direction.
  Record those three as the validation evidence, with scores and
  pages, in the training-process appendix.
- Failure modes to design around: top-1 truncation (use top-5),
  Module 8 reading gap (OCR or disclose), and live facts (never
  cite a course chunk for a market price).

## 2. WSB Trading Agent (personal, Scenario #4)
- Corpus: Modules 4, 7, 8 (option markets, valuation, strategies)
  + market data + Reddit sentiment. Sentiment is tagged UNTRUSTED:
  it can suggest an idea, it can never justify a size or a price.
- Competition protocol (write it down before Nov 2):
  same Nov 2 prices, same paper capital allocation, both strategies
  logged with timestamp + reason; both may adjust during November,
  every adjustment logged; interim (Nov 16) and final (Dec 7)
  compare P&L, and for the final also Sharpe / max drawdown.
  Jack's pick and the agent's pick are chosen independently —
  if the agent's pick leaks into Jack's, the competition is void
  and the report must say so.
- Every recommendation must state, in one block: strategy, why,
  max profit, max loss, break-even(s) including transaction costs,
  margin, and "this is speculation, not a hedge". No block, no trade.
  Validation: Module 8 Q3/Q4 (spreads, straddle) retrieval passes.
- Money separation: TDI hedge margin and personal margin draw on
  the same IBKR paper account, so the allocation (e.g. $X to TDI
  hedges, remainder to Scenario #4, on the $1m / pretend-$10m basis)
  is stated in both documents. The agent never moves TDI capital.

## 3. Bonus automation (only if it is real, not a screenshot of a plan)
- Daily brief pipeline: Excel log (source of truth) → script
  computes hedge coverage (futures notional / exposure),
  hedge effectiveness (futures P&L vs. underlying P&L),
  margin usage → agent drafts a brief → human approves →
  brief + dashboard update logged. A video clip of this running
  is the interim appendix evidence; a description of it is not.
- Auto Excel updates: same rule — the agent proposes a diff,
  a human runs it. Fully autonomous writes are a nice story and
  a terrible audit trail for a graded appendix.
- Keep the dashboard in two tabs (TDI / personal) so nothing
  from Scenario #4 can leak into the CRO view.

## 4. The appendix is a design constraint, not an afterthought
- Everything the agents say is logged verbatim (prompt, retrieved
  chunk IDs, output, timestamp) from the first message. Editing an
  agent output before appending it falsifies the appendix.
- Team rule: teammates' AI correspondence counts too ("all your
  correspondence" is team-level in a team assignment). Agree now
  that all team AI chats go into one shared log, and that nothing
  is shared outside the team.
- Training-process appendix = this RAG's build (corpus, chunking,
  embedding model, hybrid scores), the PSET validation results,
  and the blind-first sequencing rule above. That is a stronger
  story than "we used a Custom GPT".

## 5. Immediate next steps
1. Blind risk-identification run (Risk Analyst, case facts only).
2. OCR Module 8 reading + the assignment PDF into the index.
3. Build agent.py: a thin wrapper over query.py that enforces
   top-5 retrieval, citation (module/page), calculator-first
   numbers, and JSONL logging.
4. Agree the Excel log schema + PowerBI layout before Nov 2.
5. Nov 2: freeze prices, place IBKR trades, screenshot, log.
   Pre-draft the report with price/ticket cells blank — Nov 2
   is a trading day and a submission night.
