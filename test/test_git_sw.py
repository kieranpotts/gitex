"""
Test suite for git-sw command.
"""


class TestGitSw:
    """Test cases for git-sw command."""

    def test_switch_existing_branch(self, repo, bin):
        """Test switching to an existing branch."""

        # Create initial commit on main.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create a new branch and switch back to main.
        repo.git.branch("feature-branch")
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "main"

        # Run 'git-sw' inside the test repository.
        # Switch to the feature branch.
        result = repo.run(bin, "feature-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the feature branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

    def test_switch_with_create_option(self, repo, bin):
        """Test switching to a new branch with -c option."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Run 'git-sw' inside the test repository.
        # Use the '-c' option to create and switch to a new branch.
        result = repo.run(bin, "-c", "new-feature")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "new-feature"

    def test_switch_to_previous_branch(self, repo, bin):
        """Test switching to the previous branch with dash."""

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

        # Run 'git-sw' inside the test repository.
        # Switch back to the previous branch using the dash syntax.
        result = repo.run(bin, "-")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back on the original branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "main"

    def test_switch_with_detach_option(self, repo, bin):
        """Test switching with --detach option."""

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

        # Run 'git-sw' inside the test repository.
        # Use the '--detach' option to enter detached HEAD state.
        result = repo.run(bin, "--detach", commit_hash)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're in detached HEAD state at the correct commit.
        current_commit = repo.git.rev_parse("HEAD").strip()
        assert current_commit == commit_hash

    def test_switch_with_discard_changes_option(self, repo, bin):
        """Test switching with --discard-changes option."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create a new branch.
        repo.git.branch("other-branch")

        # Modify the file to create uncommitted changes.
        repo.write("file1.txt", "Modified content")

        # Run 'git-sw' inside the test repository.
        # Use '--discard-changes' to discard any unstaged and uncommitted
        # working changes.
        result = repo.run(bin, "--discard-changes", "other-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the other branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "other-branch"

        # Verify the file was restored (changes discarded).
        assert repo.read("file1.txt") == "Initial content"

    def test_switch_nonexistent_branch(self, repo, bin):
        """Test switching to a non-existent branch fails."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Run 'git-sw' inside the test repository.
        # Try to switch to a non-existent branch.
        result = repo.run(bin, "nonexistent-branch")

        # Verify error exit code.
        assert result.returncode != 0

    def test_switch_without_arguments(self, repo, bin):
        """Test that git-sw without arguments fails appropriately."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Run 'git-sw' without any arguments.
        result = repo.run(bin)

        # Git switch without arguments will fail - requires a branch name.
        assert result.returncode != 0
