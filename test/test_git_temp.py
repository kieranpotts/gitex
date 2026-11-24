"""
Test suite for git-temp command.

git-temp is scaffolded, but not implemented. `TestGitTempScaffold` covers
what the scaffold does today, and should be folded into the real suite once
the command works. `TestGitTemp` lists the planned test cases, taken from
docs/usage/git-temp.md, and is skipped until then.

Most planned tests need a fixture that does not exist yet: a project laid out
as a bare clone in `.bare`, with a `default` worktree beside it, and a bare
`origin` remote carrying the pipeline's trunks. Further variants are needed
for a `v1/*` pipeline, an unnamed pipeline, and a repository with no remote.
"""

import pytest


class TestGitTempScaffold:
    """Test cases for the git-temp scaffold."""

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        result = repo.run(bin, "--help")

        assert result.returncode == 0
        assert "Usage: git temp <slug>" in result.stdout

    def test_help_flag_short(self, repo, bin):
        """Test the -h flag shows help."""

        result = repo.run(bin, "-h")

        assert result.returncode == 0
        assert "Usage: git temp <slug>" in result.stdout

    def test_help_with_no_color(self, repo, bin):
        """Test --help wins when given with --no-color, in either order."""

        for args in (("--no-color", "--help"), ("--help", "--no-color")):
            result = repo.run(bin, *args)

            assert result.returncode == 0
            assert "Usage: git temp <slug>" in result.stdout

    def test_not_implemented(self, repo, bin):
        """Test that the scaffold refuses to run, until it is implemented."""

        result = repo.run(bin, "--no-color", "fix-auth-timeout")

        assert result.returncode == 1
        assert "error: git-temp is not implemented yet." in result.stderr
        assert result.stdout == ""


@pytest.mark.skip(reason="git-temp is not implemented yet.")
class TestGitTemp:
    """Planned test cases for git-temp command."""

    def test_creates_temp_branch_in_new_worktree(self):
        """Test the branch is cut from the tip of dev, in a sibling worktree."""

    def test_output_lines(self):
        """Test stdout gives the branch, the worktree path, the start point, and the push command."""

    def test_id_prefixes_slug_verbatim(self):
        """Test --id PRD-504 gives `latest/temp/PRD-504-<slug>`."""

    def test_v1_pipeline(self):
        """Test a branch cut from a `v1/*` worktree is `v1/temp/<slug>`, from `v1/dev`."""

    def test_unnamed_pipeline(self):
        """Test a branch cut from `dev` is `temp/<slug>`, with no prefix."""

    def test_pipeline_option(self):
        """Test --pipeline overrides the pipeline of the current branch."""

    def test_detached_head_uses_default_worktree(self):
        """Test a detached HEAD falls back to the pipeline of the `default` worktree."""

    def test_current_worktree_may_be_dirty(self):
        """Test uncommitted changes in the current worktree are left alone."""

    def test_trunk_fast_forwarded_in_its_worktree(self):
        """Test dev is fast-forwarded from origin in its own worktree."""

    def test_trunk_fast_forwarded_without_worktree(self):
        """Test dev is fast-forwarded with `fetch origin dev:dev` where no worktree has it."""

    def test_no_remote_warns_and_uses_local_refs(self):
        """Test a repository with no origin warns, and cuts from the local trunk."""

    def test_default_remote_name(self):
        """Test GITEX_DEFAULT_REMOTE_NAME selects the remote to fetch from."""

    def test_long_slug_warns(self):
        """Test a slug of 51 to 72 characters works, with a warning on stderr."""

    def test_refuses_too_long_slug(self):
        """Test a slug longer than 72 characters is refused."""

    def test_refuses_invalid_slug(self):
        """Test uppercase letters, other symbols, and a leading or trailing hyphen are refused."""

    def test_refuses_missing_slug(self):
        """Test a missing slug is a usage error."""

    def test_refuses_repeated_options(self):
        """Test --id or --pipeline given twice is a usage error."""

    def test_refuses_unknown_option(self):
        """Test an unknown option is a usage error, with a hint to try --help."""

    def test_refuses_outside_bare_layout(self):
        """Test an ordinary clone, with no `.bare` directory, is refused."""

    def test_refuses_non_pipeline_branch(self):
        """Test a current branch such as `main` is refused, without --pipeline."""

    def test_refuses_missing_trunk(self):
        """Test a pipeline with no dev trunk is refused."""

    def test_refuses_dirty_trunk_worktree(self):
        """Test a dev worktree with uncommitted changes is refused, and left alone."""

    def test_refuses_trunk_with_merge_in_progress(self):
        """Test a dev worktree with MERGE_HEAD or SQUASH_MSG is refused."""

    def test_refuses_diverged_trunk(self):
        """Test a local dev that has diverged from origin is refused."""

    def test_refuses_taken_name_locally(self):
        """Test an existing local branch of the same name is refused."""

    def test_refuses_taken_name_on_remote(self):
        """Test an existing branch of the same name on origin is refused."""

    def test_refuses_existing_worktree_path(self):
        """Test an existing file or directory at the worktree path is refused."""

    def test_nothing_pushed(self):
        """Test origin is unchanged after a successful run."""
