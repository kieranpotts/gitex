"""
Test suite for git-release command.

git-release is scaffolded, but not implemented. `TestGitReleaseScaffold`
covers what the scaffold does today, and should be folded into the real suite
once the command works. `TestGitRelease` lists the planned test cases, taken
from docs/usage/git-release.md, and is skipped until then.

Most planned tests need a fixture that does not exist yet: a project laid out
as a bare clone in `.bare`, with a `default` worktree beside it, and a bare
`origin` remote carrying `latest/dev`, `latest/test`, `latest/ready`, and
`latest/release`, with a `version: <version>` commit on `latest/test`.
"""

import pytest


class TestGitReleaseScaffold:
    """Test cases for the git-release scaffold."""

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        result = repo.run(bin, "--help")

        assert result.returncode == 0
        assert "Usage: git release <version>" in result.stdout

    def test_help_flag_short(self, repo, bin):
        """Test the -h flag shows help."""

        result = repo.run(bin, "-h")

        assert result.returncode == 0
        assert "Usage: git release <version>" in result.stdout

    def test_help_with_no_color(self, repo, bin):
        """Test --help wins when given with --no-color, in either order."""

        for args in (("--no-color", "--help"), ("--help", "--no-color")):
            result = repo.run(bin, *args)

            assert result.returncode == 0
            assert "Usage: git release <version>" in result.stdout

    def test_not_implemented(self, repo, bin):
        """Test that the scaffold refuses to run, until it is implemented."""

        result = repo.run(bin, "--no-color", "1.2.0")

        assert result.returncode == 1
        assert "error: git-release is not implemented yet." in result.stderr
        assert result.stdout == ""


@pytest.mark.skip(reason="git-release is not implemented yet.")
class TestGitRelease:
    """Planned test cases for git-release command."""

    def test_tags_and_moves_trunks(self):
        """Test the tag, ready, and release all point at the version commit."""

    def test_tag_is_annotated(self):
        """Test `git cat-file -t v<version>` prints `tag`, with the message `Release <version>`."""

    def test_tag_is_signed_when_configured(self):
        """Test tag.gpgSign or commit.gpgSign makes a signed tag."""

    def test_source_trunk_is_test(self):
        """Test the version commit is found on test, where the pipeline has one."""

    def test_source_trunk_falls_back_to_dev(self):
        """Test the version commit is found on dev, where the pipeline has no test trunk."""

    def test_leading_v_is_dropped(self):
        """Test `v1.2.0` means the same as `1.2.0`."""

    def test_ready_not_moved_past_version_commit(self):
        """Test commits after the version commit on the source trunk stay off ready."""

    def test_creates_missing_worktrees(self):
        """Test ready and release get worktrees where none has them checked out."""

    def test_first_release_creates_release_trunk(self):
        """Test a pipeline with no release trunk gets one at ready, in a new worktree."""

    def test_pre_release_tags_only(self):
        """Test a pre-release is tagged, and ready and release stay where they are."""

    def test_resumes_interrupted_release(self):
        """Test an existing tag on the version commit is kept, and the trunks are moved, with exit 0."""

    def test_complete_release_exits_2(self):
        """Test a release whose tag and trunks are all in place exits 2."""

    def test_pipeline_option(self):
        """Test --pipeline v2 releases from the v2 trunks."""

    def test_detached_head_uses_default_worktree(self):
        """Test a detached HEAD falls back to the pipeline of the `default` worktree."""

    def test_current_worktree_may_be_dirty(self):
        """Test uncommitted changes in the current worktree are left alone."""

    def test_trunks_fast_forwarded_from_remote(self):
        """Test the source trunk, ready, and release are fast-forwarded from origin first."""

    def test_no_remote_warns_and_uses_local_refs(self):
        """Test a repository with no origin warns, and releases from local refs."""

    def test_output_lines(self):
        """Test stdout gives the tag, the tagged commit, the trunks moved or created, and the push command."""

    def test_nothing_pushed(self):
        """Test origin is unchanged after a successful run."""

    def test_refuses_tag_on_other_commit(self):
        """Test an existing tag that points elsewhere is refused, and left alone."""

    def test_refuses_lightweight_tag(self):
        """Test an existing lightweight tag on the version commit is refused."""

    def test_refuses_ready_past_version_commit(self):
        """Test a ready trunk that has moved past the version commit is refused."""

    def test_refuses_release_past_version_commit(self):
        """Test a release trunk that has moved past the version commit is refused."""

    def test_refuses_missing_ready_trunk(self):
        """Test a pipeline with no ready trunk is refused."""

    def test_refuses_missing_version_commit(self):
        """Test a version with no `version: <version>` commit on the source trunk is refused."""

    def test_refuses_several_version_commits(self):
        """Test several commits with the same version subject are refused."""

    def test_ignores_version_in_commit_body(self):
        """Test a commit that mentions the version only in its body is not taken as the version commit."""

    def test_refuses_malformed_version(self):
        """Test versions such as `1.2`, `1.2.0.0`, `01.2.0`, and `1.2.0-rc` are refused."""

    def test_refuses_missing_version(self):
        """Test a missing version is a usage error."""

    def test_refuses_dirty_ready_worktree(self):
        """Test a ready worktree with uncommitted changes is refused."""

    def test_refuses_dirty_release_worktree(self):
        """Test a release worktree with MERGE_HEAD or SQUASH_MSG is refused."""

    def test_refuses_diverged_trunk(self):
        """Test a local trunk that has diverged from origin is refused."""

    def test_refuses_existing_release_worktree_path(self):
        """Test a first release is refused where the release worktree's path already exists."""

    def test_refusal_creates_nothing(self):
        """Test a refusal creates no tag and no worktree."""

    def test_refuses_outside_bare_layout(self):
        """Test an ordinary clone, with no `.bare` directory, is refused."""

    def test_refuses_unknown_option(self):
        """Test an unknown option is a usage error, with a hint to try --help."""

    def test_refuses_repeated_pipeline(self):
        """Test --pipeline given twice is a usage error."""
