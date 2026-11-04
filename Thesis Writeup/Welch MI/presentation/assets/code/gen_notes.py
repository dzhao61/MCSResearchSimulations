"""Write the speaker-notes markdown from the notes stored in the deck."""
import sys
from pptx import Presentation

deck, out = sys.argv[1], sys.argv[2]
p = Presentation(deck)
titles = []
for s in p.slides:
    t = s.shapes.title.text_frame.text if s.shapes.title is not None else ""
    titles.append(t.replace("\v", " ").replace("\n", " "))
titles[0] = "Comparing Mutual Information in Finite Samples"

L = ["# Speaker notes: Comparing Mutual Information in Finite Samples", "",
     "Synchronised with `Daniel_Zhao_Welch_MI_Presentation.pptx` (28 slides: 16 main, 12 backup). "
     "The scripts and transitions are the rehearsal draft from the presentation plan, unchanged. "
     "Learn the explanation, then speak naturally from the cues.", "",
     "## Timing", "", "| Slide | Title | Time | Finish by |", "| --- | --- | --- | --- |"]
times = []
for i in range(16):
    n = p.slides[i].notes_slide.notes_text_frame.text
    first = n.splitlines()[0]
    t, fin = first.replace("Time: ", "").replace(")", "").split(" (finish by ")
    times.append((t, fin))
    L.append(f"| {i + 1} | {titles[i]} | {t} | {fin} |")
L += ["", "Main talk target: 18:50, leaving 70 seconds before the 20-minute cut-off. "
      "Keep Slide 16 on screen when questions begin.", "", "## Main slides", ""]
for i in range(16):
    n = p.slides[i].notes_slide.notes_text_frame.text
    body = n.split("\n", 1)[1].strip()
    L.append(f"### Slide {i + 1}: {titles[i]}")
    L.append("")
    L.append(f"**Time:** {times[i][0]} (finish by {times[i][1]})")
    L.append("")
    for block in body.split("\n\n"):
        head, _, rest = block.partition("\n")
        if head in ("SCRIPT", "TRANSITION", "DELIVERY CUE", "SOURCE"):
            L.append(f"**{head.title()}**")
            L.append("")
            L.append(rest.strip())
        else:
            L.append(block.strip())
        L.append("")
L += ["## Backup slides", "",
      "Jump from Slide 16 by typing the slide number and pressing Enter; return the same way.", ""]
for i in range(16, 28):
    n = p.slides[i].notes_slide.notes_text_frame.text
    L.append(f"### Slide {i + 1}: {titles[i]}")
    L.append("")
    for block in n.split("\n\n"):
        head, _, rest = block.partition("\n")
        if head in ("QUESTION ANSWERED", "ANSWER TO GIVE", "NOTES", "SOURCE"):
            L.append(f"**{head.capitalize()}**")
            L.append("")
            L.append(rest.strip())
        else:
            L.append(block.strip())
        L.append("")
open(out, "w").write("\n".join(L).rstrip() + "\n")
print("wrote", out)
