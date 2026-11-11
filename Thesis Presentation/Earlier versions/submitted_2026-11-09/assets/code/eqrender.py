"""Render fallback images for native PowerPoint equations (shown only by apps that cannot read Office maths)."""
import io
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["mathtext.fontset"] = "stix"


def to_mathtext(latex):
    s = latex
    s = re.sub(r"\\operatorname\{([^}]*)\}", r"\\mathrm{\1}", s)
    s = re.sub(r"\\text\{([^}]*)\}", lambda m: r"\mathrm{" + m.group(1).replace(" ", r"\ ") + "}", s)
    s = s.replace(r"\mathbb E", r"\mathbb{E}").replace(r"\mathbf 1", r"\mathbf{1}")
    s = s.replace(r"\mathrm d", r"\mathrm{d}")
    s = s.replace(r"\bigl[", "[").replace(r"\bigr]", "]")
    s = s.replace(r"\frac", r"\dfrac")
    return s


def render(latex, w, h, sz, jc="left", color="#000000"):
    """Return (png bytes, width in inches of the drawn equation)."""
    fig = plt.figure(figsize=(w, h), dpi=300)
    fig.patch.set_alpha(0)
    x = {"left": 0.06 / w, "center": 0.5, "centerGroup": 0.5, "right": 1 - 0.06 / w}[jc]
    ha = {"left": "left", "center": "center", "centerGroup": "center", "right": "right"}[jc]
    t = fig.text(x, 0.5, "$" + to_mathtext(latex) + "$", fontsize=sz, ha=ha, va="center", color=color)
    fig.canvas.draw()
    bb = t.get_window_extent()
    width_in = bb.width / fig.dpi
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, transparent=True)
    plt.close(fig)
    return buf.getvalue(), width_in
