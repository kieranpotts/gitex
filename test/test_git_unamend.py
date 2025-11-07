"""
Test suite for git-unamend command.
"""

from pathlib import Path


class TestGitUnamend:
    """Test cases for git-unamend command."""

    def test_unamend_after_amend_with_new_file(self, temp_repo, script_path):
        """Test unamending after adding a new file via amend."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Amend with new file.
        Path(temp_repo.cwd(), "file2.txt").write_text("New file")
        git.add("file2.txt")
        git.commit("--amend", "--no-edit")

        # Get commit hash after amend.
        commit_after_amend = git.rev_parse("HEAD")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify HEAD moved back.
        commit_after_unamend = git.rev_parse("HEAD")
        assert commit_after_amend != commit_after_unamend

        # Verify file2.txt is still staged.
        status = git.status("--short")
        assert "M  file2.txt" in status or "A  file2.txt" in status

        # Verify original commit only has file1.txt.
        ls_tree = git.ls_tree("-r", "--name-only", "HEAD")
        assert "file1.txt" in ls_tree
        assert "file2.txt" not in ls_tree

    def test_unamend_after_amend_with_modified_file(self, temp_repo, script_path):
        """Test unamending after modifying an existing file via amend."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Version 1")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Amend with modification.
        Path(temp_repo.cwd(), "file1.txt").write_text("Version 2")
        git.add("file1.txt")
        git.commit("--amend", "--no-edit")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file content in commit is Version 1.
        show_output = git.show("HEAD:file1.txt")
        assert "Version 1" in show_output
        assert "Version 2" not in show_output

        # Verify Version 2 is staged.
        status = git.status("--short")
        assert "M  file1.txt" in status

    def test_unamend_fails_after_regular_commit(self, temp_repo, script_path):
        """Test that unamend fails when used after a regular commit."""

        git = temp_repo.git()

        # Create two commits.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        result = temp_repo.run(script_path)

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "error: the last operation was not a 'git commit --amend'" in result.stderr
        assert "hint: use 'git uncommit' to undo a regular commit" in result.stderr

        # Verify repository state is unchanged.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "second commit"

    def test_unamend_preserves_working_tree_changes(self, temp_repo, script_path):
        """Test that unamend preserves unstaged working tree changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Version 1")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Amend with new file.
        Path(temp_repo.cwd(), "file2.txt").write_text("Staged file")
        git.add("file2.txt")
        git.commit("--amend", "--no-edit")

        # Make unstaged change.
        Path(temp_repo.cwd(), "file3.txt").write_text("Unstaged file")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file3.txt still exists and is unstaged.
        assert Path(temp_repo.cwd(), "file3.txt").exists()
        status = git.status("--short")
        assert "?? file3.txt" in status

    def test_unamend_with_message_change(self, temp_repo, script_path):
        """Test unamending when the amend changed the commit message."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "original message")

        # Amend just the message.
        git.commit("--amend", "-m", "amended message")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify message is back to original.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "original message"

    def test_unamend_fails_when_called_twice(self, temp_repo, script_path):
        """Test that unamend fails when called a second time (after a reset, not an amend)."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "commit 1")

        # Second commit.
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "commit 2")

        # Amend it.
        Path(temp_repo.cwd(), "file3.txt").write_text("Content 3")
        git.add("file3.txt")
        git.commit("--amend", "--no-edit")

        # Unamend once (should work).
        result = temp_repo.run(script_path)
        assert result.returncode == 0

        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "commit 2"

        # Unamend again (should fail - last operation was reset, not amend).
        result = temp_repo.run(script_path)
        assert result.returncode == 1
        assert "error: the last operation was not a 'git commit --amend'" in result.stderr

    def test_rejects_single_argument(self, temp_repo, script_path):
        """Test that the command rejects arguments."""

        git = temp_repo.git()

        # Create a commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "commit")

        result = temp_repo.run(script_path, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "error: git-unamend does not accept any arguments" in result.stderr

    def test_rejects_multiple_arguments(self, temp_repo, script_path):
        """Test that the command rejects multiple arguments."""

        git = temp_repo.git()

        # Create a commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "commit")

        result = temp_repo.run(script_path, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "error: git-unamend does not accept any arguments" in result.stderr
