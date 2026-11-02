#!/usr/bin/env python3
"""Build appendices.docx for the AFM 322 initial report.

Appendices are NOT counted in the 6-page body limit. This file is a
DRAFT for team review: Nov 2 prices, order screenshots and the final
verbatim AI-chat export are filled in on Nov 2 / at submission.
Honesty rule for the risk table: the 'AI-identified w/o human
guidance?' column is NO for every row, because this chat discussed
the scenarios before any agent run. A blind run in a fresh session
is the only way that column could honestly become YES, and it has
not been done. Do not flip these to YES without that run.
"""
import os
from docx import Document
from docx.shared import Pt, Inches

# ---- Graph: likelihood (x) vs magnitude (y), 1-5 ----
risks = [
    ("Steel price rise", 3, 4),
    ("USD depreciation", 3, 4),
    ("Cold Nov (<37F)", 2, 5),
    ("Chicago-Toronto basis", 4, 2),
    ("Margin cash call", 3, 3),
    ("Carbon price / quality", 3, 2),
    ("Disclosure miss (if no offsets)", 2, 3),
    ("Greenwashing claim", 2, 4),
    ("OTC counterparty (forward)", 1, 3),
    ("HDD liquidity / size", 3, 3),
]
graph = "/home/hatch/workspace/afm322-report/risk-graph.png"
if not os.path.exists(graph):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    for name, L, M in risks:
        ax.scatter([L], [M], s=120)
        ax.annotate(name, (L, M), xytext=(6, 6), textcoords="offset points", fontsize=9)
    ax.set_xlim(0.5, 5.5); ax.set_ylim(0.5, 5.5)
    ax.set_xticks([1, 2, 3, 4, 5]); ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel("Likelihood (1 = rare, 5 = almost certain)")
    ax.set_ylabel("Magnitude (1 = minor, 5 = decision-changing)")
    ax.set_title("TDI November risks — likelihood x magnitude (agent-generated, team-reviewed)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(graph, dpi=200)

doc = Document()
for s in doc.sections:
    s.top_margin = Inches(1); s.bottom_margin = Inches(1)
    s.left_margin = Inches(1); s.right_margin = Inches(1)
st = doc.styles["Normal"]
st.font.name = "Times New Roman"; st.font.size = Pt(12)
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.0

def h(text):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = True
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)

def p(text): doc.add_paragraph(text)

def table(rows):
    t = doc.add_table(rows=1, cols=len(rows[0])); t.style = "Table Grid"
    for j, v in enumerate(rows[0]):
        c = t.rows[0].cells[j]; c.text = v
        for par in c.paragraphs:
            for r in par.runs: r.bold = True
    for row in rows[1:]:
        cells = t.add_row().cells
        for j, v in enumerate(row): cells[j].text = v
    return t

t = doc.add_paragraph(); r = t.add_run("APPENDICES — Initial Report (Scenarios #1–#3)"); r.bold = True
p("DRAFT — November 1, 2026, for team review. Nov 2 prices, order screenshots, carbon vendor quote, "
  "and the final verbatim AI-chat export are filled in on Nov 2 / at submission. Nothing in these "
  "appendices is an executed trade until its log row is flipped from PLANNED to EXECUTED.")

h("Appendix A — Risk table (Scenarios #1–#3)")
p("Column 'AI-identified w/o human guidance?' is NO throughout, for the reason stated in the build note: "
  "the scenarios were discussed with the agent before any unguided run. This is deliberate honesty, not an omission. "
  "If a blind run is completed in a fresh session before submission, its output replaces this table's first column.")
table([
    ["Risk", "AI w/o guidance?", "AI recommendation", "Team action", "Reason"],
    ["Steel price rise before Dec 1", "No — guided", "Long Dec HRC futures, 100 contracts", "Place Nov 2; close Dec 1", "Exact size; locks F1+b2, not spot"],
    ["USD depreciation vs CAD (Nov 30 receipt)", "No — guided", "Long CAD Dec futures in IBKR", "Place Nov 2; close Nov 30", "Paper-executable; OTC forward disclosed as real-life perfect hedge"],
    ["Carbon disclosure miss (net > target)", "No — guided", "Buy 750t verified offsets, retire in stages", "Vendor quote Nov 2; hold unretired", "Gap = 14,250 - 13,500 = 750t"],
    ["Carbon quality / greenwashing", "No — guided", "Verra VCS / Gold Standard only; name project", "Check standard, vintage, additionality", "Cheap credits carry reputation tail risk"],
    ["Cold November (< ~37.1F)", "No — guided", "Long HDD call struck ~837 (primary candidate)", "Confirm Nov 2 option quotes", "Only loss region needs insurance; quadratic payoff"],
    ["Chicago–Toronto weather basis", "No — guided", "Disclose basis; consider OTC Toronto swap as alternative", "Record Chicago vs Toronto temps in Nov", "Traded index is Chicago, park is Toronto"],
    ["Weather-market liquidity / size", "No — guided", "Do not default to 138 linear futures", "Compare call premium vs scaled futures", "138 contracts is large for a thin market"],
    ["Futures margin cash call", "No — guided", "Budget margin; monitor daily in briefs", "Record margin in log + briefs", "Variation margin can demand cash before underlying moves"],
    ["OTC counterparty risk", "No — guided", "Prefer exchange-traded in paper account", "State OTC route as disclosure only", "Forward perfection trades off against counterparty risk"],
])

h("Appendix B — Likelihood x magnitude graph + supporting research summary")
doc.add_picture(graph, width=Inches(6))
p("Reading the graph: cold November is low-likelihood but decision-changing (it flips the month to a loss), so it is "
  "insured at the tail rather than hedged linearly. Steel and FX are the high-magnitude, moderate-likelihood core exposures — "
  "they get the full futures treatment. Chicago–Toronto basis is high-likelihood but moderate magnitude: it is disclosed and "
  "monitored, not eliminated. Supporting research: CME HRC specs (20 short tons, $20/tick, financially settled, CRU index); "
  "CME CAD futures (100,000 CAD, quarterly, $10/tick); CME Chicago HDD Monthly (20 points, $20/point, financially settled, "
  "Nov 2026 maintenance $1,080/contract on Oct 26, re-verify Nov 2); Ontario EPS (O. Reg. 241/19, 50,000t + Schedule 2 activity); "
  "federal OBPS (50,000t threshold); Ecosystem Marketplace State of the VCM 2025 (2024 averages: ~$6.34/t overall, ~$15–20/t "
  "nature-based). Full notes: research-notes-2026-10-26.md.")

h("Appendix C — PowerBI dashboard (data, measures and layout)")
p("The dashboard is built from a single flat table, TDI_trade_log.xlsx / Trade_Log (one row per trade, no merged cells), "
  "so PowerBI can import it directly. Measures to define in PowerBI: Hedge Coverage = SUM(Futures Notional) / Exposure; "
  "Hedge Effectiveness = Futures P&L / Underlying P&L (sign-checked); Margin Usage = SUM(Margin_USD) / Paper Capital; "
  "Basis P&L = (Spot at Close - Futures at Close) x Contracts x Multiplier, by scenario. Layout (two tabs, never mixed): "
  "TDI tab — exposure by scenario, planned vs executed contracts, coverage %, margin usage, daily P&L and basis; Personal tab — "
  "Scenario #4 strategies only. Until Nov 2 fills the price columns, the dashboard shows PLANNED positions and sensitivities "
  "(steel $2,000 per $1/ton; HDD $2,760 per HDD point; carbon 750t gap), not profit or loss. A screenshot of the live "
  "dashboard is inserted here at submission [TBD — Nov 2 / interim]. The Excel workbook with charts is delivered alongside "
  "this appendix; it is the PowerBI source, not a substitute .pbix file, and the team should state that plainly if asked.")

h("Appendix D — AI training-process description")
p("Corpus: AFM 322 Modules 1–8 required readings and problem-set solutions only (16 files, 592 chunks after OCR of the "
  "scanned Module 8 reading: 23 pages, 51,324 characters, RapidOCR, 61 chunks). AFM 425 files and unrelated uploads were "
  "excluded. Extraction: pdftotext -layout with page breaks preserved; scanned files flagged and OCR'd, never silently dropped. "
  "Chunking: ~1,200 characters with overlap, tagged by module, kind (reading/solutions), page and source file. Embedding: "
  "FastEmbed BAAI/bge-small-en-v1.5 (384 dimensions, CPU/ONNX). Retrieval: hybrid 0.5 dense cosine + 0.5 BM25, top-5 (not top-1, "
  "because worked solutions split across chunks). Validation, before any TDI advice: Module 3 Q2 returns h* = 1.02125 and short "
  "11 contracts; Module 3 Q3 returns effective price F1 + b2 = $5.45/oz, $54,500; a novel long-hedge query generalises from "
  "copper/silver to a future purchase; Module 1 solutions cover weather direction (long HDD pays when cold); Module 8 "
  "spreads retrieval passes. External layer (CME specs, Ontario EPS, carbon prices) is separate, dated, and re-verified on the "
  "trade date — it is never served from the course index. Calculation rule: every TDI number is computed outside the language "
  "model from a retrieved formula and checked by a human. Agent wrapper: afm322-rag/agent.py, which logs every call to "
  "agent_log.jsonl with prompt, retrieved chunk IDs and scores.")

h("Appendix E — Correspondence with AI (last appendix, per the brief)")
p("Verbatim log entry on file (afm322-rag/agent_log.jsonl, Oct 26): Risk Analyst, guided (unguided = false), prompt "
  "'what risks does a company face when it will buy steel in future and receive US dollars', retrieved Module 5 reading p.2 "
  "(score 0.972), Module 3 solutions p.7 (0.924), Module 5 reading p.2 (0.891); agent_output left null in the log because the "
  "wrapper is a retrieval layer, not the language model — the model's outputs in this side chat are the correspondence to be "
  "appended verbatim. Correspondence index for this side chat (Oct 26 – Nov 1): (1) Oct 26 brainstorm and RAG proposal; "
  "(2) Oct 26 RAG build, test and contract/carbon research; (3) Oct 26 autonomous mandate, agent.py, Excel log and draft "
  "recommendations; (4) Oct 26 IBKR authorisation and the Nov 2 correction (assignment requires trades BY Nov 2, not after); "
  "(5) Oct 26 draft reports (5pp / 2pp, page-checked) and Module 8 OCR completion (592 chunks); (6) Nov 1 completion of "
  "appendices and submission pack. At submission, the team must append the full verbatim export of this chat (and any "
  "teammate AI chats) after this index, without editing agent outputs. This draft does not substitute a summary for that export.")
doc.save("/home/hatch/workspace/afm322-report/appendices-draft.docx")
print("saved appendices-draft.docx")
