"""
Test suite for git-uncommit command.
"""

import os


class TestGitUncommit:
    """Test cases for git-uncommit command."""

    def test_uncommit_single_file(self, repo, bin):
        """Test uncommitting a commit with a single file."""

        # Create initial commit.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        # Create second commit.
        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "second commit")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back to the first commit.
        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "first commit"

        # Verify file2.txt is staged.
        status = repo.git.status("--short")
        assert "A  file2.txt" in status

        # Verify only one commit exists.
        log_output = repo.git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_uncommit_multiple_files(self, repo, bin):
        """Test uncommitting a commit with multiple files."""

        # Create initial commit.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        # Create second commit with multiple files.
        repo.write("file2.txt", "Content 2")
        repo.write("file3.txt", "Content 3")
        repo.git.add(".")
        repo.git.commit("-m", "second commit")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify both files are staged.
        status = repo.git.status("--short")
        assert "A  file2.txt" in status
        assert "A  file3.txt" in status

    def test_uncommit_with_modified_file(self, repo, bin):
        """Test uncommitting a commit that modified an existing file."""

        # Create initial commit.
        repo.write("file1.txt", "Version 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        # Modify and commit.
        repo.write("file1.txt", "Version 2")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "second commit")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file is staged with Version 2.
        status = repo.git.status("--short")
        assert "M  file1.txt" in status

        # Verify commit has Version 1.
        show_output = repo.git.show("HEAD:file1.txt")
        assert "Version 1" in show_output

    def test_uncommit_with_deleted_file(self, repo, bin):
        """Test uncommitting a commit that deleted a file."""

        # Create initial commit with two files.
        repo.write("file1.txt", "Content 1")
        repo.write("file2.txt", "Content 2")
        repo.git.add(".")
        repo.git.commit("-m", "first commit")

        # Delete file2 and commit.
        os.remove(os.path.join(repo.dir(), "file2.txt"))
        repo.git.add("file2.txt")
        repo.git.commit("-m", "delete file2")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file2.txt deletion is staged.
        status = repo.git.status("--short")
        assert "D  file2.txt" in status

        # Verify commit still has file2.txt.
        ls_tree = repo.git.ls_tree("-r", "--name-only", "HEAD")
        assert "file2.txt" in ls_tree

    def test_uncommit_multiple_times(self, repo, bin):
        """Test uncommitting multiple times in succession."""

        # Create three commits.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "commit 1")

        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "commit 2")

        repo.write("file3.txt", "Content 3")
        repo.git.add("file3.txt")
        repo.git.commit("-m", "commit 3")

        # Uncommit first time.
        result = repo.run(bin)
        assert result.returncode == 0

        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "commit 2"

        # Uncommit second time.
        result = repo.run(bin)
        assert result.returncode == 0

        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "commit 1"

    def test_uncommit_with_empty_commit(self, repo, bin):
        """Test uncommitting an empty commit."""

        # Create initial commit.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        # Create empty commit.
        repo.git.commit("--allow-empty", "-m", "empty commit")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back to first commit.
        commit_msg = repo.git.log("-1", "--format=%s")
        assert commit_msg == "first commit"

        # Verify no staged changes.
        status = repo.git.status("--short")
        assert status == ""

    def test_uncommit_preserves_working_tree(self, repo, bin):
        """Test that uncommit preserves unstaged working tree changes."""

        # Create initial commit.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        # Create second commit.
        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "second commit")

        # Make unstaged change.
        repo.write("file3.txt", "Unstaged file")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file3.txt still exists and is unstaged.
        assert os.path.exists(os.path.join(repo.dir(), "file3.txt"))
        status = repo.git.status("--short")
        assert "?? file3.txt" in status

    def test_uncommit_preserves_staged_and_unstaged(self, repo, bin):
        """Test that uncommit preserves both staged and unstaged changes."""

        # Create initial commit.
        repo.write("file1.txt", "Content 1")
        repo.git.add("file1.txt")
        repo.git.commit("-m", "first commit")

        # Create second commit.
        repo.write("file2.txt", "Content 2")
        repo.git.add("file2.txt")
        repo.git.commit("-m", "second commit")

        # Make staged change.
        repo.write("file3.txt", "Staged content")
        repo.git.add("file3.txt")

        # Make unstaged change.
        repo.write("file4.txt", "Unstaged content")

        result = repo.run(bin)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file2.txt and file3.txt are staged.
        status = repo.git.status("--short")
        assert "A  file2.txt" in status
        assert "A  file3.txt" in status

        # Verify file4.txt is unstaged.
        assert "?? file4.txt" in status

    def test_fails_with_no_commits(self, repo, bin):
        """Test that uncommit fails when there are no commits in the repository."""

        result = repo.run(bin)

        # Verify error exit code.
        assert result.returncode != 0

        # Git will produce an error about HEAD~1 not being valid.
        assert "fatal:" in result.stderr or "error:" in result.stderr

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
        assert "git-uncommit does not accept any options" in result.stderr

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
        assert "git-uncommit does not accept any options" in result.stderr
