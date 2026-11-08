"""Build the Welch MI presentation (replanned 5 November; lighter formatting pass) from a copy of the vF2 donor."""
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

import plan_notes
from pptlib import (BLACK, COVER_ORANGE, NAVY, ORANGE, WHITE, circle, emu, equation, fill_text_body, hline, notes,
                    panel_text, rect, set_title, shape_fill_line, slide_number, table, text, vline)

TEMPLATE, OUT, CHARTS, PLAN_PATH = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
PLAN, PLAN_B, PLAN_APPENDIX = plan_notes.load(PLAN_PATH)
TIMING = {1: ("0:25", "0:25"), 2: ("1:15", "1:40"), 3: ("1:00", "2:40"), 4: ("1:20", "4:00"), 5: ("1:40", "5:40"),
          6: ("1:20", "7:00"), 7: ("1:40", "8:40"), 8: ("1:40", "10:20"), 9: ("1:30", "11:50"),
          10: ("1:45", "13:35"), 11: ("1:30", "15:05"), 12: ("1:40", "16:45"), 13: ("1:05", "17:50"),
          14: ("1:00", "18:50")}

# ---------------------------------------------------------------- palette and type scale
INK = "262626"          # body text
SOFT = "555555"         # secondary text
FAINT = "8C8C8C"        # footers and quiet notes
PEACH = "FDF3EC"        # soft panel fills
SKY = "EDF2F8"
ORANGE_TINT = "F5C7AA"  # hairlines and outlines
NAVY_TINT = "B8C5D6"
RULE = "E3E3E3"
ARROW = "F2A77F"
EW_TEXT = "B4501A"      # darker orange for Expanded Welch labels on pale fills
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
    hline(s, x, y + 0.38, w, color=ORANGE_TINT if color == ORANGE else NAVY_TINT, width=1.0)


def soft(s, x, y, w, h, kind="peach", outline=None, name=None):
    return rect(s, x, y, w, h, fill=PEACH if kind == "peach" else SKY, line=outline, line_w=1.0, rounded=0.04,
                name=name)


def panel(s, x, y, w, h, kind="peach", heading=None, body=None, hsz=14.5, bsz=13.5, anchor="t",
          margins=(0.2, 0.18, 0.15, 0.12), outline=None, name=None):
    p = soft(s, x, y, w, h, kind, outline=outline, name=name)
    hcol = ORANGE if kind == "peach" else NAVY
    paras = []
    if heading:
        paras.append({"runs": [(heading, {"b": True, "c": hcol})], "sz": hsz, "space_after": 4})
    for b in body or []:
        paras.append({"runs": b, "sz": bsz, "space_after": 3, "line": 1.05})
    panel_text(p, paras, sz=bsz, color=INK, anchor=anchor, margins=margins)
    return p


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
    return text(s, 10.6, 0.12, 2.13, 0.28, [[(txt, {"b": True})]], sz=10.5, color=ORANGE, align="r",
                anchor="ctr", name="Backup label", margins=(0, 0.02, 0, 0))


def head_cell(txt, color=SOFT, align="ctr", sz=13, **kw):
    return dict(paras=[txt] if isinstance(txt, (str, list)) else txt, sz=sz, b=True, color=color, align=align,
                anchor="b", bottom=ORANGE, bottom_w=1.0, **kw)


# Final thesis (8 November) wording: Wald test, shared MI, calculation success, no Holm family.
NOTE_FIXES = [
    ("Normal Wald uses those estimates with a standard normal reference.",
     "The Wald test uses those estimates with a standard normal reference."),
    ("The null study uses three common MI values", "The null study uses three shared MI values"),
    ("Invalid calculations count as non-rejections, with validity tracked separately.",
     "Unsuccessful calculations count as non-rejections, with calculation success tracked separately."),
    ("only the common MI changes", "only the shared MI changes"),
    ("At common MI 0.02,", "At shared MI 0.02,"),
    ("At common MI 0.30,", "At shared MI 0.30,"),
    ("Both tests return valid results in every repetition in all three groups",
     "Both tests' calculations succeed in every repetition in all three groups"),
    ("Common MI changes both populations together", "Shared MI changes both populations together"),
    ("Every calculation is valid in these examples.", "Every calculation succeeds in these examples."),
    ("Both methods are valid in every repetition at the highlighted point.",
     "Both methods' calculations succeed in every repetition at the highlighted point."),
    ("Both methods reject equal MI, including after Holm adjustment across the six exploratory comparisons. "
     "Expanded Welch's adjusted p-value is about 0.00149.",
     "Both methods reject equal MI at the usual 0.05 threshold. Expanded Welch's p-value is about 0.0004."),
    (" Non-rejection does not establish equality, and Holm adjustment does not repair approximate p-values.",
     " Non-rejection does not establish equality."),
    ("Thesis Section 6.4, Tables 6.2–6.3, Appendix B.7 and application CSV; Sakar and Kastro (2018), Holm (1979).",
     "Thesis Section 6.4, Tables 6.3–6.4 and application CSV; Sakar and Kastro (2018). Month: Wald p = 4.71 × 10^-5; "
     "Expanded Welch p = 3.73 × 10^-4 with 26.79 degrees of freedom (unadjusted, two-sided)."),
    ("Invalid outputs count as non-rejections, so the rate measures the complete procedure; validity is reported "
     "separately. Conditioning on validity would describe a selected subset of sampled tables.",
     "Unsuccessful calculations count as non-rejections, so the rate measures the complete procedure; calculation "
     "success is reported separately. Conditioning on success would describe a selected subset of sampled tables."),
    ("Increasing common MI changes those patterns.", "Increasing shared MI changes those patterns."),
    ("the dependence on common MI remain visible", "the dependence on shared MI remain visible"),
    ("both 100% valid. This is a different common-MI level",
     "with every calculation successful in both tests. This is a different shared-MI level"),
]
FIX_USED = [0] * len(NOTE_FIXES)


def fix_notes(body):
    for i, (old, new) in enumerate(NOTE_FIXES):
        if old in body:
            body = body.replace(old, new)
            FIX_USED[i] += 1
    return body


def main_note(n, extra=None):
    """Speaker notes for main slide n; script, transition, cue and source are copied verbatim from the plan."""
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
    body = "Not part of the timed talk. Return to Slide 14 afterwards.\n\n"
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
lead(s, ["Mutual information measures how much observing one variable reduces uncertainty about another. ",
         O("Different sample estimates can arise from sampling noise.")])
soft(s, 3.67, 1.82, 6.0, 0.64, "peach", name="Hypothesis panel")
text(s, 3.92, 1.82, 1.7, 0.64, [[B("Null hypothesis", c=ORANGE)]], sz=13, anchor="ctr")
equation(s, 5.55, 1.82, 3.9, 0.64, r"H_0:I(P)=I(Q)", sz=22, jc="left")
label(s, L, 2.78, 5.7, "Online shoppers", ORANGE)
for y, grp, n_txt, est in [(3.4, "P: new visitors", "1,694 sessions", "0.0043 nats"),
                           (4.42, "Q: returning visitors", "10,551 sessions", "0.0179 nats")]:
    p = soft(s, L, y, 2.1, 0.8, "blue")
    panel_text(p, [{"runs": [B(grp, c=NAVY)], "sz": 14, "space_after": 1}, {"runs": [n_txt], "sz": 12, "color": SOFT}],
               anchor="ctr", margins=(0.15, 0.1, 0.04, 0.04))
    arrow(s, 2.83, y + 0.31)
    for r_ in range(4):
        for c_ in range(2):
            rect(s, 3.22 + c_ * 0.3, y + 0.08 + r_ * 0.16, 0.3, 0.16, fill="F9DCC9" if c_ == 0 else "FCEDE2",
                 line=WHITE, line_w=0.75)
    arrow(s, 3.97, y + 0.31)
    p = rect(s, 4.35, y, 1.8, 0.8, fill=WHITE, line=ORANGE_TINT, line_w=1.0, rounded=0.08)
    panel_text(p, [{"runs": ["corrected MI estimate"], "sz": 11, "color": SOFT}, {"runs": [B(est)], "sz": 16}],
               align="ctr", anchor="ctr", margins=(0.05, 0.05, 0.03, 0.03))
text(s, L, 5.45, 5.7, 0.35, [["Variables: month of visit and purchase outcome."]], sz=13.5, color=SOFT,
     name="Variables")
vline(s, 6.67, 2.85, 2.95, color="D0D0D0", width=1.0, dash="sysDot")
label(s, 7.03, 2.78, 5.7, "Statistical task", ORANGE)
steps = ["Draw a count table from each population", "Estimate MI from each table",
         "Assess whether sampling noise can explain the difference"]
for i, st in enumerate(steps):
    y = 3.4 + i * 0.84
    last = i == 2
    p = rect(s, 7.1, y, 5.63, 0.62, fill=ORANGE if last else WHITE, line=None if last else ORANGE_TINT, line_w=1.0,
             rounded=0.12)
    panel_text(p, [[B(st, c=WHITE if last else INK)]], sz=14, align="ctr", anchor="ctr",
               margins=(0.1, 0.1, 0.02, 0.02))
    if i < 2:
        arrow(s, 9.82, y + 0.645, w=0.2, h=0.16, down=True)
text(s, L, 6.2, W, 0.42, [[B("Does month–purchase MI differ between the populations?")]], sz=18, color=INK,
     name="Question")
footer(s, "Month × purchase tables (10×2); corrected MI estimates in nats. Data: Sakar and Kastro (2018). "
          "Bossomaier et al. (2016)")
notes(s, main_note(2))

# =================================================================== Slide 3
s = new_slide("Literature review: foundations and the MI-specific step", 3)
lead(s, ["Existing results provide MI estimates, a normal-reference comparison and moment matching. ",
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
                            "Assess the fixed normal cutoff in finite samples",
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
panel_text(p, [[B("Contribution: ", c=ORANGE), ("Derive that sensitivity and evaluate the resulting degrees of freedom.",
                                                 {"c": INK})]], sz=15.5, align="ctr", anchor="ctr",
           margins=(0.1, 0.1, 0.02, 0.02))
footer(s, "Thesis Sections 2.2–2.5 and 3.2–3.3; full references in B14–B15")
notes(s, main_note(3))

# =================================================================== Slide 4
s = new_slide("Method: one statistic, two reference distributions", 4)
lead(s, ["Both methods use ", O("the same estimated MI difference and standard error"),
         ". Expanded Welch uses estimated degrees of freedom for a Student t reference."])
soft(s, L, 1.95, 5.8, 1.95, "peach", name="Shared statistic panel")
text(s, 0.8, 2.04, 5.4, 0.3, [[B("Shared statistic", c=ORANGE)]], sz=14.5, margins=(0, 0, 0, 0))
equation(s, 0.7, 2.35, 5.6, 0.95,
         r"T=\frac{\widehat\Delta_{\mathrm{BC}}}{\widehat{\mathrm{SE}}},\qquad\widehat{\mathrm{SE}}^2=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}",
         sz=20, jc="center")
text(s, 0.8, 3.3, 5.45, 0.5, [[CM("Δ̂", i=False), CM("BC", sub=True, i=False), ": estimated ",
                               CM("𝐼(𝑃) − 𝐼(𝑄)"), ", after leading bias correction."]], sz=13, color=SOFT,
     anchor="ctr")
panel(s, L, 4.15, 2.8, 1.75, "blue", heading="Wald test",
      body=[["Standard normal distribution; two-sided 5% cutoff about ", B("±1.96"), "."]], hsz=15, bsz=14)
panel(s, 3.6, 4.15, 2.8, 1.75, "peach", heading="Expanded Welch test",
      body=[["Student t distribution with estimated degrees of freedom; ", B("a larger cutoff"), "."]], hsz=15, bsz=14)
pic(s, "slide04_reference_distributions", 6.8, 2.0, 5.9, 3.45)
text(s, 6.6, 5.55, 6.13, 0.55, [[("Student t distribution with 5 degrees of freedom, for illustration; cutoff about "
                                  "±2.57.", {"i": True})]], sz=12.5, color=SOFT, align="ctr", name="Plot label")
footer(s, "Thesis Chapters 3–4, Figure 2.1. Calculation requirements: Slide 6 and B3")
notes(s, main_note(4))

# =================================================================== Slide 5
s = new_slide("Approach and contribution", 5)
lead(s, ["Tracking how the pointwise-MI variance changes with the table gives the sampling-variance input for ",
         O("MI-specific degrees of freedom"), "."])
label(s, L, 1.82, W, "Derivation chain", ORANGE)
blocks = [("Cell probabilities change", [["Move a small amount of probability towards one cell."]], False),
          ("Margins and pointwise MI change", [["Track their joint effect."]], False),
          ("Variance sensitivity, derived here", [[CM("𝑔"), CM("𝑃", sub=True), CM("(𝑥, 𝑦)"),
                                                   " describes the change in ", CM("𝑉(𝑃)"), "."]], True),
          ("Degrees of freedom", [["Use the spread of those sensitivities."]], True)]
for i, (hd, bd, new) in enumerate(blocks):
    x = L + i * 3.13
    panel(s, x, 2.38, 2.75, 1.32, "peach", heading=hd, body=bd, hsz=14, bsz=13.5, anchor="ctr",
          margins=(0.16, 0.14, 0.08, 0.08), outline=ORANGE_TINT if new else None)
    if i < 3:
        arrow(s, x + 2.81, 2.95, w=0.26, h=0.2)
label(s, L, 3.98, W, "Result and approximations", NAVY)
soft(s, L, 4.52, 7.65, 2.1, "blue", name="Result panel")
equation(s, 0.7, 4.6, 7.45, 1.05,
         r"\operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P}\quad\Longrightarrow\quad\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}",
         sz=20, jc="center")
text(s, 0.85, 5.68, 7.2, 0.8, [[CM("𝜏"), CM("2", sup=True), CM("(𝑃)"), " is the variance of ", CM("𝑔"),
                                CM("𝑃", sub=True), CM("(𝑋, 𝑌)"), ". Repeat for Q and combine using Welch–Satterthwaite."]],
     sz=13.5, color=INK, anchor="ctr")
soft(s, 8.45, 4.52, 4.28, 2.1, "blue")
text(s, 8.68, 4.64, 3.9, 0.32, [[B("Two approximations evaluated", c=NAVY)]], sz=14.5, margins=(0, 0, 0, 0))
for i, lab in enumerate(["First-order sampling expansion", "Scaled chi-squared moment matching"]):
    y = 5.2 + i * 0.6
    circle(s, 8.7, y, 0.32, str(i + 1), NAVY, sz=11.5)
    text(s, 9.17, y - 0.07, 3.45, 0.46, [[lab]], sz=14, color=INK, anchor="ctr")
footer(s, "Thesis Sections 4.1–4.3; exact derivative in B1, moment matching in B2")
notes(s, main_note(5))

# =================================================================== Slide 6
s = new_slide("Evaluation design", 6)
lead(s, ["Known populations separate approximation accuracy, false positives and power. Both tests receive ",
         O("the same sampled table pairs"), "."])
label(s, L, 1.82, 5.85, "Research questions", NAVY)
soft(s, L, 2.38, 5.85, 3.3, "blue")
rq = [("RQ1: Approximation accuracy", ["Sampling moments of ", CM("𝑉̂"), " and component df, including near independence"]),
      ("RQ2: False positives", ["Equal MI at 0.005, 0.02 and 0.30 nats"]),
      ("RQ3: Power", ["P MI 0.02; MI-gap magnitudes 0.005, 0.01 and 0.02 nats"])]
for i, (lab, desc) in enumerate(rq):
    y = 2.6 + i * 1.0
    circle(s, 0.82, y + 0.04, 0.34, str(i + 1), NAVY, sz=12)
    text(s, 1.35, y - 0.03, 4.95, 0.95, [{"runs": [B(lab, c=NAVY)], "sz": 15, "space_after": 2},
                                        {"runs": desc, "sz": 13.5}], color=INK)
label(s, 6.88, 1.82, 5.85, "Shared simulation grid", ORANGE)
p = soft(s, 6.88, 2.38, 5.85, 3.3, "peach")
panel_text(p, [
    {"runs": ["Four sizes: 2×2, 4×4, 8×8, 16×16"], "bullet": True, "space_after": 6},
    {"runs": ["Uniform, same-skew and different-skew margins"], "bullet": True, "space_after": 6},
    {"runs": ["Ten sample sizes: 10 to 50,000 observations per population"], "bullet": True, "space_after": 6},
    {"runs": ["100,000 independent table pairs per setting"], "bullet": True, "space_after": 12},
    {"runs": [B("Model: "), "copying construction: choose margins and solve for target MI."]},
], sz=14.5, color=INK, anchor="ctr", margins=(0.28, 0.24, 0.14, 0.14))
accent(s, L, 5.95, W, 0.6, [B("Reporting: "), "usual 0.05 p-value thresholds. Unsuccessful calculations count as "
                                               "non-rejections; calculation success is reported separately."],
       color=NAVY, sz=14.5, name="Reporting")
footer(s, "Morris et al. (2019). Thesis Chapter 5, Tables 5.1–5.3; exact vectors, sample sizes and requirements in B3")
notes(s, main_note(6))

# =================================================================== Slide 7
s = new_slide("Results: approximation accuracy", 7)
lead(s, ["The mean of ", CM("𝑉̂"), " can ", O("remain inflated"),
         " even when its population first-order sampling-variance prediction is accurate."])
text(s, L, 1.8, 6.4, 0.3, [[B("Mean of "), CM("𝑉̂", b=True), B(" / population "), CM("𝑉", b=True)]], sz=13.5,
     color=INK, name="Top plot heading", margins=(0.03, 0.03, 0, 0))
pic(s, "slide07_mean_ratio", 0.55, 2.12, 6.4, 1.85)
text(s, L, 4.12, 6.4, 0.3, [[B("Predicted / observed sampling variance of "), CM("𝑉̂", b=True)]], sz=13.5,
     color=INK, name="Bottom plot heading", margins=(0.03, 0.03, 0, 0))
pic(s, "slide07_variance_ratio", 0.55, 4.44, 6.4, 2.15)
setting(s, "Different-skew P · 4×4 · population MI 0.02 nats", x=7.4, y=1.8, w=5.33)
panel(s, 7.4, 2.25, 5.33, 1.12, "peach", heading="Mean: rare cells can inflate it.",
      body=[["Newly observed rare cells can have large pointwise-MI deviations, whose squares raise ", CM("𝑉̂"),
             "."]])
panel(s, 7.4, 3.57, 5.33, 1.6, "blue", heading="Sampling variance: linearisation can miss large changes.",
      body=[["Rare cells appear in some samples and not others;", BR(), "sample-based sensitivities can also "
             "overpredict the resulting variation."]])
accent(s, 7.4, 5.42, 5.33, 0.72, [B("At n = 1,000: "), "mean ", B("19% high", c=ORANGE),
                                 "; population variance prediction ", B("3% low", c=ORANGE),
                                 ". Both moments enter the degrees of freedom."], sz=13.5)
footer(s, "Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2. Bands: approximate 95% Monte Carlo intervals. "
          "Other sizes and Q: B4")
notes(s, main_note(7))

# =================================================================== Slide 8
s = new_slide("Results: near independence", 8)
lead(s, ["Near independence, ", O("sampling noise keeps the mean estimated component degrees of freedom positive"),
         " while the population first-order value becomes very small."])
pic(s, "slide08_near_independence_df", 0.55, 1.85, 6.4, 4.7)
setting(s, "Different-skew P · 4×4 · n = 1,000 fixed", x=7.4, y=1.8, w=5.33)
panel(s, 7.4, 2.25, 5.33, 1.45, "blue", heading="Population first-order value",
      body=[["Insert known population inputs into the component formula. Near independence, its local value is "
             "approximately n × population MI."]])
panel(s, 7.4, 3.9, 5.33, 1.12, "peach", heading="Sample estimate",
      body=[["Quadratic sampling errors create apparent association, which remains in the sample-based calculation."]])
accent(s, 7.4, 5.2, 5.33, 0.98, [B("At MI 0.0001: "), "mean estimated component df ", B("≈4.9", c=ORANGE),
                                ";", BR(), "sampling-moment target ", B("≈9.1", c=NAVY), ";", BR(),
                                "population first-order value ", B("≈0.1")], sz=13.5)
footer(s, "Thesis Section 6.1.3, Figure 6.3; Appendix A.2. Bands: approximate 95% Monte Carlo intervals. "
          "Local calculation: B5")
notes(s, main_note(8))

# =================================================================== Slide 9
s = new_slide("Results: false positives across shared MI values", 9)
lead(s, ["A larger cutoff ", O("brings some excessive false-positive rates closer to 5%"),
         ", but accuracy at one association level does not persist across shared MI values."])
setting(s, "Uniform 4×4 · n = 20 per population · equal MI in P and Q")
pic(s, "slide09_null_bars", 0.55, 2.12, 6.3, 3.95)
text(s, L, 6.25, W, 0.4, [[B("Nominal target: 5%. "), "Both tests’ calculations succeed in every repetition in "
                                                     "these examples."]], sz=13, color=SOFT, name="Validity note")
panel(s, 7.4, 2.2, 5.33, 0.95, "peach", heading="Shared MI 0.02: closer to 5%",
      body=[["Expanded Welch lowers the rate from 8.35% to 4.90%."]], bsz=14)
panel(s, 7.4, 3.35, 5.33, 0.95, "blue", heading="Shared MI 0.30: still above 5%",
      body=[["Expanded Welch still rejects in 13.11% of repetitions."]], bsz=14)
accent(s, 7.4, 4.55, 5.33, 0.95, [B("Interpretation: "), "The larger cutoff reduces rejection, while the shared "
                                                        "statistic can still have the wrong sampling distribution."])
footer(s, "Slices of the balanced null grid. Whiskers: pointwise 95% Monte Carlo intervals. Thesis Section 6.2.1, "
          "Figure 6.4; full grids in B6–B8")
notes(s, main_note(9))

# =================================================================== Slide 10
s = new_slide("Results: why bias changes rejection", 10)
lead(s, ["Similar errors in estimated uncertainty accompany ", O("opposite false-positive behaviour"), BR(),
         "when bias in the MI difference changes."])
setting(s, "16×16 · n = 1,000 per population · equal MI 0.02 nats")
Rr = dict(sz=15, color=INK, anchor="ctr", align="ctr")
rows = [[head_cell("Margins", align="l"), head_cell("Variance ratio"), head_cell("Bias / SD"),
         head_cell("Wald"), head_cell("Expanded Welch")],
        [dict(paras=["Same skew"], sz=15, color=INK, anchor="ctr"), dict(paras=["1.93"], **Rr),
         dict(paras=["≈0"], **Rr), dict(paras=["0.60%"], **Rr), dict(paras=["0.53%"], **Rr)],
        [dict(paras=["Different skew"], sz=15, color=INK, anchor="ctr"), dict(paras=["1.94"], **Rr),
         dict(paras=[[B("2.06")]], **Rr), dict(paras=["26.01%"], **Rr), dict(paras=["24.84%"], **Rr)]]
table(s, L, 2.12, [3.0, 2.25, 2.05, 2.38, 2.45], [0.48, 0.52, 0.52], rows, name="Bias contrast")
text(s, L, 3.7, W, 0.32, [[("Variance ratio: average squared estimated standard error / observed variance of the "
                            "estimated MI difference.", {"i": True})]], sz=12, color=SOFT, name="Ratio definition")
panel(s, L, 4.25, 5.95, 1.1, "blue", heading="Same skew",
      body=[["The oversized denominator suppresses the statistic; expected MI biases cancel."]], hsz=15, bsz=14)
panel(s, 6.78, 4.25, 5.95, 1.1, "peach", heading="Different skew",
      body=[["The estimated difference is shifted away from zero by unequal residual biases."]], hsz=15, bsz=14)
accent(s, L, 5.65, W, 0.7, [B("Conclusion: ", c=NAVY), "Changing the cutoff leaves the biased estimated difference "
                                                       "unchanged.", BR(), "Both tests’ calculations succeed in every repetition here."],
       color=NAVY, sz=14.5, name="Conclusion")
footer(s, "Thesis Section 6.2.4, Table 6.1. Full different-skew grid: B8; ordinary Welch comparison: B9")
notes(s, main_note(10))

# =================================================================== Slide 11
s = new_slide("Results: power across MI differences", 11)
lead(s, ["With sufficient observations, ", O("larger MI differences become easier to detect"), ".", BR(),
         "Expanded Welch’s larger cutoff lowers or preserves rejection."])
setting(s, "Uniform 4×4 · population MI in P = 0.02 nats")
text(s, L, 2.08, 6.5, 0.3, [[B("MI-gap magnitude 0.01 nats: power against sample size")]], sz=13.5, color=INK,
     name="Plot heading", margins=(0.03, 0.03, 0, 0))
pic(s, "slide11_power_gap001", 0.55, 2.45, 6.5, 4.0)
label(s, 7.45, 2.05, 5.28, "Snapshot at n = 2,500", ORANGE)
rows = [[head_cell("MI-gap magnitude (nats)", sz=12.5), head_cell("Wald", color=NAVY, sz=12.5),
         head_cell("Expanded Welch", color=EW_TEXT, sz=12.5)]]
for gap, w_, e_ in [("0.005", "11.60%", "11.14%"), ("0.01", "31.85%", "31.14%"), ("0.02", "79.24%", "78.74%")]:
    f = PEACH if gap == "0.01" else None
    rows.append([dict(paras=[gap], sz=14.5, color=INK, align="ctr", anchor="ctr", fill=f),
                 dict(paras=[w_], sz=14.5, color=INK, align="ctr", anchor="ctr", fill=f),
                 dict(paras=[e_], sz=14.5, color=INK, align="ctr", anchor="ctr", fill=f)])
table(s, 7.45, 2.6, [2.0, 1.55, 1.73], [0.62, 0.46, 0.46, 0.46], rows, name="Snapshot table")
text(s, 7.45, 4.85, 5.28, 0.85, [{"runs": [B("Power: "), "probability of rejecting equal MI when population MI "
                                           "differs. Rates use the usual 0.05 p-value threshold."], "line": 1.05}],
     sz=14, color=INK, name="Power definition")
text(s, 7.45, 5.85, 5.28, 0.5, [[("Rates divide rejections by all 100,000 repetitions; unsuccessful calculations count as "
                                  "non-rejections.", {"i": True})]], sz=11.5, color=FAINT, name="Denominator note")
footer(s, "Bands: pointwise 95% Monte Carlo intervals. Thesis Section 6.3.1, Figure 6.7; full grids in B10–B12")
notes(s, main_note(11))

# =================================================================== Slide 12
s = new_slide("Results: bias can reverse the estimated direction", 12)
lead(s, ["In sparse tables, unequal residual biases can outweigh the true MI difference and ",
         O("reverse the estimated direction"), "."])
setting(s, "Different-skew 16×16 · MI 0.02 versus 0.03 nats")
text(s, L, 2.08, 6.5, 0.3, [[B("MI-gap magnitude 0.01 nats: power against sample size")]], sz=13.5, color=INK,
     name="Plot heading", margins=(0.03, 0.03, 0, 0))
pic(s, "slide12_direction_power", 0.55, 2.45, 6.5, 4.0)
label(s, 7.45, 2.05, 5.28, "At n = 1,000", NAVY)
for y, lab, val in [(2.6, "True difference, P minus Q", "−0.0100 nats"), (3.02, "Mean estimated difference",
                                                                         "+0.0207 nats")]:
    text(s, 7.45, y, 3.0, 0.38, [lab], sz=13.5, color=SOFT, anchor="ctr", margins=(0.03, 0, 0, 0))
    text(s, 10.45, y, 2.28, 0.38, [[B(val)]], sz=16, color=INK, align="r", anchor="ctr", margins=(0, 0.03, 0, 0))
hline(s, 7.45, 3.55, 5.28, color=RULE)
text(s, 7.45, 3.66, 5.28, 1.15, [{"runs": ["Expanded Welch rejects in ", B("9.66%"), " of repetitions."], "space_after": 4},
                                {"runs": [O("Among those rejections"), ", over 99.9% have the opposite estimated direction."]}],
     sz=14, color=INK, margins=(0.03, 0.03, 0, 0))
accent(s, 7.45, 4.75, 5.28, 0.72, [B("Mechanism: "), "As positive bias diminishes, the sampling centre passes near "
                                                     "zero, so rejection initially falls before recovering."], sz=13.5)
footer(s, "At n = 1,000: 9,659 of 9,662 Expanded Welch rejections are positive; every calculation succeeds. "
          "Thesis Figure 6.9; full grid in B12")
notes(s, main_note(12))

# =================================================================== Slide 13
s = new_slide("Illustration: online shopping data", 13)
lead(s, ["Returning visitors have higher estimated month–purchase MI, and ",
         O("both approximate tests reject equal MI"), "."])
soft(s, L, 1.92, 7.3, 3.3, "peach")
text(s, 0.85, 2.05, 6.9, 0.32, [[B("Month × purchase: corrected MI estimates (nats)", c=ORANGE)]], sz=14.5,
     margins=(0, 0, 0, 0))
text(s, 0.85, 2.55, 3.2, 0.3, ["New visitors"], sz=13, color=SOFT, margins=(0, 0, 0, 0))
text(s, 0.85, 2.82, 3.2, 0.7, [[B("0.0043")]], sz=34, color=INK, margins=(0, 0, 0, 0))
text(s, 4.3, 2.55, 3.4, 0.3, ["Returning visitors"], sz=13, color=SOFT, margins=(0, 0, 0, 0))
text(s, 4.3, 2.82, 3.4, 0.7, [[B("0.0179")]], sz=34, color=INK, margins=(0, 0, 0, 0))
text(s, 0.85, 3.72, 6.8, 0.3, ["Two-sided p-values"], sz=13, color=SOFT, margins=(0, 0, 0, 0))
text(s, 0.85, 4.02, 3.4, 0.38, [[B("Wald ", c=NAVY), "4.71 × 10", ("−5", {"sup": True})]], sz=15, color=INK,
     margins=(0, 0, 0, 0))
text(s, 4.3, 4.02, 3.5, 0.38, [[B("Expanded Welch ", c=EW_TEXT), "3.73 × 10", ("−4", {"sup": True})]], sz=15,
     color=INK, margins=(0, 0, 0, 0))
hline(s, 0.85, 4.62, 6.8, color=ORANGE_TINT)
text(s, 0.85, 4.68, 6.8, 0.5, [[B("Both tests reject equal MI at the 0.05 threshold.")]], sz=13.5, color=INK,
     anchor="ctr", margins=(0, 0, 0, 0))
soft(s, 8.1, 1.92, 4.63, 3.3, "blue")
text(s, 8.35, 2.05, 4.2, 0.32, [[B("Weekend × purchase", c=NAVY)]], sz=14.5, margins=(0, 0, 0, 0))
text(s, 8.35, 2.55, 1.9, 0.3, ["New visitors"], sz=13, color=SOFT, margins=(0, 0, 0, 0))
text(s, 8.35, 2.82, 1.9, 0.7, [[B("0.0007")]], sz=34, color=INK, margins=(0, 0, 0, 0))
text(s, 10.25, 2.55, 2.3, 0.3, ["Returning visitors"], sz=13, color=SOFT, margins=(0, 0, 0, 0))
text(s, 10.25, 2.82, 2.3, 0.7, [[B("0.0007")]], sz=34, color=INK, margins=(0, 0, 0, 0))
text(s, 8.35, 3.72, 4.2, 0.3, ["Two-sided p-values"], sz=13, color=SOFT, margins=(0, 0, 0, 0))
text(s, 8.35, 4.02, 1.9, 0.38, [[B("Wald ", c=NAVY), "0.9554"]], sz=15, color=INK, margins=(0, 0, 0, 0))
text(s, 10.25, 4.02, 2.3, 0.38, [[B("Expanded Welch ", c=EW_TEXT), "0.9601"]], sz=15, color=INK,
     margins=(0, 0, 0, 0))
hline(s, 8.35, 4.62, 4.13, color=NAVY_TINT)
text(s, 8.35, 4.68, 4.13, 0.5, [[B("Estimates are close; neither test rejects equality.")]], sz=13.5, color=INK,
     anchor="ctr", margins=(0, 0, 0, 0))
accent(s, L, 5.6, W, 0.6, [B("Interpretation: "), "Population MI is unknown. The simulations provide the evidence "
                                                   "about reliability."], sz=14.5)
footer(s, "Sakar and Kastro (2018): 1,694 new and 10,551 returning sessions. Thesis Section 6.4, Tables 6.3–6.4; "
          "details in B13")
notes(s, main_note(13))

# =================================================================== Slide 14
s = new_slide("Conclusions and next steps", 14)
lead(s, ["MI-specific degrees of freedom improve some false-positive rates, while remaining failures identify ",
         O("estimation accuracy as a priority"), "."])
label(s, L, 1.82, W, "Contribution and findings", NAVY)
finds = [["Derived variance sensitivity and", BR(), "MI-specific degrees of freedom."],
         ["Brought some excessive", BR(), "false-positive rates closer to 5%;", BR(), "deepened conservatism elsewhere."],
         ["Reduced nominal power; residual bias can reverse the estimated direction."]]
for i, runs in enumerate(finds):
    x = L + i * 4.12
    soft(s, x, 2.38, 3.89, 1.72, "blue")
    circle(s, x + 3.89 / 2 - 0.18, 2.55, 0.36, str(i + 1), NAVY, sz=12)
    text(s, x + 0.25, 3.0, 3.39, 1.0, [runs], sz=15, color=NAVY, align="ctr", anchor="ctr")
label(s, L, 4.4, W, "Next steps", ORANGE)
nexts = [["Improve bias and uncertainty estimates, including quadratic variation near independence."],
         ["Test other association constructions", BR(), "and unequal sample sizes."]]
for i, runs in enumerate(nexts):
    x = L + i * 6.165
    soft(s, x, 4.95, 5.965, 0.85, "peach")
    circle(s, x + 0.22, 5.205, 0.34, str(i + 1), ORANGE, sz=12)
    text(s, x + 0.75, 4.97, 5.05, 0.81, [runs], sz=14.5, color=INK, anchor="ctr")
text(s, L, 6.25, W, 0.4, ["Thank you."], sz=16, color=SOFT, align="ctr", name="Thank you")
BACKUP_INDEX = """BACKUP INDEX (type the slide number, press Enter, then return to 14)
15  Appendix title
16  B1  Variance sensitivity
17  B2  Moment matching and combined degrees of freedom
18  B3  Population construction, grid and calculation requirements
19  B4  Approximation ratios across table sizes
20  B5  Near-independence noise calculation
21  B6  Full null results: uniform margins
22  B7  Full null results: same-skew margins
23  B8  Full null results: different-skew margins
24  B9  Ordinary Welch degrees of freedom
25  B10 Full power results: uniform margins
26  B11 Full power results: same-skew margins
27  B12 Full power results: different-skew margins
28  B13 Application details
29  B14 References: MI and testing foundations
30  B15 References: related methods and evaluation"""
notes(s, main_note(14, extra=BACKUP_INDEX))

# =================================================================== Appendix title (15)
s = prs.slides.add_slide(LAYOUT)
for ph in list(s.placeholders):
    ph._element.getparent().remove(ph._element)
text(s, 0.5, 0.6, 12.33, 6.3, [[B("Appendix")]], sz=48, color=NAVY, align="ctr", anchor="ctr", name="Appendix title")
slide_number(s, 15)
notes(s, "Appendix title. Not part of the timed talk.\n\nDELIVERY\n" + PLAN_APPENDIX)

# =================================================================== B1 (16)
s = new_slide("Variance sensitivity", 16)
backup_label(s, "Backup B1")
text(s, L, 1.08, 3.55, 0.55, [[B("Perturbation towards one cell:")]], sz=16, color=INK, anchor="ctr")
equation(s, 4.15, 1.08, 6.5, 0.55, r"P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}", sz=20)
soft(s, L, 1.85, W, 2.85, "peach")
equation(s, 3.95, 1.98, 8.6, 0.75, r"g_P(x,y)=\{\ell_P(x,y)-I(P)\}^2-V(P)", sz=22)
equation(s, 3.95, 2.78, 8.6, 0.75, r"\qquad+2\bigl[\ell_P(x,y)-\mathbb E_P\{\ell_P(X,Y)\mid X=x\}", sz=22)
equation(s, 3.95, 3.58, 8.6, 0.75, r"\qquad\qquad-\mathbb E_P\{\ell_P(X,Y)\mid Y=y\}+I(P)\bigr]", sz=22)
text(s, 0.82, 1.98, 3.0, 0.75, [[O("Changing probability weights")]], sz=15, anchor="ctr")
text(s, 0.82, 2.85, 3.0, 1.45, [[O("Changing pointwise-MI values and margins")]], sz=15, anchor="ctr")
vline(s, 3.85, 2.9, 1.35, color=ORANGE_TINT, width=1.5)
text(s, L, 5.0, 3.3, 0.55, ["Pointwise MI:"], sz=16, color=INK, anchor="ctr")
equation(s, 3.95, 5.0, 7.5, 0.55, r"\ell_P(i,j)=\log\{p_{ij}/(p_{i+}p_{+j})\}", sz=20)
text(s, L, 5.7, 3.3, 0.55, ["Sensitivity variance:"], sz=16, color=INK, anchor="ctr")
equation(s, 3.95, 5.7, 7.5, 0.55, r"\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}", sz=20)
footer(s, "Exact for positive population tables; its use for sampling errors is first order. Thesis Chapter 4")
notes(s, backup_note(1,
    extra="Regularity assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. With every cell positive, positive MI is equivalent to positive V (Appendix A.3), but positive V does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.",
    source="Thesis Chapter 4: perturbation path (eq:contamination-path), final form of g (eq:g-final) and definition of "
           "tau-squared (eq:tau-definition). This derivative is exact for positive population tables. Its use for "
           "sampling errors is first order."))

# =================================================================== B2 (17)
s = new_slide("Moment matching and combined degrees of freedom", 17)
backup_label(s, "Backup B2")
label(s, L, 1.15, W, "Component degrees of freedom", ORANGE)
soft(s, L, 1.7, W, 1.55, "peach")
equation(s, 0.8, 1.72, 11.73, 1.51,
         r"\nu_{P,\mathrm{mom}}=\frac{2[\mathbb E\{\widehat V(P)\}]^2}{\operatorname{Var}\{\widehat V(P)\}},\qquad\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}",
         sz=22, jc="center")
label(s, L, 3.55, W, "Combined degrees of freedom", NAVY)
soft(s, L, 4.1, W, 1.55, "blue")
equation(s, 0.8, 4.12, 11.73, 1.51,
         r"\widehat\nu=\frac{\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\}^2}{\{\widehat V(P)/n_P\}^2/\widehat\nu_P+\{\widehat V(Q)/n_Q\}^2/\widehat\nu_Q}",
         sz=22, jc="center")
text(s, L, 5.95, W, 0.5, ["Moment matching does not establish the normality or independence needed for an exact "
                          "Student t distribution."], sz=15, color=SOFT, name="Caveat")
footer(s, "Satterthwaite (1946). Thesis Sections 4.1 and 4.3")
notes(s, backup_note(2))

# =================================================================== B3 (18)
s = new_slide("Population construction, grid and calculation requirements", 18)
backup_label(s, "Backup B3")
soft(s, L, 1.15, W, 0.82, "peach")
equation(s, 0.8, 1.17, 11.73, 0.78,
         r"p_{ij}(\lambda)=(1-\lambda)a_i a_j+\lambda a_i\mathbf 1\{i=j\},\qquad 0\leq\lambda<1", sz=21, jc="center")
mk = lambda r_: [CM("𝑚"), CM("𝑘", sub=True), (f"({r_})", {})]
label(s, L, 2.22, 5.95, "Parameter grid", ORANGE)
p = soft(s, L, 2.78, 5.95, 2.85, "peach")
panel_text(p, [
    {"runs": ["k = 2, 4, 8, 16; uniform, same-skew or different-skew margins"], "bullet": True, "space_after": 6},
    {"runs": ["Same skew: both use "] + mk(0.8) + [". Different skew: P uses "] + mk(0.7) + [", Q uses "] + mk(0.8) +
     [", where "] + [CM("𝑚"), CM("𝑘", sub=True), CM("(𝜌) = (𝜌, (1 − 𝜌)/(𝑘 − 1), …)")],
     "bullet": True, "space_after": 6},
    {"runs": ["Null: shared MI 0.005, 0.02, 0.30. Power: P MI 0.02, Q MI 0.025, 0.03, 0.04"], "bullet": True},
], sz=13.5, color=INK, anchor="ctr", margins=(0.24, 0.2, 0.12, 0.12))
label(s, 6.78, 2.22, 5.95, "Calculation requirements and rates", NAVY)
p = soft(s, 6.78, 2.78, 5.95, 2.85, "blue")
panel_text(p, [
    {"runs": ["Each study has 360 settings,", BR(), "100,000 independent pairs per setting"], "bullet": True, "space_after": 6,
     "bullet_color": NAVY},
    {"runs": ["A Wald calculation needs a finite difference and a positive finite standard error. Expanded Welch "
              "also needs positive finite degrees of freedom."], "bullet": True, "space_after": 6, "bullet_color": NAVY},
    {"runs": ["Rate = rejections from successful calculations / all repetitions. Calculation success is reported "
              "separately."], "bullet": True, "bullet_color": NAVY},
], sz=13.5, color=INK, anchor="ctr", margins=(0.24, 0.2, 0.12, 0.12))
text(s, L, 5.9, W, 0.45, [[B("n = "), "10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000, 50,000 per group"]],
     sz=15, color=INK, anchor="ctr", name="Sample sizes")
footer(s, "Thesis Chapter 5 and Appendix B.1–B.5")
notes(s, backup_note(3,
    extra="""Full requirements (Appendix B.3): a Wald calculation succeeds when it has a finite corrected difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14 and a finite p-value. The Expanded Welch calculation additionally requires positive finite component and combined degrees of freedom and a finite p-value; if either component fails, the Expanded Welch calculation is unsuccessful. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so the Expanded Welch calculation is unsuccessful even if the other table makes the shared standard error positive and finite. Zero and undefined component degrees of freedom are distinct cases; both fail the positive-finite requirement. A failed calculation is not evidence of equality.
Sampling is independent within and between populations, and both methods receive identical sampled pairs. The construction uses the same vector for row and column margins within each population and is one association family, not all categorical distributions.""",
    source="Thesis Chapter 5 and Appendix B.1–B.5; current grid results."))

# =================================================================== B4 (19)
s = new_slide("Approximation ratios across table sizes", 19)
backup_label(s, "Backup B4")
intro(s, [B("Different-skew margins, shared MI 0.02 nats; a ratio of one indicates agreement")])
pic(s, "B4_approximation_ratios", 0.6, 1.5, 12.1, 5.3)
footer(s, [("Rows: mean of ", {"i": True}), CM("𝑉̂"), (" / ", {"i": True}), CM("𝑉"),
           ("; population-input and sample-based variance predictions / observed variance. Thesis Figure 6.1",
            {"i": True})])
notes(s, backup_note(4, opening="Colour now identifies table size; the rows are three different ratios."))

# =================================================================== B5 (20)
s = new_slide("Near-independence noise calculation", 20)
backup_label(s, "Backup B5")
intro(s, [B("Setting: 4×4, n = 1,000, MI 0.0001;  "), CM("𝑑 = 9"), B("  and  "), CM("𝜅 = 2𝑛𝐼(𝑃) ≈ 0.2")])
soft(s, L, 1.6, W, 1.0, "peach")
equation(s, 0.8, 1.62, 11.73, 0.96,
         r"G=2n\widehat I(P)\ \dot{\sim}\ \chi^2_d(\kappa),\qquad \widehat\nu_P\approx G/2", sz=22, jc="center")
text(s, L, 2.72, W, 0.35, [["In ", CM("𝐺"), ", ", CM("𝐼̂(𝑃)"), " is the uncorrected plug-in MI, not a "
                            "bias-corrected estimate."]], sz=13, color=SOFT, name="Plug-in note")
rows = [[head_cell("Quantity", color=ORANGE, align="l"), head_cell("Local prediction", color=ORANGE),
         head_cell("Observed (P)", color=ORANGE)]]
for q, a, b in [("Mean estimated component df", "4.60", "4.86"), ("Sampling-moment target", "9.00", "9.12"),
                ("Mean sample-based variance prediction / observed sampling variance", "1.96", "1.97")]:
    rows.append([dict(paras=[q], sz=15, color=INK, anchor="ctr"),
                 dict(paras=[a], sz=16, color=INK, align="ctr", anchor="ctr"),
                 dict(paras=[b], sz=16, color=INK, align="ctr", anchor="ctr")])
table(s, L, 3.35, [7.0, 2.56, 2.57], [0.5, 0.6, 0.6, 0.6], rows, name="Noise table")
footer(s, "Local approximations under fixed dimensions and positive limiting cell probabilities. Thesis Appendix A.2, "
          "Section 6.1.3")
notes(s, backup_note(5,
    extra="Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.",
))

# =================================================================== B6-B12 (21-27), with B9 ordinary Welch
mk_b = lambda r_: [("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}), B(f"({r_})")]
OPENING = ("Colours here identify the {kind}, not the method: solid lines with filled circles are the Wald test, dashed "
           "lines with open squares are the Expanded Welch test. Lower strips show calculation success.")
# (backup number, plan key, title, intro, image, figure reference, notes)
grid_slides = [
    (6, 6, "Full null results: uniform margins", [B("Equal MI in P and Q; uniform margins in both populations")],
     "B6_null_uniform", "Thesis Figure 6.4",
     "All 120 settings for the uniform profile. Slide 9 used the 4×4, n = 20 slice of this page."),
    (7, 7, "Full null results: same-skew margins", [B("Equal MI; same-skew margins ")] + mk_b(0.8) +
     [B(" in P and Q")], "B7_null_same_skew", "Thesis Figure 6.5", "All 120 settings for the same-skew profile."),
    (8, 8, "Full null results: different-skew margins", [B("Equal MI; ")] + mk_b(0.7) + [B(" in P and ")] +
     mk_b(0.8) + [B(" in Q")], "B8_null_different_skew", "Thesis Figure 6.6",
     "All 120 settings for the different-skew profile. The Slide 10 diagnostic table uses the MI 0.02, n = 1,000 slice "
     "of these populations.\nAdditional anchor: " + PLAN_B[8]["anchor"]),
    (10, 9, "Full power results: uniform margins", [B("Uniform margins; MI in P = 0.02 nats")], "B10_power_uniform",
     "Thesis Figure 6.7", "120 settings, 240 method rows for this margin profile."),
    (11, 10, "Full power results: same-skew margins", [B("Same-skew margins ")] + mk_b(0.8) +
     [B(" in P and Q; MI in P = 0.02 nats")], "B11_power_same_skew", "Thesis Figure 6.8",
     "All 120 settings for the same-skew power profile."),
    (12, 11, "Full power results: different-skew margins", mk_b(0.7) + [B(" in P, ")] + mk_b(0.8) +
     [B(" in Q; MI in P = 0.02 nats")], "B12_power_different_skew", "Thesis Figure 6.9",
     "120 settings, 240 method rows. The main point is 16×16, gap 0.01, n = 1,000.\n" + PLAN_B[11]["notes"]),
]


def ordinary_welch_slide():
    """B9: thesis Section 6.2.5 and Table 6.2 (added in the final thesis)."""
    s = new_slide("Ordinary Welch degrees of freedom", 24)
    backup_label(s, "Backup B9")
    intro(s, ["Same statistic and sampled pairs; ordinary Welch gives each component ", CM("𝑛 − 1"),
              " degrees of freedom; shared MI 0.02 nats"])
    rows = [[head_cell("Setting", align="l"), head_cell("Wald", color=NAVY), head_cell("Ordinary Welch"),
             head_cell("Expanded Welch", color=EW_TEXT)]]
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
        panel(s, L + i * 4.12, 4.4, 3.89, 1.12, "peach", heading=hd, body=[[bd]], bsz=14)
    accent(s, L, 5.85, W, 0.72, [B("Conclusion: ", c=NAVY), "MI-specific degrees of freedom change the results,", BR(),
                                 "but a larger reduction in rejection does not consistently improve calibration."],
           color=NAVY, sz=14.5, name="Conclusion")
    footer(s, "Same 100,000 sampled pairs per setting as the null study; every calculation succeeds. Thesis Section "
              "6.2.5, Table 6.2")
    notes(s, backup_note(None,
        question="Would ordinary Welch degrees of freedom work as well as the MI-specific calculation?",
        answer="“Ordinary Welch keeps the same estimated MI difference, standard error and statistic, but gives each "
               "component n minus one degrees of freedom, the rule for comparing sample means. For MI that is only a "
               "benchmark, because it ignores how the pointwise-MI variance estimate changes with the table. At n = 20 "
               "it removes less of the excess than Expanded Welch. At n = 50, where Wald is already close to 5%, "
               "Expanded Welch becomes the most conservative. In the biased 16×16 case neither choice removes the "
               "excess. So the MI-specific calculation changes the results, but a larger reduction in rejection does "
               "not consistently improve calibration.”",
        extra="The three settings reuse the main null study's 100,000 sampled pairs per setting at shared MI 0.02 nats "
              "with n_P = n_Q = n; all three methods' calculations succeed in every repetition. The thesis examines "
              "ordinary Welch only at these illustrative settings and lists this as a limitation (Section 7.2); the "
              "main comparison is with the Wald test.",
        source="Thesis Section 6.2.5, Table 6.2; Section 7.2."))


for k, plan_k, title, intro_runs, img, fig_ref, extra in grid_slides:
    s = new_slide(title, k + 15)
    backup_label(s, f"Backup B{k}")
    intro(s, intro_runs)
    pic(s, img, 0.6, 1.5, 12.1, 5.3)
    footer(s, FOOT_RATE + "Requirements in B3. " + fig_ref)
    notes(s, backup_note(plan_k, extra=extra, opening=OPENING.format(kind="shared MI" if "null" in img else "MI gap")))
    if k == 8:
        ordinary_welch_slide()

# =================================================================== B13 (28) application details
s = new_slide("Application details", 28)
backup_label(s, "Backup B13")
intro(s, ["Online Shoppers Purchasing Intention data; new (P) versus returning (Q) visitors; two-sided p-values"])


def sci(m_, e):
    return [m_ + " × 10", (f"−{e}", {"sup": True})]


label(s, L, 1.5, W, "Corrected MI estimates (nats)", ORANGE)
num = dict(sz=15, color=INK, align="ctr", anchor="ctr")
rows = [[head_cell("Predictor", align="l"), head_cell("New visitors"), head_cell("Returning visitors"),
         head_cell("Difference"), head_cell("Standard error"), head_cell("Statistic T")]]
for pr, vals in [("Month", ["0.004316", "0.017880", "−0.013563", "0.003333", "−4.069"]),
                 ("Weekend", ["0.000664", "0.000727", "−0.000063", "0.001124", "−0.056"])]:
    rows.append([dict(paras=[pr], sz=15, color=INK, anchor="ctr")] + [dict(paras=[v], **num) for v in vals])
table(s, L, 2.0, [2.3, 2.0, 2.0, 2.0, 2.0, 1.83], [0.45, 0.5, 0.5], rows, name="Estimates table")
label(s, L, 3.68, W, "Test results", NAVY)
rows = [[head_cell("Predictor", align="l"), head_cell("Expanded Welch degrees of freedom"),
         head_cell("Wald p-value", color=NAVY), head_cell("Expanded Welch p-value", color=EW_TEXT)]]
for pr, df_, w_, e_ in [("Month", "26.79", sci("4.71", 5), sci("3.73", 4)),
                        ("Weekend", "2.18", ["0.9554"], ["0.9601"])]:
    rows.append([dict(paras=[pr], sz=15, color=INK, anchor="ctr"), dict(paras=[df_], **num),
                 dict(paras=[w_], **num), dict(paras=[e_], **num)])
table(s, L, 4.18, [2.3, 3.3, 3.2, 3.33], [0.45, 0.5, 0.5], rows, name="Tests table")
text(s, L, 5.85, W, 0.85, [{"runs": ["Month tables are 10×2 (no January or April sessions) and weekend tables are 2×2. "
                                     "The leading correction subtracts 9/(2n) from each month estimate and 1/(2n) "
                                     "from each weekend estimate."], "line": 1.05}], sz=13.5, color=SOFT,
     name="Table note")
footer(s, "Sakar and Kastro (2018): 1,694 new and 10,551 returning sessions; 85 Other sessions excluded. Thesis "
          "Section 6.4, Tables 6.3–6.4")
notes(s, backup_note(None,
    question="How were the shopping comparisons set up, and why are the weekend degrees of freedom so small?",
    answer="“I compare month–purchase and weekend–purchase MI between new and returning visitors, treating the two "
           "visitor groups as independent samples. For month, the corrected difference is about 4.07 standard errors "
           "from zero, so both tests reject equal MI. For weekend, both estimates are about 0.0007 nats and the "
           "statistic is close to zero, so neither test rejects; that does not establish equality. The weekend degrees "
           "of freedom are only 2.18 despite the large samples because both variance estimates fluctuate a lot "
           "relative to their size.”",
    extra="""Dataset: 12,330 sessions, each from a different user according to its documentation. P: 1,694 sessions labelled New_Visitor; Q: 10,551 labelled Returning_Visitor; the 85 Other sessions are excluded. Outcome: the Boolean Revenue variable.
Month: January and April have no recorded sessions, so each table is 10×2. All ten months occur in both groups, although the new-visitor February row contains one session and no purchase. Zero cells are retained without adding artificial counts.
Component degrees of freedom: month 12.93 (new) and 187.93 (returning), combined 26.79; weekend 1.69 (new) and 7.71 (returning), combined 2.18.
The final thesis reports unadjusted two-sided p-values for these two comparisons only; it no longer includes a multiple-comparison family or Holm adjustment.""",
    source="Thesis Section 6.4, Tables 6.3–6.4; application CSV; Sakar and Kastro (2018)."))

# =================================================================== B14-B15 (29-30)
REFS1 = [
    [("Bossomaier, T., Barnett, L., Harré, M. and Lizier, J. T. (2016). ", {}),
     ("An Introduction to Transfer Entropy: Information Flow in Complex Systems", {"i": True}),
     (". Springer, Cham. doi:10.1007/978-3-319-43222-9", {})],
    [("Moddemeijer, R. (1989). On estimation of entropy and mutual information of continuous distributions. ", {}),
     ("Signal Processing", {"i": True}), (", 16(3), 233–248. doi:10.1016/0165-1684(89)90132-1", {})],
    [("Paninski, L. (2003). Estimation of entropy and mutual information. ", {}),
     ("Neural Computation", {"i": True}), (", 15(6), 1191–1253. doi:10.1162/089976603321780272", {})],
    [("Mora, R. and Ruiz-Castillo, J. (2009). The statistical properties of the mutual information index of "
      "multigroup segregation. Working Paper, Economic Series (48), 09-84, Universidad Carlos III de Madrid, "
      "Departamento de Economía.", {})],
    [("Satterthwaite, F. E. (1946). An approximate distribution of estimates of variance components. ", {}),
     ("Biometrics Bulletin", {"i": True}), (", 2(6), 110–114. doi:10.2307/3002019", {})],
    [("Welch, B. L. (1947). The generalization of “Student’s” problem when several different population "
      "variances are involved. ", {}), ("Biometrika", {"i": True}),
     (", 34(1–2), 28–35. doi:10.1093/biomet/34.1-2.28", {})],
]
REFS2 = [
    [("Hutcheson, K. (1970). A test for comparing diversities based on the Shannon formula. ", {}),
     ("Journal of Theoretical Biology", {"i": True}), (", 29(1), 151–154. doi:10.1016/0022-5193(70)90124-4", {})],
    [("Morris, T. P., White, I. R. and Crowther, M. J. (2019). Using simulation studies to evaluate statistical "
      "methods. ", {}), ("Statistics in Medicine", {"i": True}), (", 38(11), 2074–2102. doi:10.1002/sim.8086", {})],
    [("Pan, W. and Wall, M. M. (2002). Small-sample adjustments in using the sandwich variance estimator in "
      "generalized estimating equations. ", {}), ("Statistics in Medicine", {"i": True}),
     (", 21(10), 1429–1441. doi:10.1002/sim.1142", {})],
    [("Sakar, C. and Kastro, Y. (2018). ", {}), ("Online Shoppers Purchasing Intention Dataset", {"i": True}),
     (". UCI Machine Learning Repository. doi:10.24432/C5F88Q", {})],
    [("Wald, A. (1943). Tests of statistical hypotheses concerning several parameters when the number of "
      "observations is large. ", {}), ("Transactions of the American Mathematical Society", {"i": True}),
     (", 54(3), 426–482. doi:10.1090/S0002-9947-1943-0012401-3", {})],
]
for n, tag, title, refs in [(29, "B14", "References: MI and testing foundations", REFS1),
                            (30, "B15", "References: related methods and evaluation", REFS2)]:
    s = new_slide(title, n)
    backup_label(s, f"Backup {tag}")
    for c_, col in enumerate([refs[:3], refs[3:]]):
        text(s, L + c_ * 6.15, 1.3, 5.85, 5.5, [{"runs": r, "space_after": 12, "line": 1.05} for r in col], sz=14.5,
             color=INK, name=f"References column {c_ + 1}")
    notes(s, "Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.")

assert all(FIX_USED), [NOTE_FIXES[i][0][:60] for i, u in enumerate(FIX_USED) if not u]

cp = prs.core_properties
cp.title = "Comparing Mutual Information in Finite Samples"
cp.subject = "Normal Wald and Expanded Welch–Satterthwaite comparisons of mutual information"
cp.author = "Daniel Zhao"
cp.last_modified_by = "Daniel Zhao"
cp.comments = ""
prs.save(OUT)
import pptlib
for row in pptlib.EQUATION_LOG:
    if row[4] > 0.85:
        print("tight equation", row)
print("saved", OUT, len(prs.slides), "slides")
