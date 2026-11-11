"""Build the isolated conclusion copy and preserve its authorised signature."""

from pathlib import Path
import hashlib
import os
import re
import shutil
import subprocess
import zipfile
import collections
import json

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject

ROOT = Path(__file__).resolve().parent
PDF_NAME = "Daniel_Zhao_Welch_MI_Thesis_Revised_Conclusion.pdf"
SOURCE_NAME = "Daniel_Zhao_Welch_MI_Thesis_Revised_Conclusion_Source.zip"


def source_files():
    for name in ("main.tex", "preamble.tex", "metadata.tex", "references.bib",
                 "usydthesis.cls", ".latexmkrc", "build_copy.py", "README.md",
                 "AGENTS.md"):
        yield ROOT / name
    for folder in ("frontmatter", "chapters_rewrite", "appendices_rewrite",
                   "style", "figures_rewrite"):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file() and path.suffix in {".tex", ".pdf", ".sty", ".bst", ".py", ".json"}:
                yield path


def check_sources():
    paths = list(source_files())
    tex = {p: re.sub(r"(?<!\\)%[^\n]*", "", p.read_text())
           for p in paths if p.suffix == ".tex"}
    all_tex = "\n".join(tex.values())
    labels = re.findall(r"\\label\{([^}]+)\}", all_tex)
    if len(labels) != len(set(labels)):
        raise ValueError("Duplicate equation or section label.")
    references = set(re.findall(r"\\(?:eqref|ref|pageref)\{([^}]+)\}", all_tex))
    missing = references - set(labels)
    if missing:
        raise ValueError(f"Undefined manuscript references: {sorted(missing)}")
    forbidden = re.compile(r"\\(?:noindent|indent|parindent|parskip|parshape|hangindent|hangafter)\b")
    for path, text in tex.items():
        if path.name != "preamble.tex" and forbidden.search(text):
            raise ValueError(f"Local paragraph-style override: {path}")
    if re.search(r"\\subsubsection\b", all_tex):
        raise ValueError("Use subsections and local bold headings consistently.")
    return paths


def navigation(reader):
    def count(items):
        return sum(count(item) if isinstance(item, list) else 1 for item in items)
    links = collections.Counter()
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if annotation.get("/Subtype") == "/Link":
                if annotation.get("/A"):
                    links[str(annotation["/A"].get("/S"))] += 1
                elif "/Dest" in annotation:
                    links["direct_destination"] += 1
    return {"bookmarks": count(reader.outline),
            "named_destinations": len(reader.named_destinations),
            "links": dict(links)}


def preserve_signature(unsigned, output):
    latest = PdfReader(unsigned)
    authorised = PdfReader(ROOT / "style/authorised_compliance_page.pdf")
    assert len(authorised.pages) == 1
    assert latest.pages[1].extract_text() == authorised.pages[0].extract_text()
    assert list(latest.pages[1].mediabox) == list(authorised.pages[0].mediabox)
    assert not latest.pages[1].get("/Annots")
    assert not latest.get_fields() and not authorised.get_fields()
    annotations = [reference.get_object()
                   for reference in authorised.pages[0].get("/Annots", [])]
    signature, = [a for a in annotations if a.get("/Subtype") == "/Stamp"]
    date, = [a for a in annotations if a.get("/Subtype") == "/FreeText"]
    assert date["/Contents"] == "07/11/2026"
    writer = PdfWriter(unsigned, incremental=True)
    for annotation in (signature, date):
        clean = DictionaryObject({k: v for k, v in annotation.items() if k != "/P"})
        writer.add_annotation(1, clean.clone(writer))
    writer.write(output)
    signed = PdfReader(output)
    assert output.read_bytes().startswith(unsigned.read_bytes())
    assert len(signed.pages) == len(latest.pages)
    assert navigation(signed) == navigation(latest)
    assert not signed.get_fields()
    for before, after in zip(latest.pages, signed.pages):
        assert before.get_contents().get_data() == after.get_contents().get_data()
        assert list(before.mediabox) == list(after.mediabox)
    copied = [a.get_object() for a in signed.pages[1]["/Annots"]]
    assert len(copied) == 2
    for before, after in zip((signature, date), copied):
        assert before["/Subtype"] == after["/Subtype"]
        assert list(before["/Rect"]) == list(after["/Rect"])
        assert before["/AP"]["/N"].get_object().get_data() == after["/AP"]["/N"].get_object().get_data()
    return {"pages": len(signed.pages), "navigation": navigation(signed),
            "date": str(date["/Contents"]), "all_page_contents_preserved": True,
            "original_signature_and_date_appearances_preserved": True}


def main():
    paths = check_sources()
    build = ROOT / "build"
    for folder in (build, build / "chapters_rewrite", build / "appendices_rewrite"):
        folder.mkdir(parents=True, exist_ok=True)
    executable = shutil.which("latexmk") or "/Library/TeX/texbin/latexmk"
    environment = os.environ.copy()
    texbin = Path("/Library/TeX/texbin")
    if texbin.is_dir():
        environment["PATH"] = str(texbin) + os.pathsep + environment.get("PATH", "")
    environment["TEXINPUTS"] = ".:"
    subprocess.run([executable, "-norc", "-r", ".latexmkrc", "-pdf",
                    "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                   cwd=ROOT, env=environment, check=True)
    log = (build / "main.log").read_text()
    issues = [line for line in log.splitlines()
              if re.search(r"Warning|Overfull|Underfull|Undefined control|Missing character|^!", line)]
    if issues:
        raise RuntimeError("Review the LaTeX log before delivery:\n" + "\n".join(issues))
    output = ROOT / "deliverables"
    output.mkdir(exist_ok=True)
    shutil.copy2(build / "main.pdf", ROOT / "main.pdf")
    report = preserve_signature(ROOT / "main.pdf", output / PDF_NAME)
    with zipfile.ZipFile(output / SOURCE_NAME, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, path.relative_to(ROOT))
    checksums = []
    for name in (PDF_NAME, SOURCE_NAME):
        digest = hashlib.sha256((output / name).read_bytes()).hexdigest()
        checksums.append(f"{digest}  {name}")
    (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n")
    (ROOT / "notes/build-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"output": str(output / PDF_NAME), **report}, indent=2))


if __name__ == "__main__":
    main()
