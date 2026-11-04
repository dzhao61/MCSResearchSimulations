"""Build Daniel_Zhao_Welch_MI_Presentation.pptx from a copy of the vF2 style reference."""
import sys

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.oxml.ns import qn
from pptx.util import Pt

from pptlib import (BLACK, BLUE_LINE, BODY, COVER_ORANGE, DIVIDER, MUTED, NAVY, ORANGE, ORANGE_LINE,
                    PALE_BLUE, PALE_ORANGE, WHITE, backup_tag, circle, emu, equation, fill_text_body,
                    header_bar, hline, notes, panel_text, rect, set_title, slide_number, source_line,
                    table, text, vline)

TEMPLATE, OUT, CHARTS = sys.argv[1], sys.argv[2], sys.argv[3]

prs = Presentation(TEMPLATE)

# Keep only the cover slide from the template copy.
sld_ids = prs.slides._sldIdLst
for sld in list(sld_ids)[1:]:
    prs.part.drop_rel(sld.get(qn("r:id")))
    sld_ids.remove(sld)

CONTENT_LAYOUT = prs.slide_masters[1].slide_layouts.get_by_name("Title and Content")


def new_slide(title, n):
    s = prs.slides.add_slide(CONTENT_LAYOUT)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0:
            ph._element.getparent().remove(ph._element)
    set_title(s, title)
    slide_number(s, n)
    return s


def intro(s, runs, h=0.5, y=1.25, sz=20):
    return text(s, 0.85, y, 11.5, h, [runs], sz=sz, color=BLACK, name="Introduction",
                margins=(0.04, 0.04, 0.02, 0.02))


def B(t):
    return (t, {"b": True})


def O(t, bold=True):
    return (t, {"c": ORANGE, "b": bold})


def M(latex):
    return ("", {"math": latex})


def CM(t, **o):
    """A plain text run set in Cambria Math (Unicode maths letters), used instead of inline equations."""
    d = {"font": "Cambria Math"}
    d.update(o)
    return (t, d)


def BR():
    return ("", {"br": True})


def picture(s, name, x, y, w, h):
    return s.shapes.add_picture(f"{CHARTS}/{name}.png", emu(x), emu(y), emu(w), emu(h))


def note_main(time, finish, script, transition, cue, source):
    body = f"Time: {time} (finish by {finish})\n\nSCRIPT\n{script.strip()}\n\n"
    if transition:
        body += f"TRANSITION\n{transition.strip()}\n\n"
    body += f"DELIVERY CUE\n{cue.strip()}\n\nSOURCE\n{source.strip()}"
    return body


def note_backup(question, answer, extra, source):
    body = f"Not part of the timed talk.\n\nQUESTION ANSWERED\n{question.strip()}\n\nANSWER TO GIVE\n{answer.strip()}\n\n"
    if extra:
        body += f"NOTES\n{extra.strip()}\n\n"
    body += f"SOURCE\n{source.strip()}"
    return body


# =================================================================== Slide 1
cover = prs.slides[0]
by_name = {sh.name: sh for sh in cover.shapes}
title_ph = by_name["Title 1"]
sub_ph = by_name["Subtitle 2"]
divider = by_name["Rectangle 1040"]

title_ph.left, title_ph.top, title_ph.width, title_ph.height = emu(0.6), emu(2.05), emu(4.55), emu(1.9)
tb = title_ph.text_frame._txBody
bp = tb.find(qn("a:bodyPr"))
for c in list(bp):
    bp.remove(c)
bp.set("anchor", "b")
fill_text_body(tb, ["Comparing Mutual", "Information in", "Finite Samples"], sz=32, color=COVER_ORANGE,
               font="Aptos Display", line=0.92)

text(cover, 0.6, 4.02, 4.45, 0.8, ["Normal Wald and Expanded", "Welch–Satterthwaite Tests"], sz=19,
     color="262626", font="Aptos", name="Method subtitle", margins=(0.09, 0.04, 0.02, 0.02), line=0.95)

divider.left, divider.top, divider.width = emu(0.68), emu(5.0), emu(3.9)

sub_ph.left, sub_ph.top, sub_ph.width, sub_ph.height = emu(0.6), emu(5.15), emu(4.25), emu(1.75)
tb = sub_ph.text_frame._txBody
bp = tb.find(qn("a:bodyPr"))
for c in list(bp):
    bp.remove(c)
bp.set("anchor", "t")
fill_text_body(tb, [{"runs": [("Daniel Zhao", {"b": True})], "space_after": 4},
                    {"runs": ["Supervisor: Associate Professor Joseph T. Lizier"], "space_after": 4},
                    {"runs": ["School of Computer Science, The University of Sydney"]}],
               sz=17, color="262626", font="Aptos", line=0.95)

notes(cover, note_main(
    "0:25", "0:25",
    """My project asks whether mutual information differs between two populations when we only have finite samples. I develop an MI-specific Welch–Satterthwaite test and examine when its larger rejection cutoff improves false-positive accuracy, and what that costs in detection.""",
    "“I will start with the comparison we might want to make.”",
    "Look at the audience for the opening question. Do not read the full title and affiliation. Advance within 25 seconds.",
    "Thesis title, abstract and Chapter 1, pp. 1–3."))

# =================================================================== Slide 2
s = new_slide("Comparing association across populations", 2)
intro(s, [B("Mutual information: "), O("average reduction in uncertainty about one variable"),
          B(" obtained by observing another")], h=0.75)
text(s, 0.85, 2.05, 11.5, 0.45, [[B("Month of visit and purchase outcome")]], sz=22, name="Variables")


def group_panel(x, label, head_fill, body_fill, line):
    header_bar(s, x, 2.62, 5.9, 0.52, label, head_fill)
    rect(s, x, 3.22, 5.9, 2.75, fill=body_fill, line=line, rounded=0.05)
    gx, gy, cw, chh = x + 2.35, 3.9, 0.95, 0.36
    text(s, gx, 3.42, 2 * cw, 0.42, [[B("Purchase")]], sz=20, align="ctr", margins=(0, 0, 0, 0))
    lab = text(s, x + 0.95, gy + 0.72, 1.6, 0.42, [[B("Month")]], sz=20, align="ctr", margins=(0, 0, 0, 0))
    lab.rotation = 270
    for r in range(5):
        for c in range(2):
            rect(s, gx + c * cw, gy + r * chh, cw, chh, fill=WHITE, line=line, line_w=1.0)


group_panel(0.5, "P: new visitors", ORANGE, PALE_ORANGE, ORANGE_LINE)
group_panel(6.93, "Q: returning visitors", NAVY, PALE_BLUE, BLUE_LINE)
text(s, 0.85, 6.22, 11.5, 0.5, [[B("Does the month–purchase MI differ between these populations?")]], sz=22,
     name="Question")
source_line(s, ["Bossomaier et al. (2016); data: Sakar and Kastro (2018). Thesis Sections 1.1, 2.1 and 6.4"])
notes(s, note_main(
    "1:05", "1:30",
    """Mutual information measures the average reduction in uncertainty about one variable when we observe another. In the application later in the talk, the variables are the month of a website visit and whether that session ends in a purchase. We can measure their association separately among new visitors and returning visitors. I call their joint population distributions P and Q. The question is whether the population MI differs between those groups. It is an association question, and it does not require a causal interpretation of month. Before using observed data, however, we need a way to account for sampling uncertainty in that comparison.""",
    "“Two different sample estimates can arise even when the population MI values are equal.”",
    "Explain the definition facing the audience, then point once to each group. Do not announce the application result yet.",
    "Thesis Sections 1.1 and 2.1; Bossomaier et al. (2016). The shopping example is from Section 6.4, pp. 69–71."))

# =================================================================== Slide 3
s = new_slide("Sampling uncertainty in the MI comparison", 3)
rect(s, 2.67, 1.5, 8.0, 1.3, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.12, name="Hypothesis panel")
equation(s, 2.67, 1.5, 8.0, 1.3, r"\Delta=I(P)-I(Q),\qquad H_0:\Delta=0", sz=32, jc="center")
text(s, 0.85, 3.35, 7.7, 3.3, [
    {"runs": ["Rare category combinations may be missed or observed only once"], "bullet": True, "space_after": 16},
    {"runs": ["Errors can affect both the estimated MI difference and its standard error"], "bullet": True,
     "space_after": 16},
    {"runs": ["Under equal population MI, the intended rejection rate is ", O("5%")], "bullet": True},
], sz=24, name="Explanation")
gx, gy, c = 9.45, 3.35, 0.56
for r in range(5):
    for k in range(5):
        fill = WHITE
        if r == 3 or k == 1:
            fill = PALE_ORANGE
        if r == 3 and k == 1:
            fill = ORANGE
        rect(s, gx + k * c, gy + r * c, c, c, fill=fill, line="BFBFBF", line_w=1.0)
text(s, 8.9, 6.2, 3.9, 0.45, ["Schematic: a rare cell, its row and its column"], sz=16, color=MUTED,
     align="ctr", margins=(0, 0, 0, 0))
source_line(s, ["Thesis Chapters 1–3"])
notes(s, note_main(
    "1:00", "2:30",
    """The parameter is the signed difference, MI in P minus MI in Q, and the null hypothesis sets that difference to zero. Different samples produce different count tables, so they also produce different MI estimates. Rare combinations of categories are especially difficult because a cell can be missed in one sample and observed only once in another. These errors can change both the estimated difference and its estimated standard error. When the population MI values are equal, I want a test using the usual five-percent significance level to reject in about five percent of repetitions. That false-positive target gives us a concrete way to assess the comparison.""",
    "“The literature supplies the MI variance approximation, but choosing a Welch-type reference requires an additional calculation.”",
    "Pause after naming the null. Stress that equal MI allows different probability tables. Do not imply P = Q under every null setting.",
    "Thesis Chapters 1–3, particularly Equation (1.1) and Section 3.2."))

# =================================================================== Slide 4
s = new_slide("Existing foundations and the MI-specific contribution", 4)
hdr = dict(sz=22, color=ORANGE, b=True, bottom=ORANGE, bottom_w=1.5, anchor="b")
body = dict(sz=22, color=BLACK)
rows = [
    [dict(paras=["Part of the method"], **hdr), dict(paras=["Role in this project"], **hdr)],
    [dict(paras=["MI bias and sampling variance"], **body),
     dict(paras=["Estimate the difference and its uncertainty"], **body)],
    [dict(paras=["Welch–Satterthwaite moment matching"], **body),
     dict(paras=["Choose a reference from variance-estimator variability"], **body)],
    [dict(paras=[[B("MI-specific variance sensitivity, derived here")]], fill=PALE_ORANGE, **body),
     dict(paras=["Track changes in cell probabilities, margins and pointwise MI"], fill=PALE_ORANGE, **body)],
]
table(s, 0.85, 1.75, [5.2, 6.4], [0.62, 1.2, 1.2, 1.2], rows, name="Foundations table")
source_line(s, ["Moddemeijer (1989); Paninski (2003); Satterthwaite (1946); Welch (1947); Hutcheson (1970); "
                "Pan and Wall (2002). Thesis Sections 2.2–2.5"])
notes(s, note_main(
    "0:55", "3:25",
    """This project builds on established results rather than introducing the general Welch–Satterthwaite principle. Work on MI gives the leading bias and first-order sampling variance. Welch and Satterthwaite provide a way to choose degrees of freedom by matching variance moments, and related ideas have been used for entropy and regression comparisons. For this MI test, the additional task is to calculate how the estimated pointwise-MI variance changes when the table changes. I derive that sensitivity while allowing the cell probabilities, row totals and column totals to change together, then evaluate the resulting approximation.""",
    "“The resulting test keeps the same statistic as Wald and changes the reference distribution used to judge it.”",
    """Spend most of the slide on the final row. Say what each strand provides; do not recite every citation or claim that no equivalent formula has ever appeared anywhere.
Mora and Ruiz-Castillo (2009) is the direct normal-approximation precedent for MI comparisons, if asked.""",
    "Thesis Sections 2.2–2.5, pp. 6–17. Moddemeijer (1989); Paninski (2003); Satterthwaite (1946); Welch (1947); Hutcheson (1970); Pan and Wall (2002); Mora and Ruiz-Castillo (2009)."))

# =================================================================== Slide 5
s = new_slide("Normal Wald and Expanded Welch", 5)
intro(s, [B("Same estimates and statistic, "), O("larger rejection cutoff")])
rect(s, 0.5, 1.8, 12.33, 1.82, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.08, name="Equation panel")
equation(s, 1.0, 1.84, 4.2, 1.28, r"T=\frac{\widehat\Delta_{\mathrm{BC}}}{\widehat{\mathrm{SE}}}", sz=28, jc="center")
text(s, 1.0, 3.13, 4.2, 0.4, ["BC: leading bias correction"], sz=18, color=BODY, align="ctr",
     margins=(0, 0, 0, 0), name="BC definition")
equation(s, 5.6, 1.84, 6.8, 1.7,
         r"\widehat{\mathrm{SE}}^2=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}", sz=28, jc="center")
header_bar(s, 0.5, 3.85, 4.95, 0.5, "Normal Wald", ORANGE)
p = rect(s, 0.5, 4.41, 4.95, 0.75, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.08)
panel_text(p, ["Standard normal reference"], sz=22, anchor="ctr")
header_bar(s, 0.5, 5.32, 4.95, 0.5, "Expanded Welch", NAVY)
p = rect(s, 0.5, 5.88, 4.95, 0.98, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.08)
panel_text(p, ["Student t reference with estimated degrees of freedom"], sz=22, anchor="ctr")
picture(s, "slide05_reference_distributions", 5.78, 3.8, 7.05, 3.15)
text(s, 5.85, 3.78, 3.6, 0.4, [[("Illustration", {"b": True})]], sz=18, color=MUTED, margins=(0, 0, 0, 0))
source_line(s, ["Illustrative Student t distribution with 3 degrees of freedom. Thesis Sections 3.2–3.3 and 4.1–4.3"])
notes(s, note_main(
    "1:10", "4:35",
    """Both methods divide the MI difference, after its leading bias correction, by the same estimated standard error. The denominator adds a variance contribution from each independent sample. Pointwise MI is the information contribution of one category pair. V-hat estimates its variance, and dividing by sample size estimates the sampling variance of an MI estimate. Wald compares the statistic with the standard normal distribution. Expanded Welch uses a Student t distribution, whose degrees of freedom are estimated from the data. The example with three degrees of freedom shows why heavier tails give a larger rejection cutoff. Consequently, Expanded Welch's rejections are a subset of Wald's under these testing rules. The next question is how to calculate the degrees of freedom for MI.""",
    "“The important input is how much the variance estimate itself changes from sample to sample.”",
    """Trace the common numerator and denominator once. Point to the cutoff locations. Explain that the reference plot's three degrees of freedom are illustrative; actual values vary between sampled table pairs. Expanded Welch also needs valid degrees-of-freedom calculations; the additional validity requirements are introduced on Slide 7 and specified in B4.""",
    "Thesis Sections 3.2–3.3 and 4.1–4.3; Figure 2.1."))

# =================================================================== Slide 6
s = new_slide("Deriving the degrees of freedom", 6)
rows6 = [
    (1.5, 1.6, "1", "Sensitivity of the pointwise-MI variance",
     r"g_P(x,y)=\left.\frac{\mathrm d V(P_\varepsilon)}{\mathrm d\varepsilon}\right|_{\varepsilon=0}", 26),
    (3.25, 1.3, "2", "Sampling variation of its estimate",
     r"\operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P},\qquad \tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}", 23),
    (4.7, 1.3, "3", "Component degrees of freedom",
     r"\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}", 26),
]
for y, h, num, label, latex, esz in rows6:
    rect(s, 0.5, y, 12.33, h, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.08)
    circle(s, 0.75, y + h / 2 - 0.3, 0.6, num, ORANGE, sz=22)
    if num == "1":
        text(s, 1.55, y + 0.12, 3.75, h - 0.2, [
            {"runs": [B(label)], "space_after": 6},
            {"runs": [CM("\U0001D443"), CM("\U0001D700", sub=True), " moves a small amount of probability towards cell (",
                      CM("\U0001D465, \U0001D466"), ")"], "sz": 18, "color": BODY},
        ], sz=22, anchor="ctr")
        equation(s, 5.35, y + 0.1, 4.5, h - 0.2, latex, sz=esz, jc="left")
        text(s, 9.95, y + 0.25, 2.75, h - 0.5, [[("Track joint, row and column changes together",
                                                  {"c": ORANGE, "b": True})]], sz=18, anchor="ctr")
    else:
        text(s, 1.55, y + 0.1, 3.2, h - 0.2, [[B(label)]], sz=22, anchor="ctr")
        equation(s, 4.92, y + 0.08, 7.8, h - 0.16, latex, sz=esz, jc="left")
text(s, 0.85, 6.25, 11.6, 0.5, [["Repeat for Q and combine the components using ",
                                 O("Welch\u2013Satterthwaite moment matching")]], sz=20, name="Combine")
source_line(s, ["Satterthwaite (1946); Welch (1947). Thesis Sections 4.1–4.3"])
notes(s, note_main(
    "2:00", "6:35",
    """There are two levels of variability here. V-hat describes variation in pointwise MI across observation outcomes, but V-hat itself also changes when a new sample gives a different table. I first calculate its sensitivity to moving a small amount of probability towards one cell. That change affects the selected cell, its row and column totals, and the pointwise-MI values. The derivative g collects those effects.

Averaging the observation-level sensitivities gives a first-order approximation to the sampling error of V-hat. Its sampling variance is therefore approximately tau-squared divided by sample size. I then use Satterthwaite moment matching: twice the squared mean of a variance estimate, divided by that estimate's sampling variance. Substituting the sample-based inputs gives the component formula at the bottom. Greater fluctuation relative to the squared mean gives fewer degrees of freedom and a larger cutoff. I repeat the calculation for Q and combine the components. This is an approximate Student t reference, so the experiments must check how well these steps work.""",
    "“I checked the variance approximations first, then evaluated false positives and power using populations whose MI values are known.”",
    """Use the full two minutes. Pause at each change of level of variance. The final formula gives component degrees of freedom, not the combined degrees of freedom. Do not suggest that moment matching proves the numerator and denominator are independent. If asked for the exact derivative, show Backup B1.""",
    "Thesis Sections 4.1–4.3, pp. 23–35 (definition of g, final form of g, sampling variance of V-hat, component moment target, estimated component df, combined df)."))

# =================================================================== Slide 7
s = new_slide("Evaluation from known populations", 7)
header_bar(s, 0.5, 1.55, 6.6, 0.52, "Research questions", NAVY)
rect(s, 0.5, 2.13, 6.6, 3.82, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
rq = [("RQ1: Approximation accuracy", ["Mean and sampling variance of ", CM("\U0001D449\u0302"), ", including near independence"]),
      ("RQ2: False positives", ["Equal MI: 0.005, 0.02 and 0.30 nats"]),
      ("RQ3: Power", ["MI in P = 0.02; gaps of 0.005, 0.01 and 0.02 nats"])]
for i, (lab, comp) in enumerate(rq):
    y = 2.28 + i * 1.2
    text(s, 0.72, y, 6.2, 1.05, [
        {"runs": [(lab, {"b": True, "c": NAVY})], "space_after": 2},
        {"runs": comp},
    ], sz=20)
    if i < 2:
        hline(s, 0.75, y + 1.12, 6.1, color=BLUE_LINE)
header_bar(s, 7.35, 1.55, 5.48, 0.52, "Shared settings", ORANGE)
p = rect(s, 7.35, 2.13, 5.48, 3.82, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.05)
panel_text(p, [
    {"runs": ["Four table sizes: 2×2, 4×4, 8×8, 16×16"], "bullet": True, "space_after": 12},
    {"runs": ["Uniform, same-skew and different-skew margins"], "bullet": True, "space_after": 12},
    {"runs": ["Ten sample sizes, 10 to 50,000 observations per population"], "bullet": True, "space_after": 12},
    {"runs": ["100,000 independent table pairs per setting"], "bullet": True},
], sz=20, anchor="ctr", margins=(0.25, 0.2, 0.12, 0.12))
text(s, 0.85, 6.12, 11.5, 0.75, ["Both methods use each same pair of sampled tables. Invalid outputs count as "
                                 "non-rejections; validity is reported."], sz=18, color=BODY, name="Design note")
source_line(s, ["Morris et al. (2019). Thesis Chapter 5, Tables 5.1–5.3; construction and validity rules in Appendix B"])
notes(s, note_main(
    "1:15", "7:50",
    """I construct population tables with known MI, then draw repeated samples. MI is reported in nats, using natural logarithms. The first study checks the variance approximations. The false-positive study uses three equal-MI levels, while power fixes MI in P at 0.02 nats and gives Q three larger MI values. Both studies cross four table sizes and ten sample sizes with uniform or uneven margins. The uneven margins either agree between populations or differ, giving 360 settings each for false positives and power. Each test sees only its two sampled tables. The 100,000 repetitions measure performance rather than increasing that test's sample size. Both tests use the same sampled pairs, with invalid calculations counted as non-rejections and validity reported separately.""",
    "“The first result concerns the inputs to the degrees of freedom, before any test rejection is considered.”",
    """Explain “same skew” as the same uneven margins in both populations and “different skew” as different category frequencies. Do not recite all ten sample sizes or every margin probability. Full margin vectors and the sample-size list are in B3.""",
    "Thesis Chapter 5, pp. 39–46, Tables 5.1–5.3; Morris et al. (2019). Exact construction and validity rules: Appendix B."))

# =================================================================== Slide 8
s = new_slide("Sparse samples distort the variance inputs", 8)
intro(s, [B("Different-skew P, 16×16, population MI 0.02 nats")])
text(s, 0.55, 1.85, 5.95, 0.45, [[O("Mean estimate / population variance")]], sz=20, name="Left heading")
text(s, 6.83, 1.85, 6.25, 0.45, [[O("Variance prediction / observed sampling variance")]], sz=20,
     name="Right heading")
picture(s, "slide08_mean_ratio", 0.55, 2.33, 5.95, 3.75)
picture(s, "slide08_variance_ratio", 6.83, 2.33, 5.95, 3.75)
vline(s, 6.67, 2.0, 4.0, color=DIVIDER)
text(s, 0.85, 6.22, 11.5, 0.5, [["One indicates agreement. Errors affect both parts of the degrees-of-freedom "
                                 "calculation."]], sz=20, name="Interpretation")
source_line(s, ["Illustrative slice of the RQ1 study. Thesis Section 6.1.1, Figure 6.1. Bands: 95% Monte Carlo intervals"])
notes(s, note_main(
    "1:20", "9:10",
    """This slide isolates one population and table size so the two errors are visible. On the left, one would mean that the average V-hat equals the population quantity. Instead, the mean rises well above that benchmark before recovering. Rare cells that begin to appear can have large empirical pointwise-MI deviations and inflate the estimate.

On the right, one means that the predicted sampling variance of V-hat agrees with the variance observed across repetitions. The population first-order prediction falls below one over the sparse range. Estimating its inputs from each sample can reverse the error and overshoot. Since degrees of freedom square the mean input and divide by the sampling variance input, both errors matter. Larger samples improve the agreement in this fixed population.""",
    "“Near independence, sampling noise causes an additional separation between the population formula and the sample-based result.”",
    """Explain the left graph completely before moving right. Say “sampling variance of V-hat” explicitly. Do not call the right graph the sampling variance of the MI estimator. Avoid narrating every marker.""",
    "Thesis Section 6.1.1, pp. 47–50; Figure 6.1. At n = 50: mean ratio 12.71; population-input ratio 0.186; sample-based ratio 0.553."))

# =================================================================== Slide 9
s = new_slide("Sampling noise matters near independence", 9)
intro(s, [B("Different-skew P, 4×4, n = 1,000 per population")])
picture(s, "slide09_near_independence_df", 0.55, 1.85, 8.3, 4.85)
header_bar(s, 8.98, 1.9, 3.85, 0.52, "Near independence", ORANGE)
p = rect(s, 8.98, 2.48, 3.85, 4.2, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.06)
panel_text(p, [
    {"runs": [B("At MI 0.0001:")], "space_after": 6},
    {"runs": ["mean estimate about\u00a05"], "bullet": True, "space_after": 4},
    {"runs": ["first-order value about\u00a00.1"], "bullet": True, "space_after": 22},
    {"runs": [O("Quadratic sampling variation creates apparent association")]},
], sz=20, anchor="ctr", margins=(0.2, 0.15, 0.12, 0.12))
source_line(s, ["Thesis Section 6.1.3, Figure 6.3; Appendix A.2. Bands: 95% Monte Carlo intervals"])
notes(s, note_main(
    "1:30", "10:40",
    """Here sample size stays at one thousand and the population MI approaches zero. The black population first-order value becomes very small, but the mean degrees of freedom estimated from sampled tables remain around five at the weakest association. The green curve is the moment-matching target calculated from the actual sampling mean and variance. That target is about nine, so the mean estimate is still only about half the target.

A sampled table can show apparent association even when population association is almost absent. The sample-based variance and sensitivity retain that noise. Near independence, the linear sampling contribution becomes small, so quadratic sampling terms matter. The additional calculation in the thesis explains why the estimated degrees of freedom stay positive rather than following the shrinking population value. This is a check on the approximation, not a proof of an exact Student t distribution or a validated replacement test at independence.""",
    "“These approximation errors matter because the larger cutoff lowers rejection, and that reduction is not equally helpful everywhere.”",
    """Point to the low-MI end before describing the curves. Pause after “around five”. Explain the target's role rather than reading three symbols. Keep this slide in the shorter route.""",
    "Thesis Section 6.1.3, pp. 52–56, Figure 6.3 and Appendix A.2. At MI 0.0001, saved P values: mean df 4.859787, moment target 9.124808, population first-order df 0.096400. These are component quantities."))

# =================================================================== Slide 10
s = new_slide("The benefit depends on Wald's false-positive rate", 10)
intro(s, [B("Equal population MI = 0.02 nats; target false-positive rate = "), O("5%")])
H = dict(sz=20, b=True, anchor="ctr", bottom=None)
hdr_cells = [dict(paras=["Illustrative setting"], color=ORANGE, **H),
             dict(paras=["Normal Wald"], color=WHITE, fill=ORANGE, align="ctr", **H),
             dict(paras=["Expanded Welch"], color=WHITE, fill=NAVY, align="ctr", **H),
             dict(paras=["Interpretation"], color=BLACK, **H)]
R = dict(sz=22, anchor="ctr")
data10 = [(["Uniform 4\u00d74", BR(), "n = 20"], "8.35%", "4.90%", "Closer to 5%", PALE_ORANGE),
          (["Same skew 16\u00d716", BR(), "n = 1,000"], "0.60%", "0.53%", "Further below 5%", None),
          (["Different skew 16\u00d716", BR(), "n = 1,000"], "26.01%", "24.84%", "Still far above 5%", None)]
rows = [hdr_cells]
for i, (setting, w, e, interp, fill) in enumerate(data10):
    rows.append([dict(paras=[setting], fill=fill, **R),
                 dict(paras=[w], align="ctr", fill=fill, **R),
                 dict(paras=[[B(e)]] if i == 0 else [e], align="ctr", fill=fill, **R),
                 dict(paras=[interp], fill=fill, **R)])
table(s, 0.85, 1.95, [4.0, 2.2, 2.4, 3.0], [0.62, 1.05, 1.05, 1.05], rows, name="Illustrative null rates")
text(s, 0.85, 5.95, 11.5, 0.5, ["Both methods are valid in all 100,000 repetitions in each example."], sz=20,
     name="Validity note")
source_line(s, ["Illustrative diagnostic rows from the balanced null grid. Thesis Section 6.2.4, Table 6.1"])
notes(s, note_main(
    "1:20", "12:00",
    """I assess false-positive accuracy by closeness to five percent. The first row shows the useful case: Expanded Welch brings Wald's excessive rejection from 8.35 percent to 4.90 percent. In the second row, Wald already rejects too rarely, and the larger cutoff lowers rejection further. The third row shows a more serious failure: rejection stays around a quarter of repetitions even after the cutoff increases.

These examples have no calculation failures. Their different behaviour comes from the shared estimates and the sampling distribution of the statistic. In particular, different remaining biases can shift the MI difference away from zero under equal MI. A larger cutoff can offset some errors at a particular setting without making inference accurate across populations.""",
    "“The full experiment also changes the common MI, while keeping the population difference at zero.”",
    """Take one row at a time. Point back to the same 5% target for each row. Do not describe the table as three predetermined focus settings or as evidence of universal improvement.""",
    "Thesis Section 6.2.4 and Table 6.1, p. 62. Combined balanced-null rates."))

# =================================================================== Slide 11
s = new_slide("False-positive rates across common MI values", 11)
intro(s, [B("16×16, different-skew margins; equal MI in P and Q")])
picture(s, "slide11_null_rates", 0.55, 1.8, 12.2, 4.75)
text(s, 0.85, 6.52, 11.5, 0.45, ["Both methods are valid in every repetition at this point"], sz=20,
     name="Validity note")
source_line(s, ["Thesis Section 6.2.3, Figure 6.6. Bands: pointwise 95% Monte Carlo intervals"])
notes(s, note_main(
    "1:10", "13:10",
    """This panel keeps equal MI in the two populations but changes the common level of association. Colour identifies that common MI, and line style identifies the method. At the weakest MI and one thousand observations per population, Wald rejects in 36.38 percent of repetitions and Expanded Welch in 34.38 percent. The validity strip shows that both methods return usable results in every repetition there. The failure is inferential.

With more observations, rejection falls, and the weakest-MI curve is below the target at the largest tested sample size. The experiment can therefore pass through excessive and conservative ranges. The larger cutoff lowers rejection throughout, but it does not by itself solve either problem.""",
    "“The same larger cutoff also affects the probability of detecting a genuine MI difference.”",
    """Introduce axes and encodings before pointing to the peak. Say which common MI the highlighted values use. Avoid presenting 36.38% as the MI-0.02 value from Slide 10. The shaded bands describe Monte Carlo uncertainty at each point, not simultaneous confidence over the full grid.""",
    "Thesis Section 6.2.3, pp. 60–61; Figure 6.6. Balanced-null combined rates, 16×16, different skew, all repetitions as denominator. No threshold fitting is involved."))

# =================================================================== Slide 12
s = new_slide("Power across three MI differences", 12)
intro(s, [B("Uniform 4×4; MI in P = 0.02 nats; "), ("usual 0.05 p-value threshold for both methods", {})])
picture(s, "slide12_power", 0.55, 1.8, 12.2, 4.2)
text(s, 1.72, 3.2, 5.4, 0.42, [[("Power: rejection when population MI differs", {"b": True, "c": BODY})]],
     sz=18, name="Power definition", margins=(0, 0, 0, 0))
text(s, 0.85, 6.08, 11.5, 0.85, [["With sufficient observations, larger MI gaps are easier to detect. ",
                                  O("Expanded Welch has a lower or equal rejection rate.")]], sz=20,
     name="Interpretation")
source_line(s, ["Thesis Section 6.3.1, Figure 6.7. Bands: pointwise 95% Monte Carlo intervals"])
notes(s, note_main(
    "1:05", "14:15",
    """Power is the probability of rejecting equal MI when the population MI values differ. Colour now identifies the magnitude of the MI gap. P stays at 0.02 nats, and Q's MI increases to create the three gaps. Once samples are sufficiently large, the larger differences become easier to detect. Expanded Welch remains at or below Wald because its cutoff is larger, with the method curves becoming close at larger sample sizes.

These are power rates under the usual testing rules. Because actual false-positive rates can differ, they do not compare power at a common achieved false-positive rate. The next example also shows why a two-sided rejection can conceal an important error in direction.""",
    "“In sparse tables with different margins, bias can even make the estimated difference point towards the wrong population.”",
    """Explicitly announce the change in colour meaning from Slide 11: colour now means MI-gap magnitude. Do not interpret close curves as a plotting failure or claim Expanded Welch has higher nominal power anywhere.""",
    "Thesis Section 6.3.1, pp. 63–65, Figure 6.7; MI-gap combined rates, 4×4, uniform, all repetitions as denominator."))

# =================================================================== Slide 13
s = new_slide("Bias can reverse the estimated direction", 13)
intro(s, [B("Different-skew 16×16; MI 0.02 versus 0.03 nats")])
picture(s, "slide13_direction_power", 0.55, 1.85, 8.05, 4.9)
header_bar(s, 8.85, 1.9, 3.98, 0.52, "At n = 1,000 per population", NAVY, sz=20)
rect(s, 8.85, 2.48, 3.98, 4.27, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
text(s, 9.05, 2.6, 3.6, 0.38, ["True difference"], sz=18, color=BODY, margins=(0, 0, 0, 0))
text(s, 9.05, 2.95, 3.6, 0.6, [[B("−0.0100 nats")]], sz=30, margins=(0, 0, 0, 0))
text(s, 9.05, 3.6, 3.6, 0.38, ["Mean estimated difference"], sz=18, color=BODY, margins=(0, 0, 0, 0))
text(s, 9.05, 3.95, 3.6, 0.6, [[B("+0.0207 nats")]], sz=30, margins=(0, 0, 0, 0))
hline(s, 9.05, 4.68, 3.58, color=BLUE_LINE)
text(s, 9.05, 4.76, 3.65, 1.25, [[O("Among Expanded Welch rejections"), ", over 99.9% have the opposite estimated "
                                  "direction"]], sz=19, margins=(0, 0, 0, 0))
text(s, 9.05, 6.0, 3.65, 0.7, [[B("Unequal residual biases can outweigh the true gap")]], sz=19,
     margins=(0, 0, 0, 0))
source_line(s, ["9,659 of 9,662 Expanded Welch rejections at n = 1,000 have a positive estimated difference. "
                "Thesis Section 6.3.3, Figure 6.9"])
notes(s, note_main(
    "1:30", "15:45",
    """This example fixes a true difference of minus 0.01 nats, so Q has greater population MI. At one thousand observations per population, however, the average estimated difference is about plus 0.0207 nats. Different residual biases in the two MI estimates have outweighed the true gap and shifted the sampling centre to the other side of zero.

Expanded Welch rejects in about 9.66 percent of repetitions at this point. Among those rejections, more than 99.9 percent have a positive estimated difference, opposite to the population direction. They count as power under the two-sided definition, but they fail to identify which population has greater MI. As sample size increases, the positive bias diminishes, the centre passes near zero, and rejection initially falls before recovering. Changing the cutoff leaves that biased movement unchanged.""",
    "“The shopping data illustrate the same calculation, although their unknown population values prevent this kind of accuracy check.”",
    """Explain the two signed numbers before citing the percentage. Emphasise “among those rejections”. The bias is approximately 0.0306714 nats; the estimated mean is −0.01 plus that bias. Do not describe a positive estimate as higher true MI in P.""",
    "Thesis Section 6.3.3, pp. 67–69; Figure 6.9. Saved counts: 9,659 positive and 3 negative Expanded Welch rejections, 9,662 in total, out of 100,000 repetitions."))

# =================================================================== Slide 14
s = new_slide("An application to online shopping", 14)
intro(s, [B("Does month–purchase MI differ between new and returning visitors?")])
text(s, 0.55, 1.9, 6.9, 0.45, [[O("Corrected MI estimate (nats)"), ("   point estimates", {"c": MUTED, "sz": 18})]],
     sz=21, name="Chart heading")
cd = CategoryChartData()
cd.categories = ["New visitors\n(n = 1,694)", "Returning visitors\n(n = 10,551)"]
cd.add_series("Corrected MI estimate (nats)", (0.0043163111573871, 0.0178797492702181))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, emu(0.55), emu(2.4), emu(7.0), emu(3.85), cd)
gf.name = "Corrected MI chart"
ch = gf.chart
ch.has_legend = False
ch.has_title = False
ch.font.name = "Lato"
ch.font.size = Pt(20)
ch.font.color.rgb = RGBColor.from_string(BODY)
plot = ch.plots[0]
plot.gap_width = 70
plot.vary_by_categories = False
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = "0.0000"
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(22)
dl.font.bold = True
dl.font.color.rgb = RGBColor.from_string(BLACK)
ser = plot.series[0]
for idx, col in enumerate([ORANGE, NAVY]):
    pt = ser.points[idx]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = RGBColor.from_string(col)
va = ch.value_axis
va.minimum_scale = 0
va.maximum_scale = 0.02
va.major_unit = 0.005
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor.from_string("E6E6E6")
va.tick_labels.number_format = "0.000"
va.tick_labels.number_format_is_linked = False
va.tick_labels.font.size = Pt(18)
va.format.line.fill.background()
ca = ch.category_axis
ca.tick_labels.font.size = Pt(19)
ca.format.line.color.rgb = RGBColor.from_string("888888")
header_bar(s, 7.95, 1.9, 4.88, 0.52, "Test result", NAVY)
p = rect(s, 7.95, 2.48, 4.88, 3.77, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
text(s, 8.18, 2.62, 4.45, 0.38, ["Estimated difference, new minus returning"], sz=17, color=BODY,
     margins=(0, 0, 0, 0))
text(s, 8.18, 3.02, 4.45, 0.62, [[B("\u22120.0136 nats")]], sz=30, margins=(0, 0, 0, 0))
hline(s, 8.18, 3.8, 4.42, color=BLUE_LINE)
text(s, 8.18, 3.95, 4.45, 0.95, [["Both tests reject after ", O("Holm adjustment"), " across six comparisons"]],
     sz=20, margins=(0, 0, 0, 0))
text(s, 8.18, 5.05, 4.45, 0.9, [["Expanded Welch adjusted", BR(), ("p", {"i": True}), " = ", B("0.00149")]], sz=20,
     margins=(0, 0, 0, 0))
text(s, 0.85, 6.4, 11.5, 0.45, [[B("Observed-data illustration; population MI is unknown")]], sz=20,
     name="Caveat")
source_line(s, ["Data: Sakar and Kastro (2018), UCI Machine Learning Repository. Holm (1979). Thesis Section 6.4, "
                "Tables 6.2–6.3"])
notes(s, note_main(
    "1:15", "17:00",
    """Returning to the shopping question, I compare the association between month and purchase outcome among new and returning visitors. The corrected MI estimate is higher for returning visitors, giving a negative difference when I subtract returning-visitor MI from new-visitor MI. Both methods reject equal MI, including after Holm adjustment across the six exploratory comparisons. Expanded Welch's adjusted p-value is about 0.00149.

This is evidence from the approximate tests for a difference in month–purchase MI. It is not a causal claim about month. Unlike the simulations, the population tables are unknown, so this application illustrates how to use and interpret the outputs without measuring their false-positive accuracy. The weekend comparison does not reject equality, which also does not establish equality.""",
    "“The application makes the practical limits important, so I will finish by distinguishing the contribution from what remains to test.”",
    """Keep the emphasis on association, signed difference and adjusted inference. Keep the group sizes out of the main spoken comparison. Explain the six-comparison family if asked (B10). Do not claim Holm adjustment repairs the test's approximation errors.""",
    "Thesis Section 6.4, pp. 69–71, Tables 6.2–6.3 and Appendix B.7. Sakar and Kastro (2018); Holm (1979). Corrected MI 0.004316 (new) and 0.017880 (returning); difference −0.013563; Expanded Welch df 26.79; Holm-adjusted p 0.000189 (Wald) and 0.00149 (Expanded Welch)."))

# =================================================================== Slide 15
s = new_slide("Limitations and future work", 15)
header_bar(s, 0.5, 1.6, 5.9, 0.56, "Present limit", ORANGE)
header_bar(s, 6.93, 1.6, 5.9, 0.56, "Next investigation", NAVY)
lim = [("First-order approximation near independence", "Retain the additional quadratic sampling variation"),
       ("Bias and errors in the shared standard error", "Evaluate improved estimates one at a time"),
       ("One population construction; equal simulation sample sizes",
        "Test other association patterns and unequal sample sizes")]
C = dict(sz=22, anchor="ctr", ml=0.2, mr=0.2)
rows = [[dict(paras=[a], **C), dict(paras=[b], **C)] for a, b in lim]
table(s, 0.5, 2.25, [6.43, 5.9], [1.25, 1.25, 1.25], rows, name="Limits table")
source_line(s, ["Thesis Sections 7.2–7.3"])
notes(s, note_main(
    "1:00", "18:00",
    """The first limitation is the first-order approximation, particularly near independence, where additional quadratic sampling variation becomes important. The second is estimation: changing the reference cutoff leaves errors in the MI difference and standard error in place. A useful next step is to change one estimator at a time and check how that affects rejection and direction.

The experiments also use one copying construction and equal sample sizes. They vary several important parameters within that family, but they do not establish performance across every association pattern. Other constructions and unequal sample sizes would test how broadly the findings persist.""",
    "“The project therefore establishes a specific calculation and a clear boundary on what its cutoff adjustment can accomplish.”",
    "Use the paired rows to show why each proposed extension makes sense. Keep to one minute and protect time for the conclusion. Explain unshown limits in the question period.",
    "Thesis Sections 7.2–7.3, pp. 74–75."))

# =================================================================== Slide 16
s = new_slide("Contributions and conclusions", 16)
header_bar(s, 0.5, 1.6, 12.33, 0.52, "Contributions", NAVY)
blocks = [["Derived MI-specific ", B("variance sensitivity"), " and degrees of freedom"],
          ["Improved ", B("some"), " excessive false-positive rates, with a reduction in power"],
          ["Sparse-table failures identify ", B("estimation accuracy"), " as a priority"]]
for i, runs in enumerate(blocks):
    x = 0.5 + i * (3.97 + 0.21)
    rect(s, x, 2.3, 3.97, 3.6, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
    circle(s, x + 3.97 / 2 - 0.32, 2.55, 0.64, str(i + 1), NAVY, sz=22)
    text(s, x + 0.25, 3.4, 3.47, 2.3, [runs], sz=24, color=NAVY, align="ctr", anchor="t")
text(s, 0.85, 6.2, 11.6, 0.5, ["Thank you"], sz=20, color=MUTED, align="ctr", name="Thank you")
notes(s, note_main(
    "0:50", "18:50",
    """I derived how the estimated pointwise-MI variance responds to changes in a count table and used that sensitivity to calculate MI-specific degrees of freedom. The resulting larger cutoff brings some excessive false-positive rates closer to five percent, but also deepens conservatism and reduces power under the usual testing rules.

The sparse-table failures show why the estimates themselves remain important. A different cutoff leaves bias and standard-error errors unchanged. The contribution is therefore both the calculation and the evidence identifying its limits. Thank you, and I welcome your questions.""",
    None,
    "Face the audience for the final statements. Do not rush through “some” or imply a general recommendation. Stop at approximately 18:50 with this slide still displayed, and keep it on screen when questions begin.",
    "Final abstract; Sections 1.3 and 7.1–7.3."))

# =================================================================== B1
s = new_slide("Variance sensitivity", 17)
backup_tag(s, "Backup B1")
text(s, 0.85, 1.25, 4.4, 0.6, [[B("Perturbation towards one cell:")]], sz=22, anchor="ctr")
equation(s, 5.05, 1.22, 6.5, 0.66, r"P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}", sz=24)
rect(s, 0.5, 2.0, 12.33, 3.15, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.06, name="Equation panel")
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
source_line(s, ["Exact for positive population tables; its use for sampling errors is first order. Thesis Chapter 4"])
notes(s, note_backup(
    "What exactly did you differentiate, and where do the margin terms enter?",
    """“I differentiate the pointwise-MI variance along a one-observation perturbation. The first part changes the probability weights. The bracket also changes the log ratios, including their row and column margins. Both contributions are necessary because the pointwise-MI values themselves depend on the table.”""",
    """Regularity assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. Positive MI alone does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.""",
    "Thesis Chapter 4: perturbation path, final form of g and definition of tau-squared. The derivative is exact for positive population tables; its use for sampling errors is first order."))

# =================================================================== B2
s = new_slide("Moment matching and the combined reference", 18)
backup_tag(s, "Backup B2")
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
text(s, 0.85, 6.12, 11.5, 0.8, ["Moment matching does not establish the normality or independence needed for an "
                                "exact Student t distribution."], sz=20, name="Caveat")
source_line(s, ["Satterthwaite (1946). Thesis Sections 4.1 and 4.3"])
notes(s, note_backup(
    "Where do the component and combined degrees-of-freedom formulas come from, and why is the Student t reference approximate?",
    """“A scaled chi-squared variable has variance twice its squared mean divided by its degrees of freedom. Matching those two moments gives the target. Dividing V-hat by fixed sample size rescales the squared mean and variance equally, so it leaves the component target unchanged. Independence between the two samples lets their variance contributions add. The resulting Student t reference still requires empirical assessment.”""",
    """Scaled chi-squared derivation: take E{V-hat} times chi-squared(nu) divided by nu. Its mean is E{V-hat}, because a chi-squared variable with nu degrees of freedom has mean nu. Its variance is [E{V-hat}]^2 times 2 nu divided by nu^2, which is 2[E{V-hat}]^2 / nu. Setting that equal to Var{V-hat} gives nu_mom = 2[E{V-hat}]^2 / Var{V-hat}. Substituting V-hat for the mean and tau-hat-squared / n for the sampling variance gives the estimated component formula.""",
    "Thesis Sections 4.1 and 4.3, pp. 23–35; Satterthwaite (1946)."))

# =================================================================== B3
s = new_slide("Population construction and parameter grid", 19)
backup_tag(s, "Backup B3")
rect(s, 0.5, 1.4, 12.33, 1.0, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.1)
equation(s, 0.8, 1.42, 11.8, 0.96,
         r"p_{ij}(\lambda)=(1-\lambda)a_i a_j+\lambda a_i\mathbf 1\{i=j\},\qquad 0\leq\lambda<1", sz=26,
         jc="center")
text(s, 0.85, 2.45, 2.3, 0.5, ["Margin vector:"], sz=20, anchor="ctr")
equation(s, 3.0, 2.45, 8.5, 0.5, r"m_k(\rho)=(\rho,\,(1-\rho)/(k-1),\,\ldots,\,(1-\rho)/(k-1))", sz=20)
K = dict(sz=19, b=True, color=ORANGE, anchor="ctr")
V = dict(sz=19, anchor="ctr")


def mk(rho):
    return [("m", {"i": True}), ("k", {"i": True, "sub": True}), (f"({rho})", {})]


grid = [
    ("Table size, k", ["2, 4, 8, 16"]),
    ("Sample size, n", ["10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000, 50,000"]),
    ("Uniform", ["Both margins uniform in both populations"]),
    ("Same skew", ["P and Q each use "] + mk(0.8)),
    ("Different skew", ["P uses "] + mk(0.7) + ["; Q uses "] + mk(0.8)),
    ("Null", ["Common MI 0.005, 0.02, 0.30 nats"]),
    ("Power", ["P MI 0.02; Q MI 0.025, 0.03, 0.04 nats"]),
]
rows = [[dict(paras=[k], **K), dict(paras=[v], **V)] for k, v in grid]
table(s, 0.85, 3.0, [2.9, 8.7], [0.53] * 7, rows, name="Parameter grid")
source_line(s, ["Thesis Section 5.1, Tables 5.1–5.2; Appendix B.1–B.2"])
notes(s, note_backup(
    "How are different tables constructed at a known MI, and what parameter combinations were evaluated?",
    """“The construction mixes an independent draw with a copying draw. It preserves the specified margins, while the copying probability controls association. I solve separately for the copying probability in each population to reach the target MI. The full grid is evaluated at every null MI and power-gap value; it is not a selection of favourable cases.”""",
    "The construction is one controlled association family, not a representation of every possible categorical joint distribution.",
    "Thesis Section 5.1, Tables 5.1–5.2 and Appendix B.1–B.2."))

# =================================================================== B4
s = new_slide("Validity and rejection denominators", 20)
backup_tag(s, "Backup B4")
header_bar(s, 0.5, 1.5, 6.2, 0.5, "Normal Wald is valid with", ORANGE)
p = rect(s, 0.5, 2.05, 6.2, 2.05, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.05)
text(s, 0.7, 2.15, 5.85, 1.9, [
    {"runs": ["a finite difference and finite positive standard error"], "bullet": True, "space_after": 6},
    {"runs": [CM("\U0001D449\u0302(\U0001D443) + \U0001D449\u0302(\U0001D444) > 10"), CM("\u221214", sup=True)],
     "bullet": True, "space_after": 6},
    {"runs": ["a finite p-value"], "bullet": True},
], sz=20, anchor="ctr")
header_bar(s, 0.5, 4.3, 6.2, 0.5, "Expanded Welch is valid with", NAVY)
p = rect(s, 0.5, 4.85, 6.2, 1.95, fill=PALE_BLUE, line=BLUE_LINE, rounded=0.05)
panel_text(p, [
    {"runs": ["the Wald requirements"], "bullet": True, "space_after": 6},
    {"runs": ["positive finite component and combined degrees of freedom"], "bullet": True, "space_after": 6},
    {"runs": ["a finite p-value"], "bullet": True},
], sz=20, anchor="ctr", margins=(0.2, 0.15, 0.1, 0.1))
equation(s, 7.1, 1.6, 5.7, 1.6, r"\text{rejection rate}=\frac{\text{valid rejections}}{\text{all repetitions}}",
         sz=24, jc="center")
text(s, 7.2, 3.5, 5.5, 3.2, [
    {"runs": ["Validity is reported separately."], "space_after": 14},
    {"runs": ["An invalid calculation is not evidence that the null is true."], "space_after": 14},
    {"runs": [("Zero and undefined component degrees of freedom are different cases; both are invalid.",
               {"c": BODY})], "sz": 18},
], sz=22)
source_line(s, ["Thesis Appendix B.3–B.5; validity strips in Figures 6.4–6.9"])
notes(s, note_backup(
    "How are degenerate calculations handled, and can calculation failures explain low rejection?",
    """“The rate measures the complete implemented procedure, including failures, so invalid outputs count as non-rejections. The separate validity measure lets us see that contribution. Conditioning on validity would answer a different question and select a different subset of samples. Several important failures persist with 100% validity, including the large false-positive rate highlighted in the talk.”""",
    """Full rules: Normal Wald requires a finite corrected difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14, and a finite p-value; the threshold treats variances extremely close to zero as numerically unusable. Expanded Welch additionally requires positive finite degrees of freedom for both components and their combination, and a finite Expanded Welch p-value. A failed component makes Expanded Welch invalid. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so Expanded Welch records the comparison as invalid even if the other table makes the shared standard error positive and finite. A zero V-hat with positive tau-hat-squared gives zero component degrees of freedom, which also fails the positive requirement. The primary rejection rate divides valid rejections by all repetitions. No minimum expected-count filter is applied.""",
    "Thesis Appendix B.3–B.5 and the validity strips in Figures 6.4–6.9."))

# =================================================================== B5
s = new_slide("The near-independence noise calculation", 21)
backup_tag(s, "Backup B5")
intro(s, [B("Setting: 4\u00d74, n = 1,000, MI 0.0001;  "), CM("\U0001D451 = 9"), B("  and  "),
          CM("\U0001D705 = 2\U0001D45B\U0001D43C(\U0001D443) \u2248 0.2")], h=0.55, sz=21)
rect(s, 0.5, 1.95, 12.33, 1.2, fill=PALE_ORANGE, line=ORANGE_LINE, rounded=0.1)
equation(s, 0.8, 1.98, 11.8, 1.14,
         r"G=2n\widehat I(P)\ \dot{\sim}\ \chi^2_d(\kappa),\qquad \widehat\nu_P\approx G/2", sz=28, jc="center")
H = dict(sz=20, b=True, anchor="ctr", bottom=ORANGE, bottom_w=1.5)
rows = [[dict(paras=["Quantity"], color=ORANGE, **H), dict(paras=["Local prediction"], color=ORANGE, align="ctr", **H),
         dict(paras=["Observed (P)"], color=ORANGE, align="ctr", **H)]]
for q, a, b in [("Mean estimated component df", "4.60", "4.86"), ("Sampling-moment target", "9.00", "9.12"),
                ("Mean sample-based variance prediction / observed sampling variance", "1.96", "1.97")]:
    rows.append([dict(paras=[q], sz=20, anchor="ctr"), dict(paras=[a], sz=22, align="ctr", anchor="ctr"),
                 dict(paras=[b], sz=22, align="ctr", anchor="ctr")])
table(s, 0.85, 3.4, [6.9, 2.35, 2.35], [0.58, 0.8, 0.8, 1.05], rows, name="Noise table")
source_line(s, ["Local approximations under fixed dimensions and positive limiting cell probabilities. "
                "Thesis Appendix A.2, Section 6.1.3"])
notes(s, note_backup(
    "Why do the mean estimated degrees of freedom remain near five?",
    """“Near independence, sampling noise creates apparent association. The quadratic likelihood-ratio approximation includes that noise. Substitution into the component formula gives roughly G divided by two, whose mean is about 4.6 in this setting. The population first-order formula instead approaches n times population MI. These are different approximations, which explains their separation.”""",
    """Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.""",
    "Thesis Appendix A.2 and Section 6.1.3; Figure 6.3. These are local approximations under fixed dimensions and positive limiting cell probabilities, not exact finite-sample distribution identities."))

# =================================================================== B6-B9
FOOT = "Rejection rates use all 100,000 repetitions; invalid outputs count as non-rejections (validity: B4). "
backups_fig = [
    (22, "B6", "Null results with uniform margins", [B("Equal MI in P and Q; uniform margins in both populations")],
     "b06_null_uniform", "Thesis Figure 6.4",
     "What happens outside the highlighted different-skew 16×16 example?",
     "“Under the copying construction, equal MI and uniform margins give identical population tables. Their expected MI biases cancel in the difference, but errors in the uncertainty estimate and reference distribution can still cause excessive or conservative rejection. Increasing common MI changes those patterns.”",
     "This page contains all 120 settings for the uniform profile.", "Final Figure 6.4; balanced-null combined rates, uniform profile."),
    (23, "B7", "Null results with same-skew margins",
     [B("Equal MI; same-skew margins "), ("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}),
      B("(0.8) in P and Q")],
     "b07_null_same_skew", "Thesis Figure 6.5",
     "What changes when both populations have the same uneven category frequencies?",
     "“The population tables are still identical under equal MI, so expected bias in the difference cancels. Uneven margins leave more rare category combinations. The conservative ranges persist beyond the smallest samples and are not explained solely by calculation failures. Expanded Welch lowers those already-low rates further.”",
     "This page contains all 120 settings for the same-skew profile.", "Final Figure 6.5; balanced-null combined rates, same-skew profile."),
    (24, "B8", "Null results with different-skew margins",
     [B("Equal MI; "), ("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}), B("(0.7) in P and "),
      ("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}), B("(0.8) in Q")],
     "b08_null_different_skew", "Thesis Figure 6.6",
     "Are the severe failures restricted to the largest table, and what is visible over the complete margin-specific grid?",
     "“Here equal MI permits different population tables. The remaining MI biases need not cancel, and in the sparse largest table they can shift the estimated difference substantially away from zero. The smaller-table patterns and the dependence on common MI remain visible in this complete slice of the null grid.”",
     "This page contains all 120 settings for the different-skew profile. The main talk enlarged the 16×16 panel on Slide 11.",
     "Final Figure 6.6; balanced-null combined rates, different-skew profile."),
    (25, "B9", "Power with same-skew margins",
     [B("Same-skew margins "), ("m", {"b": True, "i": True}), ("k", {"b": True, "i": True, "sub": True}),
      B("(0.8) in P and Q; MI in P = 0.02 nats")],
     "b09_power_same_skew", "Thesis Figure 6.8",
     "Do the power patterns also occur when both groups have the same uneven margins?",
     "“These power curves use the same uneven margins in both populations. Larger tables need more observations, and the smaller MI gap remains harder to detect. For example, at n = 50,000, the 16×16 Expanded Welch power is 79.87% for the smallest gap, compared with more than 99.9% for each of the two larger gaps. The method difference is smaller than these gap and setting effects at larger sample sizes.”",
     "This page contains all 120 settings for the same-skew power profile.", "Final Figure 6.8; Section 6.3.2; MI-gap combined rates, same-skew profile."),
]
for n, tag, title, intro_runs, img, fig_ref, q, a, extra, src in backups_fig:
    s = new_slide(title, n)
    backup_tag(s, f"Backup {tag}")
    intro(s, intro_runs)
    picture(s, img, 0.55, 1.8, 12.2, 5.15)
    source_line(s, [FOOT + fig_ref], w=11.25)
    notes(s, note_backup(q, a, extra, src))

# =================================================================== B10
s = new_slide("Application details and the comparison family", 26)
backup_tag(s, "Backup B10")
intro(s, [B("Six exploratory comparisons; Holm adjustment applied separately to each method")])


def sci(m, e):
    return [m + "×10", (f"−{e}", {"sup": True})]


H = dict(sz=20, b=True, anchor="ctr", bottom=ORANGE, bottom_w=1.5)
rows = [[dict(paras=["Dataset"], color=ORANGE, **H), dict(paras=["Predictor"], color=ORANGE, **H),
         dict(paras=["Normal Wald"], color=ORANGE, align="r", **H),
         dict(paras=["Expanded Welch"], color=ORANGE, align="r", **H)]]
fam = [("Adult", "Occupation", sci("1.184", 44), sci("1.635", 42)),
       ("Adult", "Education", sci("1.890", 34), sci("4.930", 33)),
       ("Online Shoppers", "Month", sci("4.714", 5), sci("3.726", 4)),
       ("Student Performance", "Study time", ["0.1982"], ["0.2339"]),
       ("Student Performance", "Maternal education", ["0.8361"], ["0.8468"]),
       ("Online Shoppers", "Weekend", ["0.9554"], ["0.9601"])]
for d, pr, w, e in fam:
    fill = PALE_ORANGE if pr == "Month" else None
    rows.append([dict(paras=[d], sz=20, fill=fill), dict(paras=[pr], sz=20, fill=fill),
                 dict(paras=[w], sz=20, align="r", fill=fill), dict(paras=[e], sz=20, align="r", fill=fill)])
table(s, 0.85, 1.9, [3.6, 3.2, 2.4, 2.4], [0.55] + [0.56] * 6, rows, name="Comparison family")
text(s, 0.85, 6.0, 11.5, 0.8, [["Unadjusted p-values. Holm-adjusted month p-values: Normal Wald ", B("0.000189"),
                                "; Expanded Welch ", B("0.00149")]], sz=20, name="Adjusted values")
source_line(s, ["Becker and Kohavi (1996); Sakar and Kastro (2018); Cortez (2008); Holm (1979). "
                "Thesis Appendix B.7, Table B.1"])
notes(s, note_backup(
    "Why were six comparisons adjusted, and what else was tested?",
    """“The two shopping examples were selected from a fixed six-comparison exploratory family across three public datasets. I apply Holm's adjustment separately to each method's six p-values. Both adjusted month results remain below 0.05. This adjustment addresses multiplicity; it does not establish that the approximate underlying p-values are calibrated.”""",
    """Groups: 1,694 sessions labelled New_Visitor (P) and 10,551 labelled Returning_Visitor (Q); the 85 Other sessions are excluded. The dataset has 12,330 sessions, each from a different user according to its documentation. Outcome: the Boolean Revenue variable.
Month: January and April have no recorded sessions, so each month table is 10×2. All ten months occur in both groups, although the new-visitor February row contains one session and no purchase. Zero cells are retained without smoothing.
Month degrees of freedom: component 12.93 (new visitors) and 187.93 (returning visitors); combined 26.79.
Weekend: corrected MI 0.000664 (new) and 0.000727 (returning); T = −0.056; Expanded Welch df 2.18; p-values 0.9554 (Wald) and 0.9601 (Expanded Welch). Neither test rejects, and this non-rejection does not establish equality.
Holm: order each method's six p-values from smallest to largest, multiply by 6, 5, 4, 3, 2 and 1, take the cumulative maximum and cap at one. Month is the third smallest, so its multiplier is 4.
Other family members: Adult education and occupation versus income above $50,000, comparing female and male records; Student Performance study time and maternal education versus final grade at least 10 (Portuguese course), comparing schools GP and MS.""",
    "Thesis Section 6.4 and Appendix B.7, Table B.1; the application protocol. Becker and Kohavi (1996); Sakar and Kastro (2018); Cortez (2008); Holm (1979)."))

# =================================================================== B11-B12
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


def ref_slide(n, tag, title, refs, split):
    s = new_slide(title, n)
    backup_tag(s, f"Backup {tag}")
    cols = [refs[:split], refs[split:]]
    for c, col in enumerate(cols):
        text(s, 0.85 + c * 6.0, 1.55, 5.65, 5.3,
             [{"runs": r, "space_after": 14, "line": 1.0} for r in col], sz=17, color=BLACK,
             name=f"References column {c + 1}")
    return s


s = ref_slide(27, "B11", "References: MI and testing foundations", REFS1, 3)
notes(s, "Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.")
s = ref_slide(28, "B12", "References: related methods and evaluation", REFS2, 3)
notes(s, "Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.")

cp = prs.core_properties
cp.title = "Comparing Mutual Information in Finite Samples"
cp.subject = "Normal Wald and Expanded Welch\u2013Satterthwaite Tests"
cp.author = "Daniel Zhao"
cp.last_modified_by = "Daniel Zhao"
cp.keywords = "mutual information; Welch\u2013Satterthwaite; hypothesis testing"
cp.comments = ""
prs.save(OUT)
import pptlib
for row in pptlib.EQUATION_LOG:
    flag = "  <-- tight" if row[4] > 0.8 else ""
    print("eq", row, flag)
print("saved", OUT, len(prs.slides), "slides")
