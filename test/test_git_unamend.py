"""
Test suite for git-unamend command.
"""


class TestGitUnamend:
    """Test cases for git-unamend command."""

    def test_unamend_after_amend_with_new_file(self, repo, bin):
        """Test unamending after adding a new file via amend."""

        # Create initial commit.
        repo.write("file1.txt", "Initial content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Amend with new file.
        repo.write("file2.txt", "New file")
        repo.git.add("file2.txt")
        repo.git.commit("--amend", "--no-edit")

        # Get commit hash after amend.
        commit_after_amend = repo.git.rev_parse("HEAD")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify HEAD moved back.
        commit_after_unamend = repo.git.rev_parse("HEAD")
        assert commit_after_amend != commit_after_unamend

        # Verify file2.txt is still staged.
        status = repo.git.status("--short")
        assert "M  file2.txt" in status or "A  file2.txt" in status

        # Verify original commit only has file1.txt.
        ls_tree = repo.git.ls_tree("-r", "--name-only", "HEAD")
        assert "file1.txt" in ls_tree
        assert "file2.txt" not in ls_tree

    def test_unamend_after_amend_with_modified_file(self, repo, bin):
        """Test unamending after modifying an existing file via amend."""

        # Create initial commit.
        repo.write("file1.txt", "Version 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Amend with modification.
        repo.write("file1.txt", "Version 2")
        repo.git.add("file1.txt")
        repo.git.commit("--amend", "--no-edit")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file content in commit is Version 1.
        show_output = repo.git.show("HEAD:file1.txt")
        assert "Version 1" in show_output
        assert "Version 2" not in show_output

        # Verify Version 2 is staged.
        status = repo.git.status("--short")
        assert "M  file1.txt" in status

    def test_unamend_fails_after_regular_commit(self, repo, bin):
        """Test that unamend fails when used after a regular commit."""

        # Create two commits.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "second commit")

        result = repo.run(bin)

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "the last operation was not a 'git commit --amend'" in result.stderr
        assert "use 'git uncommit' to undo a regular commit" in result.stderr

        # Verify repository state is unchanged.
        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "second commit"

    def test_unamend_preserves_working_tree_changes(self, repo, bin):
        """Test that unamend preserves unstaged working tree changes."""

        # Create initial commit.
        repo.write("file1.txt", "Version 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "initial commit")

        # Amend with new file.
        repo.write("file2.txt", "Staged file")
        repo.git.add("file2.txt")
        repo.git.commit("--amend", "--no-edit")

        # Make unstaged change.
        repo.write("file3.txt", "Unstaged file")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file3.txt still exists and is unstaged.
        assert repo.exists("file3.txt")
        status = repo.git.status("--short")
        assert "?? file3.txt" in status

    def test_unamend_with_message_change(self, repo, bin):
        """Test unamending when the amend changed the commit message."""

        # Create initial commit.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "original message")

        # Amend just the message.
        repo.git.commit("--amend", "-m", "amended message")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify message is back to original.
        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "original message"

    def test_unamend_fails_when_called_twice(self, repo, bin):
        """Test that unamend fails when called a second time (after a reset, not an amend)."""

        # Create initial commit.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "commit 1")

        # Second commit.
        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "commit 2")

        # Amend it.
        repo.write("file3.txt", "Content 3")
        repo.git.add("file3.txt")
        repo.git.commit("--amend", "--no-edit")

        # Unamend once (should work).
        result = repo.run(bin)
        assert result.returncode == 0

        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "commit 2"

        # Unamend again (should fail - last operation was reset, not amend).
        result = repo.run(bin)
        assert result.returncode == 1
        assert "the last operation was not a 'git commit --amend'" in result.stderr

    def test_fails_with_no_commits(self, repo, bin):
        """Test that unamend fails when there are no commits in the repository."""

        result = repo.run(bin)

        # Verify error exit code.
        assert result.returncode != 0

        # Git will produce an error about the branch not having commits.
        assert "fatal:" in result.stderr

    def test_rejects_single_argument(self, repo, bin):
        """Test that the command rejects arguments."""

        # Create a commit.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "commit")

        result = repo.run(bin, "--help")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-unamend does not accept any options" in result.stderr

    def test_rejects_multiple_arguments(self, repo, bin):
        """Test that the command rejects multiple arguments."""

        # Create a commit.
        repo.write("file1.txt", "Content")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "commit")

        result = repo.run(bin, "arg1", "arg2")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "git-unamend does not accept any options" in result.stderr
