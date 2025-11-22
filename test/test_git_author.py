"""
Test suite for git-author command.
"""


class TestGitAuthor:
    """Test cases for git-author command."""

    def test_with_name_and_email_flags(self, test_repo, script_path):
        """Test changing author with --name and --email flags."""

        git = test_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        test_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Get commit hash before amend.
        commit_before_amend = git.rev_parse("HEAD")

        # Change the author of the commit using command-line flags.
        result = test_repo.run(
            script_path, "--name", "Jane Smith", "--email", "jane@example.com"
        )

        # Get commit hash after amend.
        commit_after_amend = git.rev_parse("HEAD")

        # Verify success exit code.
        assert result.returncode == 0

        # The command returns the new commit hash.
        # It should differ from the original hash – it's a new commit object.
        assert "New commit hash is" in result.stdout
        assert commit_after_amend in result.stdout
        assert commit_after_amend != commit_before_amend

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_with_only_name_flag_prompts_for_email(self, test_repo, script_path):
        """Test that providing only --name, prompts for email."""

        git = test_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        test_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --name flag and supply email via stdin.
        result = test_repo.run(
            script_path, "--name", "Jane Smith", input="jane@example.com\n"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_with_only_email_flag_prompts_for_name(self, test_repo, script_path):
        """Test that providing only --email, prompts for name."""

        git = test_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        test_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --email flag and supply name via stdin.
        result = test_repo.run(
            script_path, "--email", "jane@example.com", input="Jane Smith\n"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_with_no_flags_prompts_for_both(self, test_repo, script_path):
        """Test that providing no flags prompts for both name and email."""

        git = test_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        test_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide no flags and supply name and email via stdin.
        result = test_repo.run(script_path, input="Jane Smith\njane@example.com\n")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_rejects_empty_name_from_prompt(self, test_repo, script_path):
        """Test that empty name from prompt is rejected."""

        git = test_repo.git()

        # Create an initial commit.
        test_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide empty name via stdin.
        result = test_repo.run(script_path, input="\n")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "Name is required" in result.stderr

    def test_rejects_empty_email_from_prompt(self, test_repo, script_path):
        """Test that empty email from prompt is rejected."""

        git = test_repo.git()

        # Create an initial commit.
        test_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide name but empty email via stdin.
        result = test_repo.run(script_path, input="Jane Smith\n\n")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "Email is required" in result.stderr

    def test_modifying_earlier_commit_with_flags(self, test_repo, script_path):
        """Test changing author of an earlier commit using flags."""

        git = test_repo.git()

        # Create multiple commits.
        test_repo.write("file1.txt", "content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        test_repo.write("file2.txt", "content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        test_repo.write("file3.txt", "content 3")
        git.add("file3.txt")
        git.commit("-m", "third commit")

        # Get the hash of the first commit (HEAD~2).
        first_commit_before = git.rev_parse("HEAD~2")

        # Change the author of the first commit.
        result = test_repo.run(
            script_path,
            "HEAD~2",
            "--name",
            "Jane Smith",
            "--email",
            "jane@example.com",
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify output contains new commit hash.
        assert "New commit hash is" in result.stdout

        # Get the hash of the first commit after the change.
        first_commit_after = git.rev_parse("HEAD~2")

        # The commit hash should have changed.
        assert first_commit_after != first_commit_before

        # Verify the author was changed on the first commit.
        author = git.log("HEAD~2", "-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

        # Verify all three commits still exist.
        log_count = len(git.log("--oneline").strip().split("\n"))
        assert log_count == 3

    def test_modifying_earlier_commit_with_prompts(self, test_repo, script_path):
        """Test changing author of an earlier commit using prompts."""

        git = test_repo.git()

        # Create multiple commits.
        test_repo.write("file1.txt", "content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")

        test_repo.write("file2.txt", "content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        # Change the author of the first commit via prompts.
        result = test_repo.run(
            script_path, "HEAD~1", input="Jane Smith\njane@example.com\n"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("HEAD~1", "-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_modifying_earlier_commit_by_sha(self, test_repo, script_path):
        """Test changing author using a commit SHA instead of relative ref."""

        git = test_repo.git()

        # Create multiple commits.
        test_repo.write("file1.txt", "content 1")
        git.add("file1.txt")
        git.commit("-m", "first commit")
        first_commit_sha = git.rev_parse("HEAD")

        test_repo.write("file2.txt", "content 2")
        git.add("file2.txt")
        git.commit("-m", "second commit")

        # Change the author using the SHA.
        result = test_repo.run(
            script_path,
            first_commit_sha,
            "--name",
            "Jane Smith",
            "--email",
            "jane@example.com",
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("HEAD~1", "-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_rejects_name_without_value(self, test_repo, script_path):
        """Test that --name flag requires a value."""

        git = test_repo.git()

        # Create an initial commit.
        test_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --name flag but with no value.
        result = test_repo.run(script_path, "--name")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "--name requires a value" in result.stderr

    def test_rejects_email_without_value(self, test_repo, script_path):
        """Test that --email flag requires a value."""

        git = test_repo.git()

        # Create an initial commit.
        test_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --email flag but with no value.
        result = test_repo.run(script_path, "--email")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "--email requires a value" in result.stderr

    def test_rejects_unknown_option(self, test_repo, script_path):
        """Test that unknown options are rejected."""

        git = test_repo.git()

        # Create an initial commit.
        test_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Call the script with an unsupported option.
        result = test_repo.run(script_path, "--unknown")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "unknown option '--unknown'" in result.stderr

    def test_rejects_multiple_ref_arguments(self, test_repo, script_path):
        """Test that multiple positional arguments are rejected."""

        git = test_repo.git()

        # Create an initial commit.
        test_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Call the script with multiple positional arguments.
        result = test_repo.run(script_path, "HEAD", "HEAD~1")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "unexpected option" in result.stderr
