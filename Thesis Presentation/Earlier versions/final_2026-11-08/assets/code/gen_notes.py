"""Write the rehearsal notes Markdown from the built deck's speaker notes and the plan's sections 8 and 9."""
import sys

from pptx import Presentation

DECK, PLAN, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
prs = Presentation(DECK)
plan = open(PLAN, encoding="utf-8").read()


def plan_section(start, end):
    i = plan.index(start)
    j = plan.index(end, i) if end else len(plan)
    return plan[i:j].rstrip() + "\n"


# Wording in plan sections 8 and 9 that the final thesis (8 November 2026) superseded: "calculation success"
# replaces "validity", the Holm family is gone, and the new ordinary Welch backup moves later backups up by one.
SECTION_FIXES = [
    ("so I calculate its sampling variability instead.” | B1–B2 |",
     "so I calculate its sampling variability instead.” | B1–B2, B9 |"),
    ("| Could invalid calculations explain the low rejection? | “They contribute at some small sample sizes. I "
     "report their frequency separately. Important conservative ranges and the highlighted excessive-rejection cases "
     "persist when every calculation is valid.” |",
     "| Could unsuccessful calculations explain the low rejection? | “They contribute at some small sample sizes. "
     "I report calculation success separately. Important conservative ranges and the highlighted excessive-rejection "
     "cases persist when every calculation succeeds.” |"),
    ("| Why count invalid outputs as non-rejections? | “That reports the full implemented procedure's ability to "
     "reject. Restricting to valid outputs would condition on a selected subset. Reporting validity separately makes "
     "the distinction visible.” |",
     "| Why count unsuccessful calculations as non-rejections? | “That reports the full implemented procedure's "
     "ability to reject. Restricting to successful calculations would condition on a selected subset. Reporting "
     "calculation success separately makes the distinction visible.” |"),
    ("remain a limitation.” | B3, B6–B11 |", "remain a limitation.” | B3, B6–B12 |"),
    ("both methods can be inaccurate even with valid outputs.", "both methods can be inaccurate even when every "
     "calculation succeeds."),
    ("retaining zero cells within those categories.” | B12 |", "retaining zero cells within those "
     "categories.” | B13 |"),
    ("or rule out shared temporal influences.” | B12 |", "or rule out shared temporal influences.” | B13 |"),
    ("| Why are six comparisons in the Holm family? | “They were the six specified public-data comparisons: two "
     "each from Adult, Shoppers and Student Performance. Both shopping results are interpreted within that original "
     "family, with a separate adjustment for each test.” | B12 |\n", ""),
    ("Parallel studies, sample size versus repetitions, invalid-output rule |",
     "Parallel studies, sample size versus repetitions, unsuccessful-calculation rule |"),
    ("equal MI and complete validity |", "equal MI and every calculation succeeding |"),
    ("Return to example, adjusted rejection and unknown population MI |",
     "Return to example, rejection at 0.05 and unknown population MI |"),
    ("both tests reject equality after adjustment across\n  six comparisons.",
     "both tests reject equality at the usual 0.05\n  threshold."),
]


def fix_sections(text):
    for old, new in SECTION_FIXES:
        assert text.count(old) == 1, old[:80]
        text = text.replace(old, new)
    return text


LABELS = {"DELIVERY": "Delivery", "SCRIPT": "Script", "TRANSITION": "Transition", "DELIVERY CUE": "Delivery cue", "SOURCE": "Source",
          "BACKUP INDEX": "Backup index", "WHEN OPENING": "When opening", "QUESTION ANSWERED": "Question answered",
          "ANSWER TO GIVE": "Answer to give", "NOTES": "Notes"}


def to_md(note):
    """Group note blocks under their labels; scripts become quoted paragraphs."""
    sections, cur = [], None
    for block in note.split("\n\n"):
        first, _, rest = block.partition("\n")
        key = first.split(" (")[0]
        if key in LABELS:
            cur = [LABELS[key] + first[len(key):], [rest] if rest else []]
            sections.append(cur)
        elif cur is None:
            sections.append([None, [block]])
        else:
            cur[1].append(block)
    out = []
    for label, paras in sections:
        if label is None:
            out.append("\n\n".join(paras))
            continue
        out.append(f"**{label}**")
        if label.startswith("Script"):
            out.append("\n\n".join(f"> {p}" for p in paras))
        elif label.startswith("Backup index"):
            out.append("\n".join(f"- {l}" for l in "\n".join(paras).split("\n")))
        else:
            out.append("\n\n".join(p.replace("\n", "\n\n") for p in paras))
    return "\n\n".join(out)


titles = []
for sl in prs.slides:
    t = sl.shapes.title.text_frame.text if sl.shapes.title is not None else ""
    titles.append(t.replace("\n", " ").replace("\v", " "))
titles[0] = "Comparing Mutual Information in Finite Samples"

md = ["# Comparing Mutual Information in Finite Samples: speaker notes", "",
      "Daniel Zhao. Talk target 18:50 for Slides 1–14; Slide 14 stays up for questions. Slide 15 is the appendix "
      "title and the backups are Slides 16–30.",
      "Scripts, transitions, delivery cues, sources and backup answers come from the presentation execution plan "
      "(replanned 5 November 2026). Wording the final thesis (8 November 2026) superseded is updated; the README "
      "lists each change.", "", "## Main talk", ""]
for i in range(14):
    md += [f"### Slide {i + 1}: {titles[i]}", "", to_md(prs.slides[i].notes_slide.notes_text_frame.text), ""]
md += ["## Appendix", "", "### Slide 15: Appendix title", "", to_md(prs.slides[14].notes_slide.notes_text_frame.text),
       ""]
for i in range(15, len(prs.slides)):
    md += [f"### Slide {i + 1} (B{i - 14}): {titles[i]}", "", to_md(prs.slides[i].notes_slide.notes_text_frame.text),
           ""]
md += [fix_sections(plan_section("## 8. Question preparation", "## 9. Rehearsal and timing control")
                    + "\n" + plan_section("## 9. Rehearsal and timing control",
                                          "## 10. Implementation and acceptance"))]
open(OUT, "w", encoding="utf-8").write("\n".join(md))
print("wrote", OUT)
