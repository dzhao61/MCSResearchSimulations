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


# The plan carries the final wording, so sections 8 and 9 are copied without replacements.
SECTION_FIXES = []


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
      "Scripts, transitions, delivery cues, sources, and backup answers are copied from the presentation execution "
      "plan, as updated on 8 November 2026.", "", "## Main talk", ""]
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
