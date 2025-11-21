"""
Test suite for git-contrib command.
"""


class TestGitContrib:
    """Test cases for git-contrib command."""

    def test_single_contributor(self, temp_repo, script_path):
        """Test with a single contributor."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create some commits.
        temp_repo.write("file1.txt", "content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        temp_repo.write("file2.txt", "content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        result = temp_repo.run(script_path)

        assert result.returncode == 0
        assert "John Doe" in result.stdout
        assert "john.doe@example.com" in result.stdout
        assert "2" in result.stdout  # Commit count

    def test_multiple_contributors(self, temp_repo, script_path):
        """Test with multiple contributors."""

        git = temp_repo.git()

        # First contributor.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")
        temp_repo.write("file1.txt", "content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Second contributor with more commits.
        git.config("--local", "user.name", "Jane Smith")
        git.config("--local", "user.email", "jane.smith@example.com")
        temp_repo.write("file2.txt", "content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")
        temp_repo.write("file3.txt", "content 3")
        git.add("file3.txt")
        git.commit("-m", "third commit")

        # Third contributor.
        git.config("--local", "user.name", "Bob Johnson")
        git.config("--local", "user.email", "bob@example.com")
        temp_repo.write("file4.txt", "content 4")
        git.add("file4.txt")
        git.commit("-m", "fourth commit")

        result = temp_repo.run(script_path)

        assert result.returncode == 0

        # Verify all contributors are listed.
        assert "John Doe" in result.stdout
        assert "john.doe@example.com" in result.stdout
        assert "Jane Smith" in result.stdout
        assert "jane.smith@example.com" in result.stdout
        assert "Bob Johnson" in result.stdout
        assert "bob@example.com" in result.stdout

        # Verify the output is ordered by commit count (descending).
        # Jane Smith should appear first (2 commits).
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 3
        assert "Jane Smith" in lines[0]
        assert "2" in lines[0]

    def test_output_format(self, temp_repo, script_path):
        """Test the output format matches git shortlog expectations."""

        git = temp_repo.git()
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create a commit.
        temp_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "test commit")

        result = temp_repo.run(script_path)

        assert result.returncode == 0

        # Output should be in format: "     N\tName <email>"
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 1
        assert "\t" in lines[0]  # Tab-separated
        assert "John Doe <john.doe@example.com>" in lines[0]
        assert "1" in lines[0]  # Commit count

    def test_with_no_commits(self, temp_repo, script_path):
        """Test with a repository that has no commits."""

        result = temp_repo.run(script_path)

        # git shortlog returns success but empty output for repos with no commits.
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_rejects_single_argument(self, temp_repo, script_path):
        """Test that the command rejects arguments."""

        result = temp_repo.run(script_path, "--help")

        assert result.returncode == 1
        assert "git-contrib does not accept any options" in result.stderr

    def test_rejects_multiple_arguments(self, temp_repo, script_path):
        """Test that the command rejects multiple arguments."""

        result = temp_repo.run(script_path, "arg1", "arg2")

        assert result.returncode == 1
        assert "git-contrib does not accept any options" in result.stderr

    def test_ordering_by_commit_count(self, temp_repo, script_path):
        """Test that contributors are ordered by commit count (descending)."""

        git = temp_repo.git()

        # Contributor with 1 commit.
        git.config("--local", "user.name", "Alice")
        git.config("--local", "user.email", "alice@example.com")
        temp_repo.write("file1.txt", "content 1")
        git.add("file1.txt")
        git.commit("-m", "commit 1")

        # Contributor with 3 commits.
        git.config("--local", "user.name", "Bob")
        git.config("--local", "user.email", "bob@example.com")
        for i in range(2, 5):
            temp_repo.write(f"file{i}.txt", f"content {i}")
            git.add(f"file{i}.txt")
            git.commit("-m", f"commit {i}")

        # Contributor with 2 commits.
        git.config("--local", "user.name", "Charlie")
        git.config("--local", "user.email", "charlie@example.com")
        for i in range(5, 7):
            temp_repo.write(f"file{i}.txt", f"content {i}")
            git.add(f"file{i}.txt")
            git.commit("-m", f"commit {i}")

        result = temp_repo.run(script_path)

        assert result.returncode == 0

        lines = result.stdout.strip().split("\n")
        assert len(lines) == 3

        # Verify ordering: Bob (3), Charlie (2), Alice (1).
        assert "Bob" in lines[0]
        assert "3" in lines[0]
        assert "Charlie" in lines[1]
        assert "2" in lines[1]
        assert "Alice" in lines[2]
        assert "1" in lines[2]
