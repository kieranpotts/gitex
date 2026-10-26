"""
Test suite for git-orphan command.
"""

import os


class TestGitOrphan:
    """Test cases for git-orphan command."""

    def _initial_commit(self, repo):
        """Create an initial commit, so there is a history to detach from."""

        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

    def test_create_orphan_with_argument(self, repo, bin):
        """Test creating an orphan branch with name provided as argument."""

        self._initial_commit(repo)

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "orphan-branch")

        # Verify success exit code and message.
        assert result.returncode == 0
        assert "Switched to new orphan branch 'orphan-branch'." in result.stdout

        # Verify we're on the new branch.
        assert repo.git.symbolic_ref("--short", "HEAD") == "orphan-branch"

        # Verify the previous branch's files are carried over and staged.
        assert "A  file1.txt" in repo.git.status("--porcelain")

        # Verify the first commit on the new branch has no parents.
        repo.git.commit("-m", "first orphan commit")
        assert repo.git.show("-s", "--format=%P", "HEAD") == ""

    def test_create_orphan_with_stdin(self, repo, bin):
        """Test creating an orphan branch with name provided via stdin."""

        self._initial_commit(repo)

        # Run 'git-orphan' inside the test repository.
        # Provide branch name via stdin.
        result = repo.run(bin, input="interactive-branch\n")

        # Verify we're on the new branch.
        assert result.returncode == 0
        assert repo.git.symbolic_ref("--short", "HEAD") == "interactive-branch"

    def test_working_changes_are_staged(self, repo, bin):
        """Test that working changes are carried over and staged without --fresh."""

        self._initial_commit(repo)

        # Make unstaged and untracked changes.
        repo.write("file1.txt", "Modified content")
        repo.write("file2.txt", "New file")

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "orphan-branch")

        # Verify no confirmation was required.
        assert result.returncode == 0

        # Verify tracked files, with their working changes, are staged.
        status = repo.git.status("--porcelain")
        assert "A  file1.txt" in status
        assert repo.git.show(":file1.txt") == "Modified content"

        # Verify untracked files are staged, too.
        assert "A  file2.txt" in status

    def test_fresh_with_clean_working_tree(self, repo, bin):
        """Test that --fresh clears the index and working tree without prompting."""

        self._initial_commit(repo)

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "orphan-branch", "--fresh")

        # Verify success without a prompt.
        assert result.returncode == 0
        assert "Delete them and continue?" not in result.stdout

        # Verify we're on the new branch.
        assert repo.git.symbolic_ref("--short", "HEAD") == "orphan-branch"

        # Verify the index and working tree are empty.
        assert repo.git.ls_files() == ""
        assert not repo.exists("file1.txt")

    def test_fresh_confirmed_deletes_changes(self, repo, bin):
        """Test that confirming the --fresh prompt deletes all changes."""

        self._initial_commit(repo)

        # Make staged, unstaged, and untracked changes.
        repo.write("file1.txt", "Modified content")
        repo.write("staged.txt", "Staged file")
        repo.git.add("staged.txt")
        repo.mkdir("dir")
        repo.write("dir/untracked.txt", "Untracked file")

        # Run 'git-orphan' inside the test repository.
        # Confirm the deletion via stdin.
        result = repo.run(bin, "orphan-branch", "--fresh", input="y\n")

        # Verify the user was warned and prompted.
        assert result.returncode == 0
        assert "--fresh will delete" in result.stderr
        assert "Delete them and continue?" in result.stdout

        # Verify the index and working tree are empty.
        assert repo.git.ls_files() == ""
        assert repo.git.status("--porcelain") == ""
        assert not repo.exists("file1.txt")
        assert not repo.exists("staged.txt")
        assert not repo.exists("dir")

    def test_fresh_declined_changes_nothing(self, repo, bin):
        """Test that declining the --fresh prompt aborts without changes."""

        self._initial_commit(repo)

        # Make an untracked change.
        repo.write("file2.txt", "New file")

        # Run 'git-orphan' inside the test repository.
        # Decline the deletion via stdin.
        result = repo.run(bin, "orphan-branch", "--fresh", input="n\n")

        # Verify error exit code and message.
        assert result.returncode == 1
        assert "Aborted" in result.stdout

        # Verify nothing was changed.
        assert repo.git.symbolic_ref("--short", "HEAD") == "main"
        assert "orphan-branch" not in repo.git.branch()
        assert repo.exists("file1.txt")
        assert repo.exists("file2.txt")

    def test_fresh_keeps_ignored_files(self, repo, bin):
        """Test that --fresh keeps ignored files."""

        repo.write(".gitignore", "ignored.txt\n")
        repo.git.add(".gitignore")
        repo.git.commit("-m", "initial commit")
        repo.write("ignored.txt", "Ignored file")

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "orphan-branch", "--fresh")

        # Verify no prompt is needed for ignored files.
        assert result.returncode == 0
        assert "Delete them and continue?" not in result.stdout

        # Verify tracked files are removed but ignored files are kept.
        assert not repo.exists(".gitignore")
        assert repo.exists("ignored.txt")

    def test_fresh_from_subdirectory(self, repo, bin):
        """Test that --fresh clears the whole working tree from a subdirectory."""

        self._initial_commit(repo)
        repo.mkdir("sub")
        repo.write("sub/file2.txt", "Nested content")
        repo.git.add("sub/file2.txt")
        repo.git.commit("-m", "second commit")

        # Run 'git-orphan' from a subdirectory of the test repository.
        result = repo.run(bin, "orphan-branch", "--fresh", cwd=repo.path("sub"))

        # Verify the whole working tree was cleared.
        assert result.returncode == 0
        assert repo.git.ls_files() == ""
        assert not repo.exists("file1.txt")

    def test_reject_empty_branch_name_from_stdin(self, repo, bin):
        """Test that empty branch name via stdin is rejected."""

        self._initial_commit(repo)

        # Run 'git-orphan' inside the test repository.
        # Provide empty branch name via stdin.
        result = repo.run(bin, input="\n")

        # Verify error exit code and message.
        assert result.returncode == 1
        assert "Branch name cannot be empty." in result.stderr

    def test_reject_invalid_branch_name(self, repo, bin):
        """Test that an invalid branch name is rejected."""

        self._initial_commit(repo)

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "bad..name")

        # Verify error exit code and message.
        assert result.returncode == 1
        assert "is not a valid branch name." in result.stderr

    def test_reject_existing_branch_name(self, repo, bin):
        """Test that creating an orphan branch with an existing name fails."""

        self._initial_commit(repo)
        repo.git.branch("existing-branch")

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "existing-branch")

        # Verify error exit code and message.
        assert result.returncode == 1
        assert "already exists." in result.stderr

        # Verify we're still on the original branch.
        assert repo.git.symbolic_ref("--short", "HEAD") == "main"

    def test_reject_multiple_arguments(self, repo, bin):
        """Test that multiple positional arguments are rejected."""

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "branch1", "branch2")

        # Verify error exit code and message.
        assert result.returncode == 1
        assert "Unexpected argument 'branch2'." in result.stderr

    def test_reject_unknown_option(self, repo, bin):
        """Test that unknown options are rejected."""

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "--bogus")

        # Verify error exit code and message.
        assert result.returncode == 1
        assert "Unknown option '--bogus'." in result.stderr
        assert "git orphan --help" in result.stderr

    def test_help(self, repo, bin):
        """Test that --help prints usage instructions."""

        # Run 'git-orphan' inside the test repository.
        result = repo.run(bin, "--help")

        # Verify success exit code and usage output.
        assert result.returncode == 0
        assert "Usage: git orphan [<branch>] [--fresh] [--no-color]" in result.stdout
        assert "--no-color  Disable colored output." in result.stdout

    def test_force_color(self, repo, bin):
        """Test that FORCE_COLOR enables color when output is not a TTY."""

        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        env = {**os.environ, "FORCE_COLOR": "1"}
        result = repo.run(bin, "gh-pages", env=env)

        # Verify the success message is colored.
        assert result.returncode == 0
        assert "\033[" in result.stdout

    def test_no_color_flag(self, repo, bin):
        """Test that --no-color disables color, even when FORCE_COLOR is set."""

        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        env = {**os.environ, "FORCE_COLOR": "1"}
        result = repo.run(bin, "gh-pages", "--no-color", env=env)

        # Verify the branch is created and the output has no ANSI codes.
        assert result.returncode == 0
        assert "success: Switched to new orphan branch 'gh-pages'." in result.stdout
        assert "\033[" not in result.stdout
        assert "\033[" not in result.stderr

    def test_no_color_variable(self, repo, bin):
        """Test that NO_COLOR disables color, even when FORCE_COLOR is set."""

        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        env = {**os.environ, "FORCE_COLOR": "1", "NO_COLOR": "1"}
        result = repo.run(bin, "gh-pages", env=env)

        assert result.returncode == 0
        assert "success: Switched to new orphan branch 'gh-pages'." in result.stdout
        assert "\033[" not in result.stdout
        assert "\033[" not in result.stderr
