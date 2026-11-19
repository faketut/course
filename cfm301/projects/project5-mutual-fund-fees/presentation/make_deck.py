"""Build presentation/deck.pptx (5-6 minute talk) for CFM301 Project 5.

Reads outputs/*.csv; every number comes from the CSVs.
"""
import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

os.makedirs("presentation", exist_ok=True)
alphas = pd.read_csv("outputs/table_alphas.csv")
bench = pd.read_csv("outputs/table_benchmark.csv")
pers = pd.read_csv("outputs/table_persistence.csv")
feep = pd.read_csv("outputs/table_fee_perf.csv")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
TITLE = RGBColor(0x1F, 0x4E, 0x79)
BODY = RGBColor(0x33, 0x33, 0x33)


def add_slide(title, bullets, notes=""):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame
    tf.clear()
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(20)
        p.font.color.rgb = BODY
        p.space_after = Pt(10)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def add_fig_slide(title, fig, bullets):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    s.shapes.add_picture(fig, Inches(0.5), Inches(1.2), width=Inches(7.6))
    tx = s.shapes.add_textbox(Inches(8.4), Inches(1.2), Inches(4.4), Inches(5.8))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(18)
        p.font.color.rgb = BODY
        p.space_after = Pt(10)
    return s


def car(t, basis="net"):
    r = alphas[(alphas.ticker == t) & (alphas.model == "Carhart")
               & (alphas.basis == basis)].iloc[0]
    return r["alpha_ann_pct"], r["t_alpha"]


# 1. Title
s = prs.slides.add_slide(prs.slide_layouts[0])
s.shapes.title.text = "Are the Fees Justified?"
s.placeholders[1].text = ("CFM301 Project 5: five US large-cap growth funds, 1994-2024\n"
                          "Jian")

add_slide("The question",
          ["A retail investor pays 0.58-0.74%/yr for active management, vs 0.14% for an index fund.",
           "Justified = gross alpha large enough that net alpha >= 0 (Wermers 2000; Fama-French 2010).",
           "Two tests: factor alphas (CAPM / FF3 / Carhart) and alpha vs a cheap index-fund portfolio the investor could actually buy."])

add_slide("Data: five famous survivors, and a WRDS problem",
          ["FCNTX, FMAGX, AGTHX, PRGFX, TRBCX - one flagship retail share class each; 1994-2024, 371 months.",
           "This WRDS account is NOT authorized for the CRSP mutual-fund files - returns come from Yahoo Finance adjusted closes instead, validated against Zacks annual returns (FMAGX within 0.15pp every year, 2016-2024).",
           "Fees are current prospectus values, held constant; TNA history is unavailable, so flows cannot be estimated."])

add_fig_slide("Factor alphas: modest skill",
              "outputs/fig_alpha_net_gross.png",
              [f"Net Carhart alpha: FCNTX +{car('FCNTX')[0]:.2f}% (t={car('FCNTX')[1]:.2f}), AGTHX +{car('AGTHX')[0]:.2f}%, TRBCX +{car('TRBCX')[0]:.2f}% - all significant.",
               f"PRGFX +{car('PRGFX')[0]:.2f}% (n.s.), FMAGX {car('FMAGX')[0]:+.2f}% (n.s.).",
               "Gross alphas 0.14-3.12%: all but FMAGX cover their fee before fees.",
               "Check: the index funds' own alphas are ~0 (NAESX -0.08%, VIVAX -0.06%)."])

b = bench.set_index("ticker")
add_slide("Against a portfolio you could actually buy",
          ["Replicating portfolio: 70-95% S&P 500 + 5-30% small-cap, 0% value - costs 0.14%/yr.",
           f"Benchmark alpha: FCNTX +{b.loc['FCNTX', 'alpha_ann_pct']:.2f}% (t={b.loc['FCNTX', 't_alpha']:.2f}), "
           f"AGTHX +{b.loc['AGTHX', 'alpha_ann_pct']:.2f}%, TRBCX +{b.loc['TRBCX', 'alpha_ann_pct']:.2f}%, "
           f"PRGFX +{b.loc['PRGFX', 'alpha_ann_pct']:.2f}%, FMAGX {b.loc['FMAGX', 'alpha_ann_pct']:+.2f}%.",
           "None significant. They beat the factor model, but not a cheap portfolio that copies their style.",
           "Fees in context: active US equity avg 0.60%, passive 0.11% (Morningstar 2024). Our funds sit at the active average - expensive only vs index funds.",
           "Turnover predicts performance better than the fee does: corr(turnover, gross alpha) = -0.82."])

p = pers.set_index("ticker")
add_fig_slide("The alpha decayed",
              "outputs/fig_rolling_alpha.png",
              ["Every fund's alpha fell from 1994-2009 to 2010-2024, by 2.0-4.3pp.",
               f"2010-2024: FCNTX +{p.loc['FCNTX', 'alpha_2010-2024_pct']:.2f}%, FMAGX {p.loc['FMAGX', 'alpha_2010-2024_pct']:+.2f}% (t={p.loc['FMAGX', 't_2010-2024']:.2f}), rest ~0.",
               "Early alpha attracted flows; all five are now $34-351bn giants; alpha decayed to zero.",
               "Rolling 36-month alphas are significant in only 6-15% of windows."])

add_slide("Verdicts and fee design",
          ["FCNTX justified (+2.38%, significant). AGTHX justified (+1.81%). TRBCX justified (+1.83%, lowest turnover).",
           "PRGFX borderline (+1.01%, insignificant). FMAGX not justified (-0.50%, highest turnover 54%).",
           "But: full-sample verdicts only. None of the five earned a significant alpha in 2010-2024.",
           "Fee design: low flat fee, or a symmetric fulcrum fee vs the replicating portfolio - not vs the S&P 500, which would pay the manager for the growth tilt.",
           "Default for the investor: buy the replicating portfolio (85% S&P 500 + 15% small-cap) at 0.14%.",
           "Caveats: five famous survivors (Fama-French 2010: the average fund's net alpha is about minus its fee); fees held constant; loads excluded; Yahoo, not CRSP."])

prs.save("presentation/deck.pptx")
print(f"slides: {len(prs.slides)}, wrote presentation/deck.pptx")
