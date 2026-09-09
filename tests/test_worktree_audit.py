import csv
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/pstack/skills/pstack/scripts/worktree-audit.sh"


@unittest.skipUnless(all(shutil.which(tool) for tool in ["git", "bash", "jq"]),
                     "worktree audit requires git, bash and jq")
class WorktreeAuditTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="pstack-audit-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.repo = self.root / "repo"
        self.run_git("init", "-b", "main", str(self.repo))
        (self.repo / "tracked.txt").write_text("base\n")
        self.run_git("add", ".", cwd=self.repo)
        self.commit(self.repo)
        remote = self.root / "origin.git"
        self.run_git("clone", "--bare", str(self.repo), str(remote))
        self.run_git("remote", "add", "origin", str(remote), cwd=self.repo)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        gh = self.bin / "gh"
        gh.write_text('#!/bin/sh\nprintf "%s\\n" "$PSTACK_TEST_PRS"\n')
        gh.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ["PATH"],
                        PSTACK_TRANSCRIPTS_DIR="", PSTACK_TEST_PRS="[]")

    def run_git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd, check=True,
                              text=True, capture_output=True).stdout.strip()

    def commit(self, path):
        self.run_git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                     "-c", "commit.gpgsign=false", "commit", "-am", "test", cwd=path)
        return self.run_git("rev-parse", "HEAD", cwd=path)

    def worktree(self, name="topic"):
        path = self.root / name
        self.run_git("worktree", "add", "-b", "topic", str(path), cwd=self.repo)
        return path

    def set_pr(self, state, head):
        self.env["PSTACK_TEST_PRS"] = json.dumps([
            {"number": 42, "state": state, "headRefName": "topic", "headRefOid": head}
        ])

    def audit(self):
        result = subprocess.run(["bash", str(SCRIPT), str(self.repo)], env=self.env,
                                check=True, text=True, capture_output=True)
        return list(csv.DictReader(io.StringIO(result.stdout), delimiter="\t"))

    def test_closed_unmerged_pr_does_not_make_unpublished_work_safe(self):
        path = self.worktree()
        (path / "tracked.txt").write_text("unpublished\n")
        head = self.commit(path)
        self.set_pr("CLOSED", head)
        row, = self.audit()
        self.assertEqual(row["MERGED"], "no")
        self.assertEqual(row["REMOTE"], "no-remote")
        self.assertEqual(row["PR"], "#42/CLOSED")
        self.assertEqual(row["BUCKET"], "review")

    def test_old_merged_pr_does_not_cover_new_commits(self):
        path = self.worktree()
        old = self.run_git("rev-parse", "HEAD", cwd=path)
        (path / "tracked.txt").write_text("new work after merge\n")
        self.commit(path)
        self.set_pr("MERGED", old)
        row, = self.audit()
        self.assertEqual(row["BUCKET"], "review")

    def test_merged_pr_at_current_head_is_a_clean_candidate(self):
        path = self.worktree()
        (path / "tracked.txt").write_text("squash merged work\n")
        self.set_pr("MERGED", self.commit(path))
        row, = self.audit()
        self.assertEqual(row["MERGED"], "no")
        self.assertEqual(row["BUCKET"], "safe")

    def test_spaces_in_paths_preserve_untracked_work(self):
        path = self.worktree("topic with spaces")
        (path / "valuable untracked.txt").write_text("keep me\n")
        row, = self.audit()
        self.assertEqual(row["WORKTREE"], str(path))
        self.assertNotEqual(row["DIRTY"], "clean")
        self.assertEqual(row["BUCKET"], "hold-wip")

    def test_main_worktree_with_spaces_is_not_reported_as_a_candidate(self):
        moved = self.root / "main repo with spaces"
        self.repo.rename(moved)
        self.repo = moved
        self.assertEqual(self.audit(), [])

    def test_failed_status_is_unknown_instead_of_clean(self):
        self.worktree()
        self.env["PSTACK_TEST_GIT"] = shutil.which("git")
        git = self.bin / "git"
        git.write_text('#!/bin/sh\nif [ "$1" = "-C" ] && [ "$3" = "status" ]; then\n'
                       '  exit 128\nfi\nexec "$PSTACK_TEST_GIT" "$@"\n')
        git.chmod(0o755)
        row, = self.audit()
        self.assertEqual(row["DIRTY"], "unknown")
        self.assertEqual(row["BUCKET"], "review")

    def test_missing_pr_state_requires_review(self):
        self.worktree()
        (self.bin / "gh").write_text("#!/bin/sh\nexit 1\n")
        row, = self.audit()
        self.assertEqual(row["BUCKET"], "review")

    def test_open_pr_is_held_even_when_an_older_pr_was_merged(self):
        path = self.worktree()
        head = self.run_git("rev-parse", "HEAD", cwd=path)
        self.env["PSTACK_TEST_PRS"] = json.dumps([
            {"number": 41, "state": "MERGED", "headRefName": "topic", "headRefOid": head},
            {"number": 42, "state": "OPEN", "headRefName": "topic", "headRefOid": head},
        ])
        row, = self.audit()
        self.assertEqual(row["BUCKET"], "hold-open-pr")


if __name__ == "__main__":
    unittest.main()
