"""Build the current thesis before publishing verified delivery files."""

from __future__ import annotations

import argparse
import hashlib
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

`Working Draft.pdf` and `Working Draft v2.pdf` are preserved historical
artifacts, not the latest thesis. They are never replaced by packaging.

From the parent thesis folder, run `python3 package_deliverables.py` (or
`make`) to build the current manuscript and refresh all three files together.
Run `python3 package_deliverables.py --check` (or `make check`) to verify
that they still match the current source, main PDF and experimental evidence.
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
            archive.write(source, relative.as_posix())


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
                   "report_large_table_construction_check.py"]
    tests = [
        "test_focused_study.py", "test_focused_report.py", "test_report_formatting.py",
        "test_numerical_degeneracy.py", "test_focused_audit_guards.py",
        "test_thesis_derivation_audit.py", "test_welch.py",
        "test_unequal_sample_check.py",
        "test_focused_mechanisms.py",
        "test_focused_jackknife_check.py", "test_focused_jackknife_report.py",
        "test_large_table_construction_check.py",
    ]
    exact.extend(project / "experiments" / name for name in experiments)
    exact.extend(project / "tests" / name for name in tests)
    for source in exact:
        files.append((source, source.relative_to(WORKSPACE)))
    for directory in (
        project / "src",
        differential / "src",
        project / "results/focused_study",
        project / "results/unequal_sample_check",
        project / "results/large_table_construction_check",
        project / "results/focused_jackknife_check",
    ):
        for source in clean_files(directory):
            if "pilot" in source.relative_to(directory).parts:
                continue
            files.append((source, source.relative_to(WORKSPACE)))
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


def build_main() -> None:
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        fallback = Path("/Library/TeX/texbin/latexmk")
        if not fallback.is_file():
            raise FileNotFoundError("latexmk is required to build current delivery files.")
        latexmk = str(fallback)
    build = THESIS / "build"
    for directory in ("", "chapters_rewrite", "appendices_rewrite"):
        (build / directory).mkdir(parents=True, exist_ok=True)
    subprocess.run([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                    "-outdir=build", "main.tex"], cwd=THESIS, check=True)
    compiled = build / "main.pdf"
    if not compiled.is_file() or compiled.stat().st_size == 0:
        raise RuntimeError("The thesis build did not produce a PDF.")
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


def publish_deliverables() -> None:
    build_main()
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
    parser.add_argument("--check", action="store_true", help="Check existing files without rebuilding.")
    args = parser.parse_args()
    if args.check:
        check_deliverables()
        print("All delivery files match the current PDF, source and evidence.")
    else:
        publish_deliverables()


if __name__ == "__main__":
    main()
