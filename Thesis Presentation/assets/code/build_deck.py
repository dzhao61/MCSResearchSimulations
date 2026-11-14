"""Build the Welch MI presentation (replanned 5 November; application removed 9 November) from a copy of the vF2 donor."""
import datetime
import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

import plan_notes
from pptlib import (BLACK, COVER_ORANGE, DIVIDER, NAVY, ORANGE, WHITE, circle, emu, equation, fill_text_body, hline, notes,
                    panel_text, rect, set_title, shape_fill_line, slide_number, table, text, vline)

TEMPLATE, OUT, CHARTS, PLAN_PATH = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
SCRIPT_PATH = sys.argv[5] if len(sys.argv) > 5 else None   # optional spoken script (Rehearsal/…_Script_Spoken.md)
PLAN, PLAN_B, PLAN_APPENDIX = plan_notes.load(PLAN_PATH)


def load_script(path):
    """Spoken script: one '## Slide N: title' section per main slide, then '## Questions and answer guides'."""
    if not path:
        return {}, ""
    talk, _, qa = open(path, encoding="utf-8").read().partition("## Questions and answer guides")
    parts = re.split(r"^## Slide (\d+): .*$", talk, flags=re.M)
    slides = {int(parts[i]): parts[i + 1].strip() for i in range(1, len(parts), 2)}
    qa = re.sub(r"^### ", "", qa.strip(), flags=re.M)
    qa = re.sub(r"^- ", "• ", qa, flags=re.M)
    return slides, qa


SPOKEN, SPOKEN_QA = load_script(SCRIPT_PATH)

TIMING = {1: ("0:25", "0:25"), 2: ("1:15", "1:40"), 3: ("1:00", "2:40"), 4: ("1:20", "4:00"), 5: ("2:05", "6:05"),
          6: ("1:20", "7:25"), 7: ("1:40", "9:05"), 8: ("2:00", "11:05"), 9: ("1:30", "12:35"),
          10: ("1:45", "14:20"), 11: ("1:30", "15:50"), 12: ("2:00", "17:50"), 13: ("1:00", "18:50")}

# ---------------------------------------------------------------- palette and type scale
INK = "262626"          # body text
SOFT = "555555"         # secondary text
FAINT = "8C8C8C"        # footers and quiet notes
PEACH = "FDF3EC"        # soft panel fills
SKY = "EDF2F8"
GREEN = "2E7D5B"        # third category colour (Slide 10: bias in the MI difference)
MINT = "EAF4EE"         # pale fill to match GREEN
ORANGE_TINT = "F5C7AA"  # hairlines and outlines
NAVY_TINT = "B8C5D6"
GREEN_TINT = "AFD5BF"     # hairlines and outlines to match GREEN
RULE = "E3E3E3"
ARROW = "F2A77F"
EW_TEXT = "B4501A"      # darker orange for Expanded Welch labels on pale fills
CONTRIB_FILL = "FBE5D6"  # stronger peach for the contribution highlight on Slide 13
CONTRIB_FILLS = [CONTRIB_FILL, "DCE5F0", "D6ECDF"]  # stronger peach, blue and mint, by position
POS_KINDS = ["peach", "blue", "green"]  # boxes in a set: first orange, second navy, third green
POS_COLS = [ORANGE, NAVY, GREEN]
L, W = 0.6, 12.13       # left margin and content width

prs = Presentation(TEMPLATE)
sld_ids = prs.slides._sldIdLst
for sld in list(sld_ids)[1:]:
    prs.part.drop_rel(sld.get(qn("r:id")))
    sld_ids.remove(sld)
LAYOUT = prs.slide_masters[1].slide_layouts.get_by_name("Title and Content")


def new_slide(title, n):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0:
            ph._element.getparent().remove(ph._element)
    set_title(s, title, x=L, y=0.3, w=W, h=0.66, sz=28)
    slide_number(s, n)
    return s


def B(t, **o):
    d = {"b": True}
    d.update(o)
    return (t, d)


def O(t, bold=True):
    return (t, {"c": ORANGE, "b": bold})


def M(latex, fb, **o):
    """Inline native Office maths. fb is the fallback for renderers without it: a string
    or a list of runs, set in Cambria Math and inheriting this run's options."""
    runs = [CM(fb)] if isinstance(fb, str) else fb
    runs = [(t, {**o, **ro}) for t, ro in runs]
    d = {"math": latex, "fb": runs}
    d.update(o)
    return ("", d)


def TI(t, hat=False, **o):
    """Fallback text for hatted symbols: a plain Latin letter in Times New Roman italic, with a combining
    hat when asked. Renderers without Office maths place this hat correctly, unlike a hat on a Unicode
    maths-italic letter."""
    d = {"font": "Times New Roman", "i": True}
    d.update(o)
    return (t + ("\u0302" if hat else ""), d)


def CM(t, **o):
    d = {"font": "Cambria Math"}
    d.update(o)
    return (t, d)


def BR():
    return ("", {"br": True})


def lead(s, runs, h=0.64):
    return text(s, L, 0.98, W, h, [{"runs": runs}], sz=17, color=SOFT, name="Lead", margins=(0.03, 0.03, 0.02, 0.02),
                line=1.02)


def intro(s, runs):
    """Backup introduction line: one quiet sentence under the title."""
    plain = [(t, {**o, "b": False}) if isinstance(o, dict) else (t, o) for t, o in
             [(r, {}) if isinstance(r, str) else r for r in runs]]
    return text(s, L, 0.98, W, 0.4, [plain], sz=15, color=SOFT, name="Lead", margins=(0.03, 0.03, 0.02, 0.02))


def setting(s, label, x=L, y=1.66, w=W, sz=13):
    return text(s, x, y, w, 0.32, [[(label, {"b": True, "c": ORANGE})]], sz=sz, name="Setting",
                margins=(0.03, 0.03, 0, 0), anchor="ctr")


def footer(s, runs, w=11.3):
    if isinstance(runs, str):
        runs = [(runs, {"i": True})]
    return text(s, L, 7.05, w, 0.3, [runs], sz=10.5, color=FAINT, anchor="ctr", name="Source line",
                margins=(0.03, 0.02, 0, 0))


def label(s, x, y, w, txt, color):
    """Small coloured section heading with a hairline beneath (replaces solid header bars)."""
    text(s, x, y, w, 0.32, [[B(txt, c=color)]], sz=14, anchor="b", margins=(0.03, 0.03, 0, 0.02),
         name="Section label")
    hline(s, x, y + 0.38, w, color={ORANGE: ORANGE_TINT, GREEN: GREEN_TINT}.get(color, NAVY_TINT), width=1.0)


def soft(s, x, y, w, h, kind="peach", outline=None, name=None):
    fill = {"peach": PEACH, "green": MINT}.get(kind, SKY)
    return rect(s, x, y, w, h, fill=fill, line=outline, line_w=1.0, rounded=0.04,
                name=name)


def panel(s, x, y, w, h, kind="peach", heading=None, body=None, hsz=14.5, bsz=13.5, anchor="t",
          margins=(0.2, 0.18, 0.15, 0.12), outline=None, name=None):
    p = soft(s, x, y, w, h, kind, outline=outline, name=name)
    hcol = {"peach": ORANGE, "green": GREEN}.get(kind, NAVY)
    paras = []
    if heading:
        parts = heading if isinstance(heading, list) else [heading]
        runs = []
        for k_, part in enumerate(parts):
            runs += ([BR()] if k_ else []) + [(part, {"b": True, "c": hcol})]
        paras.append({"runs": runs, "sz": hsz, "space_after": 4})
    for b in body or []:
        paras.append({"runs": b, "sz": bsz, "space_after": 3, "line": 1.05})
    panel_text(p, paras, sz=bsz, color=INK, anchor=anchor, margins=margins)
    return p


CONTRIBUTIONS = [  # thesis Section 1.3, shown on Slide 13
                 ("Derivation", "How the estimated pointwise-MI variance varies between samples"),
                 ("Test construction", "The Wald statistic with estimated Student t degrees of freedom"),
                 ("Empirical evaluation", "Accuracy, false positives, power, and calculation success")]


def accent(s, x, y, w, h, runs, color=ORANGE, sz=14, name="Callout"):
    """Callout marked by a thin coloured bar at its left edge (replaces dashed boxes)."""
    rect(s, x, y + 0.04, 0.055, h - 0.08, fill=color)
    return text(s, x + 0.2, y, w - 0.2, h, [{"runs": runs, "line": 1.05}], sz=sz, color=INK, anchor="ctr",
                name=name, margins=(0.03, 0.03, 0.02, 0.02))


def pic(s, name, x, y, w, h):
    return s.shapes.add_picture(f"{CHARTS}/{name}.png", emu(x), emu(y), emu(w), emu(h))


def arrow(s, x, y, w=0.24, h=0.18, down=False, color=ARROW):
    shp = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW if down else MSO_SHAPE.RIGHT_ARROW, emu(x), emu(y), emu(w), emu(h))
    shape_fill_line(shp, color, None)
    return shp


def backup_label(s, txt):
    """Top-right breadcrumb: appendix group and the main slide the backup supports."""
    return text(s, 6.73, 0.12, 6.0, 0.28, [[(txt, {"b": True})]], sz=10.5, color=ORANGE, align="r",
                anchor="ctr", name="Backup label", margins=(0, 0.02, 0, 0))


def head_cell(txt, color=SOFT, align="ctr", sz=13, **kw):
    return dict(paras=[txt] if isinstance(txt, (str, list)) else txt, sz=sz, b=True, color=color, align=align,
                anchor="b", bottom=ORANGE, bottom_w=1.0, **kw)


# Final thesis (8 November) wording: Wald test, shared MI, calculation success, no Holm family.
# The plan carries the final-thesis wording, so notes are copied from it without replacements.
NOTE_FIXES = []
FIX_USED = [0] * len(NOTE_FIXES)


def fix_notes(body):
    for i, (old, new) in enumerate(NOTE_FIXES):
        if old in body:
            body = body.replace(old, new)
            FIX_USED[i] += 1
    return body


def main_note(n, extra=None):
    """Speaker notes for main slide n: the spoken script when given, otherwise the plan's script, cue and source."""
    if n in SPOKEN:                          # the notes are the spoken script alone, word for word
        return SPOKEN[n]
    d = PLAN[n]
    time, finish = TIMING[n]
    body = f"Time: {time} (finish by {finish})\n\nSCRIPT\n{d['script']}\n\n"
    if d["transition"]:
        body += f"TRANSITION\n{d['transition']}\n\n"
    body += f"DELIVERY CUE\n{d['cue']}\n\nSOURCE\n{d['source']}"
    if extra:
        body += f"\n\n{extra.strip()}"
    return fix_notes(body)


def backup_note(k, extra=None, source=None, opening=None, question=None, answer=None):
    """Backup notes. k is the plan's backup key (None when the final thesis required a new backup); a supplied
    question or answer replaces the plan's."""
    d = PLAN_B.get(k) or {"question": None, "answer": None, "notes": None, "anchor": None, "source": None}
    body = "Not part of the timed talk. Return to Slide 13 afterwards.\n\n"
    if opening:
        body += f"WHEN OPENING\n{opening.strip()}\n\n"
    body += f"QUESTION ANSWERED\n{question or d['question']}\n\nANSWER TO GIVE\n{answer or d['answer']}\n\n"
    if extra is None:
        extra = "\n".join(x for x in (d["notes"], d["anchor"]) if x)
    if extra:
        body += f"NOTES\n{extra.strip()}\n\n"
    body += f"SOURCE\n{(source or d['source']).strip()}"
    return fix_notes(body)


FOOT_RATE = "Rates divide rejections by all 100,000 repetitions; unsuccessful calculations count as non-rejections. "

# =================================================================== Slide 1
cover = prs.slides[0]
by = {sh.name: sh for sh in cover.shapes}
tph, sph, div = by["Title 1"], by["Subtitle 2"], by["Rectangle 1040"]
tph.left, tph.top, tph.width, tph.height = emu(0.6), emu(1.7), emu(4.5), emu(1.9)
tb = tph.text_frame._txBody
bp = tb.find(qn("a:bodyPr"))
for c in list(bp):
    bp.remove(c)
bp.set("anchor", "b")
fill_text_body(tb, ["Comparing Mutual", "Information in Finite", "Samples"], sz=29, color=COVER_ORANGE,
               font="Aptos Display", line=0.94)
text(cover, 0.6, 3.78, 4.3, 0.8, [[("Can MI-specific degrees of freedom improve comparisons between populations?",
                                    {"i": True})]], sz=15.5, color="505050", font="Aptos", name="Research question",
     margins=(0.09, 0.04, 0.02, 0.02), line=1.0)
div.left, div.top, div.width = emu(0.68), emu(4.78), emu(3.6)
sph.left, sph.top, sph.width, sph.height = emu(0.6), emu(4.95), emu(4.5), emu(1.6)
tb = sph.text_frame._txBody
bp = tb.find(qn("a:bodyPr"))
for c in list(bp):
    bp.remove(c)
bp.set("anchor", "t")
fill_text_body(tb, [{"runs": ["Daniel Zhao (", ("Master of Computer Science", {"i": True}), ")"], "space_after": 6},
                    {"runs": ["Supervisor: Associate Professor Joseph T. Lizier"], "space_after": 6},
                    {"runs": ["The University of Sydney"]}], sz=13.5, color="333333", font="Aptos", line=1.0)
notes(cover, main_note(1))

# =================================================================== Slide 2
s = new_slide("Motivation: comparing MI across populations", 2)
lead(s, ["Mutual information measures how much observing one variable reduces uncertainty about another, on average. ",
         O("Different sample estimates can arise from sampling noise.")])
soft(s, 3.0, 1.82, 7.33, 0.64, "peach", name="Hypothesis panel")
text(s, 3.25, 1.82, 1.4, 0.64, [[B("Hypotheses", c=ORANGE)]], sz=13, anchor="ctr")
equation(s, 4.6, 1.82, 5.6, 0.64, r"H_0:I(P)=I(Q)\quad\text{against}\quad H_1:I(P)\neq I(Q)", sz=22, jc="left")
label(s, L, 2.66, 5.7, "Two populations, the same two discrete variables", ORANGE)
for k_, (y, pop, est) in enumerate([(3.22, "P", r"\hat{I}(P)"), (4.18, "Q", r"\hat{I}(Q)")]):
    p = soft(s, L, y, 2.35, 0.8, POS_KINDS[k_])
    sub_ = "𝑃" if pop == "P" else "𝑄"
    tint, cells, arr = [(ORANGE_TINT, ("F9DCC9", "FCEDE2"), ARROW), (NAVY_TINT, ("D5DEEA", "E8EEF5"), NAVY_TINT)][k_]
    panel_text(p, [{"runs": [B(f"Population {pop}", c=POS_COLS[k_])], "sz": 14, "space_after": 1},
                   {"runs": [CM("𝑛"), CM(sub_, sub=True), " observed pairs (", CM("𝑋"), ", ", CM("𝑌"), ")"], "sz": 12,
                    "color": SOFT}], anchor="ctr", margins=(0.15, 0.1, 0.04, 0.04))
    arrow(s, 3.06, y + 0.31, color=arr)
    for r_ in range(4):
        for c_ in range(2):
            rect(s, 3.43 + c_ * 0.3, y + 0.08 + r_ * 0.16, 0.3, 0.16, fill=cells[c_], line=WHITE, line_w=0.75)
    arrow(s, 4.16, y + 0.31, color=arr)
    p = rect(s, 4.53, y, 1.77, 0.8, fill=WHITE, line=tint, line_w=1.0, rounded=0.08)
    panel_text(p, [{"runs": ["MI estimate"], "sz": 11, "color": SOFT}], align="ctr", anchor="t",
               margins=(0.05, 0.05, 0.08, 0.03))
    equation(s, 4.58, y + 0.3, 1.67, 0.45, est, sz=18, jc="center")
vline(s, 6.67, 2.73, 2.9, color="D0D0D0", width=1.0, dash="sysDot")
label(s, 7.03, 2.66, 5.7, "Statistical task", ORANGE)
steps = ["Summarise a sample from each population in a count table", "Estimate MI from each table",
         "Assess whether sampling noise can explain the difference"]
for i, st in enumerate(steps):
    y = 3.22 + i * 0.8
    last = i == 2
    p = rect(s, 7.03, y, 5.7, 0.6, fill=ORANGE if last else WHITE, line=None if last else ORANGE_TINT, line_w=1.0,
             rounded=0.12)
    panel_text(p, [[B(st, c=WHITE if last else INK)]], sz=14, align="ctr", anchor="ctr",
               margins=(0.1, 0.1, 0.02, 0.02))
    if i < 2:
        arrow(s, 7.03 + 5.7 / 2 - 0.1, y + 0.62, w=0.2, h=0.16, down=True)
text(s, L, 5.1, 5.75, 0.36, [["Both variables are ", B("discrete", c=INK), " (categorical), giving count tables."]], sz=13, color=SOFT, name="Variables")
accent(s, L, 5.68, W, 0.46, [B("Example: ", c=NAVY), CM("𝑋"), " = mid-semester test grade, ", CM("𝑌"),
                             " = final exam grade; ", CM("𝑃"), " = students before generative AI, ", CM("𝑄"),
                             " = students after."], color=NAVY, sz=13.5, name="Example")
text(s, L, 6.32, W, 0.42, [[B("Does MI differ between the two populations?")]], sz=18, color=INK,
     name="Question")
footer(s, "Table icons are schematic; the example is illustrative, not thesis data. Thesis Sections 1.1 and 2.1; "
          "Bossomaier et al. (2016)")
notes(s, main_note(2))

# =================================================================== Slide 3
s = new_slide("Literature review: foundations and the MI-specific step", 3)
lead(s, ["Existing results provide MI estimates, a Wald test using a standard normal distribution, and moment "
         "matching.", BR(),
         O("This project derives the MI variance sensitivity needed for its degrees of freedom.")])
H = dict(sz=14, color=ORANGE, b=True, anchor="b", align="ctr", bottom=None)
Lb = dict(sz=13.5, color=ORANGE, b=True, anchor="ctr", align="r")
C = dict(sz=14.5, color=INK, anchor="ctr", align="ctr", ml=0.18, mr=0.18)
cols = ["MI estimation and uncertainty", "Wald comparison", "Welch–Satterthwaite moment matching"]
rows = [[dict(paras=[""], **H)] + [dict(paras=[[(c_, {"i": True, "b": True})]], **H) for c_ in cols]]
data3 = [("Idea", ["Estimate MI and first-order sampling variance",
                   "Divide the estimated difference by its standard error",
                   "Match variance moments to choose degrees of freedom"]),
         ("Key work", [["Moddemeijer (1989);", "Paninski (2003)"], ["Wald (1943);", "Mora and Ruiz-Castillo (2009)"],
                       ["Satterthwaite (1946); Welch (1947);", "Hutcheson (1970); Pan and Wall (2002)"]]),
         ("Required step", ["Track variation in the variance estimate itself",
                            ["Assess the fixed cutoff from the", BR(), "standard normal distribution", BR(), "in finite samples"],
                            "Calculate the MI-specific variance sensitivity"])]
for lab, cells in data3:
    if lab == "Key work":
        rows.append([dict(paras=[lab], **Lb)] + [dict(paras=c_, **{**C, "sz": 13.5, "color": SOFT}) for c_ in cells])
    else:
        rows.append([dict(paras=[lab], **Lb)] + [dict(paras=[c_], **C) for c_ in cells])
table(s, L, 1.95, [1.45, 3.56, 3.56, 3.56], [0.72, 0.98, 1.0, 0.98], rows, name="Literature matrix")
for x in (2.05, 5.61, 9.17):
    vline(s, x, 2.08, 3.55, color=ORANGE_TINT, width=1.0)
p = soft(s, L, 6.0, W, 0.6, "peach", name="Contribution strip")
panel_text(p, [[B("Contributions: ", c=ORANGE), ("Derive that sensitivity, construct the Expanded Welch test from it, "
                                                  "and evaluate both empirically.",
                                                 {"c": INK})]], sz=15.5, align="ctr", anchor="ctr",
           margins=(0.1, 0.1, 0.02, 0.02))
footer(s, "Thesis Sections 2.2–2.5 and 3.2–3.3; full references on Slides 32–33")
notes(s, main_note(3))

# =================================================================== Slide 4
s = new_slide("Method: one statistic, two reference distributions", 4)
lead(s, ["Both methods use ", O("the same estimated MI difference and standard error"),
         ".", BR(), "Expanded Welch uses estimated degrees of freedom for a Student t distribution."])
soft(s, L, 1.95, 5.8, 2.38, "peach", name="Shared statistic panel")
text(s, 0.8, 2.04, 5.4, 0.3, [[B("Shared statistic", c=ORANGE)]], sz=14.5, margins=(0, 0, 0, 0))
equation(s, 0.7, 2.35, 5.6, 0.95,
         r"T=\frac{\widehat\Delta_{\mathrm{BC}}}{\widehat{\mathrm{SE}}},\qquad\widehat{\mathrm{SE}}^2=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}",
         sz=20, jc="center")
text(s, 0.8, 3.27, 5.45, 0.34, [[M(r"\hat{\Delta}_{\mathrm{BC}}", [("Δ̂", {"font": "Georgia"}), CM("BC", sub=True, i=False)]), ": estimated ",
                                CM("𝐼(𝑃) − 𝐼(𝑄)"), ", after leading bias correction."]], sz=13, color=SOFT,
     anchor="ctr", name="Difference definition")
text(s, 0.8, 3.62, 5.45, 0.6, [[M(r"V(P)", [TI("V"), CM("(𝑃)")]), ": population variance of pointwise MI;", BR(), M(r"\hat{V}(P)", [TI("V", hat=True), CM("(𝑃)")]),
                               " estimates it from one sampled table."]], sz=13, color=SOFT, anchor="t",
     name="Variance definition")
panel(s, L, 4.55, 2.8, 1.6, "blue", heading="Wald test",
      body=[["Standard normal distribution; two-sided 5% cutoff about ", B("±1.96"), "."]], hsz=15, bsz=14)
panel(s, 3.6, 4.55, 2.8, 1.6, "green", heading="Expanded Welch test",
      body=[["Student t distribution with estimated degrees of freedom; ", B("a larger cutoff"), "."]], hsz=15, bsz=14)
pic(s, "slide04_reference_distributions", 6.83, 1.95, 5.9, 3.75)
text(s, 6.6, 5.88, 6.13, 0.3, [[("Student t distribution with 5 degrees of freedom, for illustration; cutoff about "
                                  "±2.57.", {"i": True})]], sz=12.5, color=SOFT, align="ctr", name="Plot label")
footer(s, "Thesis Chapters 3–4, Figure 2.1. Bias correction: Slide 15. Calculation requirements: Slides 6 and 22")
notes(s, main_note(4))

# =================================================================== Slide 5
s = new_slide("Approach and contributions", 5)
lead(s, ["The estimated pointwise-MI variance changes between samples.", BR(), "We approximate that variation and ",
         O("use it to choose the degrees of freedom"), "."])
VH = M(r"\hat{V}(P)", [TI("V", hat=True), CM("(𝑃)")])
NUH = M(r"\hat{\nu}", [CM("𝜈̂")])
CW5, GAP5, Y5, H5 = 3.83, 0.32, 1.85, 3.95
STEP_COLS = [ORANGE, NAVY, GREEN]                 # the deck's three-category colours, as on Slide 10
STEP_TINTS = [ORANGE_TINT, NAVY_TINT, GREEN_TINT]
STEP_KINDS = ["peach", "blue", "green"]
heads = [[M(r"\hat{V}(P)", [TI("V", hat=True), CM("(𝑃)")], c=ORANGE, b=True), " varies between samples"],
         ["Measure that variation"], ["Turn it into degrees of freedom"]]
for i_ in range(3):
    x_ = L + i_ * (CW5 + GAP5)
    soft(s, x_, Y5, CW5, H5, STEP_KINDS[i_], name=f"Step {i_ + 1} panel")
    circle(s, x_ + 0.22, Y5 + 0.2, 0.36, str(i_ + 1), STEP_COLS[i_], sz=13, name=f"Step {i_ + 1} marker")
    text(s, x_ + 0.68, Y5 + 0.16, CW5 - 0.8, 0.44, [[(t, {"b": True, "c": STEP_COLS[i_]}) if isinstance(t, str) else t
                                                   for t in heads[i_]]], sz=15.5, anchor="ctr",
         name=f"Step {i_ + 1} heading", margins=(0.02, 0.02, 0, 0))
    if i_ < 2:
        arrow(s, x_ + CW5 + 0.05, Y5 + H5 / 2 - 0.1, w=0.22, h=0.2)


def contrib_tag(x_, y_, txt, k):
    p_ = rect(s, x_, y_, CW5 - 0.4, 0.3, fill=WHITE, line=STEP_TINTS[k], line_w=1.0, rounded=0.5, name="Contribution tag")
    panel_text(p_, [[(txt, {"b": True, "c": STEP_COLS[k]})]], sz=11.5, align="ctr", anchor="ctr", margins=(0, 0, 0, 0))


def approx_tag(x_, y_, txt, k):
    text(s, x_, y_, CW5 - 0.4, 0.34, [[B("Approximation: ", c=STEP_COLS[k]), txt]], sz=12.5, color=SOFT, anchor="ctr",
         name="Approximation tag", margins=(0.02, 0.02, 0, 0))


# Step 1: the estimate varies
x1 = L
pic(s, "slide05_vhat_spread", x1 + 0.19, Y5 + 0.75, 3.45, 1.85)
text(s, x1 + 0.2, Y5 + 2.72, CW5 - 0.4, 0.75, [["Each new sample gives a new table, and so a new ", VH, "."]],
     sz=14, color=INK, name="Step 1 text", margins=(0.02, 0.02, 0.02, 0.02))
text(s, x1 + 0.2, Y5 + 3.48, CW5 - 0.4, 0.34, [[("Schematic, not data.", {"i": True})]], sz=11.5, color=SOFT,
     anchor="ctr", name="Schematic note", margins=(0.02, 0.02, 0, 0))
# Step 2: measure the variation (contribution 1)
x2 = L + CW5 + GAP5
equation(s, x2 + 0.1, Y5 + 0.78, CW5 - 0.2, 0.85, r"\operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P}",
         sz=20, jc="center")
text(s, x2 + 0.2, Y5 + 1.75, CW5 - 0.4, 1.35, [
    {"runs": [CM("𝑔"), CM("𝑃", sub=True), CM("(𝑥, 𝑦)"), ": how much ", CM("𝑉(𝑃)"),
              " changes when a little probability moves to cell ", CM("(𝑥, 𝑦)")], "space_after": 6},
    {"runs": [CM("𝜏"), CM("2", sup=True), CM("(𝑃)"), ": the variance of ", CM("𝑔"), CM("𝑃", sub=True),
              CM("(𝑋, 𝑌)")]}], sz=13.5, color=INK, name="Step 2 definitions", margins=(0.02, 0.02, 0.02, 0.02))
contrib_tag(x2 + 0.2, Y5 + 3.1, "Contribution 1: derivation", 1)
approx_tag(x2 + 0.2, Y5 + 3.48, "first-order expansion", 1)
# Step 3: degrees of freedom (contribution 2)
x3 = L + 2 * (CW5 + GAP5)
equation(s, x3 + 0.1, Y5 + 0.72, CW5 - 0.2, 0.78,
         r"\mathrm{df}=\frac{2\times(\text{mean of }\widehat V)^2}{\text{variance of }\widehat V}", sz=15, jc="center")
equation(s, x3 + 0.1, Y5 + 1.55, CW5 - 0.2, 0.8, r"\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}",
         sz=19, jc="center")
text(s, x3 + 0.12, Y5 + 2.45, CW5 - 0.24, 0.55, [[B("More variation → fewer df → larger cutoff", c=GREEN)]],
     sz=13.5, anchor="ctr", align="ctr", name="Step 3 consequence")
contrib_tag(x3 + 0.2, Y5 + 3.1, "Contribution 2: test construction", 2)
approx_tag(x3 + 0.2, Y5 + 3.48, "moment matching", 2)
accent(s, L, 6.05, W, 0.6, [B("Then: ", c=NAVY), "repeat for Q and combine using Welch–Satterthwaite into one ", NUH,
                            " for the Student t cutoff. RQ1 checks both approximations (Slides 7–8)."],
       color=NAVY, sz=14, name="Combine")
footer(s, [("Thesis Sections 4.1–4.3. Derivations of these equations: Slides 16–18; ", {"i": True}), CM("𝑔"),
           (" and ", {"i": True}), CM("𝜏"), CM("2", sup=True), (" in full, with a worked example: Slides 19–21",
                                                               {"i": True})])
notes(s, main_note(5))

# =================================================================== Slide 6
s = new_slide("Evaluation design", 6)
lead(s, ["Known populations separate approximation accuracy, false positives, and power.", BR(), "Both tests receive ",
         O("the same sampled table pairs"), "."])
label(s, L, 1.82, 5.85, "Research questions", ORANGE)
soft(s, L, 2.38, 5.85, 3.3, "peach")
rq = [("RQ1: Approximation accuracy", ["Sampling moments of ", M(r"\hat{V}", [TI("V", hat=True)]), " and component df, including near independence"]),
      ("RQ2: False positives", ["Equal MI at 0.005, 0.02, and 0.30 nats"]),
      ("RQ3: Power", [CM("𝐼(𝑃)"), " = 0.02; MI-gap magnitudes 0.005, 0.01, and 0.02 nats"])]
for i, (lab, desc) in enumerate(rq):
    y = [2.85, 3.85, 4.6][i]
    circle(s, 0.82, y + 0.04, 0.34, str(i + 1), ORANGE, sz=12)
    text(s, 1.35, y - 0.03, 4.95, 0.95, [{"runs": [B(lab, c=ORANGE)], "sz": 15, "space_after": 2},
                                        {"runs": desc, "sz": 13.5}], color=INK)
label(s, 6.88, 1.82, 5.85, "Shared simulation grid", NAVY)
p = soft(s, 6.88, 2.38, 5.85, 3.3, "blue")
panel_text(p, [
    {"runs": ["Four sizes: 2×2, 4×4, 8×8, 16×16"], "bullet": True, "space_after": 6, "bullet_color": NAVY},
    {"runs": ["Uniform, same-skew, and different-skew margins"], "bullet": True, "space_after": 6, "bullet_color": NAVY},
    {"runs": ["Ten sample sizes: 10 to 50,000 observations per population"], "bullet": True, "space_after": 6, "bullet_color": NAVY},
    {"runs": [B("360 settings per study"), " (4 sizes × 3 margins × 10 sample sizes × 3 MI levels or gaps)"],
     "bullet": True, "space_after": 6, "bullet_color": NAVY},
    {"runs": ["100,000 independent table pairs per setting"], "bullet": True, "space_after": 12, "bullet_color": NAVY},
    {"runs": [B("Model: "), "a copying construction that fixes the margins and solves for the target MI."]},
], sz=14.5, color=INK, anchor="ctr", margins=(0.28, 0.24, 0.14, 0.14))
accent(s, L, 5.95, W, 0.6, [B("Reporting: "), "usual 0.05 p-value thresholds. Unsuccessful calculations count as "
                                               "non-rejections; calculation success is reported separately."],
       color=NAVY, sz=14.5, name="Reporting")
footer(s, "Morris et al. (2019). Thesis Chapter 5, Tables 5.1–5.3; exact vectors, sample sizes, and requirements on Slide 22")
notes(s, main_note(6))

# =================================================================== Slide 7
s = new_slide("RQ1 results: approximation accuracy", 7)
lead(s, ["The mean of ", M(r"\hat{V}", [TI("V", hat=True)]), " can ", O("remain inflated"),
         " even when its population first-order sampling-variance prediction is accurate."])
text(s, L, 1.8, 6.4, 0.3, [[B("Mean check: "), M(r"\mathbb{E}(\hat{V})", [CM("𝔼("), TI("V", hat=True), CM(")")], b=True),
                            B(" ÷ "), M(r"V", [TI("V")], b=True)]], sz=13.5,
     color=INK, name="Top plot heading", margins=(0.03, 0.03, 0, 0))
pic(s, "slide07_mean_ratio", 0.55, 2.12, 6.4, 1.85)
text(s, L, 4.12, 6.4, 0.3, [[B("Variance check: "), M(r"\tau^2/n", [CM("𝜏"), CM("2", sup=True), CM("/𝑛")], b=True),
                             B(" ÷ "), M(r"\operatorname{Var}(\hat{V})", [CM("Var("), TI("V", hat=True), CM(")")], b=True),
                             ("   predicted ÷ actual sampling variance", {"c": SOFT})]], sz=13.5,
     color=INK, name="Bottom plot heading", margins=(0.03, 0.03, 0, 0))
pic(s, "slide07_variance_ratio", 0.55, 4.44, 6.4, 2.15)
setting(s, "Different-skew P · 4×4 · population MI 0.02 nats", x=7.4, y=1.8, w=5.33)
panel(s, 7.4, 2.25, 5.33, 1.12, "peach", heading="Mean: rare cells can inflate it.",
      body=[["Newly observed rare cells can have large pointwise-MI deviations, whose squares raise ", M(r"\hat{V}", [TI("V", hat=True)]),
             "."]])
panel(s, 7.4, 3.57, 5.33, 1.6, "blue", heading=["Sampling variance:", "linearisation can miss large changes."],
      body=[["Rare cells appear in some samples and not others;", BR(), "sample-based sensitivities can also "
             "overpredict the resulting variation."]])
accent(s, 7.4, 5.37, 5.33, 1.13, [B("At n = 1,000: "), "mean ", B("19% high"), ";", BR(),
                                  "variance prediction ", B("3% low", c=NAVY), " with population-based inputs", BR(),
                                  "and ", B("8% high", c=ORANGE), " with sample-based inputs.", BR(),
                                  "Both moments enter the degrees of freedom."], sz=13.5)
footer(s, "Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2. Bands: approximate 95% Monte Carlo intervals. "
          "Other sizes and Q: Slide 23; derivation: Slide 16")
notes(s, main_note(7))

# =================================================================== Slide 8
s = new_slide("RQ1 results: near independence", 8)
lead(s, ["Near independence, first-order theory gives almost no degrees of freedom, while", BR(),
         O("sampling noise keeps the mean sample-based estimate at about half the target"), "."])
pic(s, "slide08_near_independence_df", 0.55, 1.85, 6.4, 4.3)
text(s, L, 6.2, 6.3, 0.5, [[B("Target: ", c=GREEN), "component degrees of freedom from the actual mean and variance of ",
                            M(r"\hat{V}", [TI("V", hat=True)]), " across 100,000 samples."]], sz=12.5, color=SOFT,
     name="Target definition", margins=(0.03, 0.03, 0, 0))
setting(s, "Different-skew P · 4×4 · n = 1,000 fixed", x=7.4, y=1.8, w=5.33)
panel(s, 7.4, 2.25, 5.33, 1.12, "peach", heading="Sample-based: noise keeps it near 5",
      body=[["Quadratic sampling errors create apparent association, which remains in each sample’s calculation."]])
panel(s, 7.4, 3.57, 5.33, 1.45, "blue", heading="Population-based: falls to about n × MI", anchor="ctr",
      body=[["Inserts known population inputs into the first-order formula. Near independence it is about "
             "n × population MI, which heads to zero."]])
accent(s, 7.4, 5.22, 5.33, 0.98, [B("At MI 0.0001: "), "target ", B("≈9.1", c=GREEN), ";", BR(),
                                "mean sample-based estimate ", B("≈4.9", c=ORANGE), ";", BR(),
                                "population-based value ", B("≈0.1", c=NAVY)], sz=13.5)
footer(s, "Thesis Section 6.1.3, Figure 6.3; Appendix A.2. Bands: approximate 95% Monte Carlo intervals. "
          "Definitions of the three lines: Slide 18; local calculation: Slide 24")
notes(s, main_note(8))

# =================================================================== Slide 9
s = new_slide("RQ2 results: false positives across all null settings", 9)
lead(s, ["A larger cutoff ", O("helps only where Wald rejects too often"), ";", BR(),
         "where Wald already rejects too rarely, it never brings the rate closer to 5%."])
setting(s, "All 360 null settings · equal MI in P and Q · each point is one setting")
pic(s, "slide09_null_all_settings", 0.55, 2.05, 6.4, 4.3)
text(s, L, 6.4, 6.3, 0.5, [["Below the diagonal: Expanded Welch rejects less often.", BR(), "Dashed lines: the 5% target."]],
     sz=12.5, color=SOFT, name="Chart note", margins=(0.03, 0.03, 0, 0))
panel(s, 7.4, 2.15, 5.33, 1.3, "peach", heading="Wald too high: 178 settings", anchor="ctr",
      body=[["Expanded Welch moves closer to 5% in 165, for example 8.35% to 4.90% (uniform 4×4, n = 20, MI 0.02)."]])
panel(s, 7.4, 3.65, 5.33, 1.1, "blue", heading="Wald too low: 180 settings", anchor="ctr",
      body=[["Further below 5% in 176 settings; unchanged in four."]])
accent(s, 7.4, 4.95, 5.33, 1.0, [B("Descriptive 4–6% band: "), "130 versus 136 settings.", BR(),
                                 "Bias-driven excess persists: 36.38% to 34.38%", BR(),
                                 "(different-skew 16×16, n = 1,000, MI 0.005)."], sz=13.5)
footer(s, "Tallies of the thesis null study (Sections 6.2.1–6.2.3, Figures 6.4–6.6); two settings sit exactly at 5%. "
          "Full grids on Slides 25–27")
notes(s, main_note(9))

# =================================================================== Slide 10
s = new_slide("RQ2 results: why the cutoff helps, hurts, or cannot fix it", 10)
lead(s, [O("Three kinds of estimation error"), " explain the three patterns on Slide 9."])
setting(s, "Three illustrative settings (thesis Table 6.1) · equal MI 0.02 nats · every calculation succeeds",
        y=1.45)
Rr = dict(sz=15, color=INK, anchor="ctr", align="ctr")
Lr = dict(sz=15, color=INK, anchor="ctr")
ROW_MARK = 0.55                             # room for the 1–3 markers that tie rows to the boxes below
rows = [[head_cell("Setting", align="l", ml=ROW_MARK), head_cell("Bias / SD"), head_cell("Variance ratio"),
         head_cell("Wald"), head_cell("Expanded Welch")],
        [dict(paras=["Uniform 4×4, n\u00a0=\u00a020"], ml=ROW_MARK, **Lr), dict(paras=["≈0"], **Rr),
         dict(paras=[[B("0.83")]], **Rr), dict(paras=["8.35%"], **Rr), dict(paras=["4.90%"], **Rr)],
        [dict(paras=["Same skew 16×16, n\u00a0=\u00a01,000"], ml=ROW_MARK, **Lr), dict(paras=["≈0"], **Rr),
         dict(paras=[[B("1.93")]], **Rr), dict(paras=["0.60%"], **Rr), dict(paras=["0.53%"], **Rr)],
        [dict(paras=["Different skew 16×16, n\u00a0=\u00a01,000"], ml=ROW_MARK, **Lr), dict(paras=[[B("2.06")]], **Rr),
         dict(paras=["1.94"], **Rr), dict(paras=["26.01%"], **Rr), dict(paras=["24.84%"], **Rr)]]
table(s, L, 1.92, [4.13, 1.85, 2.05, 1.85, 2.25], [0.46, 0.5, 0.5, 0.5], rows, name="Three settings")
MARK_COLS = [ORANGE, NAVY, GREEN]            # one colour per mechanism, matching each box
for i_, col in enumerate(MARK_COLS):
    circle(s, L + 0.1, 1.92 + 0.46 + 0.5 * i_ + 0.1, 0.3, str(i_ + 1), col, sz=12, name=f"Row marker {i_ + 1}")
text(s, L, 3.92, W, 0.32, [[("Bias / SD: shift of the estimated MI difference from zero, in sampling standard "
                             "deviations. Variance ratio: average squared estimated standard error / observed "
                             "variance.", {"i": True})]], sz=12, color=SOFT, name="Definitions")
for i_, (kind, hd, bd) in enumerate([
        ("peach", "Standard error too small", "Wald rejects too often. The larger cutoff offsets it: 8.35%\u00a0to\u00a04.90%."),
        ("blue", "Standard error too big", "Wald already rejects too rarely. The larger cutoff pushes it further "
                                           "below 5%."),
        ("green", "Bias in the MI difference", "The estimate sits about two SDs from zero. The larger cutoff barely "
                                               "helps: 26.01%\u00a0to\u00a024.84%.")]):
    x_ = L + i_ * 4.12
    panel(s, x_, 4.5, 3.89, 1.42, kind, body=[[bd]], bsz=13.5, margins=(0.2, 0.18, 0.53, 0.12))
    circle(s, x_ + 0.2, 4.64, 0.3, str(i_ + 1), MARK_COLS[i_], sz=12, name=f"Box marker {i_ + 1}")
    text(s, x_ + 0.6, 4.6, 3.15, 0.38, [[B(hd, c=MARK_COLS[i_])]], sz=14.5, anchor="ctr", name=f"Box heading {i_ + 1}",
         margins=(0.02, 0.02, 0, 0))
accent(s, L, 6.1, W, 0.6, [B("Conclusion: "), "A larger cutoff can offset a standard error that is too "
                                                        "small, but it cannot fix bias in the estimated MI difference."],
       sz=14.5, name="Conclusion")
footer(s, "Thesis Section 6.2.4, Table 6.1. Bias correction: Slide 15. Full grids: Slides 25–27; ordinary Welch comparison: Slide 28")
notes(s, main_note(10))

# =================================================================== Slide 11
s = new_slide("RQ3 results: the power cost of the larger cutoff", 11)
lead(s, ["Expanded Welch ", O("never has more power than Wald"), ";", BR(),
         "the loss is largest in small samples and under 0.32 points by n = 10,000."])
setting(s, "All 360 power settings · MI in P = 0.02 nats · gaps of 0.005, 0.01, and 0.02 nats")
pic(s, "slide11_power_loss_all_settings", 0.55, 2.05, 6.4, 4.3)
text(s, L, 6.4, 6.3, 0.5, [["Power lost: Wald power minus Expanded Welch power, in percentage points."]],
     sz=12.5, color=SOFT, name="Chart note", margins=(0.03, 0.03, 0, 0))
panel(s, 7.4, 2.15, 5.33, 1.55, "peach", heading="The loss is concentrated in small samples", anchor="ctr",
      body=[["Median loss: about 6 points at n = 10, about 1 point from n = 50 to 1,000, and 0.16 at n = 10,000. "
             "Failed calculations add to it at the smallest samples."]])
panel(s, 7.4, 3.9, 5.33, 1.3, "blue", heading="Small MI gaps can stay hard to detect", anchor="ctr",
      body=[["Even at n = 50,000, the 0.005 gap reaches only", BR(), "79.87%–96.47% power; gaps of 0.01 and 0.02 "
             "exceed 99.9%."]])
accent(s, 7.4, 5.4, 5.33, 0.8, [B("Power: "), "rejecting equal MI when population MI differs, in either direction, "
                                             "at the usual 0.05 threshold."], sz=13.5)
footer(s, "Tallies of the thesis power study (Sections 6.3.1–6.3.3, Figures 6.7–6.9); unsuccessful calculations count as "
          "non-rejections. Full grids on Slides 29–31")
notes(s, main_note(11))

# =================================================================== Slide 12
s = new_slide("RQ3 results: bias can reverse the estimated direction", 12)
lead(s, ["Under different-skew margins, sparse tables give rejections that ",
         O("point to the wrong population"), "."])
setting(s, "Different-skew margins · MI gap 0.01 nats · % of Expanded Welch rejections with the wrong sign")
pic(s, "slide12_wrong_direction_heatmap", 0.55, 2.05, 6.4, 4.3)
text(s, L, 6.5, 6.3, 0.46, [["Percentages are rounded.", BR(), "A value of 50% means half the rejections have the "
                            "wrong estimated sign."]], sz=12.5, color=SOFT, name="Chart note", margins=(0.03, 0.03, 0, 0))
panel(s, 7.4, 2.15, 5.33, 1.3, "peach", heading="Outlined cell: 16×16, n = 1,000",
      body=[["True difference −0.0100 nats; mean estimate +0.0207. Expanded Welch rejects in 9.66% of repetitions, "
             "and over 99.9% of those point the wrong way."]])
p = soft(s, 7.4, 3.65, 5.33, 1.62, "blue", name="Bias panel")
panel_text(p, [
    {"runs": [("Higher-order bias outweighs the gap", {"b": True, "c": NAVY})], "sz": 14.5, "space_after": 5},
    {"runs": [B("Leading term:"), " 0.11 nats each; equal n cancels it"], "bullet": True, "bullet_color": NAVY, "space_after": 4},
    {"runs": [B("Higher-order bias:"), " differs between P’s and Q’s margins, shifting the difference by +0.031 nats "
              "(3× the gap)"], "bullet": True, "bullet_color": NAVY, "space_after": 4},
    {"runs": [B("Fix:"), " more data, not a larger cutoff"], "bullet": True, "bullet_color": NAVY},
], sz=13.5, color=INK, anchor="t", margins=(0.2, 0.18, 0.15, 0.12))
accent(s, 7.4, 5.47, 5.33, 0.9, [B("Across all 360 power settings, "), "28 have at least 90% of rejections pointing "
                                "the wrong way. All 28 are 8×8 or 16×16 with different-skew margins."], sz=13.5)
footer(s, "Tallies of the thesis power-study diagnostics (Section 6.3.3, Figure 6.9); other gaps show the same pattern. "
          "Outlined cell: 9,659 of 9,662 rejections positive")
notes(s, main_note(12))

# =================================================================== Slide 13 (conclusions)
s = new_slide("Conclusions and next steps", 13)
lead(s, ["MI-specific degrees of freedom improve some false-positive rates, while remaining failures identify ",
         O("estimation accuracy as a priority"), "."])
label(s, L, 1.7, W, "Contributions", ORANGE)
for i, (name, desc) in enumerate(CONTRIBUTIONS):       # stronger peach and large numerals: the slide's highlight
    x = L + i * 4.12
    rect(s, x, 2.2, 3.89, 0.92, fill=CONTRIB_FILLS[i], rounded=0.04, name=f"Contribution {i + 1}")
    text(s, x + 0.12, 2.2, 0.55, 0.92, [[(str(i + 1), {"b": True, "c": POS_COLS[i]})]], sz=34, align="ctr", anchor="ctr",
         name=f"Contribution {i + 1} number", margins=(0, 0, 0, 0))
    text(s, x + 0.72, 2.2, 3.05, 0.92, [{"runs": [B(name, c=[EW_TEXT, NAVY, GREEN][i])], "sz": 14.5, "space_after": 2},
                                        {"runs": [desc], "line": 1.0}], sz=12.5, color=INK, anchor="ctr",
         name=f"Contribution {i + 1} text")
label(s, L, 3.26, W, "Findings by research question", NAVY)
finds = [("RQ1", "Approximation accuracy", "Approximations improve as samples grow; near independence, first-order "
                                            "theory misses sampling noise."),
         ("RQ2", "False positives", "Helped only where Wald rejected too often; pushed conservative settings further "
                                    "below\u00a05%."),
         ("RQ3", "Power and direction", "At the same nominal 5% threshold, power is no higher; bias can make "
                                        "rejections point the wrong way.")]
for i, (rq, hd, bd) in enumerate(finds):
    x = L + i * 4.12
    soft(s, x, 3.76, 3.89, 1.25, POS_KINDS[i], name=f"Finding {rq}")
    pill = rect(s, x + 0.2, 3.9, 0.56, 0.27, fill=POS_COLS[i], rounded=0.5, name=f"{rq} tag")
    panel_text(pill, [[(rq, {"b": True})]], sz=11, color=WHITE, align="ctr", anchor="ctr", margins=(0, 0, 0, 0))
    text(s, x + 0.86, 3.87, 2.9, 0.33, [[B(hd, c=POS_COLS[i])]], sz=13.5, anchor="ctr", name=f"{rq} heading")
    text(s, x + 0.2, 4.24, 3.55, 0.72, [{"runs": [bd], "line": 1.0}], sz=12.5, color=INK, name=f"{rq} finding")
accent(s, L, 5.12, W, 0.38, [B("Scope: ", c=NAVY), "The evaluation covers one population construction and equal "
                                                "sample sizes, with the Wald test as the main benchmark."],
       color=NAVY, sz=13, name="Scope")
label(s, L, 5.58, W, "Next steps", ORANGE)
nexts = ["Reduce bias in the estimated MI difference and improve its standard error and degrees of freedom, "
         "including near independence.",
         "Test other association constructions and unequal sample sizes."]
for i, txt in enumerate(nexts):
    x = L + i * 6.165
    arrow(s, x + 0.04, 6.18, w=0.26, h=0.2)
    text(s, x + 0.42, 6.02, 5.5, 0.52, [{"runs": [txt], "line": 1.0}], sz=13, color=INK, anchor="ctr",
         name=f"Next step {i + 1}")
text(s, L, 6.64, W, 0.32, ["Thank you."], sz=15, color=SOFT, align="ctr", name="Thank you")
BACKUP_INDEX = """BACKUP INDEX (type the slide number, press Enter, then return to 13)
14  Appendix title and index
Method (supports Slides 4–5)
15  Bias correction
16  Derivation 1 of 3: how much the variance estimate varies
17  Derivation 2 of 3: moment matching gives the df rule
18  Derivation 3 of 3: estimated and combined degrees of freedom
19  Variance sensitivity in full
20  Variance sensitivity in cell probabilities
21  Worked example: sensitivities and degrees of freedom
Evaluation design (supports Slide 6)
22  Population construction, grid, and calculation requirements
RQ1: approximation accuracy (supports Slides 7–8)
23  Approximation ratios across table sizes
24  Near-independence noise calculation
RQ2: full null results (supports Slides 9–10)
25  Full null results: uniform margins
26  Full null results: same-skew margins
27  Full null results: different-skew margins
28  Ordinary Welch degrees of freedom
RQ3: full power results (supports Slides 11–12)
29  Full power results: uniform margins
30  Full power results: same-skew margins
31  Full power results: different-skew margins
References
32  References: MI and testing foundations
33  References: related methods and evaluation"""
notes(s, main_note(13, extra=BACKUP_INDEX))

# =================================================================== Appendix title (14)
s = prs.slides.add_slide(LAYOUT)
for ph in list(s.placeholders):
    ph._element.getparent().remove(ph._element)
text(s, L, 2.45, 3.4, 0.85, [[B("Appendix")]], sz=44, color=NAVY, anchor="ctr", name="Appendix title")
text(s, L, 3.3, 3.4, 0.4, ["Backup slides for questions"], sz=17, color=SOFT, name="Appendix subtitle")
text(s, L, 3.85, 3.3, 1.2, ["Grouped in the order of the talk. To jump, type the slide number and press Enter. "
                            "Type 13 to return to the conclusion."], sz=13, color=FAINT, name="Jump hint")
vline(s, 4.35, 1.2, 5.4, color=RULE, width=1.0)
APPENDIX_GROUPS = [   # (group heading, colour, x, y, [(physical slide, short title)]), in talk order
    ("Method (Slides 4–5)", ORANGE, 4.75, 1.2,
     [(15, "Bias correction"), (16, "Derivation 1: variance of the estimate"), (17, "Derivation 2: moment matching"),
      (18, "Derivation 3: estimated and combined df"), (19, "Variance sensitivity in full"),
      (20, "Sensitivity in cell probabilities"), (21, "Worked example")]),
    ("Evaluation design (Slide 6)", ORANGE, 4.75, 4.27, [(22, "Populations, grid, requirements")]),
    ("References", ORANGE, 4.75, 5.31, [(32, "MI and testing foundations"), (33, "Related methods, evaluation")]),
    ("RQ1 accuracy (Slides 7–8)", NAVY, 8.83, 1.2, [(23, "Ratios by table size"), (24, "Near-independence noise")]),
    ("RQ2 null results (Slides 9–10)", NAVY, 8.83, 2.6,
     [(25, "Uniform margins"), (26, "Same-skew margins"), (27, "Different-skew margins"),
      (28, "Ordinary Welch comparison")]),
    ("RQ3 power results (Slides 11–12)", NAVY, 8.83, 4.68,
     [(29, "Uniform margins"), (30, "Same-skew margins"), (31, "Different-skew margins")])]
for grp, col, gx, gy, items in APPENDIX_GROUPS:
    label(s, gx, gy, 3.9, grp, col)
    ix_rows = [[dict(paras=[[B(str(n), c=ORANGE)]], sz=13.5, anchor="ctr", ml=0.02, mr=0.02, bottom=None),
                dict(paras=[ttl], sz=13.5, color=INK, anchor="ctr", ml=0.02, mr=0.02, bottom=None)]
               for n, ttl in items]
    table(s, gx, gy + 0.46, [0.5, 3.4], [0.34] * len(items), ix_rows, name=f"Index {grp}")
slide_number(s, 14)
notes(s, f"Questions and answer guides\n\n{SPOKEN_QA}" if SPOKEN_QA else
      "Appendix title. Not part of the timed talk.\n\nDELIVERY\n" + PLAN_APPENDIX)

# =================================================================== Slide 15: bias correction
s = new_slide("Bias correction", 15)
backup_label(s, "Appendix · Method · for Slide 4")
intro(s, [B("The leading correction removes the 1/n bias from each estimate; with equal sample sizes it cancels "
            "from the difference")])
LW4 = 6.95                                   # formula column width
label(s, L, 1.55, LW4, "Plug-in estimate and its leading bias", ORANGE)
equation(s, L, 2.02, LW4, 0.8, r"\widehat I(P)=\sum_{i,j:\,\widehat p_{ij}>0}\,\widehat p_{ij}\log"
         r"\frac{\widehat p_{ij}}{\widehat p_{i+}\,\widehat p_{+j}}", sz=18)
equation(s, L, 2.86, LW4, 0.62, r"\mathbb E\{\widehat I(P)\}-I(P)=\frac{(r-1)(c-1)}{2n_P}+O(n_P^{-2})", sz=18)
text(s, L, 3.52, LW4, 0.5, [[CM("𝑟"), " and ", CM("𝑐"), " are the numbers of rows and columns. The bias is positive "
                             "even when ", CM("𝑋"), " and ", CM("𝑌"), " are independent (Miller, 1955)."]],
     sz=12.5, color=SOFT, name="Bias note")
label(s, L, 4.12, LW4, "Bias-corrected difference", NAVY)
equation(s, L, 4.6, LW4, 0.8, r"\widehat\Delta_{\mathrm{BC}}=\left\{\widehat I(P)-\frac{(r-1)(c-1)}{2n_P}\right\}"
         r"-\left\{\widehat I(Q)-\frac{(r-1)(c-1)}{2n_Q}\right\}", sz=17)
text(s, L, 5.45, LW4, 0.5, [["Without it, unequal sample sizes bias the difference: 0.005 nats for a 2×2 table with ",
                             CM("𝑛"), CM("𝑃", sub=True), " = 50 and ", CM("𝑛"), CM("𝑄", sub=True),
                             " = 100, at equal MI."]], sz=12.5, color=SOFT, name="Unequal note")
CX4 = L + LW4 + 0.35                         # card column
CW4 = L + W - CX4
for i_, (kind, hd, bd) in enumerate([
        ("peach", "Size of the leading term",
         ["16×16 at n\u00a0=\u00a01,000: 225/2,000 ≈ 0.11 nats per estimate, over five times the MI of 0.02."]),
        ("blue", "It cancels in these simulations",
         [CM("𝑛"), CM("𝑃", sub=True), " = ", CM("𝑛"), CM("𝑄", sub=True), " and the table sizes match, so ",
          M(r"\hat{\Delta}_{\mathrm{BC}}", [("Δ̂", {"font": "Georgia"}), CM("BC", sub=True, i=False)]),
          " equals the raw plug-in difference."]),
        ("green", "What remains",
         ["Higher-order bias, which depends on the whole table and can differ between P and Q. Different-skew "
          "16×16, n\u00a0=\u00a01,000: true difference −0.01 nats, mean estimate +0.0207 (Slide 12)."])]):
    panel(s, CX4, [1.55, 2.87, 4.19][i_], CW4, [1.12, 1.12, 1.6][i_], kind, heading=hd, body=[bd], hsz=14.5,
          bsz=13.5, name=f"Bias card {i_ + 1}")
accent(s, L, 6.12, W, 0.55, [B("Beyond the leading term: ", c=NAVY), "Panzeri–Treves, the jackknife, Chao–Shen "
                             "coverage, and NSB estimators (thesis Section 2.2.2)."], color=NAVY, sz=14,
       name="Beyond")
footer(s, "Thesis Equations 2.7–2.9 and 3.7; Sections 2.2, 3.1.2 and 5.5. References: Slides 32–33")
notes(s, backup_note(15))

# =================================================================== Slides 16-18: derivations behind Slide 5
# Each is a ladder of numbered steps: the step in words, the equation, and the thesis reference.
DSX, DSW = L + 0.48, 3.55                    # step text
EQX = L + 4.2                                # equation column
REFX = L + W - 1.45                          # thesis reference column
EQW = REFX - EQX - 0.1
VHP = M(r"\hat{V}(P)", [TI("V", hat=True), CM("(𝑃)")])
PH = M(r"\hat{P}", [TI("P", hat=True)])
NP = [CM("𝑛"), CM("𝑃", sub=True)]
EV = r"\mathbb E\{\widehat V(P)\}"
VV = r"\operatorname{Var}\{\widehat V(P)\}"


def ladder(s, rows, y, col):
    """rows: (step runs, [(latex, size, height, colour or None)], thesis reference, row height)."""
    for i_, (step, eqs, ref, h) in enumerate(rows):
        circle(s, L + 0.04, y + h / 2 - 0.15, 0.3, str(i_ + 1), col, sz=12, name=f"Step {i_ + 1} marker")
        text(s, DSX, y, DSW, h, [{"runs": step, "line": 1.0}], sz=13.5, color=INK, anchor="ctr",
             name=f"Step {i_ + 1} text")
        ey = y + (h - sum(e[2] for e in eqs)) / 2
        for latex, sz_, eh, ecol in eqs:
            equation(s, EQX, ey, EQW, eh, latex, sz=sz_, color=ecol or BLACK, name=f"Step {i_ + 1} equation")
            ey += eh
        text(s, REFX, y, L + W - REFX, h, [[ref]], sz=11.5, color=SOFT, align="r", anchor="ctr",
             name=f"Step {i_ + 1} reference", margins=(0, 0.02, 0, 0))
        if i_ < len(rows) - 1:
            hline(s, L, y + h, W, color=DIVIDER, width=0.75)
        y += h
    return y


def result_box(s, y, h, kind, col, heading, latex, sz=19):
    soft(s, L, y, W, h, kind, name="Result")
    text(s, L + 0.2, y, EQX - L - 0.3, h, [[B(heading, c=col)]], sz=14, anchor="ctr", name="Result heading")
    equation(s, EQX, y + 0.03, L + W - EQX - 0.2, h - 0.06, latex, sz=sz, name="Result equation")


# ---------------------------------------------------------------- Derivation 1 (Slide 16)
s = new_slide("Derivation 1 of 3: how much the variance estimate varies", 16)
backup_label(s, "Appendix · Method · for Slide 5, step 2")
intro(s, ["A first-order expansion of ", VHP, " = ", CM("𝑉"), "(", PH, ") around the population table ", CM("𝑃")])
y = ladder(s, [
    (["Write the sample table as an average of one-observation tables"],
     [(r"\widehat P-P=\frac{1}{n_P}\sum_{a=1}^{n_P}\,\left(\delta_{Z_a}-P\right)", 17, 0.62, None),
      (r"\delta_{Z_a}:\ \text{all probability on the cell of observation }a", 13, 0.28, SOFT)], "Eq. 4.30", 0.88),
    (["Expand ", CM("𝑉"), " to first order along the line from ", CM("𝑃"), " to ", PH],
     [(r"\widehat V(P)-V(P)=V(\widehat P)-V(P)\approx\frac{\mathrm d}{\mathrm dt}V\{P+t(\widehat P-P)\}\;\;"
       r"\mathrm{at}\;\;t=0", 17, 0.62, None)], "Section 4.3.1", 0.68),
    (["The derivative is linear in the table change, so it splits into one term per observation"],
     [(r"\widehat V(P)-V(P)\approx\frac{1}{n_P}\sum_{a=1}^{n_P}\,g_P(Z_a)", 17, 0.62, None),
      (r"g_P(x,y)=\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)\;\;\mathrm{at}\;\;\varepsilon=0,\qquad "
       r"P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}", 13, 0.46, SOFT)], "Eqs. 4.10, 4.11, 4.31", 1.06),
    (["The sensitivities average to zero, so the mean is ", CM("𝑉(𝑃)"), " to first order"],
     [(r"\mathbb E_P\{g_P(X,Y)\}=0\quad\Rightarrow\quad" + EV + r"\approx V(P)", 17, 0.5, None)], "Eq. 4.35", 0.6),
    (["Observations are independent, so the variances of the terms add"],
     [(VV + r"\approx\frac{1}{n_P^2}\sum_{a=1}^{n_P}\,\operatorname{Var}_P\{g_P(Z_a)\}=\frac{\tau^2(P)}{n_P}", 17, 0.7,
       None),
      (r"\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}", 13, 0.28, SOFT)], "Eqs. 4.36–4.38", 0.96),
], 1.48, NAVY)
result_box(s, y + 0.1, 0.8, "blue", NAVY, "Result: Slide 5, step 2",
           EV + r"\approx V(P),\qquad" + VV + r"\approx\frac{\tau^2(P)}{n_P}", sz=18)
text(s, L, y + 0.94, W, 0.34, [["First order: drops terms quadratic in the cell errors and needs positive cell "
                                "probabilities. Slide 7 checks both approximations; ", CM("𝑔"),
                                " in full: Slides 19–20."]], sz=12.5, color=SOFT, anchor="ctr", name="Derivation note")
footer(s, "Thesis Sections 4.2.1, 4.3.1 and 4.3.2")
notes(s, backup_note(16))

# ---------------------------------------------------------------- Derivation 2 (Slide 17)
s = new_slide("Derivation 2 of 3: moment matching gives the df rule", 17)
backup_label(s, "Appendix · Method · for Slide 5, step 3")
intro(s, ["Satterthwaite (1946): give ", VHP, " a scaled chi-squared distribution with the same mean and variance"])
y = ladder(s, [
    (["Model the estimate as a scaled", BR(), "chi-squared variable with ", CM("𝜈"), " degrees", BR(), "of freedom"],
     [(r"\widehat V(P)\ \dot{\sim}\ " + EV + r"\,\frac{\chi^2_\nu}{\nu}", 17, 0.62, None)], "Eq. 4.2", 0.74),
    (["Use the chi-squared moments; the model’s mean then matches for any ", CM("𝜈")],
     [(r"\mathbb E(\chi^2_\nu)=\nu,\quad\operatorname{Var}(\chi^2_\nu)=2\nu\quad\Rightarrow\quad"
       r"\mathbb E(\mathrm{model})=" + EV, 17, 0.5, None)], "Eqs. 4.3–4.4", 0.74),
    (["Its variance depends on ", CM("𝜈")],
     [(r"\operatorname{Var}(\mathrm{model})=\frac{[" + EV + r"]^2}{\nu^2}\,2\nu=\frac{2[" + EV + r"]^2}{\nu}", 17,
       0.68, None)], "Eqs. 4.5–4.6", 0.8),
    (["Set it equal to the actual variance and solve for ", CM("𝜈")],
     [(r"\frac{2[" + EV + r"]^2}{\nu}=" + VV + r"\quad\Rightarrow\quad\nu_{P,\mathrm{mom}}=\frac{2[" + EV + r"]^2}{"
       + VV + "}", 17, 0.72, None)], "Eq. 4.7", 0.86),
    (["The test divides by the fixed ", *NP, ";", BR(), "the factor cancels"],
     [(r"\frac{2[\mathbb E\{\widehat V(P)/n_P\}]^2}{\operatorname{Var}\{\widehat V(P)/n_P\}}=\frac{2[" + EV +
       r"]^2/n_P^2}{" + VV + r"/n_P^2}=\nu_{P,\mathrm{mom}}", 17, 0.72, None)], "Section 4.1.2", 0.86),
], 1.48, GREEN)
result_box(s, y + 0.1, 0.72, "green", GREEN, "Result: the df rule on Slide 5, step 3",
           r"\mathrm{df}=\frac{2\times(\text{mean of }\widehat V)^2}{\text{variance of }\widehat V}=\nu_{P,\mathrm{mom}}",
           sz=18)
text(s, L, y + 0.9, W, 0.62, [
    {"runs": [B("Check: "), "for normal data, ", CM("𝑠"), CM("2", sup=True), " is exactly ",
              M(r"\sigma^2\chi^2_{n-1}/(n-1)", [CM("𝜎"), CM("2", sup=True), CM("𝜒"), CM("2", sup=True),
                                                CM("𝑛−1", sub=True), CM("/(𝑛 − 1)")]),
              ", so the rule gives ordinary Welch’s ", CM("𝑛 − 1"), " (Slide 28)."], "space_after": 2},
    {"runs": ["Moment matching motivates the Student t reference. It does not establish the standard normal numerator, "
              "or its independence from the variance estimates."]}], sz=12.5, color=SOFT, name="Derivation note")
footer(s, "Satterthwaite (1946). Thesis Section 4.1.2")
notes(s, backup_note(17))

# ---------------------------------------------------------------- Derivation 3 (Slide 18)
s = new_slide("Derivation 3 of 3: estimated and combined degrees of freedom", 18)
backup_label(s, "Appendix · Method · for Slide 5, step 3")
intro(s, ["Put Derivation 1 into Derivation 2, estimate the inputs from one table, then combine ", CM("𝑃"), " and ",
          CM("𝑄")])
y = ladder(s, [
    (["Substitute the first-order mean and variance from Derivation 1"],
     [(r"\nu_{P,\mathrm{mom}}\approx\frac{2V(P)^2}{\tau^2(P)/n_P}=\frac{2n_PV(P)^2}{\tau^2(P)}=\nu_{P,\mathrm{FO}}", 17,
       0.68, None)], "Eq. 4.39", 0.78),
    (["Read it as two over the relative variance: more variation, fewer df"],
     [(VV + r"\,/\,V(P)^2\approx\frac{\tau^2(P)}{n_PV(P)^2}=\frac{2}{\nu_{P,\mathrm{FO}}}", 17, 0.68, None)],
     "Eq. 4.40", 0.78),
    (["Estimate the inputs from the table, over occupied cells (cell forms: Slide 20)"],
     [(r"\widehat\tau^2(P)=\sum_{i,j}\,\widehat p_{ij}\left\{\widehat g_P(i,j)-\sum_{k,l}\,\widehat p_{kl}\,"
       r"\widehat g_P(k,l)\right\}^2", 17, 0.72, None)], "Eqs. 4.41–4.42", 0.84),
    (["Plug in to get the component estimate; the same for ", CM("𝑄")],
     [(r"\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}", 17, 0.72, None)], "Eq. 4.43", 0.8),
    (["Combine: moment-match the squared standard error. The samples are independent, so means and variances add"],
     [(r"\widehat{\mathrm{SE}}^2=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}", 15, 0.6, SOFT),
      (r"\widehat\nu=\frac{\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\}^2}{\{\widehat V(P)/n_P\}^2/\widehat\nu_P+"
       r"\{\widehat V(Q)/n_Q\}^2/\widehat\nu_Q}", 17, 0.72, None)], "Eq. 4.44", 1.38),
], 1.48, GREEN)
TAU_H = M(r"\hat{\tau}^2(P)", [CM("𝜏̂"), CM("2", sup=True), CM("(𝑃)")])
DF_CARDS = [
    ([M(r"\hat{\nu}_{P}", [CM("𝜈̂"), CM("𝑃", sub=True)]), B(": estimate used by the test", c=ORANGE)],
     [VHP, ", ", TAU_H, ", and ", *NP, " from one table"]),
    ([M(r"\nu_{P,\mathrm{FO}}", [CM("𝜈"), CM("𝑃,FO", sub=True)]), B(": population, first order", c=NAVY)],
     [CM("𝑉(𝑃)"), ", ", CM("𝜏"), CM("2", sup=True), CM("(𝑃)"), ", and ", *NP]),
    ([M(r"\nu_{P,\mathrm{mom}}", [CM("𝜈"), CM("𝑃,mom", sub=True)]), B(": target", c=GREEN)],
     ["Sampling mean and variance of ", VHP])]
CWD = (W - 0.4) / 3
for i_, (hd, bd) in enumerate(DF_CARDS):
    x_ = L + i_ * (CWD + 0.2)
    soft(s, x_, y + 0.1, CWD, 0.8, POS_KINDS[i_], name=f"df card {i_ + 1}")
    text(s, x_ + 0.15, y + 0.14, CWD - 0.3, 0.72, [{"runs": hd, "sz": 14, "space_after": 2}, {"runs": bd}], sz=12.5,
         color=INK, anchor="ctr", name=f"df card {i_ + 1} text")
footer(s, [("Slide 8 compares all three. Requires ", {"i": True}), CM("𝜏"), CM("2", sup=True),
           ("(P) > 0 (Assumption 5). Thesis Sections 4.3.3–4.3.4, Table 4.1", {"i": True})])
notes(s, backup_note(18))

# =================================================================== Slide 19: variance sensitivity in full
s = new_slide("Variance sensitivity in full", 19)
backup_label(s, "Appendix · Method · detail for Slide 16")
text(s, L, 1.2, 3.55, 0.55, [[B("Perturbation towards one cell:")]], sz=16, color=INK, anchor="ctr")
equation(s, 4.15, 1.2, 6.5, 0.55, r"P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}", sz=20)
soft(s, L, 2.05, W, 3.0, "peach")
equation(s, 3.95, 2.2, 8.6, 0.75, r"g_P(x,y)=\{\ell_P(x,y)-I(P)\}^2-V(P)", sz=22)
equation(s, 3.95, 3.08, 8.6, 0.75, r"\qquad+2\bigl[\ell_P(x,y)-\mathbb E_P\{\ell_P(X,Y)\mid X=x\}", sz=22)
equation(s, 3.95, 3.96, 8.6, 0.75, r"\qquad\qquad-\mathbb E_P\{\ell_P(X,Y)\mid Y=y\}+I(P)\bigr]", sz=22)
text(s, 0.82, 2.2, 3.0, 0.75, [[O("Changing probability weights")]], sz=15, anchor="ctr")
text(s, 0.82, 3.08, 3.0, 1.63, [[O("Changing pointwise-MI values and margins")]], sz=15, anchor="ctr")
vline(s, 3.85, 3.15, 1.49, color=ORANGE_TINT, width=1.5)
text(s, L, 5.45, 3.3, 0.55, ["Pointwise MI:"], sz=16, color=INK, anchor="ctr")
equation(s, 3.95, 5.45, 7.5, 0.55, r"\ell_P(i,j)=\log\{p_{ij}/(p_{i+}p_{+j})\}", sz=20)
text(s, L, 6.2, 3.3, 0.55, ["Sensitivity variance:"], sz=16, color=INK, anchor="ctr")
equation(s, 3.95, 6.2, 7.5, 0.55, r"\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}", sz=20)
footer(s, "Exact for positive population tables; its use for sampling errors is first order. Thesis Chapter 4")
notes(s, backup_note(19,
    extra="Assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. With every cell positive, positive MI is equivalent to positive V (Appendix A.3), but positive V does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.",
    source="Thesis Chapter 4: perturbation path (eq:contamination-path), final form of g (eq:g-final), and definition of "
           "tau-squared (eq:tau-definition). This derivative is exact for positive population tables. Its use for "
           "sampling errors is first order."))

# =================================================================== Slide 20: sensitivity in cell probabilities
s = new_slide("Variance sensitivity in cell probabilities", 20)
backup_label(s, "Appendix · Method · detail for Slide 16")
intro(s, ["Each quantity as an expectation, variance, or derivative, and as a sum over the cells of one table"])
QW, DW = 2.8, 4.3                         # quantity and definition column widths
DX, CX = L + QW, L + QW + DW
CWID = L + W - CX
GRID = [  # quantity, definition, cell form, row height
    ("Pointwise MI", r"\ell_P(x,y)=\log\frac{\Pr(X=x,\,Y=y)}{\Pr(X=x)\Pr(Y=y)}",
     r"\ell_{ij}=\log\frac{p_{ij}}{p_{i+}\,p_{+j}}", 0.6),
    ("MI", r"I(P)=\mathbb E_P\{\ell_P(X,Y)\}", r"I=\sum_{i,j}\,p_{ij}\,\ell_{ij}", 0.54),
    ("Variance of pointwise MI", r"V(P)=\operatorname{Var}_P\{\ell_P(X,Y)\}",
     r"V=\sum_{i,j}\,p_{ij}(\ell_{ij}-I)^2", 0.54),
    ("Row mean of pointwise MI", r"\mathbb E_P\{\ell_P(X,Y)\mid X=i\}",
     r"\bar\ell_{i+}=\frac{1}{p_{i+}}\sum_{j}\,p_{ij}\,\ell_{ij}", 0.62),
    ("Column mean of pointwise MI", r"\mathbb E_P\{\ell_P(X,Y)\mid Y=j\}",
     r"\bar\ell_{+j}=\frac{1}{p_{+j}}\sum_{i}\,p_{ij}\,\ell_{ij}", 0.62),
    ("Sensitivity of V to cell (i, j)", None,
     r"g_{ij}=(\ell_{ij}-I)^2-V+2(\ell_{ij}-\bar\ell_{i+}-\bar\ell_{+j}+I)", 0.88),
    ("Variance of the sensitivities", r"\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}",
     r"\tau^2=\sum_{i,j}\,p_{ij}\,g_{ij}^2", 0.54),
    ("Component degrees of freedom",
     r"\nu_P=\frac{2[\mathbb E\{\widehat V(P)\}]^2}{\operatorname{Var}\{\widehat V(P)\}}\approx\frac{2n_PV(P)^2}{\tau^2(P)}",
     r"\widehat\nu_P=\frac{2n_P{\widehat V}^2}{{\widehat\tau}^2}", 0.7),
]
y = 1.35
for txt, x_ in [("Quantity", L), ("Definition", DX), ("In cell probabilities", CX)]:
    text(s, x_ + 0.08, y, 3.5, 0.3, [[B(txt)]], sz=13, color=SOFT, anchor="b", name="Grid heading")
y += 0.34
hline(s, L, y, W, color=NAVY_TINT, width=1.0)
for q, d, c, h in GRID:
    if q.startswith("Sensitivity of V"):
        soft(s, L, y + 0.03, W, h - 0.06, "peach")
        text(s, L + 0.08, y, QW - 0.1, h, [[O(q)]], sz=14, anchor="ctr", name="Grid quantity")
        equation(s, DX, y + 0.02, DW - 0.1, 0.54, r"g_P(i,j)=\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)"
                 r"\;\;\mathrm{at}\;\;\varepsilon=0", sz=17)
        equation(s, DX, y + 0.54, DW - 0.1, 0.34, r"P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(i,j)}", sz=14,
                 color=SOFT)
        equation(s, CX, y, CWID, h, c, sz=17)
    else:
        text(s, L + 0.08, y, QW - 0.1, h, [[q]], sz=14, color=INK, anchor="ctr", name="Grid quantity")
        equation(s, DX, y, DW - 0.1, h, d, sz=17)
        equation(s, CX, y, CWID, h, c, sz=17)
        hline(s, L, y + h, W, color=DIVIDER, width=0.75)
    y += h
text(s, L, y + 0.03, W, 0.27, [["The sensitivities have probability-weighted mean zero. Estimates replace each ",
                               CM("𝑝"), CM("𝑖𝑗", sub=True), " with ", CM("𝑛"), CM("𝑖𝑗", sub=True), CM("/𝑛"),
                               CM("𝑃", sub=True), " over occupied cells. Worked example: next slide."]],
     sz=12.5, color=SOFT, name="Estimate note")
footer(s, "Thesis Equations 2.3, 2.4, 4.7, 4.9–4.11, 4.29, 4.36 and 4.41–4.43")
notes(s, backup_note(20))

# =================================================================== Slide 21: worked example
s = new_slide("Worked example: sensitivities and degrees of freedom", 21)
backup_label(s, "Appendix · Method · example for Slides 16–20")
intro(s, ["Thesis table ", CM("𝑁"), CM("𝑃", sup=True), ": one cell step by step, then all nine cells"])
LW = 3.75                                   # left column: tables
label(s, L, 1.5, LW, "Counts", NAVY)


def count_cell(v, hi=False, total=False, top=None, sz=15):
    return dict(paras=[[(v, {"b": hi, "c": ORANGE if hi else (SOFT if total else INK)})]], sz=sz, align="ctr",
                anchor="ctr", ml=0.04, mr=0.04, bottom=None, top=top, fill=PEACH if hi and not total else None)


N_P = [[35, 10, 5], [10, 20, 5], [5, 5, 10]]
count_rows = [[count_cell(str(v), hi=(i == 0 and j == 0)) for j, v in enumerate(r)] +
              [count_cell(str(sum(r)), hi=(i == 0), total=True)] for i, r in enumerate(N_P)]
count_rows.append([count_cell(str(sum(r[j] for r in N_P)), hi=(j == 0), total=True, top=DIVIDER) for j in range(3)] +
                  [count_cell("105", total=True, top=DIVIDER)])
table(s, L + 0.3, 2.0, [0.72, 0.72, 0.72, 0.84], [0.36] * 4, count_rows, name="Example counts")
text(s, L, 3.55, LW, 0.55, [["Row and column totals in grey; ", M(r"\hat{p}_{ij}", [TI("p", hat=True), CM("𝑖𝑗", sub=True)]), " = ", CM("𝑛"),
                            CM("𝑖𝑗", sub=True), " / 105."]], sz=12.5, color=SOFT, name="Counts note")
label(s, L, 4.1, LW, "Sensitivities of all nine cells", NAVY)
G_P = [["0.422", "−1.048", "−1.382"], ["−1.048", "0.758", "−1.134"], ["−1.382", "−1.134", "1.620"]]
g_rows = [[count_cell(v, hi=(i == 0 and j == 0), sz=14) for j, v in enumerate(r)] for i, r in enumerate(G_P)]
table(s, L + 0.3, 4.6, [0.95, 0.95, 0.95], [0.36] * 3, g_rows, name="Example sensitivities")
text(s, L, 5.75, LW, 0.75, [["Calculated from thesis Equation 4.41. Their weighted mean is zero."]], sz=12.5,
     color=SOFT, name="Sensitivities note")
RX = L + LW + 0.45                          # right column: steps
RW = L + W - RX
label(s, RX, 1.5, RW, "Cell (1, 1), step by step", ORANGE)
STEPS = [("1  Pointwise MI", r"\widehat\ell_{11}=\log\frac{35/105}{(50/105)(50/105)}=0.385", 0.62),
         ("2  MI and variance of pointwise MI",
          r"\widehat I=\sum_{i,j}\,\widehat p_{ij}\,\widehat\ell_{ij}=0.137,\qquad"
          r"\widehat V=\sum_{i,j}\,\widehat p_{ij}(\widehat\ell_{ij}-\widehat I)^2=0.272", 0.55),
         ("3  Row 1 mean (column 1 is the same, by symmetry)",
          r"\bar\ell_{1+}=\frac{35(0.385)+10(-0.511)+5(-0.644)}{50}=0.103", 0.62),
         ("4  Sensitivity",
          r"\widehat g_{11}=(0.385-0.137)^2-0.272+2(0.385-0.103-0.103+0.137)=0.422", 0.42)]
y = 1.98
for lab, eq, h in STEPS:
    text(s, RX, y, RW, 0.27, [[B(lab, c=SOFT)]], sz=13, name="Step label")
    equation(s, RX + 0.3, y + 0.27, RW - 0.3, h, eq, sz=17)
    y += 0.27 + h + 0.07
soft(s, RX, y + 0.02, RW, 6.85 - y - 0.02, "blue")
text(s, RX + 0.2, y + 0.08, RW - 0.4, 0.28, [[B("5  All nine cells", c=NAVY)]], sz=13, name="Step label")
equation(s, RX + 0.5, y + 0.4, RW - 0.7, 0.75,
         r"{\widehat\tau}^2=\sum_{i,j}\,\widehat p_{ij}\,\widehat g_{ij}^{\,2}=0.932,\qquad"
         r"\widehat\nu_P=\frac{2(105)(0.272)^2}{0.932}=16.65", sz=17)
footer(s, "Thesis Section 4.4.1 (Equation 4.47). Cell (1, 1) adds (35/105)(0.422)² = 0.059 to the sum in step 5. "
          "Results use unrounded values")
notes(s, backup_note(21))

# =================================================================== Slide 22: evaluation design
s = new_slide("Population construction, grid, and calculation requirements", 22)
backup_label(s, "Appendix · Evaluation design · for Slide 6")
soft(s, L, 1.2, W, 0.95, "peach", name="Construction panel")
text(s, L + 0.25, 1.2, 2.6, 0.95, [[B("Copying construction", c=ORANGE)]], sz=15, anchor="ctr",
     name="Construction label")
equation(s, 3.2, 1.22, 8.9, 0.91,
         r"p_{ij}(\lambda)=(1-\lambda)a_i a_j+\lambda a_i\mathbf 1\{i=j\},\qquad 0\leq\lambda<1", sz=23, jc="center")
mk = lambda r_: [CM("𝑚"), CM("𝑘", sub=True), (f"({r_})", {})]
label(s, L, 2.5, 5.95, "Parameter grid", ORANGE)
p = soft(s, L, 3.08, 5.95, 3.62, "peach")
panel_text(p, [
    {"runs": ["k = 2, 4, 8, 16; uniform, same-skew,", BR(), "or different-skew margins"], "bullet": True, "space_after": 14},
    {"runs": ["n = 10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000, 50,000 per group"], "bullet": True,
     "space_after": 14},
    {"runs": ["Same skew: both use "] + mk(0.8) + [".", BR(), "Different skew: P uses "] + mk(0.7) + [", Q uses "] +
     mk(0.8) + [",", BR(), "where "] + [CM("𝑚"), CM("𝑘", sub=True), CM("(𝜌) = (𝜌, (1 − 𝜌)/(𝑘 − 1), …)")],
     "bullet": True, "space_after": 14},
    {"runs": ["Null: shared MI 0.005, 0.02, 0.30.", BR(), "Power: ", CM("𝐼(𝑃)"), " = 0.02; ", CM("𝐼(𝑄)"), " = 0.025, 0.03, 0.04"], "bullet": True},
], sz=15.5, color=INK, anchor="ctr", margins=(0.28, 0.24, 0.2, 0.2))
label(s, 6.78, 2.5, 5.95, "Calculation requirements and rates", NAVY)
p = soft(s, 6.78, 3.08, 5.95, 3.62, "blue")
panel_text(p, [
    {"runs": ["Each null or power study has 360 settings,", BR(), "100,000 independent pairs per setting"], "bullet": True, "space_after": 14,
     "bullet_color": NAVY},
    {"runs": ["A Wald calculation needs a finite difference and a positive finite standard error. Expanded Welch "
              "also needs positive finite degrees of freedom."], "bullet": True, "space_after": 14, "bullet_color": NAVY},
    {"runs": ["Rate = rejections from successful calculations / all repetitions.", BR(),
              "Calculation success is reported separately."], "bullet": True, "bullet_color": NAVY},
], sz=15.5, color=INK, anchor="ctr", margins=(0.28, 0.24, 0.2, 0.2))
footer(s, "Thesis Chapter 5 and Appendix B.1–B.5")
notes(s, backup_note(22,
    extra="""Full requirements (Appendix B.3): a Wald calculation succeeds when it has a finite corrected difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14, and a finite p-value. The Expanded Welch calculation additionally requires positive finite component and combined degrees of freedom and a finite p-value; if either component fails, the Expanded Welch calculation is unsuccessful. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so the Expanded Welch calculation is unsuccessful even if the other table makes the shared standard error positive and finite. Zero and undefined component degrees of freedom are distinct cases; both fail the positive-finite requirement. A failed calculation is not evidence of equality.
Sampling is independent within and between populations, and both methods receive identical sampled pairs. The construction uses the same vector for row and column margins within each population and is one association family, not all categorical distributions.""",
    source="Thesis Chapter 5 and Appendix B.1–B.5; current grid results."))

# =================================================================== Slide 23: approximation ratios
s = new_slide("Approximation ratios across table sizes", 23)
backup_label(s, "Appendix · RQ1 · for Slide 7")
intro(s, [B("Different-skew margins, shared MI 0.02 nats; a ratio of one indicates agreement")])
pic(s, "B4_approximation_ratios", 0.6, 1.5, 12.1, 5.3)
footer(s, [("Rows as in thesis Figure 6.1. The variance checks use the true ", {"i": True}), CM("𝜏"),
           CM("2", sup=True), (" or the average estimated ", {"i": True}), CM("𝜏̂"), CM("2", sup=True),
           (" from 100,000 samples", {"i": True})])
notes(s, backup_note(23, opening="Colour now identifies table size; the rows are three different ratios."))

# =================================================================== Slide 24: near-independence noise
s = new_slide("Near-independence noise calculation", 24)
backup_label(s, "Appendix · RQ1 · for Slide 8")
intro(s, [B("Setting: 4×4, n = 1,000, MI 0.0001;  "), CM("𝑑 = 9"), B("  and  "), CM("𝜅 = 2𝑛𝐼(𝑃) ≈ 0.2")])
soft(s, L, 1.65, W, 1.15, "peach")
equation(s, 0.8, 1.7, 11.73, 1.05,
         r"G=2n\widehat I(P)\ \dot{\sim}\ \chi^2_d(\kappa),\qquad \widehat\nu_P\approx G/2", sz=24, jc="center")
text(s, L, 2.95, W, 0.35, [["In ", CM("𝐺"), ", ", M(r"\hat{I}(P)", [TI("I", hat=True), CM("(𝑃)")]), " is the uncorrected plug-in MI, not a "
                            "bias-corrected estimate."]], sz=13, color=SOFT, name="Plug-in note")
rows = [[head_cell("Quantity", color=ORANGE, align="l"), head_cell("Local prediction", color=ORANGE),
         head_cell("Observed (P)", color=ORANGE)]]
for q, a, b in [("Sample-based estimate (mean component df)", "4.60", "4.86"), ("Target (from sampling moments)", "9.00", "9.12"),
                ("Mean sample-based variance prediction / observed sampling variance", "1.96", "1.97")]:
    rows.append([dict(paras=[q], sz=16, color=INK, anchor="ctr"),
                 dict(paras=[a], sz=17, color=INK, align="ctr", anchor="ctr"),
                 dict(paras=[b], sz=17, color=INK, align="ctr", anchor="ctr")])
table(s, L, 3.55, [7.0, 2.56, 2.57], [0.55, 0.8, 0.8, 0.8], rows, name="Noise table")
footer(s, "Local approximations under fixed dimensions and positive limiting cell probabilities. Thesis Appendix A.2, "
          "Section 6.1.3")
notes(s, backup_note(24,
    extra="Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.",
))

# =================================================================== Slides 25-31: full grids, with the ordinary Welch comparison on 28
mk_b = lambda r_: [("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}), B(f"({r_})")]
OPENING = ("Colours here identify the {kind}, not the method: solid lines with filled circles are the Wald test, dashed "
           "lines with open squares are the Expanded Welch test. Lower strips show calculation success.")
# (physical slide, appendix group, title, intro, image, figure reference, notes)
grid_slides = [
    (25, "RQ2 · for Slide 9", "Full null results: uniform margins", [B("Equal MI in P and Q; uniform margins in both populations")],
     "B6_null_uniform", "Thesis Figure 6.4",
     "All 120 settings for the uniform profile. Slide 9 plots each setting here as one point; its 8.35% to 4.90% example is the 4×4, n = 20, MI 0.02 setting."),
    (26, "RQ2 · for Slide 9", "Full null results: same-skew margins", [B("Equal MI; same-skew margins ")] + mk_b(0.8) +
     [B(" in P and Q")], "B7_null_same_skew", "Thesis Figure 6.5", "All 120 settings for the same-skew profile."),
    (27, "RQ2 · for Slide 9", "Full null results: different-skew margins", [B("Equal MI; ")] + mk_b(0.7) + [B(" in P and ")] +
     mk_b(0.8) + [B(" in Q")], "B8_null_different_skew", "Thesis Figure 6.6",
     "All 120 settings for the different-skew profile. The Slide 10 diagnostic table uses the MI 0.02, n = 1,000 slice "
     "of these populations.\nAdditional anchor: " + PLAN_B[27]["anchor"]),
    (29, "RQ3 · for Slides 11–12", "Full power results: uniform margins", [B("Uniform margins; MI in P = 0.02 nats")], "B10_power_uniform",
     "Thesis Figure 6.7", "120 settings, 240 method rows for this margin profile."),
    (30, "RQ3 · for Slides 11–12", "Full power results: same-skew margins", [B("Same-skew margins ")] + mk_b(0.8) +
     [B(" in P and Q; MI in P = 0.02 nats")], "B11_power_same_skew", "Thesis Figure 6.8",
     "All 120 settings for the same-skew power profile."),
    (31, "RQ3 · for Slides 11–12", "Full power results: different-skew margins", mk_b(0.7) + [B(" in P, ")] + mk_b(0.8) +
     [B(" in Q; MI in P = 0.02 nats")], "B12_power_different_skew", "Thesis Figure 6.9",
     "120 settings, 240 method rows. The main point is 16×16, gap 0.01, n = 1,000.\n" + PLAN_B[31]["notes"]),
]


def ordinary_welch_slide():
    """Slide 28: thesis Section 6.2.5 and Table 6.2 (added in the final thesis)."""
    s = new_slide("Ordinary Welch degrees of freedom", 28)
    backup_label(s, "Appendix · RQ2 · for Slide 10")
    intro(s, ["Same statistic and sampled pairs; ordinary Welch gives each component ", CM("𝑛 − 1"),
              " degrees of freedom; shared MI 0.02 nats"])
    rows = [[head_cell("Setting", align="l"), head_cell("Wald"), head_cell("Ordinary Welch"),
             head_cell("Expanded Welch")]]
    for setting_, w_, o_, e_ in [("Uniform 4×4, n = 20", "8.35%", "7.35%", "4.90%"),
                                 ("Uniform 4×4, n = 50", "4.87%", "4.57%", "3.24%"),
                                 ("Different skew 16×16, n = 1,000", "26.01%", "25.95%", "24.84%")]:
        rows.append([dict(paras=[setting_], sz=15, color=INK, anchor="ctr")] +
                    [dict(paras=[v], sz=15, color=INK, align="ctr", anchor="ctr") for v in (w_, o_, e_)])
    table(s, L, 1.62, [4.6, 2.45, 2.5, 2.58], [0.5, 0.55, 0.55, 0.55], rows, name="Ordinary Welch table")
    text(s, L, 3.85, W, 0.3, [[("False-positive rates; nominal target 5%.", {"i": True})]], sz=12, color=SOFT,
         name="Table note")
    for i, (hd, bd) in enumerate([("n = 20", "Ordinary Welch reduces the excess less than Expanded Welch."),
                                  ("n = 50", "Wald is already close to 5%; Expanded Welch is the most conservative."),
                                  ("Different skew 16×16", "Neither choice removes the excess caused by bias.")]):
        panel(s, L + i * 4.12, 4.4, 3.89, 1.12, ["peach", "blue", "green"][i], heading=hd, body=[[bd]], bsz=14)
    accent(s, L, 5.85, W, 0.72, [B("Conclusion: "), "MI-specific degrees of freedom change the results,", BR(),
                                 "but a larger reduction in rejection does not consistently improve calibration."],
           sz=14.5, name="Conclusion")
    footer(s, "Same 100,000 sampled pairs per setting as the null study; every calculation succeeds. Thesis Section "
              "6.2.5, Table 6.2")
    notes(s, backup_note(28))


for k, grp, title, intro_runs, img, fig_ref, extra in grid_slides:
    s = new_slide(title, k)
    backup_label(s, f"Appendix · {grp}")
    intro(s, intro_runs)
    pic(s, img, 0.6, 1.5, 12.1, 5.3)
    footer(s, FOOT_RATE + "Requirements on Slide 22. " + fig_ref)
    notes(s, backup_note(k, extra=extra, opening=OPENING.format(kind="shared MI" if "null" in img else "MI gap")))
    if k == 27:
        ordinary_welch_slide()

# =================================================================== Slides 32-33: references
REFS1 = [
    [("Bossomaier, T., Barnett, L., Harré, M. and Lizier, J. T. (2016). ", {}),
     ("An Introduction to Transfer Entropy: Information Flow in Complex Systems", {"i": True}),
     (". Springer, Cham. doi:10.1007/978-3-319-43222-9", {})],
    [("Moddemeijer, R. (1989). On estimation of entropy and mutual information of continuous distributions. ", {}),
     ("Signal Processing", {"i": True}), (", 16(3), 233–248. doi:10.1016/0165-1684(89)90132-1", {})],
    [("Paninski, L. (2003). Estimation of entropy and mutual information. ", {}),
     ("Neural Computation", {"i": True}), (", 15(6), 1191–1253. doi:10.1162/089976603321780272", {})],
    [("Miller, G. A. (1955). Note on the bias of information estimates. In H. Quastler (Ed.), ", {}),
     ("Information Theory in Psychology: Problems and Methods", {"i": True}),
     (" (pp. 95–100). Free Press, Glencoe, Illinois.", {})],
    [("Mora, R. and Ruiz-Castillo, J. (2009). The statistical properties of the mutual information index of "
      "multigroup segregation. Working Paper, Economic Series (48), 09-84, Universidad Carlos III de Madrid, "
      "Departamento de Economía.", {})],
    [("Satterthwaite, F. E. (1946). An approximate distribution of estimates of variance components. ", {}),
     ("Biometrics Bulletin", {"i": True}), (", 2(6),", {}), BR(), ("110–114. doi:10.2307/3002019", {})],
    [("Welch, B. L. (1947). The generalization of “Student’s” problem when several different population "
      "variances are involved. ", {}), ("Biometrika", {"i": True}),
     (", 34(1–2), 28–35. doi:10.1093/biomet/34.1-2.28", {})],
]
REFS1.sort(key=lambda ref: ref[0][0])   # alphabetical by first author

REFS2 = [
    [("Chao, A. and Shen, T.-J. (2003). Nonparametric estimation of Shannon’s index of diversity when there are "
      "unseen species in sample. ", {}), ("Environmental and Ecological Statistics", {"i": True}),
     (", 10(4), 429–443. doi:10.1023/A:1026096204727", {})],
    [("Hutcheson, K. (1970). A test for comparing diversities based on the Shannon formula. ", {}),
     ("Journal of Theoretical Biology", {"i": True}), (", 29(1),", {}), BR(),
     ("151–154. doi:10.1016/0022-5193(70)90124-4", {})],
    [("Morris, T. P., White, I. R. and Crowther, M. J. (2019). Using simulation studies to evaluate statistical "
      "methods. ", {}), ("Statistics in Medicine", {"i": True}), (", 38(11), 2074–2102. doi:10.1002/sim.8086", {})],
    [("Nemenman, I., Shafee, F. and Bialek, W. (2002). Entropy and inference, revisited. In T. G. Dietterich, "
      "S. Becker and Z. Ghahramani (Eds.), ", {}),
     ("Advances in Neural Information Processing Systems 14", {"i": True}), (" (pp. 471–478). MIT Press.", {})],
    [("Pan, W. and Wall, M. M. (2002). Small-sample adjustments in using the sandwich variance estimator in "
      "generalized estimating equations. ", {}), ("Statistics in Medicine", {"i": True}),
     (", 21(10), 1429–1441. doi:10.1002/sim.1142", {})],
    [("Panzeri, S. and Treves, A. (1996). Analytical estimates of limited sampling biases in different information "
      "measures. ", {}), ("Network: Computation in Neural Systems", {"i": True}),
     (", 7(1), 87–107.", {}), BR(), ("doi:10.1088/0954-898X/7/1/006", {})],
    [("Wald, A. (1943). Tests of statistical hypotheses concerning several parameters when the number of "
      "observations is large. ", {}), ("Transactions of the American Mathematical Society", {"i": True}),
     (", 54(3), 426–482. doi:10.1090/S0002-9947-1943-0012401-3", {})],
]
for n, title, refs in [(32, "References: MI and testing foundations", REFS1),
                       (33, "References: related methods and evaluation", REFS2)]:
    s = new_slide(title, n)
    backup_label(s, "Appendix · References")
    half = (len(refs) + 1) // 2
    for c_, col in enumerate([refs[:half], refs[half:]]):
        text(s, L + c_ * 6.15, 1.3, 5.85, 5.5, [{"runs": r, "space_after": 12, "line": 1.05} for r in col], sz=14.5,
             color=INK, name=f"References column {c_ + 1}")
    notes(s, "Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.")



cp = prs.core_properties
cp.title = "Comparing Mutual Information in Finite Samples"
cp.subject = "Normal Wald and Expanded Welch–Satterthwaite comparisons of mutual information"
cp.author = "Daniel Zhao"
cp.last_modified_by = "Daniel Zhao"
cp.comments = ""
cp.keywords = "final"
cp.modified = datetime.datetime(2026, 11, 14)     # final version
prs.save(OUT)
import pptlib
for row in pptlib.EQUATION_LOG:
    if row[4] > 0.85:
        print("tight equation", row)
print("saved", OUT, len(prs.slides), "slides")
