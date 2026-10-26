"""
Test suite for the color handling in lib/print.sh, and for the `--no-color`
option that every command built on it accepts.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

# ANSI escape sequences all start with this prefix.
ESC = "\033["

ROOT = Path(__file__).parent.parent.resolve()

# The plain output of the print-test script, by stream, when color is off.
PLAIN_STDOUT = "success: Something worked.\n\nAnswer this:\nFor your information.\n"
PLAIN_STDERR = (
    "error: Something failed.\nwarning: Something is off.\nTry this instead.\n> "
)

# Commands that parse their own options. These are tested in their own suites.
CUSTOM_PARSERS = {"git-author", "git-br", "git-orphan", "gitex"}


def commands_without_options():
    """
    List the commands that source lib/print.sh and accept no options other than
    `--no-color`. Pass-through commands like `git co`, which do not source
    lib/print.sh, are excluded.
    """

    return sorted(
        path.name
        for path in (ROOT / "bin").iterdir()
        if path.name not in CUSTOM_PARSERS and "lib/print.sh" in path.read_text()
    )


@pytest.fixture
def script(tmp_path):
    """
    Create a script that sources lib/print.sh and calls every print helper. The
    script lives in a bin/ directory beside a copy of lib/, matching the layout
    that print.sh expects.
    """

    shutil.copytree(ROOT / "lib", tmp_path / "lib")

    (tmp_path / "bin").mkdir()
    script = tmp_path / "bin" / "print-test"
    script.write_text(
        '. "$(dirname "$0")/../lib/print.sh"\n'
        'print_error "Something failed."\n'
        'print_warning "Something is off."\n'
        'print_hint "Try this instead."\n'
        'print_success "Something worked."\n'
        'print_prompt "Answer this:"\n'
        'print_info "For your information."\n'
    )

    return str(script)


def run(script, **env):
    """Run the script with stdout and stderr piped, not attached to a TTY."""

    return subprocess.run(
        ["bash", script],
        capture_output=True,
        text=True,
        env={**os.environ, **env},
    )


def run_with_tty(script, stream, **env):
    """
    Run the script with one stream attached to a pseudo-terminal, and the
    other stream piped.

    Args:
        script: Path to the script to run.
        stream: The stream to attach to the pseudo-terminal, "stdout" or "stderr".
        **env: Environment variables to add to the script's environment.

    Returns:
        A tuple of the stdout and stderr output.
    """

    leader, follower = os.openpty()
    streams = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
    streams[stream] = follower
    try:
        process = subprocess.Popen(
            ["bash", script],
            text=True,
            env={**os.environ, **env},
            **streams,
        )
        os.close(follower)
        stdout, stderr = process.communicate()
        tty_output = os.read(leader, 4096).decode()
    finally:
        os.close(leader)

    # The terminal translates "\n" to "\r\n" on output.
    tty_output = tty_output.replace("\r\n", "\n")
    if stream == "stdout":
        return tty_output, stderr
    return stdout, tty_output


class TestPrint:
    """Test cases for the color handling in lib/print.sh."""

    def test_no_color_when_not_a_tty(self, script):
        """Test that piped output has no color, from any helper."""

        result = run(script)

        # Verify the messages are printed exactly, without ANSI codes.
        assert result.stdout == PLAIN_STDOUT
        assert result.stderr == PLAIN_STDERR

    @pytest.mark.parametrize("stream", ["stdout", "stderr"])
    def test_color_checked_per_stream(self, script, stream):
        """Test that only the stream attached to a TTY is colored."""

        output = dict(zip(["stdout", "stderr"], run_with_tty(script, stream)))
        other = "stderr" if stream == "stdout" else "stdout"

        assert ESC in output[stream]
        assert ESC not in output[other]

    @pytest.mark.parametrize("stream", ["stdout", "stderr"])
    @pytest.mark.parametrize("value", ["1", ""])
    @pytest.mark.parametrize("name", ["NO_COLOR", "GITEX_NO_COLOR"])
    def test_no_color_variables_disable_color_on_tty(self, script, name, value, stream):
        """Test that NO_COLOR and GITEX_NO_COLOR, even if empty, disable color on a TTY."""

        stdout, stderr = run_with_tty(script, stream, **{name: value})

        assert stdout == PLAIN_STDOUT
        assert stderr == PLAIN_STDERR

    @pytest.mark.parametrize("value", ["1", ""])
    def test_force_color_enables_color_when_not_a_tty(self, script, value):
        """Test that FORCE_COLOR, even if empty, enables color on piped output."""

        result = run(script, FORCE_COLOR=value)

        assert ESC in result.stderr
        assert ESC in result.stdout

    def test_force_color_colors_each_helper(self, script):
        """Test which helpers color their messages."""

        result = run(script, FORCE_COLOR="1")
        lines = (result.stdout + result.stderr).splitlines()

        def line(text):
            return next(line for line in lines if text in line)

        # Verify every helper colors its message, except print_info.
        assert ESC in line("Something failed.")
        assert ESC in line("Something is off.")
        assert ESC in line("Try this instead.")
        assert ESC in line("Something worked.")
        assert ESC in line("Answer this:")
        assert ESC not in line("For your information.")

    @pytest.mark.parametrize("value", ["1", ""])
    @pytest.mark.parametrize("name", ["NO_COLOR", "GITEX_NO_COLOR"])
    def test_no_color_takes_precedence_over_force_color(self, script, name, value):
        """Test that NO_COLOR and GITEX_NO_COLOR, even if empty, beat FORCE_COLOR."""

        result = run(script, FORCE_COLOR="1", **{name: value})

        assert result.stdout == PLAIN_STDOUT
        assert result.stderr == PLAIN_STDERR


class TestNoColorOption:
    """Test cases for the `--no-color` option of commands that accept no other options."""

    def test_commands_are_found(self):
        """Test that the command list is not empty, so the tests below run."""

        assert len(commands_without_options()) >= 50

    @pytest.mark.parametrize("command", commands_without_options())
    def test_force_color_applies(self, repo, command):
        """Test that FORCE_COLOR colors the command's error output."""

        # The invalid argument stops the command before it does anything.
        env = {**os.environ, "FORCE_COLOR": "1"}
        result = repo.run(str(ROOT / "bin" / command), "bogus", env=env)

        assert result.returncode == 1
        assert ESC in result.stderr

    @pytest.mark.parametrize("args", [("--no-color", "bogus"), ("bogus", "--no-color")])
    @pytest.mark.parametrize("command", commands_without_options())
    def test_no_color_flag(self, repo, command, args):
        """Test that --no-color is accepted, and beats FORCE_COLOR, in any position."""

        # The invalid argument stops the command before it does anything.
        env = {**os.environ, "FORCE_COLOR": "1"}
        result = repo.run(str(ROOT / "bin" / command), *args, env=env)

        # Verify --no-color is not itself rejected, and color is disabled.
        assert result.returncode == 1
        assert result.stderr == (
            "error: Unexpected argument 'bogus'.\n"
            f"{command} accepts no arguments other than --no-color.\n"
        )

    @pytest.mark.parametrize("command", commands_without_options())
    def test_first_unexpected_argument_reported(self, repo, command):
        """Test that only the first unexpected argument is reported, even if empty."""

        result = repo.run(str(ROOT / "bin" / command), "", "bogus", "--no-color")

        assert result.returncode == 1
        assert result.stderr == (
            "error: Unexpected argument ''.\n"
            f"{command} accepts no arguments other than --no-color.\n"
        )

    @pytest.mark.parametrize("name", ["NO_COLOR", "GITEX_NO_COLOR"])
    @pytest.mark.parametrize("command", commands_without_options())
    def test_no_color_variables(self, repo, command, name):
        """Test that NO_COLOR and GITEX_NO_COLOR beat FORCE_COLOR."""

        env = {**os.environ, "FORCE_COLOR": "1", name: "1"}
        result = repo.run(str(ROOT / "bin" / command), "bogus", env=env)

        assert result.returncode == 1
        assert ESC not in result.stderr

    @pytest.mark.parametrize("command", commands_without_options())
    def test_usage_comment_lists_no_color(self, command):
        """Test that the script's header comment documents --no-color."""

        source = (ROOT / "bin" / command).read_text()
        usage = re.search(r"^# Usage:\n#\s+\$ (.*)$", source, re.M)

        assert usage, f"{command} has no usage comment"
        assert usage.group(1).endswith("[--no-color]")

    @pytest.mark.parametrize("command", commands_without_options())
    def test_usage_doc_lists_no_color(self, command):
        """Test that the command's usage doc documents --no-color."""

        doc = (ROOT / "docs" / "usage" / f"{command}.md").read_text()

        assert "[--no-color]" in doc
        assert "- `--no-color`: Disable colored output." in doc
