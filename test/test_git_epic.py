"""
Test suite for git-epic command.

git-epic is scaffolded, but not implemented. `TestGitEpicScaffold` covers
what the scaffold does today, and should be folded into the real suite once
the command works. `TestGitEpic` lists the planned test cases, taken from
docs/usage/git-epic.md, and is skipped until then.

git-epic shares its behavior with git-temp, apart from the branch name's type
component. The shared behavior is tested in full in test_git_temp.py, so this
file covers what differs, plus a smoke test of the shared path.
"""

import pytest


class TestGitEpicScaffold:
    """Test cases for the git-epic scaffold."""

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        result = repo.run(bin, "--help")

        assert result.returncode == 0
        assert "Usage: git epic <slug>" in result.stdout

    def test_help_flag_short(self, repo, bin):
        """Test the -h flag shows help."""

        result = repo.run(bin, "-h")

        assert result.returncode == 0
        assert "Usage: git epic <slug>" in result.stdout

    def test_help_with_no_color(self, repo, bin):
        """Test --help wins when given with --no-color, in either order."""

        for args in (("--no-color", "--help"), ("--help", "--no-color")):
            result = repo.run(bin, *args)

            assert result.returncode == 0
            assert "Usage: git epic <slug>" in result.stdout

    def test_not_implemented(self, repo, bin):
        """Test that the scaffold refuses to run, until it is implemented."""

        result = repo.run(bin, "--no-color", "billing-v2-rewrite")

        assert result.returncode == 1
        assert "error: git-epic is not implemented yet." in result.stderr
        assert result.stdout == ""


@pytest.mark.skip(reason="git-epic is not implemented yet.")
class TestGitEpic:
    """Planned test cases for git-epic command."""

    def test_creates_epic_branch_in_new_worktree(self):
        """Test `latest/epic/<slug>` is cut from the tip of `latest/dev`, in `<project>/latest-epic-<slug>`."""

    def test_output_lines(self):
        """Test stdout gives the branch, the worktree path, the start point, and the push command."""

    def test_id_and_pipeline(self):
        """Test --id PRD-187 --pipeline v1 gives `v1/epic/PRD-187-<slug>`."""

    def test_unnamed_pipeline(self):
        """Test a branch cut from `dev` is `epic/<slug>`, with no prefix."""

    def test_refuses_taken_name(self):
        """Test an existing epic branch of the same name is refused."""

    def test_refuses_invalid_slug(self):
        """Test an invalid slug is refused, with a message naming git-epic."""

    def test_refuses_unknown_option(self):
        """Test an unknown option is a usage error, with a hint to try 'git epic --help'."""
