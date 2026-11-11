"""Build and package the isolated direct-derivation thesis copy."""

from pathlib import Path
import hashlib
import os
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
PDF_NAME = "Daniel_Zhao_Welch_MI_Thesis_Direct_Derivation.pdf"
SOURCE_NAME = "Daniel_Zhao_Welch_MI_Thesis_Direct_Derivation_Source.zip"


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
    shutil.copy2(build / "main.pdf", output / PDF_NAME)
    with zipfile.ZipFile(output / SOURCE_NAME, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, path.relative_to(ROOT))
    checksums = []
    for name in (PDF_NAME, SOURCE_NAME):
        digest = hashlib.sha256((output / name).read_bytes()).hexdigest()
        checksums.append(f"{digest}  {name}")
    (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n")
    print(f"Built isolated comparison copy: {output / PDF_NAME}")


if __name__ == "__main__":
    main()
