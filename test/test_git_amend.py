"""
Test suite for git-amend command.
"""


class TestGitAmend:
    """Test cases for git-amend command."""

    def test_amend_with_unstaged_changes(self, repo, bin):
        """Test amending with unstaged changes."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Make unstaged changes.
        repo.write("file1.txt", "Modified content")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify there's still only one commit.
        log_output = repo.git.log("--oneline")
        assert log_output.count("\n") == 0

        # Verify the new file content exists in the commit.
        show_output = repo.git.show("HEAD:file1.txt")
        assert "Modified content" in show_output

        # Verify the original commit message is unchanged.
        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "initial commit"

    def test_amend_with_untracked_files(self, repo, bin):
        """Test amending with new untracked files."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Create untracked file.
        repo.write("file2.txt", "New file")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the new file was added to the commit.
        ls_tree = repo.git.ls_tree("-r", "--name-only", "HEAD")
        assert "file1.txt" in ls_tree
        assert "file2.txt" in ls_tree

        # Verify still only one commit.
        log_output = repo.git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_amend_with_staged_changes(self, repo, bin):
        """Test amending with already staged changes."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Make and stage changes.
        repo.write("file1.txt", "Staged content")
        repo.git.add("file1.txt")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the changes were added to the last commit.
        show_output = repo.git.show("HEAD:file1.txt")
        assert "Staged content" in show_output

    def test_amend_with_staged_changes_only_when_mixed(self, repo, bin):
        """Test that only staged changes are amended when there are both staged and working changes."""

        # Create initial commit.
        repo.write("file1.txt", "Initial file 1 content")
        repo.write("file2.txt", "Initial file 2 content")
        repo.git.add(".")
        repo.git.commit("-m", "initial commit")

        # Staged change.
        repo.write("file1.txt", "Staged content")
        repo.git.add("file1.txt")

        # Unstaged change.
        repo.write("file2.txt", "Unstaged content")

        # Untracked file.
        repo.write("file3.txt", "Untracked file")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify only staged changes were included.
        assert "Staged content" in repo.git.show("HEAD:file1.txt")

        # Verify unstaged changes were NOT included.
        # For file 2, only the original committed content should be committed.
        assert "Initial file 2 content" in repo.git.show("HEAD:file2.txt")

        # Verify untracked file was NOT included.
        ls_tree = repo.git.ls_tree("-r", "--name-only", "HEAD")
        assert "file3.txt" not in ls_tree

        # Verify still only one commit.
        log_output = repo.git.log("--oneline")
        assert log_output.count("\n") == 0

        # Verify unstaged and untracked changes still exist in working tree.
        status = repo.git.status("--short")
        assert "M file2.txt" in status or " M file2.txt" in status
        assert "?? file3.txt" in status

    def test_amend_with_only_unstaged_and_untracked(self, repo, bin):
        """Test that all working changes are staged when there are no staged changes."""

        # Create initial commit.
        repo.write("file1.txt", "Initial file 1 content")
        repo.write("file2.txt", "Initial file 2 content")
        repo.git.add(".")
        repo.git.commit("-m", "initial commit")

        # Unstaged change (no staging).
        repo.write("file1.txt", "Unstaged content")

        # Untracked file (no staging).
        repo.write("file3.txt", "Untracked file")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify all working changes were included.
        assert "Unstaged content" in repo.git.show("HEAD:file1.txt")
        assert "Untracked file" in repo.git.show("HEAD:file3.txt")

        # Verify still only one commit.
        log_output = repo.git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_commit_message_preserved(self, repo, bin):
        """Test that the commit message is preserved when amending."""

        # Create initial commit with specific message.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "feature: my shiny new feature")

        # Make changes.
        repo.write("file1.txt", "Modified")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify commit message is unchanged.
        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "feature: my shiny new feature"

    def test_no_changes_to_amend(self, repo, bin):
        """Test that a message is printed when there are no changes to amend."""

        # Create initial commit.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify output message.
        assert "nothing to amend, working tree clean" in result.stdout

        # Verify the commit hasn't changed.
        log_output = repo.git.log("--oneline")
        commit_msg = repo.git.log("-1", "--format=%s")
        assert log_output.count("\n") == 0
        assert commit_msg == "initial commit"

    def test_error_no_commits_exist(self, repo, bin):
        """Test error when there are no commits to amend."""

        # Create a file but don't commit.
        repo.write("file1.txt", "Content")

        result = repo.run(bin)

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "no commits exist to amend" in result.stderr

    def test_rejects_single_argument(self, repo, bin):
        """Test that the command rejects arguments."""

        # Create initial commit.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        result = repo.run(bin, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-amend does not accept any options" in result.stderr

    def test_rejects_multiple_arguments(self, repo, bin):
        """Test that the command rejects multiple arguments."""

        # Create initial commit.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        result = repo.run(bin, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-amend does not accept any options" in result.stderr
