"""
Test suite for git-co command.
"""


class TestGitCo:
    """Test cases for git-co command."""

    def test_checkout_existing_branch(self, repo, bin):
        """Test checking out an existing branch."""

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
        assert current_branch == "main"

        # Use git-co to checkout the feature branch.
        result = repo.run(bin, "feature-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the feature branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

    def test_checkout_with_create_branch_option(self, repo, bin):
        """Test checking out a new branch with -b option."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Use git-co with -b to create and checkout a new branch.
        result = repo.run(bin, "-b", "new-feature")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "new-feature"

    def test_checkout_specific_file(self, repo, bin):
        """Test checking out a specific file to discard changes."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Original content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Modify the file.
        repo.write("file1.txt", "Modified content")

        # Verify the file is modified.
        assert repo.read("file1.txt") == "Modified content"

        # Use git-co to checkout the file from HEAD.
        result = repo.run(bin, "HEAD", "--", "file1.txt")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the file is restored to original content.
        assert repo.read("file1.txt") == "Original content"

    def test_checkout_detached_head(self, repo, bin):
        """Test checking out a specific commit (detached HEAD)."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Get the commit hash.
        first_commit_hash = repo.git.rev_parse("HEAD").strip()

        # Create another commit.
        repo.write("file2.txt", "More content")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "second commit")

        # Use git-co to checkout the first commit.
        result = repo.run(bin, first_commit_hash)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're in detached HEAD state at the correct commit.
        current_commit = repo.git.rev_parse("HEAD").strip()
        assert current_commit == first_commit_hash

    def test_checkout_without_arguments(self, repo, bin):
        """Test that git-co without arguments behaves like git checkout."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Run git-co without arguments - should show help/error from repo.git.
        result = repo.run(bin)

        # Git checkout without arguments will succeed.
        # The exact behavior depends on Git version.
        assert result.returncode == 0

    def test_checkout_nonexistent_branch(self, repo, bin):
        """Test checking out a non-existent branch fails."""

        # Configure Git user.
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Try to checkout a non-existent branch.
        result = repo.run(bin, "nonexistent-branch")

        # Verify error exit code.
        assert result.returncode != 0
