"""
Test suite for gitex command.
"""


class TestGitex:
    """Test cases for gitex command."""

    def test_no_arguments_shows_help(self, repo, bin):
        """Test that running gitex with no arguments shows help."""

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex" in result.stdout
        assert "Get help with using GitEx." in result.stdout
        assert "--version" in result.stdout
        assert "--commands" in result.stdout
        assert "--help" in result.stdout

    def test_help_flag_short(self, repo, bin):
        """Test the -h flag shows help."""

        result = repo.run(bin, "-h")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex" in result.stdout
        assert "Get help with using GitEx." in result.stdout

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        result = repo.run(bin, "--help")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex" in result.stdout
        assert "Get help with using GitEx." in result.stdout

    def test_version_flag_short(self, repo, bin):
        """Test the -v flag shows version."""

        result = repo.run(bin, "-v")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx v" in result.stdout

    def test_version_flag_long(self, repo, bin):
        """Test the --version flag shows version."""

        result = repo.run(bin, "--version")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx v" in result.stdout

    def test_commands_flag_short(self, repo, bin):
        """Test the -c flag lists commands."""

        result = repo.run(bin, "-c")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx commands:" in result.stdout
        assert "git amend" in result.stdout
        assert "git author" in result.stdout
        assert "git whoami" in result.stdout
        assert "git uncommit" in result.stdout
        assert "git unamend" in result.stdout

    def test_commands_flag_long(self, repo, bin):
        """Test the --commands flag lists commands."""

        result = repo.run(bin, "--commands")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx commands:" in result.stdout
        assert "git amend" in result.stdout
        assert "git author" in result.stdout
        assert "git whoami" in result.stdout
        assert "git uncommit" in result.stdout
        assert "git unamend" in result.stdout

    def test_version_output_format(self, repo, bin):
        """Test that version output has correct format."""

        result = repo.run(bin, "--version")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 1
        assert lines[0].startswith("GitEx v")

    def test_help_contains_examples(self, repo, bin):
        """Test that help output contains usage examples."""

        result = repo.run(bin, "--help")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Examples:" in result.stdout
        assert "$ git gitex --version" in result.stdout
        assert "$ git gitex --commands" in result.stdout

    def test_unknown_option(self, repo, bin):
        """Test that unknown options return an error."""

        result = repo.run(bin, "--unknown")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "unknown option: --unknown" in result.stderr
        assert "Try 'gitex --help' for more information." in result.stderr

    def test_too_many_arguments(self, repo, bin):
        """Test that multiple arguments return an error."""

        result = repo.run(bin, "--version", "--commands")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "too many options" in result.stderr
        assert "Try 'gitex --help' for more information." in result.stderr
