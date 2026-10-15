"""Build presentation/deck.pptx (5-6 minute deck) with python-pptx."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

NAVY = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x33, 0x33, 0x33)

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


def content_slide(title, bullets, img_path=None, text_width_in=11.5,
                  img_left_in=6.9, img_width_in=5.7):
    s = prs.slides.add_slide(BLANK)
    add_bg(s)
    tx = s.shapes.add_textbox(Inches(0.7), Inches(0.3), Inches(11.9), Inches(1.0))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = NAVY
    left = Inches(0.9)
    width = Inches(text_width_in)
    tx = s.shapes.add_textbox(left, Inches(1.5), width, Inches(5.5))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(19)
        p.font.color.rgb = DARK
        p.space_after = Pt(16)
        p.level = 0
    if img_path:
        s.shapes.add_picture(img_path, Inches(img_left_in), Inches(1.5),
                             width=Inches(img_width_in))
    return s


title_slide(
    "Does Earnings Yield Survive Fama-French?\nTesting a Factor Beyond Market, Size, Value, and Momentum",
    "CFM301 Project 2: Finding and Testing a Factor\nJian  |  October 2026")

content_slide("The factor: earnings yield (E/P)", [
    "Each month, sort stocks on trailing earnings yield = TTM net income / market cap; "
    "go long high-E/P (cheap) and short low-E/P (expensive).",
    "It goes beyond Mkt / SMB / HML / UMD: value intuition (Basu, 1977) plus a profitability "
    "tilt \u2014 E/P is high both when prices are depressed and when earnings are strong.",
    "Not armchair: five of my own WorldQuant BRAIN alphas (in-sample Sharpe 2.17\u20132.59) are "
    "built on forward earnings yield (analyst EBIT / pre-tax-profit estimates \u00f7 market cap). "
    "This project tests the trailing, accounting-based analog on CRSP/Compustat.",
])

content_slide("Data & point-in-time construction", [
    "CRSP monthly stock file via WRDS (Jan 2000\u2013Dec 2024 — the WRDS vintage ends Dec 2024): "
    "1,294,973 stock-months on 12,802 PERMNOs; RET is the total return (dividends + splits).",
    "Compustat quarterly fundamentals (1.25M firm-quarters) linked via the CCM link table. "
    "For formation month-end t: TTM net income = sum of niq over the latest four quarters with "
    "report date rdq \u2264 t (no lookahead); market cap = |PRC| \u00d7 SHROUT \u00d7 1000.",
    "Cleaning: 0 duplicate rows; 6,407 missing returns dropped; returns winsorized at 1/99% "
    "([-44%, +62%], 25,771 obs); EY missing for 13.1% of stock-months (insufficient filing "
    "history); EY winsorized at 1/99% (22,516 obs). All t-stats Newey-West.",
])

content_slide("Main result: a monotone, significant premium", [
    "EY factor (Q5 \u2212 Q1, equal-weighted, 2001\u20132024, n = 289): +18.68%/yr, Sharpe 1.03, "
    "Newey-West t = 4.13.",
    "Quintile returns are monotone: Q1 (low EY) \u22122.02%/yr \u2192 Q5 (high EY) +16.65%/yr; "
    "EY loadings in MKT+EY regressions rise monotonically (Q1 \u03b2 = \u22120.96, t = \u221219.7).",
    "Average R\u00b2 with MKT+EY: 0.821 on the quintiles, 0.766 on the French 25 Size-B/M.",
], img_path="outputs/fig_cumret.png")

content_slide("Does it survive the standard benchmarks?", [
    "Adding EY to CAPM / FF3 / FF5 raises average R\u00b2 on the 25 Size-B/M portfolios by "
    "1.57 / 0.54 / 0.27 pp, with 10, 14 and 11 of 25 portfolios showing significant EY loadings.",
    "Spanning test: regressing EY on the five Fama-French factors leaves \u03b1 = 14.90%/yr "
    "(t = 5.11, R\u00b2 = 0.50) \u2014 half of EY's variance is orthogonal to FF5.",
    "Verdict: EY is not repackaged value or profitability. It carries independent information.",
])

content_slide("Sensitivity & limits: where the premium lives", [
    "Robust: ex-COVID months 19.3%/yr (t = 4.34); subperiods 2002\u201309: 10.6% (t = 1.38), "
    "2010\u201319: 16.7% (t = 4.49), 2020\u201324: 29.7% (t = 2.28).",
    "Fragile: tercile sorts give only 4.2%/yr (t = 0.92, insignificant) \u2014 the signal lives "
    "in the extremes. Value-weighting the legs halves it to 9.5%/yr (t = 1.80).",
    "The premium is a microcap story: Q1 averages $409mm market cap. Delisting returns were "
    "not pulled, so distressed delisters are excluded \u2014 this understates the short leg's "
    "losses, making 18.68% conservative as a paper number, before trading costs.",
], img_path="outputs/fig_quintile_spread.png")

content_slide("Interpretation & takeaway", [
    "Rational: compensation for distress/earnings risk \u2014 drawdowns cluster in recessions. "
    "Behavioral: underreaction to earnings news + neglected microcaps; the nonlinearity "
    "(quintiles work, terciles don't) fits mispricing better than a linear risk loading.",
    "Efficiency: rejects strict semi-strong efficiency, but supports Grossman-Stiglitz "
    "near-efficiency \u2014 where the premium is largest, arbitrage is costliest; at "
    "implementable scale (VW, t = 1.80) the market looks much closer to efficient.",
    "For a quant PM: trailing EY holds genuine orthogonal information beyond FF5 \u2014 but the "
    "harvestable premium is far smaller than the 18.68% headline. Model capacity, turnover "
    "and microcap costs before allocating.",
])

os.makedirs("presentation", exist_ok=True)
prs.save("presentation/deck.pptx")
print(f"Wrote presentation/deck.pptx ({len(prs.slides)} slides)")
