"""Exercise automatic publication against temporary local Git repositories."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "package_deliverables.py"
spec = importlib.util.spec_from_file_location("build_push_package", SCRIPT)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class BuildPushTests(unittest.TestCase):
    def git(self, *arguments, repo=None):
        return subprocess.run(["git", "-C", str(repo or self.repo), *arguments],
                              check=True, capture_output=True, text=True).stdout.strip()

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="thesis-push-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "workspace"
        self.repo.mkdir()
        self.remote = self.root / "remote.git"
        self.git("init", "--quiet", "-b", "main")
        self.git("init", "--bare", "--quiet", str(self.remote))
        self.git("config", "user.name", "Build Hook Test")
        self.git("config", "user.email", "build-hook@example.invalid")
        self.git("remote", "add", "origin", str(self.remote))
        self.thesis = self.repo / "Thesis Writeup/Welch MI"
        self.thesis.mkdir(parents=True)
        self.source = self.thesis / "main.tex"
        self.source.write_text("initial source")
        self.unrelated = self.repo / "unrelated.txt"
        self.unrelated.write_text("initial unrelated work")
        self.historical = self.thesis / "Working Draft.pdf"
        self.historical.write_text("historical draft")
        self.presentation = self.thesis / "presentation/slides.txt"
        self.presentation.parent.mkdir()
        self.presentation.write_text("initial slides")
        (self.repo / ".gitignore").write_text("*.npz\n")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Initial state")
        self.git("push", "--quiet", "-u", "origin", "main")
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.object(package, "WORKSPACE", self.repo))
        stack.enter_context(patch.object(package, "THESIS", self.thesis))

    def push(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            package.push_build(**kwargs)

    def remote_head(self, branch="main"):
        return self.git("rev-parse", f"refs/heads/{branch}", repo=self.remote)

    def test_commits_only_build_files_and_preserves_unrelated_staged_work(self):
        self.source.write_text("updated source")
        added = self.thesis / "frontmatter/new [draft].tex"
        added.parent.mkdir()
        added.write_text("new source")
        ignored = self.thesis / "figures_rewrite/large.npz"
        ignored.parent.mkdir()
        ignored.write_text("ignored evidence")
        self.unrelated.write_text("staged unrelated work")
        self.git("add", "unrelated.txt")
        staged = self.git("diff", "--cached", "--binary", "--", "unrelated.txt")
        self.historical.write_text("uncommitted historical edit")
        self.presentation.write_text("uncommitted presentation edit")
        self.push()
        files = set(self.git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())
        self.assertEqual(files, {self.source.relative_to(self.repo).as_posix(),
                                 added.relative_to(self.repo).as_posix()})
        self.assertEqual(self.git("diff", "--cached", "--binary", "--", "unrelated.txt"), staged)
        self.assertEqual(self.git("show", "HEAD:unrelated.txt"), "initial unrelated work")
        self.assertEqual(self.remote_head(), self.git("rev-parse", "HEAD"))
        self.assertFalse(self.git("ls-files", "--", str(ignored)))
        self.assertTrue(self.git("diff", "--", str(self.historical)))
        self.assertTrue(self.git("diff", "--", str(self.presentation)))

    def test_push_rejection_preserves_commit_and_retry_does_not_duplicate_it(self):
        reject = self.remote / "hooks/pre-receive"
        reject.write_text("#!/bin/sh\nexit 1\n")
        reject.chmod(0o755)
        old_remote = self.remote_head()
        self.source.write_text("ready to publish")
        with self.assertRaisesRegex(RuntimeError, "Automatic push failed"):
            self.push()
        local = self.git("rev-parse", "HEAD")
        self.assertNotEqual(local, old_remote)
        self.assertEqual(self.remote_head(), old_remote)
        self.assertEqual(self.source.read_text(), "ready to publish")
        reject.unlink()
        self.push()
        self.assertEqual(self.git("rev-parse", "HEAD"), local)
        self.assertEqual(self.remote_head(), local)

    def test_new_branch_sets_up_matching_origin_branch(self):
        main = self.remote_head()
        self.git("checkout", "--quiet", "-b", "thesis-update")
        self.source.write_text("branch revision")
        self.push()
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "@{upstream}"), "origin/thesis-update")
        self.assertEqual(self.remote_head("thesis-update"), self.git("rev-parse", "HEAD"))
        self.assertEqual(self.remote_head(), main)

    def test_detached_head_does_not_stage_or_commit(self):
        self.git("checkout", "--quiet", "--detach")
        head = self.git("rev-parse", "HEAD")
        self.source.write_text("local revision")
        with self.assertRaises(subprocess.CalledProcessError):
            self.push()
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.assertFalse(self.git("diff", "--cached", "--name-only"))

    def test_explicit_review_notes_can_be_included_without_adding_other_notes(self):
        note = self.thesis / "notes/BUILD_RECORD.md"
        note.parent.mkdir()
        note.write_text("reviewed build record")
        other = note.parent / "UNRELATED.md"
        other.write_text("unfinished work")
        self.push(extra_paths=(note,))
        self.assertEqual(self.git("show", f"HEAD:{note.relative_to(self.repo)}"), note.read_text())
        self.assertFalse(self.git("ls-files", "--", str(other)))


if __name__ == "__main__":
    unittest.main()
