"""
Test suite for git-bump command.

git-bump is scaffolded, but not implemented. `TestGitBumpScaffold` covers
what the scaffold does today, and should be folded into the real suite once
the command works. The other classes list the planned test cases, taken from
docs/usage/git-bump.md, and are skipped until then.

Most planned tests need a fixture that does not exist yet: a project laid out
as a bare clone in `.bare`, with a `default` worktree beside it, and a bare
`origin` remote carrying the pipeline's trunks and release tags.
"""

import pytest

NOT_IMPLEMENTED = pytest.mark.skip(reason="git-bump is not implemented yet.")


class TestGitBumpScaffold:
    """Test cases for the git-bump scaffold."""

    def test_help_flag_long(self, repo, bin):
        """Test the --help flag shows help."""

        result = repo.run(bin, "--help")

        assert result.returncode == 0
        assert "Usage: git bump" in result.stdout

    def test_help_flag_short(self, repo, bin):
        """Test the -h flag shows help."""

        result = repo.run(bin, "-h")

        assert result.returncode == 0
        assert "Usage: git bump" in result.stdout

    def test_help_with_no_color(self, repo, bin):
        """Test --help wins when given with --no-color, in either order."""

        for args in (("--no-color", "--help"), ("--help", "--no-color")):
            result = repo.run(bin, *args)

            assert result.returncode == 0
            assert "Usage: git bump" in result.stdout

    def test_not_implemented(self, repo, bin):
        """Test that the scaffold refuses to run, until it is implemented."""

        result = repo.run(bin, "--no-color")

        assert result.returncode == 1
        assert "error: git-bump is not implemented yet." in result.stderr
        assert result.stdout == ""


@NOT_IMPLEMENTED
class TestGitBumpClassification:
    """Planned test cases for classifying commits."""

    def test_breaking_is_major(self):
        """Test a commit of any type flagged BREAKING calls for a major bump."""

    def test_behavior_fix_quality_are_minor(self):
        """Test behavior, fix, and quality commits call for a minor bump."""

    def test_maintenance_refactor_style_chore_are_patch(self):
        """Test maintenance, refactor, style, and chore commits call for a patch bump."""

    def test_create_update_delete_are_patch(self):
        """Test create, update, and delete commits call for a patch bump."""

    def test_step_version_revert_are_none(self):
        """Test step, version, and revert commits call for no bump."""

    def test_incompat_classified_by_type(self):
        """Test `refactor: ... - INCOMPAT` calls for a patch bump, not a major one."""

    def test_revert_pair_dropped(self):
        """Test a commit and its revert, matched by the `Reverts:` footer, are both left out."""

    def test_untyped_commit_is_minor_with_warning(self):
        """Test a commit with no recognized type counts as minor, and is named on stderr."""

    def test_zero_major_absorbs_breaking(self):
        """Test a BREAKING commit after v0.3.1 gives 0.4.0, with a warning."""

    def test_highest_bump_wins(self):
        """Test a mix of patch, minor, and major commits gives a major bump."""

    def test_merge_commits_ignored(self):
        """Test merge commits are left out of the range."""

    def test_changelog_only_commits_ignored(self):
        """Test a commit touching only the changelog does not call for a bump."""

    def test_nothing_to_release_exits_2(self):
        """Test a range with no bump-worthy commit prints the current version, and exits 2."""


@NOT_IMPLEMENTED
class TestGitBumpVersions:
    """Planned test cases for baselines, series, pre-releases, and first releases."""

    def test_baseline_ignores_pre_release_tags(self):
        """Test v1.5.0-rc.0 is never taken as the baseline."""

    def test_series_narrows_baseline(self):
        """Test the `v1` pipeline takes its baseline from `v1.*` tags only."""

    def test_refuses_major_bump_in_major_series(self):
        """Test a BREAKING commit in the `v1` pipeline is refused, naming the commit."""

    def test_refuses_minor_bump_in_minor_series(self):
        """Test a minor bump in the `v2.4-LTS` pipeline is refused."""

    def test_pre_release_counter(self):
        """Test --pre rc gives rc.0, then rc.2 where v1.5.0-rc.1 exists."""

    def test_refuses_invalid_pre_stage(self):
        """Test a --pre stage with anything but lowercase letters is refused."""

    def test_first_release_is_1_0_0(self):
        """Test a pipeline with no release tags gets 1.0.0."""

    def test_initial_version_variable(self):
        """Test GITEX_INITIAL_VERSION=0.1.0 sets the first release's version."""

    def test_refuses_released_changelog_without_tag(self):
        """Test a changelog with a released section, but no release tag, is refused."""

    def test_refuses_existing_tag(self):
        """Test a tag that already exists for the next version is refused."""

    def test_refuses_non_semver_tags(self):
        """Test a project with calendar-versioned tags is refused."""


@NOT_IMPLEMENTED
class TestGitBumpFiles:
    """Planned test cases for the changelog, the manifests, and the commit."""

    def test_changelog_heading_promoted(self):
        """Test `## [Unreleased]` becomes `## [1.5.0] - <today>`, under a new empty `## [Unreleased]`."""

    def test_changelog_entries_unchanged(self):
        """Test every line other than the headings is byte-for-byte unchanged, including link references."""

    def test_changelog_crlf_preserved(self):
        """Test a changelog with CRLF line endings keeps them on the new lines."""

    def test_changelog_variable(self):
        """Test GITEX_CHANGELOG points at a changelog other than CHANGELOG.md."""

    def test_refuses_missing_unreleased_section(self):
        """Test a changelog with no `## [Unreleased]` heading is refused."""

    def test_refuses_empty_unreleased_section(self):
        """Test an unreleased section holding only blank lines is refused."""

    def test_package_json_version(self):
        """Test the version field in package.json is set, and nothing else changes."""

    def test_pyproject_project_version(self):
        """Test the version in the [project] table of pyproject.toml is set."""

    def test_pyproject_poetry_version(self):
        """Test the version in the [tool.poetry] table of pyproject.toml is set."""

    def test_cargo_package_version(self):
        """Test the version in the [package] table of Cargo.toml is set, and dependency versions are not."""

    def test_refuses_manifest_with_no_match(self):
        """Test a manifest whose version field matches no line is refused, and no file is written."""

    def test_refuses_manifest_with_several_matches(self):
        """Test a manifest whose version field matches several lines is refused, and no file is written."""

    def test_lockfiles_untouched(self):
        """Test package-lock.json, poetry.lock, and Cargo.lock are never edited."""

    def test_commit_touches_only_changelog_and_manifests(self):
        """Test the version commit's subject, and that it changes no other file."""

    def test_no_changelog_and_no_manifest(self):
        """Test the version is printed, and no commit is made."""

    def test_pre_release_leaves_changelog(self):
        """Test --pre sets the manifests, and leaves the changelog unchanged."""

    def test_refuses_pre_release_without_manifest(self):
        """Test --pre in a project with no manifest is refused."""

    def test_dry_run_changes_nothing(self):
        """Test --dry-run prints the version and deciding commits, and changes no file, commit, or tag."""

    def test_dry_run_still_refuses(self):
        """Test --dry-run runs every check, eg. an empty unreleased section."""

    def test_hook_rejection_leaves_edits_uncommitted(self):
        """Test a commit-msg hook that rejects the commit leaves the edits in the worktree, and exits 1."""

    def test_output_lines(self):
        """Test stdout gives the version, the baseline, the bump level, the deciding commits, and the commit."""

    def test_no_tag_created(self):
        """Test no tag is created, and nothing is pushed."""


@NOT_IMPLEMENTED
class TestGitBumpRefusals:
    """Planned test cases for preconditions and usage errors."""

    def test_refuses_detached_head(self):
        """Test a detached HEAD is refused."""

    def test_refuses_release_trunks(self):
        """Test the test, ready, and release trunks are refused."""

    def test_refuses_dirty_worktree(self):
        """Test uncommitted changes are refused."""

    def test_refuses_operation_in_progress(self):
        """Test a merge, rebase, cherry-pick, revert, or squash in progress is refused."""

    def test_refuses_outside_bare_layout(self):
        """Test an ordinary clone, with no `.bare` directory, is refused."""

    def test_no_remote_warns_and_uses_local_tags(self):
        """Test a repository with no origin warns, and works from local tags."""

    def test_refuses_unknown_option(self):
        """Test an unknown option is a usage error, with a hint to try --help."""

    def test_refuses_repeated_pre(self):
        """Test --pre given twice is a usage error."""
