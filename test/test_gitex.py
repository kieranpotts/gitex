"""
Test suite for gitex command.
"""


class TestGitex:
    """Test cases for gitex command."""

    def test_no_arguments_shows_help(self, temp_repo, script_path):
        """Test that running gitex with no arguments shows help."""

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex [options]" in result.stdout
        assert "Get help with using GitEx." in result.stdout
        assert "--version" in result.stdout
        assert "--commands" in result.stdout
        assert "--help" in result.stdout

    def test_help_flag_short(self, temp_repo, script_path):
        """Test the -h flag shows help."""

        result = temp_repo.run(script_path, "-h")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex [options]" in result.stdout
        assert "Get help with using GitEx." in result.stdout

    def test_help_flag_long(self, temp_repo, script_path):
        """Test the --help flag shows help."""

        result = temp_repo.run(script_path, "--help")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex [options]" in result.stdout
        assert "Get help with using GitEx." in result.stdout

    def test_version_flag_short(self, temp_repo, script_path):
        """Test the -v flag shows version."""

        result = temp_repo.run(script_path, "-v")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx v" in result.stdout

    def test_version_flag_long(self, temp_repo, script_path):
        """Test the --version flag shows version."""

        result = temp_repo.run(script_path, "--version")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx v" in result.stdout

    def test_commands_flag_short(self, temp_repo, script_path):
        """Test the -c flag lists commands."""

        result = temp_repo.run(script_path, "-c")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx commands:" in result.stdout
        assert "git amend" in result.stdout
        assert "git author" in result.stdout
        assert "git whoami" in result.stdout
        assert "git uncommit" in result.stdout
        assert "git unamend" in result.stdout

    def test_commands_flag_long(self, temp_repo, script_path):
        """Test the --commands flag lists commands."""

        result = temp_repo.run(script_path, "--commands")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx commands:" in result.stdout
        assert "git amend" in result.stdout
        assert "git author" in result.stdout
        assert "git whoami" in result.stdout
        assert "git uncommit" in result.stdout
        assert "git unamend" in result.stdout

    def test_version_output_format(self, temp_repo, script_path):
        """Test that version output has correct format."""

        result = temp_repo.run(script_path, "--version")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 1
        assert lines[0].startswith("GitEx v")

    def test_help_contains_examples(self, temp_repo, script_path):
        """Test that help output contains usage examples."""

        result = temp_repo.run(script_path, "--help")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Examples:" in result.stdout
        assert "$ git gitex --version" in result.stdout
        assert "$ git gitex --commands" in result.stdout

    def test_unknown_option(self, temp_repo, script_path):
        """Test that unknown options return an error."""

        result = temp_repo.run(script_path, "--unknown")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "unknown option: --unknown" in result.stderr
        assert "Try 'gitex --help' for more information." in result.stderr

    def test_too_many_arguments(self, temp_repo, script_path):
        """Test that multiple arguments return an error."""

        result = temp_repo.run(script_path, "--version", "--commands")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "too many arguments" in result.stderr
        assert "Try 'gitex --help' for more information." in result.stderr
