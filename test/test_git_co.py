"""
Test suite for git-co command.
"""

from pathlib import Path


class TestGitCo:
    """Test cases for git-co command."""

    def test_checkout_existing_branch(self, temp_repo, script_path):
        """Test checking out an existing branch."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit on main.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Create a new branch and switch back to main.
        git.branch("feature-branch")
        current_branch = git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch in ["main", "master"]

        # Use git-co to checkout the feature branch.
        result = temp_repo.run(script_path, "feature-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the feature branch.
        current_branch = git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "feature-branch"

    def test_checkout_with_create_branch_option(self, temp_repo, script_path):
        """Test checking out a new branch with -b option."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Use git-co with -b to create and checkout a new branch.
        result = temp_repo.run(script_path, "-b", "new-feature")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "new-feature"

    def test_checkout_specific_file(self, temp_repo, script_path):
        """Test checking out a specific file to discard changes."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        file_path = Path(temp_repo.cwd(), "file1.txt")
        file_path.write_text("Original content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Modify the file.
        file_path.write_text("Modified content")

        # Verify the file is modified.
        assert file_path.read_text() == "Modified content"

        # Use git-co to checkout the file from HEAD.
        result = temp_repo.run(script_path, "HEAD", "--", "file1.txt")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the file is restored to original content.
        assert file_path.read_text() == "Original content"

    def test_checkout_with_multiple_options(self, temp_repo, script_path):
        """Test checkout with multiple options forwarded."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Use git-co with -B to force-create a branch.
        result = temp_repo.run(script_path, "-B", "force-branch")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're on the new branch.
        current_branch = git.rev_parse("--abbrev-ref", "HEAD").strip()
        assert current_branch == "force-branch"

    def test_checkout_detached_head(self, temp_repo, script_path):
        """Test checking out a specific commit (detached HEAD)."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Get the commit hash.
        commit_hash = git.rev_parse("HEAD").strip()

        # Create another commit.
        Path(temp_repo.cwd(), "file2.txt").write_text("More content")
        git.add("file2.txt")
        git.commit("-m", "Second commit")

        # Use git-co to checkout the first commit.
        result = temp_repo.run(script_path, commit_hash)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're in detached HEAD state at the correct commit.
        current_commit = git.rev_parse("HEAD").strip()
        assert current_commit == commit_hash

    def test_checkout_without_arguments(self, temp_repo, script_path):
        """Test that git-co without arguments behaves like git checkout."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Run git-co without arguments (should show help/error from git).
        result = temp_repo.run(script_path)

        # Git checkout without arguments will succeed (just shows current branch info).
        # The exact behavior depends on Git version.
        assert result.returncode == 0

    def test_checkout_nonexistent_branch(self, temp_repo, script_path):
        """Test checking out a non-existent branch fails."""

        git = temp_repo.git()

        # Configure Git user.
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "Initial commit")

        # Try to checkout a non-existent branch.
        result = temp_repo.run(script_path, "nonexistent-branch")

        # Verify error exit code.
        assert result.returncode != 0
