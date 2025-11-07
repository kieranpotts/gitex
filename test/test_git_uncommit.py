"""
Test suite for git-uncommit command.
"""

from pathlib import Path


class TestGitUncommit:
    """Test cases for git-uncommit command."""

    def test_uncommit_single_file(self, temp_repo, script_path):
        """Test uncommitting a commit with a single file."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create second commit.
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back to the first commit.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "first commit"

        # Verify file2.txt is staged.
        status = git.status("--short")
        assert "A  file2.txt" in status

        # Verify only one commit exists.
        log_output = git.log("--oneline")
        assert log_output.count("\n") == 0

    def test_uncommit_multiple_files(self, temp_repo, script_path):
        """Test uncommitting a commit with multiple files."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create second commit with multiple files.
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        Path(temp_repo.cwd(), "file3.txt").write_text("Content 3")
        git.add(".")
        git.commit("-m", "second commit")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify both files are staged.
        status = git.status("--short")
        assert "A  file2.txt" in status
        assert "A  file3.txt" in status

    def test_uncommit_with_modified_file(self, temp_repo, script_path):
        """Test uncommitting a commit that modified an existing file."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Version 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Modify and commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Version 2")
        git.add("file1.txt")
        git.commit("-m", "second commit")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file is staged with Version 2.
        status = git.status("--short")
        assert "M  file1.txt" in status

        # Verify commit has Version 1.
        show_output = git.show("HEAD:file1.txt")
        assert "Version 1" in show_output

    def test_uncommit_with_deleted_file(self, temp_repo, script_path):
        """Test uncommitting a commit that deleted a file."""

        git = temp_repo.git()

        # Create initial commit with two files.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add(".")
        git.commit("-m", "first commit")

        # Delete file2 and commit.
        Path(temp_repo.cwd(), "file2.txt").unlink()
        git.add("file2.txt")
        git.commit("-m", "delete file2")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file2.txt deletion is staged.
        status = git.status("--short")
        assert "D  file2.txt" in status

        # Verify commit still has file2.txt.
        ls_tree = git.ls_tree("-r", "--name-only", "HEAD")
        assert "file2.txt" in ls_tree

    def test_uncommit_multiple_times(self, temp_repo, script_path):
        """Test uncommitting multiple times in succession."""

        git = temp_repo.git()

        # Create three commits.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "commit 1")

        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "commit 2")

        Path(temp_repo.cwd(), "file3.txt").write_text("Content 3")
        git.add("file3.txt")
        git.commit("-m", "commit 3")

        # Uncommit first time.
        result = temp_repo.run(script_path)
        assert result.returncode == 0

        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "commit 2"

        # Uncommit second time.
        result = temp_repo.run(script_path)
        assert result.returncode == 0

        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "commit 1"

    def test_uncommit_with_empty_commit(self, temp_repo, script_path):
        """Test uncommitting an empty commit."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create empty commit.
        git.commit("--allow-empty", "-m", "empty commit")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify we're back to first commit.
        commit_msg = git.log("-1", "--format=%s")
        assert commit_msg == "first commit"

        # Verify no staged changes.
        status = git.status("--short")
        assert status == ""

    def test_uncommit_preserves_working_tree(self, temp_repo, script_path):
        """Test that uncommit preserves unstaged working tree changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create second commit.
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        # Make unstaged change.
        Path(temp_repo.cwd(), "file3.txt").write_text("Unstaged file")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file3.txt still exists and is unstaged.
        assert Path(temp_repo.cwd(), "file3.txt").exists()
        status = git.status("--short")
        assert "?? file3.txt" in status

    def test_uncommit_preserves_staged_and_unstaged(self, temp_repo, script_path):
        """Test that uncommit preserves both staged and unstaged changes."""

        git = temp_repo.git()

        # Create initial commit.
        Path(temp_repo.cwd(), "file1.txt").write_text("Content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        # Create second commit.
        Path(temp_repo.cwd(), "file2.txt").write_text("Content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        # Make staged change.
        Path(temp_repo.cwd(), "file3.txt").write_text("Staged content")
        git.add("file3.txt")

        # Make unstaged change.
        Path(temp_repo.cwd(), "file4.txt").write_text("Unstaged content")

        result = temp_repo.run(script_path)

        # Verify success exit code.
        assert result.returncode == 0

        # Verify file2.txt and file3.txt are staged.
        status = git.status("--short")
        assert "A  file2.txt" in status
        assert "A  file3.txt" in status

        # Verify file4.txt is unstaged.
        assert "?? file4.txt" in status

    def test_fails_with_no_commits(self, temp_repo, script_path):
        """Test that uncommit fails when there are no commits in the repository."""

        result = temp_repo.run(script_path)

        # Verify error exit code.
        assert result.returncode != 0

        # Git will produce an error about HEAD~1 not being valid.
        assert "fatal:" in result.stderr or "error:" in result.stderr

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
        assert "git-uncommit does not accept any arguments" in result.stderr

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
        assert "git-uncommit does not accept any arguments" in result.stderr
