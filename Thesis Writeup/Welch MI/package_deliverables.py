"""Build the current thesis before publishing verified delivery files."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


THESIS = Path(__file__).resolve().parent
WORKSPACE = THESIS.parents[1]
DELIVERABLES = THESIS / "deliverables"
PDF_NAME = "Daniel_Zhao_Welch_MI_Thesis.pdf"
SOURCE_NAME = "Daniel_Zhao_Welch_MI_Thesis_Source.zip"
SUPPLEMENT_NAME = "Daniel_Zhao_Welch_MI_Experiment_Supplement.zip"
DELIVERY_README = """# Current Delivery Files

Use these stable filenames for the latest successfully packaged thesis:

- `Daniel_Zhao_Welch_MI_Thesis.pdf`: final full manuscript to send for review.
- `Daniel_Zhao_Welch_MI_Thesis_Source.zip`: self-contained current LaTeX source.
- `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`: current code and evidence.
- `SHA256SUMS.txt`: checksums for those three current files.

Historical working drafts are preserved in `archive/` and as existing
snapshot PDFs. Packaging builds `main.tex` and never rebuilds those drafts.

From the thesis folder, run `python3 package_deliverables.py` (or
`make`) to build the main manuscript and refresh all three files together.
Run `python3 package_deliverables.py --check` (or `make check`) to verify
that they still match the current source, main PDF and experimental evidence.
Direct `latexmk` builds of `main.tex` also refresh this delivery set through
the project's post-build hook. Failed builds do not publish delivery files.
"""


def clean_files(root: Path, *, suffixes: set[str] | None = None):
    if not root.is_dir():
        raise FileNotFoundError(f"Required input directory is missing: {root}")
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if suffixes is None or path.suffix in suffixes:
            yield path


def write_zip(path: Path, files: list[tuple[Path, Path]]) -> None:
    names = [relative.as_posix() for _, relative in files]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate paths in delivery archive.")
    for source, relative in files:
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe delivery path: {relative}")
        if not source.is_file():
            raise FileNotFoundError(source)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, relative in sorted(files, key=lambda item: item[1].as_posix()):
            archive.write(source, relative.as_posix(),
                          compress_type=zipfile.ZIP_STORED if source.suffix in {".npz", ".zip", ".gz"} else zipfile.ZIP_DEFLATED)


def source_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    root_names = ["main.tex", "preamble.tex", "metadata.tex", "references.bib", "README.md"]
    files.extend((THESIS / name, Path(name)) for name in root_names)
    for directory in ("frontmatter", "chapters_rewrite", "appendices_rewrite"):
        for source in clean_files(THESIS / directory, suffixes={".tex"}):
            files.append((source, source.relative_to(THESIS)))
    for source in clean_files(
        THESIS / "figures_rewrite", suffixes={".pdf", ".py", ".json", ".tex"}
    ):
        if not (source.name.startswith("focused_") or source.name == "evidence_values.tex"):
            continue
        files.append((source, source.relative_to(THESIS)))
    return files


def supplement_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    project = WORKSPACE / "WelchSatterthwaiteMI"
    differential = WORKSPACE / "DifferentialMI"
    exact = [
        project / "README.md",
        project / "EXPERIMENT_SUPPLEMENT_README.md",
        project / "requirements-thesis.txt",
        differential / "pyproject.toml",
    ]
    experiments = ["focused_study_core.py", "run_focused_study.py",
                   "report_focused_study.py", "report_formatting.py", "audit_focused_study.py",
                   "thesis_redesign_core.py", "run_detection_breakdown_sweep.py",
                   "run_unequal_sample_check.py", "report_unequal_sample_check.py",
                   "report_focused_mechanisms.py",
                   "run_focused_jackknife_check.py", "report_focused_jackknife_check.py",
                   "run_large_table_construction_check.py",
                   "report_large_table_construction_check.py",
                   "redesign_study.py", "redesign_report.py", "report_ratio_tools.py",
                   "report_chapter6_mechanisms.py",
                   "calibration_sensitivity.py", "report_calibration_sensitivity.py",
                   "same_skew_extension_core.py", "run_same_skew_extension.py",
                   "report_same_skew_extension.py"]
    tests = [
        "test_calibration_sensitivity.py", "test_report_ratio_tools.py",
        "test_approximation_redesign.py", "test_thesis_consistency.py", "test_focused_study.py", "test_focused_report.py", "test_report_formatting.py",
        "test_numerical_degeneracy.py", "test_focused_audit_guards.py",
        "test_thesis_derivation_audit.py", "test_welch.py",
        "test_unequal_sample_check.py",
        "test_focused_mechanisms.py",
        "test_focused_jackknife_check.py", "test_focused_jackknife_report.py",
        "test_large_table_construction_check.py",
        "test_same_skew_extension.py", "test_same_skew_report.py",
    ]
    exact.extend(project / "experiments" / name for name in experiments)
    exact.extend(project / "tests" / name for name in tests)
    for source in exact:
        files.append((source, source.relative_to(WORKSPACE)))
    files.append((THESIS / "notes/CHAPTER_6_MECHANISM_EVIDENCE_2026-10-28.json",
                  Path("WelchSatterthwaiteMI/supplementary_displays/chapter6_mechanisms/evidence.json")))
    for directory in (
        project / "src",
        differential / "src",
        project / "results/approximation_redesign",
        project / "results/focused_study",
        project / "results/unequal_sample_check",
        project / "results/large_table_construction_check",
        project / "results/focused_jackknife_check",
        project / "results/same_skew_extension",
        project / "supplementary_displays",
    ):
        for source in clean_files(directory):
            if "pilot" in source.relative_to(directory).parts:
                continue
            files.append((source, source.relative_to(WORKSPACE)))
    for name in (
        "focused_null_table.tex",
        "focused_detection_margins_full.pdf",
        "focused_same_detection_sizes_full.pdf",
    ):
        files.append((THESIS / "figures_rewrite" / name,
                      Path("WelchSatterthwaiteMI/supplementary_displays") / name))
    for source in clean_files(differential / "tests", suffixes={".py"}):
        files.append((source, source.relative_to(WORKSPACE)))
    practical = WORKSPACE / "PracticalMIExploration"
    for name in ("run_exploration.py", "test_exploration.py", "test_thesis_application.py",
                 "README.md", "PROTOCOL.md"):
        source = practical / name
        files.append((source, source.relative_to(WORKSPACE)))
    for directory in (practical / "raw", practical / "thesis_application"):
        for source in clean_files(directory):
            files.append((source, source.relative_to(WORKSPACE)))
    return files


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_paragraph_style() -> None:
    """Reject paragraph-style drift before compiling or checking a delivery."""
    def uncomment(text: str) -> str:
        return re.sub(r"(?<!\\)%[^\n]*", "", text)

    preamble = uncomment((THESIS / "preamble.tex").read_text())
    required = {
        "use no paragraph indent": r"\\setlength\{\\parindent\}\{0pt\}",
        "use half a line of paragraph spacing": r"\\setlength\{\\parskip\}\{0\.5\\baselineskip\}",
    }
    for description, pattern in required.items():
        if len(re.findall(pattern, preamble)) != 1:
            raise AssertionError(f"Paragraph style must {description} in preamble.tex.")
    for length in ("parindent", "parskip"):
        if len(re.findall(r"\\" + length + r"\b", preamble)) != 1:
            raise AssertionError(f"Define {length} only once in preamble.tex.")
    overrides = re.compile(
        r"\\(?:noindent|indent|parindent|parskip|parshape|hangindent|hangafter|"
        r"@afterindenttrue|@afterindentfalse)\b"
    )
    for source, relative in source_files():
        if source.suffix != ".tex" or relative == Path("preamble.tex"):
            continue
        for number, line in enumerate(uncomment(source.read_text()).splitlines(), 1):
            if overrides.search(line):
                raise AssertionError(
                    f"Local paragraph-style override at {relative}:{number}; "
                    "use the shared preamble rule."
                )


def build_main() -> None:
    check_paragraph_style()
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        fallback = Path("/Library/TeX/texbin/latexmk")
        if not fallback.is_file():
            raise FileNotFoundError("latexmk is required to build current delivery files.")
        latexmk = str(fallback)
    build = THESIS / "build"
    for directory in ("", "chapters_rewrite", "appendices_rewrite"):
        (build / directory).mkdir(parents=True, exist_ok=True)
    # This command publishes once below; suppress the direct-latexmk hook here.
    subprocess.run([latexmk, "-e", "$success_cmd = '';", "-pdf",
                    "-interaction=nonstopmode", "-halt-on-error",
                    "-outdir=build", "main.tex"], cwd=THESIS, check=True)
    sync_main_pdf(build / "main.pdf")


def sync_main_pdf(compiled: Path) -> None:
    compiled = compiled.resolve()
    if compiled.name != "main.pdf" or THESIS.resolve() not in compiled.parents:
        raise ValueError("Only a main.pdf inside the active thesis folder can be published.")
    if not compiled.is_file() or compiled.stat().st_size == 0:
        raise RuntimeError("The thesis build did not produce a PDF.")
    if not compiled.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("The thesis build output is not a PDF.")
    log = compiled.with_suffix(".log")
    if not log.is_file() or "Output written on" not in log.read_text(errors="replace"):
        raise RuntimeError("A completed LaTeX log is required before publishing.")
    issues = [line for line in log.read_text(errors="replace").splitlines()
              if any(marker in line for marker in ("Warning", "Overfull", "Underfull"))]
    if issues:
        raise RuntimeError("Resolve LaTeX formatting/reference warnings before publishing:\n"
                           + "\n".join(issues))
    target = THESIS / "main.pdf"
    if not target.exists() or sha256(target) != sha256(compiled):
        temporary = THESIS / ".main.pdf.tmp"
        shutil.copyfile(compiled, temporary)
        temporary.replace(target)


def check_archive(path: Path, files: list[tuple[Path, Path]]) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(files) or set(names) != {p.as_posix() for _, p in files}:
            raise AssertionError(f"Delivery archive inventory is stale: {path.name}")
        for source, relative in files:
            with archive.open(relative.as_posix()) as handle:
                digest = hashlib.file_digest(handle, "sha256").hexdigest()
            if digest != sha256(source):
                raise AssertionError(f"Delivery archive is stale: {path.name}: {relative}")


def check_deliverables() -> None:
    check_paragraph_style()
    if sha256(DELIVERABLES / PDF_NAME) != sha256(THESIS / "main.pdf"):
        raise AssertionError("Delivery PDF does not match the current main PDF.")
    check_archive(DELIVERABLES / SOURCE_NAME, source_files())
    check_archive(DELIVERABLES / SUPPLEMENT_NAME, supplement_files())
    expected = "".join(f"{sha256(DELIVERABLES / name)}  {name}\n"
                       for name in (PDF_NAME, SOURCE_NAME, SUPPLEMENT_NAME))
    if (DELIVERABLES / "SHA256SUMS.txt").read_text() != expected:
        raise AssertionError("Delivery checksums are stale.")
    if (DELIVERABLES / "README.md").read_text() != DELIVERY_README:
        raise AssertionError("Delivery instructions are stale.")


def publish_deliverables(*, compiled: Path | None = None) -> None:
    if compiled is None:
        build_main()
    else:
        check_paragraph_style()
        sync_main_pdf(compiled)
    DELIVERABLES.mkdir(exist_ok=True)
    sources, supplement = source_files(), supplement_files()
    # Prepare and verify everything before replacing the previous delivery set.
    with tempfile.TemporaryDirectory(prefix=".refresh-", dir=DELIVERABLES) as temporary:
        staging = Path(temporary)
        shutil.copyfile(THESIS / "main.pdf", staging / PDF_NAME)
        write_zip(staging / SOURCE_NAME, sources)
        write_zip(staging / SUPPLEMENT_NAME, supplement)
        check_archive(staging / SOURCE_NAME, sources)
        check_archive(staging / SUPPLEMENT_NAME, supplement)
        (staging / "README.md").write_text(DELIVERY_README)
        checksums = "".join(f"{sha256(staging / name)}  {name}\n"
                            for name in (PDF_NAME, SOURCE_NAME, SUPPLEMENT_NAME))
        (staging / "SHA256SUMS.txt").write_text(checksums)
        for name in (PDF_NAME, SOURCE_NAME, SUPPLEMENT_NAME, "README.md", "SHA256SUMS.txt"):
            (staging / name).replace(DELIVERABLES / name)
    for name in (PDF_NAME, SOURCE_NAME, SUPPLEMENT_NAME):
        print(f"{name}: {(DELIVERABLES / name).stat().st_size} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    checks = parser.add_mutually_exclusive_group()
    checks.add_argument("--check", action="store_true", help="Check existing files without rebuilding.")
    checks.add_argument("--check-style", action="store_true",
                        help="Check paragraph-style sources without building or refreshing files.")
    checks.add_argument("--publish-built", type=Path, metavar="PDF",
                        help="Post-build hook: publish a completed main PDF without compiling again.")
    args = parser.parse_args()
    if args.publish_built is not None:
        compiled = args.publish_built
        if not compiled.is_absolute():
            compiled = THESIS / compiled
        publish_deliverables(compiled=compiled)
    elif args.check_style:
        check_paragraph_style()
        print("Paragraph style is consistent across the current thesis sources.")
    elif args.check:
        check_deliverables()
        print("All delivery files match the current PDF, source and evidence.")
    else:
        publish_deliverables()


if __name__ == "__main__":
    main()
