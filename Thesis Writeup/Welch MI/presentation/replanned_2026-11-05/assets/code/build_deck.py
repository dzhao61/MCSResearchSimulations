"""Build the replanned (5 November) Welch MI presentation from a copy of the vF2 style donor."""
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

import plan_notes
from pptlib import (BLACK, BLUE_LINE, BODY, COVER_ORANGE, DIVIDER, MUTED, NAVY, ORANGE, ORANGE_LINE, PALE_BLUE,
                    PALE_ORANGE, WHITE, circle, emu, equation, fill_text_body, header_bar, hline, notes, panel_text,
                    rect, set_title, shape_fill_line, slide_number, table, text, vline)

TEMPLATE, OUT, CHARTS, PLAN_PATH = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
PLAN, PLAN_B = plan_notes.load(PLAN_PATH)
TIMING = {1: ("0:25", "0:25"), 2: ("1:15", "1:40"), 3: ("1:00", "2:40"), 4: ("1:20", "4:00"), 5: ("1:40", "5:40"),
          6: ("1:20", "7:00"), 7: ("1:40", "8:40"), 8: ("1:40", "10:20"), 9: ("1:30", "11:50"),
          10: ("1:45", "13:35"), 11: ("1:30", "15:05"), 12: ("1:40", "16:45"), 13: ("1:05", "17:50"),
          14: ("1:00", "18:50")}
EW_TEXT = "B4501A"  # darker orange for Expanded Welch text labels on pale fills

prs = Presentation(TEMPLATE)
sld_ids = prs.slides._sldIdLst
for sld in list(sld_ids)[1:]:
    prs.part.drop_rel(sld.get(qn("r:id")))
    sld_ids.remove(sld)
LAYOUT = prs.slide_masters[1].slide_layouts.get_by_name("Title and Content")


def new_slide(title, n, sz=36):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0:
            ph._element.getparent().remove(ph._element)
    set_title(s, title, x=0.8, y=0.38, w=11.9, h=0.8, sz=sz)
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


def lead(s, runs, h=0.78):
    return text(s, 0.85, 1.2, 11.7, h, [{"runs": runs, "b": True}], sz=20, name="Lead",
                margins=(0.04, 0.04, 0.02, 0.02), line=0.98)


def setting(s, label, x=0.85, y=1.98, w=11.5, sz=18, color=ORANGE):
    return text(s, x, y, w, 0.38, [[(label, {"b": True, "c": color})]], sz=sz, name="Setting",
                margins=(0.02, 0.02, 0, 0))


def footer(s, runs, w=11.2):
    if isinstance(runs, str):
        runs = [(runs, {"i": True})]
    return text(s, 0.85, 7.03, w, 0.34, [runs], sz=14, color=MUTED, anchor="ctr", name="Source line",
                margins=(0, 0.02, 0, 0))


def pic(s, name, x, y, w, h):
    return s.shapes.add_picture(f"{CHARTS}/{name}.png", emu(x), emu(y), emu(w), emu(h))


def panel(s, x, y, w, h, kind="peach", heading=None, body=None, hsz=19, bsz=17, dashed=False, anchor="t",
          margins=(0.2, 0.18, 0.14, 0.12), name=None):
    fill, line, hcol = {"peach": (PALE_ORANGE, ORANGE_LINE, ORANGE), "blue": (PALE_BLUE, BLUE_LINE, NAVY),
                        "white": (WHITE, ORANGE, ORANGE)}[kind]
    if dashed:
        line = ORANGE
    p = rect(s, x, y, w, h, fill=fill, line=line, line_w=1.75 if dashed else 1.0, rounded=0.06, name=name,
             dash="dash" if dashed else None)
    paras = []
    if heading:
        paras.append({"runs": [(heading, {"b": True, "c": hcol})], "sz": hsz, "space_after": 4})
    if body:
        for b in (body if isinstance(body, list) and body and isinstance(body[0], (list, dict)) else [body]):
            paras.append(b if isinstance(b, dict) else {"runs": b if isinstance(b, list) else [b], "sz": bsz,
                                                        "space_after": 4})
    panel_text(p, paras, sz=bsz, anchor=anchor, margins=margins)
    return p


def arrow(s, x, y, w=0.36, h=0.3, down=False, color=ORANGE):
    shp = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW if down else MSO_SHAPE.RIGHT_ARROW, emu(x), emu(y), emu(w), emu(h))
    shape_fill_line(shp, color, None)
    return shp


def backup_label(s, label):
    return text(s, 10.6, 0.12, 2.35, 0.34, [[(label, {"b": True})]], sz=14, color=ORANGE, align="r",
                anchor="ctr", name="Backup label", margins=(0, 0.02, 0, 0))


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
    return body


def backup_note(k, extra=None, source=None, opening=None):
    """Backup notes; the question and answer are copied verbatim from the plan."""
    d = PLAN_B[k]
    body = "Not part of the timed talk. Return to Slide 14 afterwards.\n\n"
    if opening:
        body += f"WHEN OPENING\n{opening.strip()}\n\n"
    body += f"QUESTION ANSWERED\n{d['question']}\n\nANSWER TO GIVE\n{d['answer']}\n\n"
    if extra is None:
        extra = "\n".join(x for x in (d["notes"], d["anchor"]) if x)
    if extra:
        body += f"NOTES\n{extra.strip()}\n\n"
    body += f"SOURCE\n{(source or d['source']).strip()}"
    return body


FOOT_RATE = "Rates divide valid rejections by all 100,000 repetitions; invalid outputs count as non-rejections. "

# =================================================================== Slide 1
cover = prs.slides[0]
by = {sh.name: sh for sh in cover.shapes}
tph, sph, div = by["Title 1"], by["Subtitle 2"], by["Rectangle 1040"]
tph.left, tph.top, tph.width, tph.height = emu(0.6), emu(1.6), emu(4.6), emu(2.05)
tb = tph.text_frame._txBody
bp = tb.find(qn("a:bodyPr"))
for c in list(bp):
    bp.remove(c)
bp.set("anchor", "b")
fill_text_body(tb, ["Comparing Mutual", "Information in Finite", "Samples"], sz=31, color=COVER_ORANGE,
               font="Aptos Display", line=0.92)
text(cover, 0.6, 3.78, 4.4, 0.85, [[("Can MI-specific degrees of freedom improve comparisons between populations?",
                                     {"i": True})]], sz=18, color="404040", font="Aptos", name="Research question",
     margins=(0.09, 0.04, 0.02, 0.02), line=0.95)
div.left, div.top, div.width = emu(0.68), emu(4.85), emu(3.9)
sph.left, sph.top, sph.width, sph.height = emu(0.6), emu(5.0), emu(4.3), emu(1.75)
tb = sph.text_frame._txBody
bp = tb.find(qn("a:bodyPr"))
for c in list(bp):
    bp.remove(c)
bp.set("anchor", "t")
fill_text_body(tb, [{"runs": ["Daniel Zhao (", ("Master of Computer Science", {"i": True}), ")"], "space_after": 5},
                    {"runs": ["Supervisor: Associate Professor Joseph T. Lizier"], "space_after": 5},
                    {"runs": ["The University of Sydney"]}], sz=18, color="262626", font="Aptos", line=0.95)
notes(cover, main_note(1))

# =================================================================== Slide 2
s = new_slide("Motivation: comparing MI across populations", 2)
lead(s, ["Mutual information measures how much observing one variable reduces uncertainty about another. ",
         O("Different sample estimates can arise from sampling noise.")])
rect(s, 3.2, 2.08, 6.93, 0.75, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.2, name="Hypothesis panel")
text(s, 3.45, 2.08, 2.2, 0.75, [[B("Null hypothesis", c=ORANGE)]], sz=18, anchor="ctr")
equation(s, 5.55, 2.08, 4.4, 0.75, r"H_0:I(P)=I(Q)", sz=28, jc="left")
text(s, 0.5, 3.0, 5.9, 0.45, [[B("Online shoppers", c=ORANGE)]], sz=22, name="Example heading")
for y, grp, n_txt, est in [(3.55, "P: new visitors", "1,694 sessions", "0.0043 nats"),
                           (4.68, "Q: returning visitors", "10,551 sessions", "0.0179 nats")]:
    p = rect(s, 0.5, y, 2.3, 0.95, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.08)
    panel_text(p, [{"runs": [B(grp, c=NAVY)], "sz": 18, "space_after": 2}, {"runs": [n_txt], "sz": 16, "color": BODY}],
               anchor="ctr", margins=(0.14, 0.1, 0.06, 0.06))
    arrow(s, 2.9, y + 0.33, w=0.34, h=0.28)
    for r_ in range(4):
        for c_ in range(2):
            rect(s, 3.35 + c_ * 0.4, y + 0.06 + r_ * 0.21, 0.4, 0.21, fill="F8D9C4" if c_ == 0 else "FCEBDD",
                 line=WHITE, line_w=1.0)
    arrow(s, 4.27, y + 0.33, w=0.34, h=0.28)
    p = rect(s, 4.7, y + 0.05, 1.75, 0.85, fill=WHITE, line=ORANGE, line_w=1.5, rounded=0.1)
    panel_text(p, [{"runs": ["corrected MI estimate"], "sz": 14, "color": BODY}, {"runs": [B(est)], "sz": 20}],
               align="ctr", anchor="ctr", margins=(0.05, 0.05, 0.03, 0.03))
text(s, 0.5, 5.75, 6.0, 0.4, [["Variables: month of visit and purchase outcome."]], sz=18, color=BODY,
     name="Variables")
vline(s, 6.68, 3.05, 3.2, color="9A9A9A", width=1.5, dash="dash")
text(s, 6.95, 3.0, 5.9, 0.45, [[B("Statistical task", c=ORANGE)]], sz=22, name="Task heading")
steps = ["Draw a count table from each population", "Estimate MI from each table",
         "Assess whether sampling noise can explain the difference"]
for i, st in enumerate(steps):
    y = 3.55 + i * 0.93
    last = i == 2
    p = rect(s, 7.25, y, 5.3, 0.68, fill=ORANGE if last else WHITE, line=ORANGE, line_w=1.5, rounded=0.12)
    panel_text(p, [[B(st, c=WHITE if last else BLACK)]], sz=18, align="ctr", anchor="ctr",
               margins=(0.1, 0.1, 0.03, 0.03))
    if i < 2:
        arrow(s, 9.75, y + 0.71, w=0.3, h=0.2, down=True)
text(s, 0.85, 6.33, 11.6, 0.48, [[B("Does month–purchase MI differ between the populations?")]], sz=22,
     name="Question")
footer(s, "Month × purchase tables (10×2); corrected MI estimates in nats. Data: Sakar and Kastro (2018). "
          "Bossomaier et al. (2016)")
notes(s, main_note(2))

# =================================================================== Slide 3
s = new_slide("Literature review: foundations and the MI-specific step", 3, sz=34)
lead(s, ["Existing results provide MI estimates, a normal-reference comparison and moment matching. ",
         O("This project derives the MI variance sensitivity needed for its degrees of freedom.")])
H = dict(sz=19, color=ORANGE, b=True, anchor="b", align="ctr", bottom=None)
L = dict(sz=19, color=ORANGE, b=True, anchor="ctr", align="r")
C = dict(sz=18, anchor="ctr", align="ctr", ml=0.12, mr=0.12)
cols = ["MI estimation and uncertainty", "Normal Wald comparison", "Welch–Satterthwaite moment matching"]
rows = [[dict(paras=[""], **H)] + [dict(paras=[[(c_, {"i": True, "b": True})]], **H) for c_ in cols]]
data3 = [("Idea", ["Estimate MI and first-order sampling variance",
                   "Divide the estimated difference by its standard error",
                   "Match variance moments to choose degrees of freedom"]),
         ("Key work", ["Moddemeijer (1989); Paninski (2003)", "Mora and Ruiz-Castillo (2009)",
                       "Satterthwaite (1946); Welch (1947); Hutcheson (1970); Pan and Wall (2002)"]),
         ("Required step", ["Track variation in the variance estimate itself",
                            "Assess the fixed normal cutoff in finite samples",
                            "Calculate the MI-specific variance sensitivity"])]
for lab, cells in data3:
    rows.append([dict(paras=[lab], **L)] + [dict(paras=[c_], **C) for c_ in cells])
table(s, 0.5, 2.12, [1.75, 3.53, 3.53, 3.53], [0.78, 1.0, 1.12, 1.02], rows, name="Literature matrix")
for x in (2.25, 5.78, 9.31):
    vline(s, x, 2.25, 3.75, color=ORANGE, width=2.0)
p = rect(s, 1.6, 6.27, 10.1, 0.6, fill=ORANGE, rounded=0.2, name="Contribution strip")
panel_text(p, [[B("Contribution: ", c=WHITE), ("Derive that sensitivity and evaluate the resulting degrees of freedom.",
                                                {"c": WHITE, "b": True})]], sz=19, align="ctr", anchor="ctr",
           margins=(0.1, 0.1, 0.02, 0.02))
footer(s, "Thesis Sections 2.2–2.5 and 3.2–3.3; full references in B13–B14")
notes(s, main_note(3))

# =================================================================== Slide 4
s = new_slide("Method: one statistic, two reference distributions", 4)
lead(s, ["Both methods use ", O("the same estimated MI difference and standard error"),
         ". Expanded Welch uses estimated degrees of freedom for a Student t reference."])
rect(s, 0.5, 2.1, 5.85, 2.12, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.06, name="Shared statistic panel")
text(s, 0.7, 2.18, 5.4, 0.36, [[B("Shared statistic", c=ORANGE)]], sz=18)
equation(s, 0.6, 2.5, 5.65, 1.05,
         r"T=\frac{\widehat\Delta_{\mathrm{BC}}}{\widehat{\mathrm{SE}}},\qquad\widehat{\mathrm{SE}}^2=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}",
         sz=24, jc="center")
text(s, 0.62, 3.55, 5.68, 0.62, [[CM("Δ̂", i=False), CM("BC", sub=True, i=False), ": estimated ",
                                  CM("𝐼(𝑃) − 𝐼(𝑄)"), ", after leading bias correction."]], sz=17, color=BODY,
     anchor="ctr")
header_bar(s, 0.5, 4.38, 2.82, 0.5, "Normal Wald", NAVY, sz=20)
panel(s, 0.5, 4.94, 2.82, 1.92, "blue", body=[["Standard normal distribution; two-sided 5% cutoff about ", B("±1.96"),
                                              "."]], bsz=19, anchor="ctr", margins=(0.16, 0.14, 0.1, 0.1))
header_bar(s, 3.53, 4.38, 2.82, 0.5, "Expanded Welch", ORANGE, sz=20)
panel(s, 3.53, 4.94, 2.82, 1.92, "peach", body=[["Student t distribution with estimated degrees of freedom; ",
                                                B("a larger cutoff"), "."]], bsz=19, anchor="ctr",
      margins=(0.16, 0.14, 0.1, 0.1))
pic(s, "slide04_reference_distributions", 6.6, 2.15, 6.3, 3.9)
text(s, 6.75, 6.15, 6.05, 0.7, [[("Student t distribution with 5 degrees of freedom, for illustration; cutoff about ±2.57.",
                                  {"i": True})]], sz=17, color=BODY, align="ctr", name="Plot label")
footer(s, "Thesis Chapters 3–4, Figure 2.1. Additional validity rules: Slide 6 and B3")
notes(s, main_note(4))

# =================================================================== Slide 5
s = new_slide("Approach and contribution", 5)
lead(s, ["Tracking how the pointwise-MI variance changes with the table gives the sampling-variance input for ",
         O("MI-specific degrees of freedom"), "."])
header_bar(s, 0.5, 2.05, 12.33, 0.45, "Derivation chain", ORANGE, sz=19)
blocks = [("Cell probabilities change", [["Move a small amount of probability towards one cell."]], False),
          ("Margins and pointwise MI change", [["Track their joint effect."]], False),
          ("Variance sensitivity, derived here", [[CM("𝑔"), CM("𝑃", sub=True), CM("(𝑥, 𝑦)"),
                                                   " describes the change in ", CM("𝑉(𝑃)"), "."]], True),
          ("Degrees of freedom", [["Use the spread of those sensitivities."]], True)]
for i, (hd, bd, new) in enumerate(blocks):
    x = 0.5 + i * 3.2
    panel(s, x, 2.62, 2.73, 1.55, "peach", heading=hd, body=bd, hsz=18, bsz=17, dashed=new, anchor="ctr",
          margins=(0.14, 0.12, 0.08, 0.08))
    if i < 3:
        arrow(s, x + 2.79, 3.25, w=0.36, h=0.3)
header_bar(s, 0.5, 4.38, 12.33, 0.45, "Result and approximations", NAVY, sz=19)
rect(s, 0.5, 4.93, 7.7, 1.95, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.06, name="Result panel")
equation(s, 0.6, 4.98, 7.5, 1.22,
         r"\operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P}\quad\Longrightarrow\quad\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}",
         sz=24, jc="center")
text(s, 0.75, 6.2, 7.3, 0.62, [[CM("𝜏"), CM("2", sup=True), CM("(𝑃)"), " is the variance of ", CM("𝑔"),
                                CM("𝑃", sub=True), CM("(𝑋, 𝑌)"), ". Repeat for Q and combine using Welch–Satterthwaite."]],
     sz=17, color=BLACK, anchor="ctr")
rect(s, 8.4, 4.93, 4.43, 1.95, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.06)
text(s, 8.6, 5.02, 4.1, 0.4, [[B("Two approximations evaluated", c=NAVY)]], sz=18)
for i, lab in enumerate(["First-order sampling expansion", "Scaled chi-squared moment matching"]):
    y = 5.55 + i * 0.62
    circle(s, 8.65, y, 0.44, str(i + 1), NAVY, sz=16)
    text(s, 9.2, y - 0.04, 3.55, 0.52, [[lab]], sz=17, anchor="ctr")
footer(s, "Thesis Sections 4.1–4.3; exact derivative in B1, moment matching in B2")
notes(s, main_note(5))

# =================================================================== Slide 6
s = new_slide("Evaluation design", 6)
lead(s, ["Known populations separate approximation accuracy, false positives and power. Both tests receive ",
         O("the same sampled table pairs"), "."])
header_bar(s, 0.5, 2.05, 6.15, 0.47, "Research questions", NAVY, sz=19)
rect(s, 0.5, 2.6, 6.15, 3.4, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
rq = [("RQ1: Approximation accuracy", ["Sampling moments of ", CM("𝑉̂"), " and component df, including near independence"]),
      ("RQ2: False positives", ["Equal MI at 0.005, 0.02 and 0.30 nats"]),
      ("RQ3: Power", ["P MI 0.02; MI-gap magnitudes 0.005, 0.01 and 0.02 nats"])]
for i, (lab, desc) in enumerate(rq):
    y = 2.75 + i * 1.08
    circle(s, 0.68, y + 0.12, 0.46, str(i + 1), NAVY, sz=16)
    text(s, 1.3, y, 5.2, 1.0, [{"runs": [B(lab, c=NAVY)], "sz": 19, "space_after": 2}, {"runs": desc, "sz": 17}])
header_bar(s, 6.9, 2.05, 5.93, 0.47, "Shared simulation grid", ORANGE, sz=19)
p = rect(s, 6.9, 2.6, 5.93, 3.4, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.05)
panel_text(p, [
    {"runs": ["Four sizes: 2×2, 4×4, 8×8, 16×16"], "bullet": True, "space_after": 6},
    {"runs": ["Uniform, same-skew and different-skew margins"], "bullet": True, "space_after": 6},
    {"runs": ["Ten sample sizes: 10 to 50,000 observations per population"], "bullet": True, "space_after": 6},
    {"runs": ["100,000 independent table pairs per setting"], "bullet": True, "space_after": 12},
    {"runs": [B("Model: "), "copying construction: choose margins and solve for target MI."]},
], sz=18, anchor="ctr", margins=(0.25, 0.2, 0.12, 0.12))
text(s, 0.85, 6.12, 11.6, 0.75, [[B("Reporting: "), "usual 0.05 p-value thresholds. Invalid outputs count as "
                                  "non-rejections; validity is reported separately."]], sz=18, name="Reporting")
footer(s, "Morris et al. (2019). Thesis Chapter 5, Tables 5.1–5.3; exact vectors, sample sizes and rules in B3")
notes(s, main_note(6))

# =================================================================== Slide 7
s = new_slide("Results: approximation accuracy", 7)
lead(s, ["The mean of ", CM("𝑉̂", b=True), " can ", O("remain inflated"),
         " even when its population first-order sampling-variance prediction is accurate."])
text(s, 0.6, 1.98, 6.7, 0.36, [[B("Mean of "), CM("𝑉̂", b=True), B(" / population "), CM("𝑉", b=True)]], sz=18,
     name="Top plot heading")
pic(s, "slide07_mean_ratio", 0.5, 2.3, 6.85, 2.0)
text(s, 0.6, 4.32, 6.7, 0.36, [[B("Predicted / observed sampling variance of "), CM("𝑉̂", b=True)]], sz=18,
     name="Bottom plot heading")
pic(s, "slide07_variance_ratio", 0.5, 4.64, 6.85, 2.3)
setting(s, "Different-skew P · 4×4 · population MI 0.02 nats", x=7.65, w=5.25, sz=17)
panel(s, 7.65, 2.42, 5.18, 1.6, "peach", heading="Mean: rare cells can inflate it.",
      body=[["Newly observed rare cells can have large pointwise-MI deviations, whose squares raise ", CM("𝑉̂"),
             "."]], hsz=18, bsz=17)
panel(s, 7.65, 4.15, 5.18, 1.75, "blue", heading="Sampling variance: linearisation can miss large changes.",
      body=[["Rare cells appear in some samples and not others; sample-based sensitivities can also overpredict the "
             "resulting variation."]], hsz=18, bsz=17)
panel(s, 7.65, 6.02, 5.18, 0.88, "white", dashed=True,
      body=[[B("At n = 1,000: mean "), B("19% high", c=ORANGE), B("; population variance prediction "),
             B("3% low", c=ORANGE), B(". Both moments enter the degrees of freedom.")]], bsz=16, anchor="ctr",
      margins=(0.16, 0.12, 0.05, 0.05))
footer(s, "Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2. Bands: approximate 95% Monte Carlo intervals. "
          "Other sizes and Q: B4")
notes(s, main_note(7))

# =================================================================== Slide 8
s = new_slide("Results: near independence", 8)
lead(s, ["Near independence, ", O("sampling noise keeps the mean estimated component degrees of freedom positive"),
         " while the population first-order value becomes very small."])
pic(s, "slide08_near_independence_df", 0.5, 2.0, 6.95, 4.85)
setting(s, "Different-skew P · 4×4 · n = 1,000 fixed", x=7.75, w=5.1, sz=18)
panel(s, 7.75, 2.42, 5.08, 1.72, "blue", heading="Population first-order value",
      body=[["Insert known population inputs into the component formula. Near independence, its local value is "
             "approximately n × population MI."]], hsz=18, bsz=17)
panel(s, 7.75, 4.27, 5.08, 1.55, "peach", heading="Sample estimate",
      body=[["Quadratic sampling errors create apparent association, which remains in the sample-based calculation."]],
      hsz=18, bsz=17)
panel(s, 7.75, 5.95, 5.08, 0.95, "white", dashed=True,
      body=[[B("At MI 0.0001: "), "mean estimated component df ", B("≈4.9", c=ORANGE), "; sampling-moment target ",
             B("≈9.1", c=NAVY), "; population first-order value ", B("≈0.1")]], bsz=16, anchor="ctr",
      margins=(0.16, 0.12, 0.05, 0.05))
footer(s, "Thesis Section 6.1.3, Figure 6.3; Appendix A.2. Bands: approximate 95% Monte Carlo intervals. "
          "Local calculation: B5")
notes(s, main_note(8))

# =================================================================== Slide 9
s = new_slide("Results: false positives across common MI values", 9, sz=34)
lead(s, ["A larger cutoff ", O("brings some excessive false-positive rates closer to 5%"),
         ", but accuracy at one association level does not persist across common MI values."])
setting(s, "Uniform 4×4 · n = 20 per population · equal MI in P and Q")
pic(s, "slide09_null_bars", 0.5, 2.38, 6.9, 4.03)
text(s, 0.85, 6.5, 11.9, 0.42, [[B("Nominal target: 5%. "), "Both tests are valid in every repetition in these "
                                                           "examples."]], sz=18, name="Validity note")
panel(s, 7.75, 2.45, 5.08, 1.22, "peach", heading="Common MI 0.02: closer to 5%",
      body=[["Expanded Welch lowers the rate from 8.35% to 4.90%."]], hsz=19, bsz=18)
panel(s, 7.75, 3.8, 5.08, 1.22, "blue", heading="Common MI 0.30: still above 5%",
      body=[["Expanded Welch still rejects in 13.11% of repetitions."]], hsz=19, bsz=18)
panel(s, 7.75, 5.15, 5.08, 1.2, "white", dashed=True,
      body=[[B("Interpretation: "), "The larger cutoff reduces rejection, while the shared statistic can still have "
                                    "the wrong sampling distribution."]], bsz=18, anchor="ctr",
      margins=(0.18, 0.14, 0.06, 0.06))
footer(s, "Slices of the balanced null grid. Whiskers: pointwise 95% Monte Carlo intervals. Thesis Section 6.2.1, "
          "Figure 6.4; full grids in B6–B8")
notes(s, main_note(9))

# =================================================================== Slide 10
s = new_slide("Results: why bias changes rejection", 10)
lead(s, ["Similar errors in estimated uncertainty accompany ", O("opposite false-positive behaviour"),
         " when bias in the MI difference changes."])
setting(s, "16×16 · n = 1,000 per population · equal MI 0.02 nats")
Hh = dict(sz=19, b=True, color=WHITE, fill=ORANGE, anchor="ctr", align="ctr", bottom=None)
Rr = dict(sz=19, anchor="ctr", align="ctr")
rows = [[dict(paras=["Margins"], **{**Hh, "align": "l"}), dict(paras=["Variance ratio"], **Hh),
         dict(paras=["Bias / SD"], **Hh), dict(paras=["Normal Wald"], **Hh), dict(paras=["Expanded Welch"], **Hh)],
        [dict(paras=["Same skew"], sz=19, anchor="ctr", fill=PALE_ORANGE), dict(paras=["1.93"], fill=PALE_ORANGE, **Rr),
         dict(paras=["≈0"], fill=PALE_ORANGE, **Rr), dict(paras=["0.60%"], fill=PALE_ORANGE, **Rr),
         dict(paras=["0.53%"], fill=PALE_ORANGE, **Rr)],
        [dict(paras=["Different skew"], sz=19, anchor="ctr"), dict(paras=["1.94"], **Rr),
         dict(paras=[[B("2.06")]], **Rr), dict(paras=["26.01%"], **Rr), dict(paras=["24.84%"], **Rr)]]
table(s, 0.5, 2.42, [3.0, 2.3, 2.1, 2.45, 2.48], [0.56, 0.56, 0.56], rows, name="Bias contrast")
text(s, 0.6, 4.14, 12.2, 0.4, [[("Variance ratio: average squared estimated standard error / observed variance of the "
                                 "estimated MI difference.", {"i": True})]], sz=15, color=BODY, name="Ratio definition")
panel(s, 0.5, 4.6, 6.0, 1.38, "blue", heading="Same skew",
      body=[["The oversized denominator suppresses the statistic; expected MI biases cancel."]], hsz=20, bsz=19,
      anchor="ctr")
panel(s, 6.83, 4.6, 6.0, 1.38, "peach", heading="Different skew", dashed=True,
      body=[["The estimated difference is shifted away from zero by unequal residual biases."]], hsz=20, bsz=19,
      anchor="ctr")
p = rect(s, 0.5, 6.12, 12.33, 0.8, fill=NAVY, rounded=0.15, name="Conclusion bar")
panel_text(p, [[B("Conclusion: ", c=WHITE), ("Changing the cutoff leaves the biased estimated difference unchanged. "
                                              "Both tests are valid in every repetition here.", {"c": WHITE})]],
           sz=18, align="ctr", anchor="ctr", margins=(0.2, 0.2, 0.02, 0.02))
footer(s, "Thesis Section 6.2.4, Table 6.1; current null rates and diagnostics. Full different-skew grid: B8")
notes(s, main_note(10))

# =================================================================== Slide 11
s = new_slide("Results: power across MI differences", 11)
lead(s, ["With sufficient observations, ", O("larger MI differences become easier to detect"),
         ". Expanded Welch's larger cutoff lowers or preserves rejection."])
setting(s, "Uniform 4×4 · population MI in P = 0.02 nats")
text(s, 0.6, 2.38, 6.8, 0.36, [[B("MI-gap magnitude 0.01 nats: power against sample size")]], sz=17, name="Plot heading")
pic(s, "slide11_power_gap001", 0.5, 2.72, 6.9, 4.25)
text(s, 7.75, 2.38, 5.1, 0.4, [[B("Snapshot at n = 2,500", c=ORANGE)]], sz=19, name="Snapshot heading")
Hs = dict(sz=18, b=True, color=WHITE, anchor="ctr", align="ctr", bottom=None)
rows = [[dict(paras=["MI-gap magnitude (nats)"], fill="555555", **{**Hs, "sz": 17}),
         dict(paras=["Normal Wald"], fill=NAVY, **{**Hs, "sz": 17}),
         dict(paras=["Expanded Welch"], fill=ORANGE, **{**Hs, "sz": 17})]]
for gap, w_, e_ in [("0.005", "11.60%", "11.14%"), ("0.01", "31.85%", "31.14%"), ("0.02", "79.24%", "78.74%")]:
    f = PALE_ORANGE if gap == "0.01" else None
    rows.append([dict(paras=[gap], sz=19, align="ctr", anchor="ctr", fill=f),
                 dict(paras=[w_], sz=19, align="ctr", anchor="ctr", fill=f),
                 dict(paras=[e_], sz=19, align="ctr", anchor="ctr", fill=f)])
table(s, 7.75, 2.85, [2.0, 1.45, 1.63], [0.8, 0.5, 0.5, 0.5], rows, name="Snapshot table")
text(s, 7.75, 5.3, 5.1, 1.05, [{"runs": [B("Power: "), "probability of rejecting equal MI when population MI differs. "
                                         "Rates use the usual 0.05 p-value threshold."]}], sz=18,
     name="Power definition")
text(s, 7.75, 6.35, 5.1, 0.6, [[("Rates divide valid rejections by all 100,000 repetitions; invalid outputs count as "
                                  "non-rejections.", {"i": True})]], sz=14, color=MUTED, name="Denominator note")
footer(s, "Bands: pointwise 95% Monte Carlo intervals. Thesis Section 6.3.1, Figure 6.7; full grids in B9–B11")
notes(s, main_note(11))

# =================================================================== Slide 12
s = new_slide("Results: bias can reverse the estimated direction", 12)
lead(s, ["In sparse tables, unequal residual biases can outweigh the true MI difference and ",
         O("reverse the estimated direction"), "."])
setting(s, "Different-skew 16×16 · MI 0.02 versus 0.03 nats")
text(s, 0.6, 2.38, 7.0, 0.36, [[B("MI-gap magnitude 0.01 nats: power against sample size")]], sz=17, name="Plot heading")
pic(s, "slide12_direction_power", 0.5, 2.72, 7.1, 4.25)
header_bar(s, 7.95, 2.42, 4.88, 0.48, "At n = 1,000", NAVY, sz=19)
rect(s, 7.95, 2.95, 4.88, 2.58, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
for y, lab, val in [(3.05, "True difference, P minus Q", "−0.0100 nats"), (3.53, "Mean estimated difference",
                                                                          "+0.0207 nats")]:
    text(s, 8.15, y, 2.8, 0.45, [lab], sz=16, color=BODY, anchor="ctr", margins=(0, 0, 0, 0))
    text(s, 10.9, y, 1.8, 0.45, [[B(val)]], sz=20, align="r", anchor="ctr", margins=(0, 0, 0, 0))
hline(s, 8.15, 4.07, 4.53, color=BLUE_LINE)
text(s, 8.15, 4.14, 4.55, 1.35, [{"runs": ["Expanded Welch rejects in ", B("9.66%"), " of repetitions."], "space_after": 4},
                               {"runs": [O("Among those rejections"), ", over 99.9% have the opposite estimated direction."]}],
     sz=18, margins=(0, 0, 0, 0))
panel(s, 7.95, 5.62, 4.88, 1.28, "white", dashed=True,
      body=[[B("Mechanism: "), "As positive bias diminishes, the sampling centre passes near zero, so rejection "
                               "initially falls before recovering."]], bsz=17, anchor="ctr",
      margins=(0.16, 0.12, 0.05, 0.05))
footer(s, "At n = 1,000: 9,659 of 9,662 Expanded Welch rejections are positive; both methods 100% valid. "
          "Thesis Figure 6.9; full grid in B11", w=11.25)
notes(s, main_note(12))

# =================================================================== Slide 13
s = new_slide("Illustration: online shopping data", 13)
lead(s, ["Returning visitors have higher estimated month–purchase MI, and ",
         O("both approximate tests reject equal MI after adjustment"), "."])
header_bar(s, 0.5, 2.1, 7.45, 0.5, "Month × purchase: corrected MI estimates (nats)", ORANGE, sz=19, align="l")
rect(s, 0.5, 2.66, 7.45, 3.3, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.05)
text(s, 0.75, 2.78, 3.2, 0.36, ["New visitors"], sz=17, color=BODY, margins=(0, 0, 0, 0))
text(s, 0.75, 3.1, 3.2, 0.85, [[B("0.0043")]], sz=44, margins=(0, 0, 0, 0))
text(s, 4.25, 2.78, 3.4, 0.36, ["Returning visitors"], sz=17, color=BODY, margins=(0, 0, 0, 0))
text(s, 4.25, 3.1, 3.4, 0.85, [[B("0.0179")]], sz=44, margins=(0, 0, 0, 0))
text(s, 0.75, 4.08, 7.0, 0.36, ["Holm-adjusted p-values across six comparisons"], sz=16, color=BODY,
     margins=(0, 0, 0, 0))
text(s, 0.75, 4.42, 3.4, 0.45, [[B("Normal Wald ", c=NAVY), "0.000189"]], sz=20, margins=(0, 0, 0, 0))
text(s, 4.25, 4.42, 3.6, 0.45, [[B("Expanded Welch ", c=EW_TEXT), "0.00149"]], sz=20, margins=(0, 0, 0, 0))
p = rect(s, 0.75, 5.12, 6.95, 0.6, fill=WHITE, line=ORANGE_LINE, rounded=0.15)
panel_text(p, [[B("Both tests reject equal MI after Holm adjustment")]], sz=17, anchor="ctr",
           margins=(0.15, 0.1, 0.02, 0.02))
header_bar(s, 8.2, 2.1, 4.63, 0.5, "Weekend × purchase", NAVY, sz=19, align="l")
panel(s, 8.2, 2.66, 4.63, 3.3, "blue", body=[[B("Estimates are close; neither test rejects equality.", c=NAVY)]],
      bsz=21, anchor="ctr", margins=(0.25, 0.2, 0.1, 0.1))
panel(s, 0.5, 6.1, 12.33, 0.78, "white", dashed=True,
      body=[[B("Interpretation: "), "Population MI is unknown. The simulations provide the evidence about reliability."]],
      bsz=18, anchor="ctr", margins=(0.2, 0.15, 0.03, 0.03))
footer(s, "Sakar and Kastro (2018): 1,694 new and 10,551 returning sessions. Holm (1979). Thesis Section 6.4; "
          "details in B12", w=11.25)
notes(s, main_note(13))

# =================================================================== Slide 14
s = new_slide("Conclusions and next steps", 14)
lead(s, ["MI-specific degrees of freedom improve some false-positive rates, while remaining failures identify ",
         O("estimation accuracy as a priority"), "."])
header_bar(s, 0.5, 2.08, 12.33, 0.47, "Contribution and findings", NAVY, sz=19)
finds = [["Derived variance sensitivity and MI-specific degrees of freedom."],
         ["Brought some excessive false-positive rates closer to 5%; deepened conservatism elsewhere."],
         ["Reduced nominal power; residual bias can reverse the estimated direction."]]
for i, runs in enumerate(finds):
    x = 0.5 + i * 4.18
    rect(s, x, 2.65, 3.97, 2.2, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
    circle(s, x + 3.97 / 2 - 0.27, 2.8, 0.54, str(i + 1), NAVY, sz=18)
    text(s, x + 0.2, 3.42, 3.57, 1.38, [runs], sz=19, color=NAVY, align="ctr", anchor="ctr")
header_bar(s, 0.5, 5.02, 12.33, 0.47, "Next steps", ORANGE, sz=19)
nexts = [["Improve bias and uncertainty estimates, including quadratic variation near independence."],
         ["Test other association constructions and unequal sample sizes."]]
for i, runs in enumerate(nexts):
    x = 0.5 + i * 6.27
    rect(s, x, 5.58, 6.06, 0.98, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.08)
    circle(s, x + 0.2, 5.8, 0.52, str(i + 1), ORANGE, sz=18)
    text(s, x + 0.9, 5.62, 5.05, 0.9, [runs], sz=18, anchor="ctr")
text(s, 0.85, 6.6, 11.6, 0.4, ["Thank you."], sz=18, color=MUTED, align="ctr", name="Thank you")
BACKUP_INDEX = """BACKUP INDEX (type the slide number, press Enter, then return to 14)
15  B1  Variance sensitivity
16  B2  Moment matching and combined degrees of freedom
17  B3  Population construction, grid and validity
18  B4  Approximation ratios across table sizes
19  B5  Near-independence noise calculation
20  B6  Full null results: uniform margins
21  B7  Full null results: same-skew margins
22  B8  Full null results: different-skew margins
23  B9  Full power results: uniform margins
24  B10 Full power results: same-skew margins
25  B11 Full power results: different-skew margins
26  B12 Application details and comparison family
27  B13 References: MI and testing foundations
28  B14 References: related methods and evaluation"""
notes(s, main_note(14, extra=BACKUP_INDEX))

# =================================================================== B1 (15)
s = new_slide("Variance sensitivity", 15)
backup_label(s, "Backup B1")
text(s, 0.85, 1.25, 4.4, 0.6, [[B("Perturbation towards one cell:")]], sz=22, anchor="ctr")
equation(s, 5.05, 1.22, 6.5, 0.66, r"P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}", sz=24)
rect(s, 0.5, 2.0, 12.33, 3.15, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.06)
equation(s, 4.05, 2.12, 8.6, 0.85, r"g_P(x,y)=\{\ell_P(x,y)-I(P)\}^2-V(P)", sz=26)
equation(s, 4.05, 3.02, 8.6, 0.85, r"\qquad+2\bigl[\ell_P(x,y)-\mathbb E_P\{\ell_P(X,Y)\mid X=x\}", sz=26)
equation(s, 4.05, 3.92, 8.6, 0.85, r"\qquad\qquad-\mathbb E_P\{\ell_P(X,Y)\mid Y=y\}+I(P)\bigr]", sz=26)
text(s, 0.75, 2.12, 3.2, 0.85, [[O("Changing probability weights")]], sz=20, anchor="ctr")
text(s, 0.75, 3.1, 3.2, 1.6, [[O("Changing pointwise-MI values and margins")]], sz=20, anchor="ctr")
vline(s, 3.98, 3.12, 1.55, color=ORANGE, width=2)
text(s, 0.85, 5.35, 3.9, 0.7, ["Pointwise MI:"], sz=22, anchor="ctr")
equation(s, 4.05, 5.35, 7.5, 0.7, r"\ell_P(i,j)=\log\{p_{ij}/(p_{i+}p_{+j})\}", sz=24)
text(s, 0.85, 6.1, 3.9, 0.7, ["Sensitivity variance:"], sz=22, anchor="ctr")
equation(s, 4.05, 6.1, 7.5, 0.7, r"\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}", sz=24)
footer(s, "Exact for positive population tables; its use for sampling errors is first order. Thesis Chapter 4")
notes(s, backup_note(1,
    extra="Regularity assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. Positive MI alone does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.",
    source="Thesis Chapter 4: perturbation path (eq:contamination-path), final form of g (eq:g-final) and definition of "
           "tau-squared (eq:tau-definition). This derivative is exact for positive population tables. Its use for "
           "sampling errors is first order."))

# =================================================================== B2 (16)
s = new_slide("Moment matching and combined degrees of freedom", 16)
backup_label(s, "Backup B2")
header_bar(s, 0.5, 1.45, 12.33, 0.5, "Component degrees of freedom", ORANGE)
rect(s, 0.5, 2.0, 12.33, 1.62, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.06)
equation(s, 0.8, 2.02, 11.8, 1.58,
         r"\nu_{P,\mathrm{mom}}=\frac{2[\mathbb E\{\widehat V(P)\}]^2}{\operatorname{Var}\{\widehat V(P)\}},\qquad\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}",
         sz=26, jc="center")
header_bar(s, 0.5, 3.8, 12.33, 0.5, "Combined degrees of freedom", NAVY)
rect(s, 0.5, 4.35, 12.33, 1.62, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.06)
equation(s, 0.8, 4.37, 11.8, 1.58,
         r"\widehat\nu=\frac{\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\}^2}{\{\widehat V(P)/n_P\}^2/\widehat\nu_P+\{\widehat V(Q)/n_Q\}^2/\widehat\nu_Q}",
         sz=26, jc="center")
text(s, 0.85, 6.12, 11.5, 0.8, ["Moment matching does not establish the normality or independence needed for an exact "
                                "Student t distribution."], sz=20, name="Caveat")
footer(s, "Satterthwaite (1946). Thesis Sections 4.1 and 4.3")
notes(s, backup_note(2))

# =================================================================== B3 (17)
s = new_slide("Population construction, grid and validity", 17)
backup_label(s, "Backup B3")
rect(s, 0.5, 1.4, 12.33, 0.95, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.12)
equation(s, 0.8, 1.42, 11.8, 0.91,
         r"p_{ij}(\lambda)=(1-\lambda)a_i a_j+\lambda a_i\mathbf 1\{i=j\},\qquad 0\leq\lambda<1", sz=26, jc="center")
mk = lambda r_: [CM("𝑚"), CM("𝑘", sub=True), (f"({r_})", {})]
header_bar(s, 0.5, 2.55, 6.05, 0.47, "Parameter grid", ORANGE, sz=19)
p = rect(s, 0.5, 3.08, 6.05, 3.0, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.05)
panel_text(p, [
    {"runs": ["k = 2, 4, 8, 16; uniform, same-skew or different-skew margins"], "bullet": True, "space_after": 5},
    {"runs": ["Same skew: both use "] + mk(0.8) + [". Different skew: P uses "] + mk(0.7) + [", Q uses "] + mk(0.8) +
     [", where "] + [CM("𝑚"), CM("𝑘", sub=True), CM("(𝜌) = (𝜌, (1 − 𝜌)/(𝑘 − 1), …)")], "bullet": True, "space_after": 5},
    {"runs": ["Null: common MI 0.005, 0.02, 0.30. Power: P MI 0.02, Q MI 0.025, 0.03, 0.04"], "bullet": True},
], sz=17, anchor="ctr", margins=(0.22, 0.18, 0.1, 0.1))
header_bar(s, 6.78, 2.55, 6.05, 0.47, "Validity and rates", NAVY, sz=19)
p = rect(s, 6.78, 3.08, 6.05, 3.0, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
panel_text(p, [
    {"runs": ["Each study has 360 settings, 100,000 independent pairs per setting"], "bullet": True, "space_after": 5,
     "bullet_color": NAVY},
    {"runs": ["Wald needs a finite difference and positive finite standard error. Expanded Welch also needs valid "
              "positive finite df calculations."], "bullet": True, "space_after": 5, "bullet_color": NAVY},
    {"runs": ["Rate = valid rejections / all repetitions. Report validity separately."], "bullet": True,
     "bullet_color": NAVY},
], sz=17, anchor="ctr", margins=(0.22, 0.18, 0.1, 0.1))
text(s, 0.85, 6.2, 11.6, 0.7, [[B("n = "), "10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000, 50,000 per group"]],
     sz=19, anchor="ctr", name="Sample sizes")
footer(s, "Thesis Chapter 5 and Appendix B.1–B.5")
notes(s, backup_note(3,
    extra="""Full rules (Appendix B): Normal Wald requires a finite estimated difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14 and a finite Wald p-value. Expanded Welch additionally requires positive finite component and combined degrees of freedom and a finite p-value. A failed component makes Expanded Welch invalid. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so the comparison is invalid even if the other table makes the shared standard error positive and finite. Zero and undefined component degrees of freedom are distinct cases; both fail the positive-finite rule. A failed calculation is not evidence of equality.
Sampling is independent within and between populations, and both methods receive identical sampled pairs. The construction uses the same vector for row and column margins within each population and is one association family, not all categorical distributions.""",
    source="Thesis Chapter 5 and Appendix B.1–B.5; current grid results."))

# =================================================================== B4 (18)
s = new_slide("Approximation ratios across table sizes", 18)
backup_label(s, "Backup B4")
lead(s, [B("Different-skew margins, common MI 0.02 nats; a ratio of one indicates agreement")], h=0.45)
pic(s, "B4_approximation_ratios", 0.5, 1.68, 12.3, 5.3)
footer(s, [("Rows: mean of ", {"i": True}), CM("𝑉̂"), (" / ", {"i": True}), CM("𝑉"),
           ("; population-input and sample-based variance predictions / observed variance. Thesis Figure 6.1",
            {"i": True})], w=11.25)
notes(s, backup_note(4, opening="Colour now identifies table size; the rows are three different ratios."))

# =================================================================== B5 (19)
s = new_slide("Near-independence noise calculation", 19)
backup_label(s, "Backup B5")
lead(s, [B("Setting: 4×4, n = 1,000, MI 0.0001;  "), CM("𝑑 = 9"), B("  and  "),
         CM("𝜅 = 2𝑛𝐼(𝑃) ≈ 0.2")], h=0.5)
rect(s, 0.5, 1.9, 12.33, 1.2, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.1)
equation(s, 0.8, 1.92, 11.8, 1.16,
         r"G=2n\widehat I(P)\ \dot{\sim}\ \chi^2_d(\kappa),\qquad \widehat\nu_P\approx G/2", sz=28, jc="center")
text(s, 0.85, 3.17, 11.5, 0.4, [["In ", CM("𝐺"), ", ", CM("𝐼̂(𝑃)"), " is the uncorrected plug-in MI, not a "
                                 "bias-corrected estimate."]], sz=17, color=BODY, name="Plug-in note")
H5 = dict(sz=19, b=True, anchor="ctr", bottom=ORANGE, bottom_w=1.5)
rows = [[dict(paras=["Quantity"], color=ORANGE, **H5), dict(paras=["Local prediction"], color=ORANGE, align="ctr", **H5),
         dict(paras=["Observed (P)"], color=ORANGE, align="ctr", **H5)]]
for q, a, b in [("Mean estimated component df", "4.60", "4.86"), ("Sampling-moment target", "9.00", "9.12"),
                ("Mean sample-based variance prediction / observed sampling variance", "1.96", "1.97")]:
    rows.append([dict(paras=[q], sz=19, anchor="ctr"), dict(paras=[a], sz=21, align="ctr", anchor="ctr"),
                 dict(paras=[b], sz=21, align="ctr", anchor="ctr")])
table(s, 0.85, 3.72, [6.9, 2.35, 2.35], [0.56, 0.72, 0.72, 0.98], rows, name="Noise table")
footer(s, "Local approximations under fixed dimensions and positive limiting cell probabilities. Thesis Appendix A.2, "
          "Section 6.1.3")
notes(s, backup_note(5,
    extra="Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.",
))

# =================================================================== B6-B11 (20-25)
mk_b = lambda r_: [("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}), B(f"({r_})")]
grid_slides = [
    (6, "Full null results: uniform margins", [B("Equal MI in P and Q; uniform margins in both populations")],
     "B6_null_uniform", "Thesis Figure 6.4",
     "All 120 settings for the uniform profile. Slide 9 used the 4×4, n = 20 slice of this page."),
    (7, "Full null results: same-skew margins", [B("Equal MI; same-skew margins ")] + mk_b(0.8) + [B(" in P and Q")],
     "B7_null_same_skew", "Thesis Figure 6.5", "All 120 settings for the same-skew profile."),
    (8, "Full null results: different-skew margins", [B("Equal MI; ")] + mk_b(0.7) + [B(" in P and ")] + mk_b(0.8) +
     [B(" in Q")], "B8_null_different_skew", "Thesis Figure 6.6",
     "All 120 settings for the different-skew profile. The Slide 10 diagnostic table uses the MI 0.02, n = 1,000 slice "
     "of these populations.\nAdditional anchor: " + PLAN_B[8]["anchor"]),
    (9, "Full power results: uniform margins", [B("Uniform margins; MI in P = 0.02 nats")], "B9_power_uniform",
     "Thesis Figure 6.7", "120 settings, 240 method rows for this margin profile."),
    (10, "Full power results: same-skew margins", [B("Same-skew margins ")] + mk_b(0.8) +
     [B(" in P and Q; MI in P = 0.02 nats")], "B10_power_same_skew", "Thesis Figure 6.8",
     "All 120 settings for the same-skew power profile."),
    (11, "Full power results: different-skew margins", mk_b(0.7) + [B(" in P, ")] + mk_b(0.8) +
     [B(" in Q; MI in P = 0.02 nats")], "B11_power_different_skew", "Thesis Figure 6.9",
     "120 settings, 240 method rows. The main point is 16×16, gap 0.01, n = 1,000.\n" + PLAN_B[11]["notes"]),
]
for k, title, intro_runs, img, fig_ref, extra in grid_slides:
    s = new_slide(title, k + 14)
    backup_label(s, f"Backup B{k}")
    lead(s, intro_runs, h=0.45)
    pic(s, img, 0.5, 1.68, 12.3, 5.3)
    footer(s, FOOT_RATE + "Rules in B3. " + fig_ref, w=11.25)
    kind = "common MI" if "null" in img else "MI gap"
    notes(s, backup_note(k, extra=extra,
                         opening=f"Colours here identify the {kind}, not the method: solid lines with filled circles "
                                 "are Normal Wald, dashed lines with open squares are Expanded Welch. Lower strips "
                                 "show validity."))

# =================================================================== B12 (26)
s = new_slide("Application details and comparison family", 26)
backup_label(s, "Backup B12")
lead(s, [B("Unadjusted p-values for six exploratory comparisons; Holm adjusts each method separately")], h=0.45)


def sci(m_, e):
    return [m_ + "×10", (f"−{e}", {"sup": True})]


H12 = dict(sz=19, b=True, anchor="ctr", bottom=ORANGE, bottom_w=1.5)
rows = [[dict(paras=["Dataset"], color=ORANGE, **H12), dict(paras=["Predictor"], color=ORANGE, **H12),
         dict(paras=["Normal Wald"], color=ORANGE, align="r", **H12),
         dict(paras=["Expanded Welch"], color=ORANGE, align="r", **H12)]]
fam = [("Adult", "Occupation", sci("1.184", 44), sci("1.635", 42)),
       ("Adult", "Education", sci("1.890", 34), sci("4.930", 33)),
       ("Online Shoppers", "Month", sci("4.714", 5), sci("3.726", 4)),
       ("Student Performance", "Study time", ["0.1982"], ["0.2339"]),
       ("Student Performance", "Maternal education", ["0.8361"], ["0.8468"]),
       ("Online Shoppers", "Weekend", ["0.9554"], ["0.9601"])]
for d_, pr, w_, e_ in fam:
    f = PALE_ORANGE if pr == "Month" else None
    rows.append([dict(paras=[d_], sz=19, fill=f), dict(paras=[pr], sz=19, fill=f),
                 dict(paras=[w_], sz=19, align="r", fill=f), dict(paras=[e_], sz=19, align="r", fill=f)])
table(s, 0.85, 1.85, [3.6, 3.2, 2.4, 2.4], [0.55] + [0.56] * 6, rows, name="Comparison family")
text(s, 0.85, 6.0, 11.5, 0.6, [["Holm-adjusted month p-values: Normal Wald ", B("0.000189"), "; Expanded Welch ",
                                 B("0.00149")]], sz=20, anchor="ctr", name="Adjusted values")
footer(s, "Becker and Kohavi (1996); Sakar and Kastro (2018); Cortez (2008); Holm (1979). Thesis Appendix B.7, Table B.1")
notes(s, backup_note(12,
    extra="""Groups: 1,694 sessions labelled New_Visitor (P) and 10,551 labelled Returning_Visitor (Q); the 85 Other sessions are excluded. The dataset has 12,330 sessions, each from a different user according to its documentation. Outcome: the Boolean Revenue variable.
Month: January and April have no recorded sessions, so each month table is 10×2. All ten months occur in both groups, although the new-visitor February row contains one session and no purchase. Zero cells are retained without smoothing.
Month degrees of freedom: component 12.93 (new) and 187.93 (returning); combined 26.79.
Weekend: corrected MI 0.000664 (new) and 0.000727 (returning); T = −0.056; Expanded Welch df 2.18; p-values 0.9554 (Wald) and 0.9601 (Expanded Welch). Neither test rejects, and this non-rejection does not establish equality.
Holm: order each method's six p-values from smallest to largest, multiply by 6, 5, 4, 3, 2 and 1, take the cumulative maximum and cap at one. Month is the third smallest, so its multiplier is 4.""",
    source="Thesis Section 6.4 and Appendix B.7, Table B.1; the application protocol. Becker and Kohavi (1996); Sakar and Kastro (2018); Cortez (2008); Holm (1979)."))

# =================================================================== B13-B14 (27-28)
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
    [("Welch, B. L. (1947). The generalization of “Student's” problem when several different population "
      "variances are involved. ", {}), ("Biometrika", {"i": True}),
     (", 34(1–2), 28–35. doi:10.1093/biomet/34.1-2.28", {})],
]
REFS2 = [
    [("Hutcheson, K. (1970). A test for comparing diversities based on the Shannon formula. ", {}),
     ("Journal of Theoretical Biology", {"i": True}), (", 29(1), 151–154. doi:10.1016/0022-5193(70)90124-4", {})],
    [("Pan, W. and Wall, M. M. (2002). Small-sample adjustments in using the sandwich variance estimator in "
      "generalized estimating equations. ", {}), ("Statistics in Medicine", {"i": True}),
     (", 21(10), 1429–1441. doi:10.1002/sim.1142", {})],
    [("Morris, T. P., White, I. R. and Crowther, M. J. (2019). Using simulation studies to evaluate statistical "
      "methods. ", {}), ("Statistics in Medicine", {"i": True}), (", 38(11), 2074–2102. doi:10.1002/sim.8086", {})],
    [("Sakar, C. and Kastro, Y. (2018). ", {}), ("Online Shoppers Purchasing Intention Dataset", {"i": True}),
     (". UCI Machine Learning Repository. doi:10.24432/C5F88Q", {})],
    [("Holm, S. (1979). A simple sequentially rejective multiple test procedure. ", {}),
     ("Scandinavian Journal of Statistics", {"i": True}), (", 6(2), 65–70. https://www.jstor.org/stable/4615733", {})],
]
for n, tag, title, refs in [(27, "B13", "References: MI and testing foundations", REFS1),
                            (28, "B14", "References: related methods and evaluation", REFS2)]:
    s = new_slide(title, n)
    backup_label(s, f"Backup {tag}")
    for c_, col in enumerate([refs[:3], refs[3:]]):
        text(s, 0.85 + c_ * 6.0, 1.55, 5.65, 5.3, [{"runs": r, "space_after": 14, "line": 1.0} for r in col], sz=17,
             name=f"References column {c_ + 1}")
    notes(s, "Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.")

cp = prs.core_properties
cp.title = "Comparing Mutual Information in Finite Samples"
cp.subject = "Normal Wald and Expanded Welch–Satterthwaite comparisons of mutual information"
cp.author = "Daniel Zhao"
cp.last_modified_by = "Daniel Zhao"
cp.comments = ""
prs.save(OUT)
import pptlib
for row in pptlib.EQUATION_LOG:
    if row[4] > 0.8:
        print("tight equation", row)
print("saved", OUT, len(prs.slides), "slides")
