"""
Test suite for git-amend command.
"""

from pathlib import Path


class TestGitAmend:
    """Test cases for git-amend command."""

    def test_amend_with_unstaged_changes(self, temp_repo, script_path):
        """Test amending with unstaged changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Make unstaged changes.
        Path(temp_repo.cwd(), "file1.txt").write_text("Modified content")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify there's still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

        # Verify the new file content exists in the commit.
        show_output = git.show("HEAD:file1.txt")
        assert "Modified content" in show_output

        # Verify the original commit message is unchanged.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "initial commit"

    def test_amend_with_untracked_files(self, temp_repo, script_path):
        """Test amending with new untracked files."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create untracked file.
        Path(temp_repo.cwd(), "file2.txt").write_text("New file")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the new file was added to the commit.
        ls_tree = git.ls_tree("-r", "--name-only", "HEAD")
        assert "file1.txt" in ls_tree
        assert "file2.txt" in ls_tree

        # Verify still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_amend_with_staged_changes(self, temp_repo, script_path):
        """Test amending with already staged changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        # Make and stage changes.
        Path(temp_repo.cwd(), "file1.txt").write_text("Staged content")
        git.add("file1.txt")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the changes were added to the last commit.
        show_output = git.show("HEAD:file1.txt")
        assert "Staged content" in show_output

    def test_amend_with_staged_changes_only_when_mixed(self, temp_repo, script_path):
        """Test that only staged changes are amended when there are both staged and working changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial file 1 content")
        Path(temp_repo.cwd(), "file2.txt").write_text("Initial file 2 content")
        git.add(".")
        git.commit("-m", "initial commit")

        # Staged change.
        Path(temp_repo.cwd(), "file1.txt").write_text("Staged content")
        git.add("file1.txt")

        # Unstaged change.
        Path(temp_repo.cwd(), "file2.txt").write_text("Unstaged content")

        # Untracked file.
        Path(temp_repo.cwd(), "file3.txt").write_text("Untracked file")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify only staged changes were included.
        assert "Staged content" in git.show("HEAD:file1.txt")

        # Verify unstaged changes were NOT included.
        # For file 2, only the original committed content should be committed.
        assert "Initial file 2 content" in git.show("HEAD:file2.txt")

        # Verify untracked file was NOT included.
        ls_tree = git.ls_tree("-r", "--name-only", "HEAD")
        assert "file3.txt" not in ls_tree

        # Verify still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

        # Verify unstaged and untracked changes still exist in working tree.
        status = git.status("--short")
        assert "M file2.txt" in status or " M file2.txt" in status
        assert "?? file3.txt" in status

    def test_amend_with_only_unstaged_and_untracked(self, temp_repo, script_path):
        """Test that all working changes are staged when there are no staged changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Initial file 1 content")
        Path(temp_repo.cwd(), "file2.txt").write_text("Initial file 2 content")
        git.add(".")
        git.commit("-m", "initial commit")

        # Unstaged change (no staging).
        Path(temp_repo.cwd(), "file1.txt").write_text("Unstaged content")

        # Untracked file (no staging).
        Path(temp_repo.cwd(), "file3.txt").write_text("Untracked file")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify all working changes were included.
        assert "Unstaged content" in git.show("HEAD:file1.txt")
        assert "Untracked file" in git.show("HEAD:file3.txt")

        # Verify still only one commit.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_commit_message_preserved(self, temp_repo, script_path):
        """Test that the commit message is preserved when amending."""

        git = temp_repo.git()

        # Create initial commit with specific message.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "my custom commit message")

        # Make changes.
        Path(temp_repo.cwd(), "file1.txt").write_text("Modified")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify commit message is unchanged.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "my custom commit message"

    def test_no_changes_to_amend(self, temp_repo, script_path):
        """Test that a message is printed when there are no changes to amend."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify output message.
        assert "nothing to amend, working tree clean" in result.stdout

        # Verify the commit hasn't changed.
        log_output = git.log("--oneline")
        commit_msg = git.log("-1", "--format=%s")
        assert log_output.count("\n") == 0
        assert commit_msg == "initial commit"

    def test_error_no_commits_exist(self, temp_repo, script_path):
        """Test error when there are no commits to amend."""

        # Create a file but don't commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")

        result = temp_repo.run(script_path)

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "error: no commits exist to amend" in result.stderr

    def test_rejects_single_argument(self, temp_repo, script_path):
        """Test that the command rejects arguments."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        result = temp_repo.run(script_path, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "error: git-amend does not accept any arguments" in result.stderr

    def test_rejects_multiple_arguments(self, temp_repo, script_path):
        """Test that the command rejects multiple arguments."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content")
        git.add("file1.txt")
        git.commit("-m", "initial commit")

        result = temp_repo.run(script_path, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "error: git-amend does not accept any arguments" in result.stderr
