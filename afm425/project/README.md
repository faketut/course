# Topic 13 — The Hedge-Fund Treasury Basis Trade and Systemic Risk (2024–2026)

## What is in this folder

- `analysis/basis_trade.py` — the mandatory original quantitative
  analysis, recomputed from stated assumptions. Run it:
  `python3 analysis/basis_trade.py`. Outputs in `outputs/`
  (`basis_trade_results.json` / `.csv`). All checks pass.
- `report/basis-trade-draft.md` — full first draft (v0.1) in the
  brief's 5-page structure, with the quant summary, appendices,
  AI declaration and AI-critique skeleton, and references.
- `research/research-plan.md` — primary sources, data to pull,
  and the verification checklist before this draft becomes submittable.
- `presentation/outline.md` — 10-minute talk plan for this topic.
- `confirmation-email.md` — draft email to the professor, NOT sent,
  with [brackets] for the missing facts.

## Headline finding (from the model — see the draft for the workings)

A $100m representative basis trade at a 2% repo haircut runs on
$2m of equity (50x leverage). Over 3 months to delivery it earns
+$120,000 (6.0% of equity): $1.00m coupon − $0.98m repo cost +
$0.10m basis convergence. Each stress on its own is large next to
that equity: repo +50 bp costs $122,500 (6.1%); a haircut rise
2% → 4% demands another $2.0m (100%); a 0.50-point basis widening
loses $500,000 (25%); and a 50 bp yield *fall* — the direction that
makes the cash bond gain — triggers a ~$4.09m futures variation-
margin call (204% of equity) while the cash gain stays unrealised.
A 50 bp yield *rise*, by contrast, is hedged to ~$0. That asymmetry
— duration-hedged, not cash-flow-hedged — is the report's thesis.
Scaled to the Fed's Sep 2025 aggregate ($830bn basis trade), a
0.10-point basis widening is an ~$830m collective loss.

## Deadlines (unchanged)

- Report (5 pp, excl. appendices/references) + deck: **Tue Nov 24,
  2026, 11:59 pm**. File names: `AFM425 Report Group 8` /
  `AFM425 Presentation Group 8` — Group 8.
- Presentation: 18 min (10 + 8 Q&A), Nov 25 / 30 / Dec 2 / 7.
  Session date still unknown.
- 13 days left at Nov 11. Next steps: confirm (A)/(B) + send the
  email, pull the primary data in `research-plan.md`, re-run the
  model on the actual CTD, fill the AI-critique appendix, team review.
