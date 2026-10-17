"""Build the final PDF, source archive, experiment supplement and checksums."""

from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path


THESIS = Path(__file__).resolve().parent
WORKSPACE = THESIS.parents[1]
DELIVERABLES = THESIS / "deliverables"


def clean_files(root: Path, *, suffixes: set[str] | None = None):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if suffixes is None or path.suffix in suffixes:
            yield path


def write_zip(path: Path, files: list[tuple[Path, Path]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, relative in sorted(files, key=lambda item: item[1].as_posix()):
            archive.write(source, relative.as_posix())


def source_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    root_names = [
        "main.tex", "main(improved conjuntion).tex", "AGENTS.md",
        "preamble.tex", "metadata.tex", "references.bib", "README.md",
        "package_deliverables.py",
        "EXEMPLAR_REVIEW_NOTES.md", "DLI_EXEMPLAR_REVIEW_NOTES.md",
        "LITERATURE_SOURCE_CHECK.md", "REVIEW_RESPONSE.md",
        "BIBLIOGRAPHY_REVIEW_RESPONSE.md",
        "SCIENTIFIC_AUDIT.md", "SUBMISSION_CHECK.md", "THESIS_GOAL.md",
        "THESIS_REWRITE_PLAN.md",
        "FOCUSED_EXPERIMENT_PLAN.md",
        "THESIS_DEPTH_PLAN.md",
        "UNEQUAL_SAMPLE_CHECK_PLAN.md",
        "LARGE_TABLE_CONSTRUCTION_CHECK_PLAN.md",
    ]
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
    return files


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    DELIVERABLES.mkdir(exist_ok=True)
    pdf = DELIVERABLES / "Daniel_Zhao_Welch_MI_Thesis.pdf"
    source_zip = DELIVERABLES / "Daniel_Zhao_Welch_MI_Thesis_Source.zip"
    supplement_zip = DELIVERABLES / "Daniel_Zhao_Welch_MI_Experiment_Supplement.zip"
    shutil.copyfile(THESIS / "main.pdf", pdf)
    write_zip(source_zip, source_files())
    write_zip(supplement_zip, supplement_files())
    artifacts = [pdf, source_zip, supplement_zip]
    checksums = "".join(f"{sha256(path)}  {path.name}\n" for path in artifacts)
    (DELIVERABLES / "SHA256SUMS.txt").write_text(checksums)
    for artifact in artifacts:
        print(f"{artifact.name}: {artifact.stat().st_size} bytes")


if __name__ == "__main__":
    main()
