"""Small helpers for building the Welch MI deck on a copy of Daniel's vF2 template."""
import copy
import functools
import io
import os
import re
import subprocess
import tempfile
import zipfile

from lxml import etree
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A14_NS = "http://schemas.microsoft.com/office/drawing/2010/main"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"

BLACK = "000000"
BODY = "333333"
MUTED = "595959"
ORANGE = "E97132"
COVER_ORANGE = "E97132"
NAVY = "1F3A5C"
PALE_ORANGE = "FFF1E8"
PALE_BLUE = "E8EFF7"
ORANGE_LINE = "F5C6A7"
BLUE_LINE = "C8D8EA"
DIVIDER = "DDDDDD"
WHITE = "FFFFFF"
FONT = "Lato"
MATH_FONT = "Cambria Math"


def emu(v):
    return int(Inches(v))


# ------------------------------------------------------------------ maths
def _math_italic(ch):
    o = ord(ch)
    if ch == "h":
        return "ℎ"
    if "a" <= ch <= "z":
        return chr(0x1D44E + o - ord("a"))
    if "A" <= ch <= "Z":
        return chr(0x1D434 + o - ord("A"))
    if 0x3B1 <= o <= 0x3C9 and o != 0x3C2:
        return chr(0x1D6FC + o - 0x3B1)
    if ch == "ϵ":
        return "\U0001D716"
    return ch


@functools.lru_cache(maxsize=None)
def _pandoc_omml(latex, display):
    with tempfile.TemporaryDirectory() as d:
        md = os.path.join(d, "m.md")
        out = os.path.join(d, "m.docx")
        with open(md, "w") as f:
            f.write(("$$%s$$" if display else "$%s$") % latex)
        subprocess.run(["pandoc", md, "-o", out], check=True)
        xml = zipfile.ZipFile(out).read("word/document.xml")
    root = etree.fromstring(xml)
    tag = "oMathPara" if display else "oMath"
    el = root.find(".//{%s}%s" % (M_NS, tag))
    assert el is not None, latex
    return etree.tostring(el)


def omml(latex, sz, display=True, color=BLACK, jc="left", bold=False):
    """Return an <a14:m> element holding native Office maths for a LaTeX string."""
    el = etree.fromstring(_pandoc_omml(latex, display))
    if display:
        jc_el = el.find("{%s}oMathParaPr/{%s}jc" % (M_NS, M_NS))
        if jc_el is not None:
            jc_el.set("{%s}val" % M_NS, jc)
    for r in el.iter("{%s}r" % M_NS):
        sty = r.find("{%s}rPr/{%s}sty" % (M_NS, M_NS))
        plain = sty is not None and sty.get("{%s}val" % M_NS) == "p"
        rpr = etree.Element("{%s}rPr" % A_NS, lang="en-AU", sz=str(int(sz * 100)),
                            b="1" if bold else "0", i="0" if plain else "1")
        fill = etree.SubElement(rpr, "{%s}solidFill" % A_NS)
        etree.SubElement(fill, "{%s}srgbClr" % A_NS, val=color)
        etree.SubElement(rpr, "{%s}latin" % A_NS, typeface=MATH_FONT)
        mrpr = r.find("{%s}rPr" % M_NS)
        r.insert(1 if mrpr is not None else 0, rpr)
        t = r.find("{%s}t" % M_NS)
        if t is not None and t.text and not plain:
            t.text = "".join(_math_italic(c) for c in t.text)
    wrap = etree.Element("{%s}m" % A14_NS, nsmap={"a14": A14_NS})
    wrap.append(el)
    return wrap


# ------------------------------------------------------------------ text
def _rpr(parent, sz, color, b=False, i=False, font=FONT, baseline=None, tag="rPr"):
    rpr = etree.SubElement(parent, qn("a:" + tag), lang="en-AU", sz=str(int(round(sz * 100))),
                           b="1" if b else "0", i="1" if i else "0", dirty="0")
    if baseline:
        rpr.set("baseline", str(baseline))
    fill = etree.SubElement(rpr, qn("a:solidFill"))
    etree.SubElement(fill, qn("a:srgbClr"), val=color)
    etree.SubElement(rpr, qn("a:latin"), typeface=font)
    etree.SubElement(rpr, qn("a:cs"), typeface=font)
    return rpr


def fill_text_body(txBody, paras, sz=22, color=BLACK, align="l", font=FONT, line=None,
                   space_after=0, bullet=False, space_before=0):
    """Fill a txBody with paragraphs.

    paras: list of paragraphs. A paragraph is a str, or a list of runs, or a dict
    {"runs": [...], "sz":, "align":, "bullet":, "space_after":, "space_before":, "color":, "b":}.
    A run is a str or a tuple (text, opts) with opts keys b, i, c, sz, sub, sup, math, font.
    Returns True when any run contains maths.
    """
    for p in txBody.findall(qn("a:p")):
        txBody.remove(p)
    has_math = False
    for para in paras:
        popts = {}
        if isinstance(para, dict):
            popts = para
            runs = para["runs"]
        else:
            runs = para
        if isinstance(runs, str):
            runs = [runs]
        psz = popts.get("sz", sz)
        pcol = popts.get("color", color)
        pb = popts.get("b", False)
        p = etree.SubElement(txBody, qn("a:p"))
        ppr = etree.SubElement(p, qn("a:pPr"), algn=popts.get("align", align))
        is_bullet = popts.get("bullet", bullet)
        if is_bullet:
            ppr.set("marL", str(emu(0.32)))
            ppr.set("indent", str(-emu(0.32)))
        ln = popts.get("line", line)
        if ln:
            lsp = etree.SubElement(ppr, qn("a:lnSpc"))
            etree.SubElement(lsp, qn("a:spcPct"), val=str(int(ln * 100000)))
        sb = popts.get("space_before", space_before)
        if sb:
            e = etree.SubElement(ppr, qn("a:spcBef"))
            etree.SubElement(e, qn("a:spcPts"), val=str(int(sb * 100)))
        sa = popts.get("space_after", space_after)
        if sa:
            e = etree.SubElement(ppr, qn("a:spcAft"))
            etree.SubElement(e, qn("a:spcPts"), val=str(int(sa * 100)))
        if is_bullet:
            bc = etree.SubElement(ppr, qn("a:buClr"))
            etree.SubElement(bc, qn("a:srgbClr"), val=popts.get("bullet_color", ORANGE))
            etree.SubElement(ppr, qn("a:buFont"), typeface="Arial")
            etree.SubElement(ppr, qn("a:buChar"), char="•")
        else:
            etree.SubElement(ppr, qn("a:buNone"))
        for run in runs:
            text, o = (run, {}) if isinstance(run, str) else run
            rsz = o.get("sz", psz)
            if o.get("math") is not None:
                has_math = True
                p.append(omml(o["math"], rsz, display=False, color=o.get("c", pcol)))
                continue
            if o.get("br"):
                br = etree.SubElement(p, qn("a:br"))
                _rpr(br, rsz, pcol)
                continue
            r = etree.SubElement(p, qn("a:r"))
            baseline = -25000 if o.get("sub") else (30000 if o.get("sup") else None)
            _rpr(r, rsz, o.get("c", pcol), b=o.get("b", pb), i=o.get("i", False),
                 font=o.get("font", font), baseline=baseline)
            t = etree.SubElement(r, qn("a:t"))
            t.text = text
            if text != text.strip():
                t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        _rpr(p, psz, pcol, tag="endParaRPr")
    return has_math


def _body_pr(txBody, anchor="t", margins=(0.04, 0.04, 0.03, 0.03), wrap=True):
    bp = txBody.find(qn("a:bodyPr"))
    for k in list(bp.attrib):
        del bp.attrib[k]
    bp.set("wrap", "square" if wrap else "none")
    l, r, t, b = margins
    bp.set("lIns", str(emu(l)))
    bp.set("rIns", str(emu(r)))
    bp.set("tIns", str(emu(t)))
    bp.set("bIns", str(emu(b)))
    bp.set("rtlCol", "0")
    bp.set("anchor", anchor)
    for c in list(bp):
        bp.remove(c)
    etree.SubElement(bp, qn("a:noAutofit"))


def wrap_alternate(shape, fallback_text):
    """Wrap a shape containing a14:m maths in mc:AlternateContent, as PowerPoint does."""
    sp = shape._element
    parent = sp.getparent()
    idx = parent.index(sp)
    fb = copy.deepcopy(sp)
    for m in fb.iter("{%s}m" % A14_NS):
        pass
    for p in fb.iter(qn("a:p")):
        for m in list(p.findall("{%s}m" % A14_NS)):
            r = etree.Element(qn("a:r"))
            _rpr(r, 18, BLACK)
            t = etree.SubElement(r, qn("a:t"))
            t.text = fallback_text
            p.replace(m, r)
    ac = etree.Element("{%s}AlternateContent" % MC_NS, nsmap={"mc": MC_NS, "a14": A14_NS})
    ch = etree.SubElement(ac, "{%s}Choice" % MC_NS, Requires="a14")
    fbk = etree.SubElement(ac, "{%s}Fallback" % MC_NS)
    parent.remove(sp)
    ch.append(sp)
    fbk.append(fb)
    parent.insert(idx, ac)


def text(slide, x, y, w, h, paras, sz=22, color=BLACK, align="l", anchor="t", name=None,
         margins=(0.04, 0.04, 0.03, 0.03), fallback="equation", **kw):
    shape = slide.shapes.add_textbox(emu(x), emu(y), emu(w), emu(h))
    if name:
        shape.name = name
    tb = shape.text_frame._txBody
    _body_pr(tb, anchor=anchor, margins=margins)
    has_math = fill_text_body(tb, paras, sz=sz, color=color, align=align, **kw)
    if has_math:
        wrap_alternate(shape, fallback)
    return shape


def wrap_alternate_picture(shape, rId):
    """Wrap a maths shape in mc:AlternateContent with a picture fallback, as PowerPoint saves equations."""
    sp = shape._element
    parent = sp.getparent()
    idx = parent.index(sp)
    fb = copy.deepcopy(sp)
    spPr = fb.find(qn("p:spPr"))
    nofill = spPr.find(qn("a:noFill"))
    blip_fill = etree.Element(qn("a:blipFill"))
    etree.SubElement(blip_fill, qn("a:blip"), {qn("r:embed"): rId})
    st = etree.SubElement(blip_fill, qn("a:stretch"))
    etree.SubElement(st, qn("a:fillRect"))
    if nofill is not None:
        spPr.replace(nofill, blip_fill)
    else:
        spPr.insert(2, blip_fill)
    tb = fb.find(qn("p:txBody"))
    for p in tb.findall(qn("a:p")):
        tb.remove(p)
    p = etree.SubElement(tb, qn("a:p"))
    r = etree.SubElement(p, qn("a:r"))
    rpr = etree.SubElement(r, qn("a:rPr"), lang="en-AU")
    etree.SubElement(rpr, qn("a:noFill"))
    etree.SubElement(r, qn("a:t")).text = " "
    ac = etree.Element("{%s}AlternateContent" % MC_NS, nsmap={"mc": MC_NS, "a14": A14_NS})
    ch = etree.SubElement(ac, "{%s}Choice" % MC_NS, Requires="a14")
    fbk = etree.SubElement(ac, "{%s}Fallback" % MC_NS)
    parent.remove(sp)
    ch.append(sp)
    fbk.append(fb)
    parent.insert(idx, ac)


def equation(slide, x, y, w, h, latex, sz=26, color=BLACK, jc="left", anchor="ctr", name=None):
    shape = slide.shapes.add_textbox(emu(x), emu(y), emu(w), emu(h))
    if name:
        shape.name = name
    tb = shape.text_frame._txBody
    _body_pr(tb, anchor=anchor)
    for p in tb.findall(qn("a:p")):
        tb.remove(p)
    p = etree.SubElement(tb, qn("a:p"))
    etree.SubElement(p, qn("a:pPr"), algn={"left": "l", "center": "ctr", "centerGroup": "ctr", "right": "r"}[jc])
    p.append(omml(latex, sz, display=True, color=color, jc=jc))
    _rpr(p, sz, color, tag="endParaRPr")
    import eqrender
    png, width = eqrender.render(latex, w, h, sz, jc, "#" + color)
    EQUATION_LOG.append((slide.slide_id, latex[:50], round(width, 2), w, round(width / w, 2)))
    _, rId = slide.part.get_or_add_image_part(io.BytesIO(png))
    wrap_alternate_picture(shape, rId)
    return shape


EQUATION_LOG = []


# ------------------------------------------------------------------ shapes
def _solid(el_parent_tag_owner, color):
    pass


def shape_fill_line(shape, fill=None, line=None, line_w=1.0, dash=None):
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(fill)
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(line)
        shape.line.width = Pt(line_w)
        if dash:
            ln = shape._element.spPr.find(qn("a:ln"))
            etree.SubElement(ln, qn("a:prstDash"), val=dash)
    sh = shape._element
    # remove theme shadow/effects from the shape style
    st = sh.find(qn("p:style"))
    if st is not None:
        sh.remove(st)


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, rounded=None, name=None, dash=None):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded is not None else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(kind, emu(x), emu(y), emu(w), emu(h))
    if rounded is not None:
        s.adjustments[0] = rounded
    shape_fill_line(s, fill, line, line_w, dash)
    if name:
        s.name = name
    s.text_frame._txBody.find(qn("a:bodyPr")).set("anchor", "ctr")
    return s


def panel_text(shape, paras, sz=22, color=BLACK, align="l", anchor="t", margins=(0.2, 0.2, 0.12, 0.12), **kw):
    tb = shape.text_frame._txBody
    _body_pr(tb, anchor=anchor, margins=margins)
    fill_text_body(tb, paras, sz=sz, color=color, align=align, **kw)


def header_bar(slide, x, y, w, h, label, fill, sz=22, align="ctr", name=None):
    s = rect(slide, x, y, w, h, fill=fill, rounded=0.16, name=name)
    panel_text(s, [[(label, {"b": True})]], sz=sz, color=WHITE, align=align, anchor="ctr",
               margins=(0.15, 0.15, 0.02, 0.02))
    return s


def circle(slide, x, y, d, label, fill, sz=20, name=None):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, emu(x), emu(y), emu(d), emu(d))
    shape_fill_line(s, fill, None)
    if name:
        s.name = name
    panel_text(s, [[(label, {"b": True})]], sz=sz, color=WHITE, align="ctr", anchor="ctr",
               margins=(0, 0, 0, 0))
    return s


def hline(slide, x, y, w, color=DIVIDER, width=1.25, dash=None):
    c = slide.shapes.add_connector(1, emu(x), emu(y), emu(x + w), emu(y))
    c.line.color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(color)
    c.line.width = Pt(width)
    if dash:
        ln = c._element.spPr.find(qn("a:ln"))
        etree.SubElement(ln, qn("a:prstDash"), val=dash)
    st = c._element.find(qn("p:style"))
    if st is not None:
        c._element.remove(st)
    return c


def vline(slide, x, y, h, color=DIVIDER, width=1.25, dash=None):
    c = slide.shapes.add_connector(1, emu(x), emu(y), emu(x), emu(y + h))
    c.line.color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(color)
    c.line.width = Pt(width)
    if dash:
        ln = c._element.spPr.find(qn("a:ln"))
        etree.SubElement(ln, qn("a:prstDash"), val=dash)
    st = c._element.find(qn("p:style"))
    if st is not None:
        c._element.remove(st)
    return c


# ------------------------------------------------------------------ tables
NO_STYLE = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def _ln(tcPr, tag, color=None, w=1.0):
    ln = etree.SubElement(tcPr, qn("a:" + tag), w=str(int(Pt(w))) if color else "0")
    if color:
        f = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(f, qn("a:srgbClr"), val=color)
    else:
        etree.SubElement(ln, qn("a:noFill"))


def table(slide, x, y, col_w, row_h, cells, name=None):
    """cells: rows of dicts {paras, sz, color, align, fill, b, anchor, bottom(line colour), top}."""
    nr, nc = len(cells), len(col_w)
    gf = slide.shapes.add_table(nr, nc, emu(x), emu(y), emu(sum(col_w)), emu(sum(row_h)))
    if name:
        gf.name = name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for k in ("firstRow", "bandRow", "firstCol", "lastRow", "lastCol", "bandCol"):
        if tblPr.get(k) is not None:
            del tblPr.attrib[k]
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = NO_STYLE
    for j, w in enumerate(col_w):
        tbl.columns[j].width = emu(w)
    for i, h in enumerate(row_h):
        tbl.rows[i].height = emu(h)
    for i, row in enumerate(cells):
        for j, spec in enumerate(row):
            cell = tbl.cell(i, j)
            tc = cell._tc
            txBody = tc.get_or_add_txBody()
            fill_text_body(txBody, spec.get("paras", [""]), sz=spec.get("sz", 20),
                           color=spec.get("color", BLACK), align=spec.get("align", "l"),
                           line=spec.get("line"))
            if spec.get("b"):
                for r in txBody.iter(qn("a:rPr")):
                    r.set("b", "1")
            old = tc.find(qn("a:tcPr"))
            if old is not None:
                tc.remove(old)
            tcPr = etree.SubElement(tc, qn("a:tcPr"), marL=str(emu(spec.get("ml", 0.14))),
                                    marR=str(emu(spec.get("mr", 0.14))), marT=str(emu(0.06)),
                                    marB=str(emu(0.06)), anchor=spec.get("anchor", "ctr"))
            _ln(tcPr, "lnL")
            _ln(tcPr, "lnR")
            _ln(tcPr, "lnT", spec.get("top"), spec.get("top_w", 1.0))
            _ln(tcPr, "lnB", spec.get("bottom", DIVIDER), spec.get("bottom_w", 1.0))
            if spec.get("fill"):
                f = etree.SubElement(tcPr, qn("a:solidFill"))
                etree.SubElement(f, qn("a:srgbClr"), val=spec["fill"])
            else:
                etree.SubElement(tcPr, qn("a:noFill"))
    return gf


# ------------------------------------------------------------------ slide furniture
def set_title(slide, title, x=0.8486, y=0.4063, w=11.5, h=0.8074, sz=36):
    ph = slide.shapes.title
    ph.left, ph.top, ph.width, ph.height = emu(x), emu(y), emu(w), emu(h)
    tb = ph.text_frame._txBody
    bp = tb.find(qn("a:bodyPr"))
    for c in list(bp):
        bp.remove(c)
    bp.set("anchor", "b")
    bp.set("lIns", str(emu(0.04)))
    bp.set("rIns", str(emu(0.04)))
    etree.SubElement(bp, qn("a:normAutofit"))
    fill_text_body(tb, [[(title, {"b": True})]], sz=sz, color=BLACK, align="l")
    return ph


def slide_number(slide, n):
    s = slide.shapes.add_textbox(emu(12.18), emu(7.02), emu(0.75), emu(0.36))
    s.name = "Slide number"
    tb = s.text_frame._txBody
    _body_pr(tb, anchor="ctr", margins=(0, 0.02, 0, 0))
    for p in tb.findall(qn("a:p")):
        tb.remove(p)
    p = etree.SubElement(tb, qn("a:p"))
    etree.SubElement(p, qn("a:pPr"), algn="r")
    fld = etree.SubElement(p, qn("a:fld"), id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}", type="slidenum")
    _rpr(fld, 14, "7F7F7F")
    t = etree.SubElement(fld, qn("a:t"))
    t.text = str(n)
    _rpr(p, 14, "7F7F7F", tag="endParaRPr")


def source_line(slide, runs, w=11.2):
    return text(slide, 0.85, 7.02, w, 0.36, [runs], sz=14, color=MUTED, anchor="ctr", name="Source line",
                margins=(0.0, 0.02, 0.0, 0.0))


def backup_tag(slide, label):
    return text(slide, 10.6, 0.14, 2.35, 0.36, [[(label, {"b": True})]], sz=14, color=ORANGE, align="r",
                anchor="ctr", name="Backup label", margins=(0, 0.02, 0, 0))


def notes(slide, body):
    slide.notes_slide.notes_text_frame.text = body.strip()
