"""
Test suite for the `gitex` command.
"""

import os


class TestGitEx:
    """Test cases for the `gitex` command."""

    def test_no_arguments_shows_help(self, repo, bin):
        """Test that running `gitex` with no arguments shows help."""

        # Execute the script-under-test witthout options.
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

        # Execute the script-under-test with the '-h' option.
        result = repo.run(bin, "-h")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex" in result.stdout
        assert "Get help with using GitEx." in result.stdout

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        # Execute the script-under-test with the '--help' option.
        result = repo.run(bin, "--help")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Usage: gitex" in result.stdout
        assert "Get help with using GitEx." in result.stdout

    def test_version_flag_short(self, repo, bin):
        """Test the -v flag shows version."""

        # Execute the script-under-test with the '-v' option.
        result = repo.run(bin, "-v")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx v" in result.stdout

    def test_version_flag_long(self, repo, bin):
        """Test the --version flag shows version."""

        # Execute the script-under-test with the '--version' option.
        result = repo.run(bin, "--version")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "GitEx v" in result.stdout

    def test_commands_flag_short(self, repo, bin):
        """Test the -c flag lists commands."""

        # Execute the script-under-test with the '-c' option.
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

        # Execute the script-under-test with the '--commands' option.
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

        # Execute the script-under-test with the '--version' option.
        result = repo.run(bin, "--version")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 1
        assert lines[0].startswith("GitEx v")

    def test_help_contains_examples(self, repo, bin):
        """Test that help output contains usage examples."""

        # Execute the script-under-test with the '--help' option.
        result = repo.run(bin, "--help")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify stdout.
        assert "Examples:" in result.stdout
        assert "$ git gitex --version" in result.stdout
        assert "$ git gitex --commands" in result.stdout

    def test_unknown_option(self, repo, bin):
        """Test that unknown options return an error."""

        # Execute the script-under-test with the '--unknown' option.
        result = repo.run(bin, "--unknown")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "Unknown option '--unknown'." in result.stderr
        assert "Try 'gitex --help' for more information." in result.stderr

    def test_too_many_arguments(self, repo, bin):
        """Test that multiple arguments return an error."""

        # Execute the script-under-test with the '--commands' option.
        result = repo.run(bin, "--version", "--commands")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify stderr.
        assert "Too many options." in result.stderr
        assert "Try 'gitex --help' for more information." in result.stderr

    def test_no_color_flag(self, repo, bin):
        """Test that --no-color disables color, even when FORCE_COLOR is set."""

        env = {**os.environ, "FORCE_COLOR": "1"}
        result = repo.run(bin, "--no-color", "--unknown", env=env)

        # Verify the error message is printed without ANSI codes.
        assert result.returncode == 1
        assert "error: Unknown option '--unknown'." in result.stderr
        assert "\033[" not in result.stderr

    def test_no_color_flag_with_action(self, repo, bin):
        """Test that --no-color can be combined with an action."""

        result = repo.run(bin, "--version", "--no-color")

        # Verify the action runs.
        assert result.returncode == 0
        assert result.stdout.startswith("GitEx v")

    def test_no_color_flag_with_commands(self, repo, bin):
        """Test that --no-color can be combined with --commands, in either order."""

        for args in (["--commands", "--no-color"], ["--no-color", "-c"]):
            result = repo.run(bin, *args)

            # Verify the commands are listed.
            assert result.returncode == 0
            assert "GitEx commands:" in result.stdout
            assert "git amend [--no-color]" in result.stdout

    def test_commands_list_no_color(self, repo, bin):
        """Test that every command in the --commands list shows --no-color."""

        result = repo.run(bin, "--commands")
        usages = [
            line for line in result.stdout.splitlines() if line.startswith("  git ")
        ]

        assert usages
        for usage in usages:
            assert usage.endswith(" [--no-color]"), usage

    def test_no_color_flag_alone_shows_help(self, repo, bin):
        """Test that --no-color without an action shows help."""

        result = repo.run(bin, "--no-color")

        assert result.returncode == 0
        assert "Usage: gitex" in result.stdout

    def test_no_color_flag_with_too_many_options(self, repo, bin):
        """Test that --no-color does not count towards the single action allowed."""

        result = repo.run(bin, "--no-color", "--version", "--commands")

        assert result.returncode == 1
        assert "Too many options." in result.stderr

    def test_help_lists_no_color(self, repo, bin):
        """Test that --help documents --no-color."""

        result = repo.run(bin, "--help")

        assert "[--no-color]" in result.stdout
        assert "--no-color      Disable colored output." in result.stdout

    def test_color_environment_variables(self, repo, bin):
        """Test that FORCE_COLOR enables color, and NO_COLOR beats it."""

        forced = repo.run(bin, "--unknown", env={**os.environ, "FORCE_COLOR": "1"})
        disabled = repo.run(
            bin, "--unknown", env={**os.environ, "FORCE_COLOR": "1", "NO_COLOR": "1"}
        )

        assert "\033[" in forced.stderr
        assert "\033[" not in disabled.stderr
        assert "error: Unknown option '--unknown'." in disabled.stderr
