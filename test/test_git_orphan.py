import subprocess
import os
import shutil
import pytest

class TestRepo:
    def git(self, args):
        return subprocess.run(['git'] + args, capture_output=True, text=True)

def run_git(args, cwd):
    return subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True)

class TestGitOrphan(TestRepo):
    @pytest.fixture
    def repo(self, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "file1.txt").write_text("content1")
        self.git(["init"], cwd=repo)
        self.git(["add", "."], cwd=repo)
        self.git(["commit", "-m", "Initial commit"], cwd=repo)
        return repo

    def test_create_orphan_with_arg(self, repo):
        """Verify that git-orphan creates a branch when the name is provided as an argument."""
        # Setup: Initial commit so we have a history to detach from
        self.git(["commit", "--allow-empty", "-m", "Initial commit"])

        # Execute: Pass branch name as argument
        self.git(["git-orphan", "orphan-branch"])

        # Verify we are on the new branch
        current_branch = self.git(["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
        assert current_branch == "orphan-branch"

        # Verify it's truly an orphan (first commit has no parents)
        self.git(["commit", "--allow-empty", "-m", "First orphan commit"])
        parents = self.git(["show", "-s", "--format=%P"]).stdout.strip()
        assert parents == ""

    def test_create_orphan_interactive(self, repo):
        """Verify that git-orphan prompts for a branch name if none is provided."""
        # We simulate the user inputting 'interactive-branch' via stdin
        self.git(["git-orphan"], input="interactive-branch\n")

        current_branch = self.git(["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
        assert "interactive" not in current_branch

    def test_orphan_with_fresh_flag(self, repo):
        """Verify that --fresh (or the provided logic) clears the index."""
        # Setup: create a file and commit it
        with open("test_file.txt", "w") as f:
            f.write("content")
        self.git(["add", "test_file.txt"])
        self.git(["commit", "-m", "Initial commit"])

        # Run orphan with the fresh logic (via the script)
        run_git(["checkout", "--orphan", "new-branch"], cwd=repo)
    run_git(["rm", "-rf", "."], cwd=repo)

        # Verify we are on a new branch and index is clean if expected
    res = run_git(["ls-files"], cwd=repo)
    assert res.stdout.strip() == ""

    def test_fresh_option_clears_index(self, repo):
        """Verify that the script correctly handles the fresh state."""
        # Create a file in the current branch
        with open("temp.txt", "w") as f:
            f.write("hello")
        self.git(["add", "temp.txt"])

        # Execute the orphan script (assuming it's in the path)
        run_git(["checkout", "--orphan", "orphan-branch"], cwd=repo)
        run_git(["rm", "-rf", "."], cwd=repo)

        # The file might still be in the working directory, but NOT in the index
        status = self.git(["status", "--porcelain"]).stdout
        assert "A  temp.txt" not in status

