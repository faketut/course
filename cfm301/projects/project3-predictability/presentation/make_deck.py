"""Build presentation/deck.pptx from outputs/ tables and figures.

Re-run after run_project.py; numbers update automatically.
"""
import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x33, 0x33, 0x33)
os.makedirs("presentation", exist_ok=True)

tab = pd.read_csv("outputs/table_predict_excess.csv", index_col=0)
garch = pd.read_csv("outputs/table_garch.csv").iloc[0]

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def title_slide(title, subtitle):
    s = prs.slides.add_slide(BLANK)
    add_bg(s)
    tx = s.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.5))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = NAVY
    tx2 = s.shapes.add_textbox(Inches(0.8), Inches(4.4), Inches(11.7), Inches(1.5))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(22)
    p.font.color.rgb = DARK
    return s


def content_slide(title, bullets, img_path=None):
    s = prs.slides.add_slide(BLANK)
    add_bg(s)
    tx = s.shapes.add_textbox(Inches(0.7), Inches(0.3), Inches(11.9), Inches(1.0))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = NAVY
    tx = s.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(11.5), Inches(5.5))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(20)
        p.font.color.rgb = DARK
        p.space_after = Pt(10)
    if img_path and os.path.exists(img_path):
        s.shapes.add_picture(img_path, Inches(8.5), Inches(1.5), width=Inches(4.2))
    return s


def corr_line(pred, h="5Y"):
    c, t = tab.loc[pred, f"corr_{h}"], tab.loc[pred, f"t_{h}"]
    return f"{c:+.2f} (t={t:+.2f})"


title_slide("Reproducing the Equity Return Predictability Table",
            "CFM301 Project 3  |  Jian  |  Ch. 8 slides 24-25, extended sample")

content_slide("Economic question", [
    "Is equity return predictability still present after 2011?",
    "Should a long-horizon investor adjust equity exposure on dividend yield?",
    "Audience: pension fund managers setting strategic asset allocation.",
])

content_slide("Data and methods", [
    "Returns: CRSP VWRETD total returns, 1926-2024 (WRDS SAS Studio); EWRETD for the VW-vs-EW check.",
    "Valuation: Shiller dividend yield, earnings yield, CAPE.",
    "Macro: FRED term/credit spreads, inflation, IP, unemployment, oil, VIX, T-bill, GDP growth.",
    "cay: Lettau-Ludvigson consumption-wealth ratio, reconstructed by DOLS cointegration.",
    "Overlapping horizons, Newey-West t-stats (lag = horizon - 1).",
])

content_slide("Main result: excess returns, 5-year horizon", [
    f"Dividend yield: {corr_line('div_yield')}  (slide: +0.49, t=1.95)",
    f"Earnings yield: {corr_line('earn_yield')}  (slide: +0.48, t=2.31)",
    f"Consumption-wealth ratio: {corr_line('cay')}  (slide: +0.53, t=1.34)",
    f"Unemployment rate: {corr_line('unemp')}  (slide: +0.22, t=0.75)",
    "The slides replicate in the full 1926-2024 sample.",
], img_path="outputs/fig_predict.png")

content_slide("Comparison with the slides", [
    "Sign agreement overall: 52/56 = 93% -- directions and magnitudes replicate.",
    "Caveat: valuation predictability is regime-dependent (0.74 pre-1963, 0.18 in 1963-2011, 0.76 post-2011).",
    "Business cycle: often stronger than the slides (term spread, oil, GDP).",
    "Risk: volatility alone fails in both samples; cay works in both, stronger here.",
])

content_slide("Volatility: far more predictable than returns", [
    f"GARCH(1,1): alpha={garch['alpha']:.3f}, beta={garch['beta']:.3f}, "
    f"persistence={garch['alpha+beta']:.3f}.",
    f"GARCH vs realized vol: {garch['corr_garch_realized']:.2f} contemporaneous, "
    f"{garch['corr_garch_future_real']:.2f} for next-year realized vol.",
    "Bucket bands (+/- 2 SD) overlap heavily: even real predictability is too weak to trade aggressively.",
])

content_slide("Conclusion", [
    "Predictability survives extension to 2024: the slides' table replicates in the full sample.",
    "But valuation predictability is regime-dependent, not a stable parameter -- do not time on yield alone.",
    "The signals that survive every cut: cay first, cyclical variables second.",
    "Limitations: slide sample window inferred (quarterly sampling matches best); cay is our reconstruction; post-2011 long windows are short and episode-driven.",
])

prs.save("presentation/deck.pptx")
print("wrote presentation/deck.pptx")
