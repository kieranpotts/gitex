"""
Test suite for git-integrate command.

git-integrate is scaffolded, but not implemented. `TestGitIntegrateScaffold`
covers what the scaffold does today, and should be folded into the real suite
once the command works. The other classes list the planned test cases, taken
from docs/usage/git-integrate.md, and are skipped until then.

Most planned tests need a fixture that does not exist yet: a project laid out
as a bare clone in `.bare`, with a `default` worktree beside it, and a bare
`origin` remote carrying `latest/dev`, `latest/test`, `latest/ready`, and
`latest/release`. Some tests need a variant with no `test` trunk.
"""

import pytest

NOT_IMPLEMENTED = pytest.mark.skip(reason="git-integrate is not implemented yet.")


class TestGitIntegrateScaffold:
    """Test cases for the git-integrate scaffold."""

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        result = repo.run(bin, "--help")

        assert result.returncode == 0
        assert "Usage: git integrate [<target>]" in result.stdout

    def test_help_flag_short(self, repo, bin):
        """Test the -h flag shows help."""

        result = repo.run(bin, "-h")

        assert result.returncode == 0
        assert "Usage: git integrate [<target>]" in result.stdout

    def test_help_with_no_color(self, repo, bin):
        """Test --help wins when given with --no-color, in either order."""

        for args in (("--no-color", "--help"), ("--help", "--no-color")):
            result = repo.run(bin, *args)

            assert result.returncode == 0
            assert "Usage: git integrate [<target>]" in result.stdout

    def test_not_implemented(self, repo, bin):
        """Test that the scaffold refuses to run, until it is implemented."""

        result = repo.run(bin, "--no-color")

        assert result.returncode == 1
        assert "error: git-integrate is not implemented yet." in result.stderr
        assert result.stdout == ""


@NOT_IMPLEMENTED
class TestGitIntegrateStrategies:
    """Planned test cases for each row of the strategy table."""

    def test_temp_into_dev_rebases_then_fast_forwards(self):
        """Test the temp branch is rebased onto dev, and dev fast-forwarded, with no merge commit."""

    def test_temp_into_dev_is_the_default_target(self):
        """Test a temp source with no target integrates into the pipeline's dev."""

    def test_epic_into_dev_merges_down_then_squashes(self):
        """Test the epic gets a `merge: sync with` commit, and dev gains exactly one commit."""

    def test_epic_into_dev_carries_the_epics_tree(self):
        """Test `git diff --quiet <epic> <dev>` succeeds after the squash."""

    def test_dev_into_epic_makes_merge_commit(self):
        """Test dev is merged into the epic, in the epic's worktree."""

    def test_dev_into_test_fast_forwards(self):
        """Test the dev-to-test promotion."""

    def test_test_into_ready_fast_forwards(self):
        """Test the test-to-ready promotion."""

    def test_dev_into_ready_without_test_trunk(self):
        """Test dev is promoted straight to ready where the pipeline has no test trunk."""

    def test_ready_into_release_fast_forwards(self):
        """Test the ready-to-release promotion."""

    def test_target_with_or_without_prefix(self):
        """Test `test` and `latest/test` name the same target."""

    def test_creates_missing_target_worktree(self):
        """Test a target with no worktree gets one, named after the branch."""

    def test_shared_branches_fast_forwarded_from_remote(self):
        """Test trunks and epics are fast-forwarded from origin first, and a temp branch is not."""

    def test_unnamed_pipeline(self):
        """Test `temp/<slug>` into `dev`, with no pipeline prefix."""

    def test_output_lines(self):
        """Test stdout gives `<target> <hash>`, the target worktree, the strategy token, and the push command."""

    def test_no_remote_warns_and_uses_local_refs(self):
        """Test a repository with no origin warns, and integrates from local refs."""

    def test_nothing_pushed_or_deleted(self):
        """Test origin is unchanged, and no branch or worktree is deleted."""


@NOT_IMPLEMENTED
class TestGitIntegrateSquashMessage:
    """Planned test cases for the epic's squash commit message."""

    def test_type_is_highest_impact(self):
        """Test the type ranking: behavior, fix, quality, maintenance, step, refactor, style, chore."""

    def test_unranked_types_are_ignored(self):
        """Test commits with other types, or no type, do not set the type."""

    def test_refuses_when_no_ranked_type(self):
        """Test an epic with no ranked commit type is refused."""

    def test_breaking_flag_propagates(self):
        """Test the subject carries `- BREAKING` if any commit does."""

    def test_incompat_flag_propagates(self):
        """Test the subject carries `- INCOMPAT` if any commit does, and none is BREAKING."""

    def test_intermediate_flags_dropped(self):
        """Test WIP, TEMPORARY, and EXPERIMENT do not reach the subject."""

    def test_body_lists_subjects_oldest_first(self):
        """Test the body lists the epic's non-merge commit subjects, oldest first."""

    def test_long_subject_warns(self):
        """Test a subject of 51 to 72 characters works, with a warning on stderr."""

    def test_refuses_too_long_subject(self):
        """Test a subject longer than 72 characters is refused before anything changes."""

    def test_hook_rejection_leaves_trunk_unchanged(self):
        """Test a commit-msg hook that rejects the message leaves dev unchanged, and the epic un-squashed."""


@NOT_IMPLEMENTED
class TestGitIntegrateRefusals:
    """Planned test cases for each refusal, conflict, and no-op."""

    def test_already_integrated_exits_2(self):
        """Test a source that is an ancestor of the target exits 2, and prints the target as it stands."""

    def test_squashed_epic_exits_2(self):
        """Test a second run after squashing an epic exits 2, rather than fail."""

    def test_conflict_on_rebase(self):
        """Test a rebase conflict lists the paths on stdout, aborts, and leaves both branches as they were."""

    def test_conflict_on_merge_down(self):
        """Test a merge-down conflict lists the paths, aborts, and leaves both branches as they were."""

    def test_conflict_on_squash(self):
        """Test a squash conflict lists the paths, resets, and leaves both branches as they were."""

    def test_refuses_pair_not_in_table(self):
        """Test eg. temp into test is refused."""

    def test_refuses_dev_into_ready_with_test_trunk(self):
        """Test dev into ready is refused where the pipeline has a test trunk."""

    def test_refuses_backport(self):
        """Test a target in another pipeline is refused."""

    def test_refuses_wip_commit_on_temp(self):
        """Test a temp branch carrying a `- WIP` commit is refused."""

    def test_refuses_temporary_commit_on_temp(self):
        """Test a temp branch carrying a `- TEMPORARY` commit is refused."""

    def test_refuses_non_fast_forward_promotion(self):
        """Test a trunk promotion that is not a fast-forward is refused."""

    def test_refuses_trunk_source_without_target(self):
        """Test a trunk source with no target is a usage error."""

    def test_refuses_epic_without_message(self):
        """Test an epic into dev without -m is refused."""

    def test_refuses_message_for_other_pairs(self):
        """Test -m is refused for any pair other than an epic into dev."""

    def test_refuses_detached_head(self):
        """Test a detached HEAD is refused."""

    def test_refuses_dirty_current_worktree(self):
        """Test uncommitted changes in the current worktree are refused."""

    def test_refuses_dirty_target_worktree(self):
        """Test uncommitted changes, MERGE_HEAD, or SQUASH_MSG in the target worktree are refused."""

    def test_refuses_diverged_shared_branch(self):
        """Test a trunk or epic that has diverged from origin is refused."""

    def test_refusal_creates_no_worktree(self):
        """Test a refusal never leaves a newly created target worktree behind."""

    def test_refuses_outside_bare_layout(self):
        """Test an ordinary clone, with no `.bare` directory, is refused."""

    def test_refuses_unknown_option(self):
        """Test an unknown option is a usage error, with a hint to try --help."""

    def test_refuses_repeated_message(self):
        """Test -m given twice is a usage error."""
