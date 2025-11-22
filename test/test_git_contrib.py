"""
Test suite for git-contrib command.
"""


class TestGitContrib:
    """Test cases for git-contrib command."""

    def test_single_contributor(self, test_repo, script_path):
        """Test with a single contributor."""

        test_repo.git.config("--local", "user.name", "John Doe")
        test_repo.git.config("--local", "user.email", "john.doe@example.com")

        # Make first commit.
        test_repo.write("file1.txt", "content 1")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "first commit")

        # Make second commit.
        test_repo.write("file2.txt", "content 2")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("-m", "second commit")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "John Doe" in result.stdout
        assert "john.doe@example.com" in result.stdout
        assert "2" in result.stdout  # Commit count

    def test_multiple_contributors(self, test_repo, script_path):
        """Test with multiple contributors."""

        # Set first contributor.
        test_repo.git.config("--local", "user.name", "John Doe")
        test_repo.git.config("--local", "user.email", "john.doe@example.com")

        # First commit, made by first contributor.
        test_repo.write("file1.txt", "content 1")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "first commit")

        # Switch to second contributor.
        test_repo.git.config("--local", "user.name", "Jane Smith")
        test_repo.git.config("--local", "user.email", "jane.smith@example.com")

        # Second commit, made by second contributor.
        test_repo.write("file2.txt", "content 2")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("-m", "second commit")

        # Third commit, made by second contributor.
        test_repo.write("file3.txt", "content 3")
        test_repo.git.add("file3.txt")
        test_repo.git.commit("-m", "third commit")

        # Switch to third contributor.
        test_repo.git.config("--local", "user.name", "Bob Johnson")
        test_repo.git.config("--local", "user.email", "bob@example.com")

        # Fourth commit, made by third contributor.
        test_repo.write("file4.txt", "content 4")
        test_repo.git.add("file4.txt")
        test_repo.git.commit("-m", "fourth commit")

        # Fifth commit, made by third contributor.
        test_repo.write("file5.txt", "content 5")
        test_repo.git.add("file5.txt")
        test_repo.git.commit("-m", "fifth commit")

        # Switch back to second contributor.
        test_repo.git.config("--local", "user.name", "Jane Smith")
        test_repo.git.config("--local", "user.email", "jane.smith@example.com")

        # Sixth commit, made by second contributor.
        test_repo.write("file6.txt", "content 6")
        test_repo.git.add("file6.txt")
        test_repo.git.commit("-m", "sixth commit")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify all three contributors are listed.
        assert "John Doe" in result.stdout
        assert "john.doe@example.com" in result.stdout
        assert "Jane Smith" in result.stdout
        assert "jane.smith@example.com" in result.stdout
        assert "Bob Johnson" in result.stdout
        assert "bob@example.com" in result.stdout

        # Verify the output is ordered by commit count (descending):
        # Jane = 3, Bob = 2, John = 1
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 3
        assert "Jane Smith" in lines[0]
        assert "3" in lines[0]
        assert "Bob Johnson" in lines[1]
        assert "2" in lines[1]
        assert "John Doe" in lines[2]
        assert "1" in lines[2]

    def test_output_format(self, test_repo, script_path):
        """Test the output format matches git shortlog expectations."""

        # User config.
        test_repo.git.config("--local", "user.name", "John Doe")
        test_repo.git.config("--local", "user.email", "john.doe@example.com")

        # Create a commit.
        test_repo.write("test.txt", "content")
        test_repo.git.add("test.txt")
        test_repo.git.commit("-m", "test commit")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Output should be in format: "     N\tName <email>"
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 1
        assert "\t" in lines[0]  # Tab-separated
        assert "John Doe <john.doe@example.com>" in lines[0]
        assert "1" in lines[0]  # Commit count

    def test_with_no_commits(self, test_repo, script_path):
        """Test with a repository that has no commits."""

        result = test_repo.run(script_path)

        # 'git shortlog' returns success but empty output for repos with no commits.
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_rejects_single_argument(self, test_repo, script_path):
        """Test that the command rejects arguments."""

        result = test_repo.run(script_path, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr error message.
        assert "git-contrib does not accept any options" in result.stderr

    def test_rejects_multiple_arguments(self, test_repo, script_path):
        """Test that the command rejects multiple arguments."""

        result = test_repo.run(script_path, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr error message.
        assert "git-contrib does not accept any options" in result.stderr
