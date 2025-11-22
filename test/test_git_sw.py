"""
Test suite for git-sw command.
"""

from pathlib import Path


class TestGitSw:
    """Test cases for git-sw command."""

    def test_switch_existing_branch(self, test_repo, script_path):
        """Test switching to an existing branch."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit on main.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Create a new branch and switch back to main.
        test_repo.git.branch("feature-branch")
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch in ["main", "master"]

        # Use git-sw to switch to the feature branch.
        result = test_repo.run(script_path, "feature-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the feature branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

    def test_switch_with_create_option(self, test_repo, script_path):
        """Test switching to a new branch with -c option."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Use git-sw with -c to create and switch to a new branch.
        result = test_repo.run(script_path, "-c", "new-feature")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "new-feature"

    def test_switch_to_previous_branch(self, test_repo, script_path):
        """Test switching to the previous branch with dash."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Create and switch to a new branch.
        test_repo.git.branch("feature-branch")
        test_repo.git.switch("feature-branch")

        # Verify we're on feature-branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

        # Use git-sw to switch back to previous branch using dash.
        result = test_repo.run(script_path, "-")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back on the original branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch in ["main", "master"]

    def test_switch_with_detach_option(self, test_repo, script_path):
        """Test switching with --detach option."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Get the commit hash.
        commit_hash = test_repo.git.rev_parse("HEAD").strip()

        # Create another commit.
        Path(test_repo.cwd(), "file2.txt").write_text("More content")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("-m", "second commit")

        # Use git-sw with --detach to enter detached HEAD state.
        result = test_repo.run(script_path, "--detach", commit_hash)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're in detached HEAD state at the correct commit.
        current_commit = test_repo.git.rev_parse("HEAD").strip()
        assert current_commit == commit_hash

    def test_switch_with_discard_changes_option(self, test_repo, script_path):
        """Test switching with --discard-changes option."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        file_path = Path(test_repo.cwd(), "file1.txt")
        file_path.write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Create a new branch.
        test_repo.git.branch("other-branch")

        # Modify the file to create uncommitted changes.
        file_path.write_text("Modified content")

        # Use git-sw with --discard-changes to switch, discarding working changes.
        result = test_repo.run(script_path, "--discard-changes", "other-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the other branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "other-branch"

        # Verify the file was restored (changes discarded).
        assert file_path.read_text() == "Initial content"

    def test_switch_nonexistent_branch(self, test_repo, script_path):
        """Test switching to a non-existent branch fails."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Try to switch to a non-existent branch.
        result = test_repo.run(script_path, "nonexistent-branch")

        # Verify error exit code.
        assert result.returncode != 0

    def test_switch_without_arguments(self, test_repo, script_path):
        """Test that git-sw without arguments fails appropriately."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Run git-sw without arguments.
        result = test_repo.run(script_path)

        # Git switch without arguments will fail - requires a branch name.
        assert result.returncode != 0
