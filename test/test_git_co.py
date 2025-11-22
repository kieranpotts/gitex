"""
Test suite for git-co command.
"""

from pathlib import Path


class TestGitCo:
    """Test cases for git-co command."""

    def test_checkout_existing_branch(self, test_repo, script_path):
        """Test checking out an existing branch."""

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

        # Use git-co to checkout the feature branch.
        result = test_repo.run(script_path, "feature-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the feature branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

    def test_checkout_with_create_branch_option(self, test_repo, script_path):
        """Test checking out a new branch with -b option."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Use git-co with -b to create and checkout a new branch.
        result = test_repo.run(script_path, "-b", "new-feature")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = test_repo.git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "new-feature"

    def test_checkout_specific_file(self, test_repo, script_path):
        """Test checking out a specific file to discard changes."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        file_path = Path(test_repo.cwd(), "file1.txt")
        file_path.write_text("Original content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Modify the file.
        file_path.write_text("Modified content")

        # Verify the file is modified.
        assert file_path.read_text() == "Modified content"

        # Use git-co to checkout the file from HEAD.
        result = test_repo.run(script_path, "HEAD", "--", "file1.txt")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the file is restored to original content.
        assert file_path.read_text() == "Original content"

    def test_checkout_detached_head(self, test_repo, script_path):
        """Test checking out a specific commit (detached HEAD)."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Get the commit hash.
        first_commit_hash = test_repo.git.rev_parse("HEAD").strip()

        # Create another commit.
        Path(test_repo.cwd(), "file2.txt").write_text("More content")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("-m", "second commit")

        # Use git-co to checkout the first commit.
        result = test_repo.run(script_path, first_commit_hash)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're in detached HEAD state at the correct commit.
        current_commit = test_repo.git.rev_parse("HEAD").strip()
        assert current_commit == first_commit_hash

    def test_checkout_without_arguments(self, test_repo, script_path):
        """Test that git-co without arguments behaves like git checkout."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Run git-co without arguments - should show help/error from test_repo.git.
        result = test_repo.run(script_path)

        # Git checkout without arguments will succeed.
        # The exact behavior depends on Git version.
        assert result.returncode == 0

    def test_checkout_nonexistent_branch(self, test_repo, script_path):
        """Test checking out a non-existent branch fails."""

        # Configure Git user.
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Try to checkout a non-existent branch.
        result = test_repo.run(script_path, "nonexistent-branch")

        # Verify error exit code.
        assert result.returncode != 0
