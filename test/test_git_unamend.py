"""
Test suite for git-unamend command.
"""

from pathlib import Path


class TestGitUnamend:
    """Test cases for git-unamend command."""

    def test_unamend_after_amend_with_new_file(self, test_repo, script_path):
        """Test unamending after adding a new file via amend."""

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Initial content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Amend with new file.
        Path(test_repo.cwd(), "file2.txt").write_text("New file")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("--amend", "--no-edit")

        # Get commit hash after amend.
        commit_after_amend = test_repo.git.rev_parse("HEAD")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify HEAD moved back.
        commit_after_unamend = test_repo.git.rev_parse("HEAD")
        assert commit_after_amend != commit_after_unamend

        # Verify file2.txt is still staged.
        status = test_repo.git.status("--short")
        assert "M  file2.txt" in status or "A  file2.txt" in status

        # Verify original commit only has file1.txt.
        ls_tree = test_repo.git.ls_tree("-r", "--name-only", "HEAD")
        assert "file1.txt" in ls_tree
        assert "file2.txt" not in ls_tree

    def test_unamend_after_amend_with_modified_file(self, test_repo, script_path):
        """Test unamending after modifying an existing file via amend."""

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Version 1")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Amend with modification.
        Path(test_repo.cwd(), "file1.txt").write_text("Version 2")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("--amend", "--no-edit")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file content in commit is Version 1.
        show_output = test_repo.git.show("HEAD:file1.txt")
        assert "Version 1" in show_output
        assert "Version 2" not in show_output

        # Verify Version 2 is staged.
        status = test_repo.git.status("--short")
        assert "M  file1.txt" in status

    def test_unamend_fails_after_regular_commit(self, test_repo, script_path):
        """Test that unamend fails when used after a regular commit."""

        # Create two commits.
        Path(test_repo.cwd(), "file1.txt").write_text("Content 1")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "first commit")

        Path(test_repo.cwd(), "file2.txt").write_text("Content 2")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("-m", "second commit")

        result = test_repo.run(script_path)

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "the last operation was not a 'git commit --amend'" in result.stderr
        assert "use 'git uncommit' to undo a regular commit" in result.stderr

        # Verify repository state is unchanged.
        commit_msg = test_repo.git.log("-1", "--format=%s")
        assert commit_msg == "second commit"

    def test_unamend_preserves_working_tree_changes(self, test_repo, script_path):
        """Test that unamend preserves unstaged working tree changes."""

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Version 1")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "initial commit")

        # Amend with new file.
        Path(test_repo.cwd(), "file2.txt").write_text("Staged file")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("--amend", "--no-edit")

        # Make unstaged change.
        Path(test_repo.cwd(), "file3.txt").write_text("Unstaged file")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file3.txt still exists and is unstaged.
        assert Path(test_repo.cwd(), "file3.txt").exists()
        status = test_repo.git.status("--short")
        assert "?? file3.txt" in status

    def test_unamend_with_message_change(self, test_repo, script_path):
        """Test unamending when the amend changed the commit message."""

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "original message")

        # Amend just the message.
        test_repo.git.commit("--amend", "-m", "amended message")

        result = test_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify message is back to original.
        commit_msg = test_repo.git.log("-1", "--format=%s")
        assert commit_msg == "original message"

    def test_unamend_fails_when_called_twice(self, test_repo, script_path):
        """Test that unamend fails when called a second time (after a reset, not an amend)."""

        # Create initial commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Content 1")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "commit 1")

        # Second commit.
        Path(test_repo.cwd(), "file2.txt").write_text("Content 2")
        test_repo.git.add("file2.txt")
        test_repo.git.commit("-m", "commit 2")

        # Amend it.
        Path(test_repo.cwd(), "file3.txt").write_text("Content 3")
        test_repo.git.add("file3.txt")
        test_repo.git.commit("--amend", "--no-edit")

        # Unamend once (should work).
        result = test_repo.run(script_path)
        assert result.returncode == 0

        commit_msg = test_repo.git.log("-1", "--format=%s")
        assert commit_msg == "commit 2"

        # Unamend again (should fail - last operation was reset, not amend).
        result = test_repo.run(script_path)
        assert result.returncode == 1
        assert "the last operation was not a 'git commit --amend'" in result.stderr

    def test_fails_with_no_commits(self, test_repo, script_path):
        """Test that unamend fails when there are no commits in the repository."""

        result = test_repo.run(script_path)

        # Verify error exit code.
        assert result.returncode != 0

        # Git will produce an error about the branch not having commits.
        assert "fatal:" in result.stderr

    def test_rejects_single_argument(self, test_repo, script_path):
        """Test that the command rejects arguments."""

        # Create a commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "commit")

        result = test_repo.run(script_path, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-unamend does not accept any options" in result.stderr

    def test_rejects_multiple_arguments(self, test_repo, script_path):
        """Test that the command rejects multiple arguments."""

        # Create a commit.
        Path(test_repo.cwd(), "file1.txt").write_text("Content")
        test_repo.git.add("file1.txt")
        test_repo.git.commit("-m", "commit")

        result = test_repo.run(script_path, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-unamend does not accept any options" in result.stderr
