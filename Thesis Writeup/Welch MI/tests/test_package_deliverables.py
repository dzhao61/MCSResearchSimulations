from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "package_deliverables.py"
PREAMBLE = (SCRIPT.parent / "preamble.tex").read_text()
LATEXMKRC = (SCRIPT.parent / ".latexmkrc").read_text()
spec = importlib.util.spec_from_file_location("delivery_package", SCRIPT)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.thesis = self.root / "thesis"
        self.thesis.mkdir()
        self.delivery = self.thesis / "deliverables"
        self.delivery.mkdir()
        self.source = self.thesis / "main.tex"
        self.source.write_text("current source")
        (self.thesis / "preamble.tex").write_text(PREAMBLE)
        self.evidence = self.root / "evidence.txt"
        self.evidence.write_text("current evidence")
        (self.thesis / "main.pdf").write_bytes(b"old compiled PDF")
        self.historical_main = self.thesis / "archive/previous-main.pdf"
        self.historical_main.parent.mkdir()
        self.historical_main.write_bytes(b"historical main PDF")
        self.sources = [(self.source, Path("main.tex"))]
        self.supplement = [(self.evidence, Path("project/evidence.txt"))]
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.object(package, "THESIS", self.thesis))
        stack.enter_context(patch.object(package, "DELIVERABLES", self.delivery))
        stack.enter_context(patch.object(package, "source_files", return_value=self.sources))
        stack.enter_context(patch.object(package, "supplement_files", return_value=self.supplement))

    def publish(self):
        def rebuild():
            (self.thesis / "main.pdf").write_bytes(b"new compiled PDF")
        with patch.object(package, "build_main", side_effect=rebuild) as build:
            with contextlib.redirect_stdout(io.StringIO()):
                package.publish_deliverables()
        return build

    def test_success_builds_before_copying_and_preserves_historical_drafts(self):
        for name in ("Working Draft.pdf", "Working Draft v2.pdf", "Working Draft v3.pdf"):
            (self.delivery / name).write_bytes(b"historical draft")
        build = self.publish()
        build.assert_called_once_with()
        self.assertEqual((self.delivery / package.PDF_NAME).read_bytes(), b"new compiled PDF")
        for name in ("Working Draft.pdf", "Working Draft v2.pdf", "Working Draft v3.pdf"):
            self.assertEqual((self.delivery / name).read_bytes(), b"historical draft")
        self.assertEqual(self.historical_main.read_bytes(), b"historical main PDF")
        self.assertEqual((self.thesis / "main.pdf").read_bytes(), b"new compiled PDF")
        package.check_deliverables()
        self.assertFalse(list(self.delivery.glob(".refresh-*")))

    def test_build_uses_separate_directory_and_updates_canonical_pdf(self):
        def compile_pdf(*args, **kwargs):
            (self.thesis / "build/main.pdf").write_bytes(b"%PDF-fresh build")
            (self.thesis / "build/main.log").write_text("Output written on build/main.pdf")
        with patch.object(package.shutil, "which", return_value="/latexmk"):
            with patch.object(package.subprocess, "run", side_effect=compile_pdf) as run:
                package.build_main()
        args, kwargs = run.call_args
        self.assertIn("-outdir=build", args[0])
        self.assertIn("$success_cmd = '';", args[0])
        self.assertEqual(args[0][-1], "main.tex")
        self.assertEqual(kwargs, {"cwd": self.thesis, "check": True})
        self.assertEqual((self.thesis / "main.pdf").read_bytes(), b"%PDF-fresh build")
        self.assertTrue((self.thesis / "build/chapters_rewrite").is_dir())

    def test_post_build_publishes_without_a_second_compilation(self):
        build = self.thesis / "build"
        build.mkdir()
        compiled = build / "main.pdf"
        compiled.write_bytes(b"%PDF-completed external build")
        compiled.with_suffix(".log").write_text("Output written on build/main.pdf")
        with patch.object(package, "build_main") as rebuild:
            with contextlib.redirect_stdout(io.StringIO()):
                package.publish_deliverables(compiled=compiled)
        rebuild.assert_not_called()
        self.assertEqual((self.delivery / package.PDF_NAME).read_bytes(), compiled.read_bytes())
        package.check_deliverables()

    def test_post_build_rejects_incomplete_or_warning_outputs_before_publishing(self):
        self.publish()
        before = {p.name: p.read_bytes() for p in self.delivery.iterdir()}
        build = self.thesis / "build"
        build.mkdir()
        compiled = build / "main.pdf"
        compiled.write_bytes(b"%PDF-current build")
        for log in (None, "Incomplete run", "Output written on build/main.pdf\nOverfull \\hbox"):
            if log is not None:
                compiled.with_suffix(".log").write_text(log)
            with self.subTest(log=log), self.assertRaises(RuntimeError):
                package.publish_deliverables(compiled=compiled)
            self.assertEqual(before, {p.name: p.read_bytes() for p in self.delivery.iterdir()})

    @unittest.skipUnless(shutil.which("perl"), "The latexmk hook requires Perl.")
    def test_latexmk_hook_targets_only_main_and_passes_output_without_shell_expansion(self):
        hook = self.thesis / ".latexmkrc"
        hook.write_text(LATEXMKRC)
        stub = self.thesis / "package_deliverables.py"
        stub.write_text("import sys\nfrom pathlib import Path\n"
                        "Path('hook-args.txt').write_text(repr(sys.argv[1:]))\n")
        historical = self.thesis / "Working Draft v3.tex"
        historical.write_text("historical source")
        run = subprocess.run(["perl", "-e",
                              'do $ARGV[0] or die $@; welch_publish_delivery($ARGV[1], $ARGV[2]);',
                              str(hook), str(historical), "build/Working Draft v3.pdf"],
                             cwd=self.thesis, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse((self.thesis / "hook-args.txt").exists())
        output = "build/main with spaces.pdf"
        run = subprocess.run(["perl", "-e",
                              'do $ARGV[0] or die $@; welch_publish_delivery($ARGV[1], $ARGV[2]);',
                              str(hook), str(self.source), output],
                             cwd=self.thesis, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual((self.thesis / "hook-args.txt").read_text(),
                         repr(["--publish-built", output]))

    @unittest.skipUnless(shutil.which("perl"), "The latexmk hook requires Perl.")
    def test_latexmk_hook_surfaces_delivery_failure(self):
        hook = self.thesis / ".latexmkrc"
        hook.write_text(LATEXMKRC)
        (self.thesis / "package_deliverables.py").write_text("raise SystemExit(3)\n")
        run = subprocess.run(["perl", "-e",
                              'do $ARGV[0] or die $@; welch_publish_delivery($ARGV[1], $ARGV[2]);',
                              str(hook), str(self.source), "build/main.pdf"],
                             cwd=self.thesis, capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("Delivery refresh failed", run.stderr)

    def test_failed_build_leaves_previous_delivery_untouched(self):
        self.publish()
        before = {p.name: p.read_bytes() for p in self.delivery.iterdir()}
        with patch.object(package, "build_main", side_effect=subprocess.CalledProcessError(1, "latexmk")):
            with self.assertRaises(subprocess.CalledProcessError):
                package.publish_deliverables()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.delivery.iterdir()})

    def test_paragraph_override_stops_build_before_latex_or_pdf_changes(self):
        self.source.write_text(r"\noindent An inconsistent opening paragraph.")
        before = (self.thesis / "main.pdf").read_bytes()
        with patch.object(package.subprocess, "run") as run:
            with self.assertRaisesRegex(AssertionError, "main.tex:1"):
                package.build_main()
        run.assert_not_called()
        self.assertEqual((self.thesis / "main.pdf").read_bytes(), before)

    def test_style_check_ignores_comments_but_rejects_local_length_changes(self):
        self.source.write_text("% \\noindent Historical note\nOrdinary paragraph.")
        package.check_paragraph_style()
        for override in (r"\setlength{\parindent}{1.5em}", r"\parskip=1em"):
            self.source.write_text(override)
            with self.subTest(override=override), self.assertRaises(AssertionError):
                package.check_paragraph_style()

    def test_preamble_cannot_restore_indents_or_override_the_rule_later(self):
        path = self.thesis / "preamble.tex"
        for changed in (
            PREAMBLE.replace(r"\setlength{\parindent}{0pt}",
                             r"\setlength{\parindent}{1.5em}"),
            PREAMBLE + "\n" + r"\parindent=1.5em",
        ):
            path.write_text(changed)
            with self.subTest(changed=changed), self.assertRaises(AssertionError):
                package.check_paragraph_style()

    def test_failed_archive_preparation_leaves_previous_delivery_untouched(self):
        self.publish()
        before = {p.name: p.read_bytes() for p in self.delivery.iterdir()}
        with patch.object(package, "build_main"), patch.object(package, "write_zip", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                package.publish_deliverables()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.delivery.iterdir()})

    def test_check_rejects_stale_pdf_source_evidence_or_checksums(self):
        self.publish()
        for path in (self.thesis / "main.pdf", self.source, self.evidence,
                     self.delivery / "SHA256SUMS.txt"):
            original = path.read_bytes()
            path.write_bytes(b"changed after packaging")
            with self.subTest(path=path.name), self.assertRaises(AssertionError):
                package.check_deliverables()
            path.write_bytes(original)
        package.check_deliverables()

    def test_archive_validation_detects_missing_or_added_members(self):
        self.publish()
        package.write_zip(self.delivery / package.SOURCE_NAME,
                          self.sources + [(self.evidence, Path("unexpected.txt"))])
        with self.assertRaises(AssertionError):
            package.check_archive(self.delivery / package.SOURCE_NAME, self.sources)

    def test_archive_writer_rejects_missing_duplicate_and_unsafe_inputs(self):
        for inputs, error in ((self.sources * 2, ValueError),
                              ([(self.source, Path("../outside"))], ValueError),
                              ([(self.root / "missing", Path("missing"))], FileNotFoundError)):
            path = self.root / "invalid.zip"
            with self.subTest(inputs=inputs), self.assertRaises(error):
                package.write_zip(path, inputs)
            self.assertFalse(path.exists())

    def test_missing_required_directory_does_not_silently_disappear(self):
        with self.assertRaises(FileNotFoundError):
            list(package.clean_files(self.root / "missing"))


if __name__ == "__main__":
    unittest.main()
