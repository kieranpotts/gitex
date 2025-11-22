"""
Test suite for git-whoami command.
"""


class TestGitWhoami:
    """Test cases for git-whoami command."""

    def test_with_name_and_email_set(self, repo, bin):
        """Test when both user.name and user.email are configured."""

        # Git config: user name and email provided.
        repo.git.config("--local", "user.name", "John Doe")
        repo.git.config("--local", "user.email", "john.doe@example.com")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "name:  John Doe" in result.stdout
        assert "email: john.doe@example.com" in result.stdout

    def test_with_neither_name_nor_email_set(self, repo, bin):
        """Test when neither user.name nor user.email are configured."""

        # Git config: user name and email both empty.
        repo.git.config("--local", "user.name", "")
        repo.git.config("--local", "user.email", "")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "name:  [not set]" in result.stdout
        assert "email: [not set]" in result.stdout

    def test_with_only_name_set(self, repo, bin):
        """Test when only user.name is configured."""

        # Git config: user name provided, email empty.
        repo.git.config("--local", "user.name", "Jane Doe")
        repo.git.config("--local", "user.email", "")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "name:  Jane Doe" in result.stdout
        assert "email: [not set]" in result.stdout

    def test_with_only_email_set(self, repo, bin):
        """Test when only user.email is configured."""

        # Git config: email provided, name empty.
        repo.git.config("--local", "user.name", "")
        repo.git.config("--local", "user.email", "jane.doe@example.com")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "name:  [not set]" in result.stdout
        assert "email: jane.doe@example.com" in result.stdout

    def test_output_line_count(self, repo, bin):
        """Test that the output does not exceed the expected number of lines."""

        # Git config: user name and email provided.
        repo.git.config("--local", "user.name", "John Doe")
        repo.git.config("--local", "user.email", "john.doe@example.com")

        result = repo.run(bin)

        # Verify stdout structure.
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 2
        assert lines[0].startswith("name:  ")
        assert lines[1].startswith("email: ")

    def test_with_special_characters_in_name(self, repo, bin):
        """Test with special characters in username."""

        # Git config: user name includes special characters.
        repo.git.config("--local", "user.name", "José García-Pérez")
        repo.git.config("--local", "user.email", "jose@example.com")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout – special characters printed verbatim.
        assert "name:  José García-Pérez" in result.stdout
        assert "email: jose@example.com" in result.stdout

    def test_rejects_single_argument(self, repo, bin):
        """Test that the command rejects arguments."""

        result = repo.run(bin, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "git-whoami does not accept any options" in result.stderr

    def test_rejects_multiple_arguments(self, repo, bin):
        """Test that the command rejects multiple arguments."""

        result = repo.run(bin, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "git-whoami does not accept any options" in result.stderr
