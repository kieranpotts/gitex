"""
Test suite for git-sw command.
"""

import os


class TestGitSw:
    """Test cases for git-sw command."""

    def test_switch_existing_branch(self, repo, bin):
        """Test switching to an existing branch."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit on main.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create a new branch and switch back to main.
        repo.git.branch("feature-branch")
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch in ["main", "master"]

        # Use git-sw to switch to the feature branch.
        result = repo.run(bin, "feature-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the feature branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

    def test_switch_with_create_option(self, repo, bin):
        """Test switching to a new branch with -c option."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Use git-sw with -c to create and switch to a new branch.
        result = repo.run(bin, "-c", "new-feature")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "new-feature"

    def test_switch_to_previous_branch(self, repo, bin):
        """Test switching to the previous branch with dash."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create and switch to a new branch.
        repo.git.branch("feature-branch")
        repo.git.switch("feature-branch")

        # Verify we're on feature-branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

        # Use git-sw to switch back to previous branch using dash.
        result = repo.run(bin, "-")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back on the original branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch in ["main", "master"]

    def test_switch_with_detach_option(self, repo, bin):
        """Test switching with --detach option."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Get the commit hash.
        commit_hash = repo.git.rev_parse("HEAD").strip()

        # Create another commit.
        repo.write("file2.txt", "More content")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "second commit")

        # Use git-sw with --detach to enter detached HEAD state.
        result = repo.run(bin, "--detach", commit_hash)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're in detached HEAD state at the correct commit.
        current_commit = repo.git.rev_parse("HEAD").strip()
        assert current_commit == commit_hash

    def test_switch_with_discard_changes_option(self, repo, bin):
        """Test switching with --discard-changes option."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create a new branch.
        repo.git.branch("other-branch")

        # Modify the file to create uncommitted changes.
        repo.write("file1.txt", "Modified content")

        # Use git-sw with --discard-changes to switch, discarding working changes.
        result = repo.run(bin, "--discard-changes", "other-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the other branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "other-branch"

        # Verify the file was restored (changes discarded).
        file_path = os.path.join(repo.dir(), "file1.txt")
        with open(file_path, "r") as f:
            assert f.read() == "Initial content"

    def test_switch_nonexistent_branch(self, repo, bin):
        """Test switching to a non-existent branch fails."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Try to switch to a non-existent branch.
        result = repo.run(bin, "nonexistent-branch")

        # Verify error exit code.
        assert result.returncode != 0

    def test_switch_without_arguments(self, repo, bin):
        """Test that git-sw without arguments fails appropriately."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Run git-sw without arguments.
        result = repo.run(bin)

        # Git switch without arguments will fail - requires a branch name.
        assert result.returncode != 0
