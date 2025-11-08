"""
Test suite for git-author command.
"""


class TestGitAuthor:
    """Test cases for git-author command."""

    def test_with_name_and_email_flags(self, temp_repo, script_path):
        """Test changing author with --name and --email flags."""

        git = temp_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        temp_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Get commit hash before amend.
        commit_before_amend = git.rev_parse("HEAD")

        # Change the author of the commit using command-line flags.
        result = temp_repo.run(
            script_path, "--name", "Jane Smith", "--email", "jane@example.com"
        )

        # Get commit hash after amend.
        commit_after_amend = git.rev_parse("HEAD")

        # Verify success exit code.
        assert result.returncode == 0

        # The command returns the new commit hash.
        # It should differ from the original hash – it's a new commit object.
        assert len(result.stdout.strip()) == 40  # SHA-1 hash length.
        assert commit_after_amend != commit_before_amend

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_with_only_name_flag_prompts_for_email(self, temp_repo, script_path):
        """Test that providing only --name requires --email or interactive input."""

        git = temp_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        temp_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --name flag and supply email via stdin.
        result = temp_repo.run(
            script_path, "--name", "Jane Smith", input="jane@example.com\n"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    def test_with_only_email_flag_prompts_for_name(self, temp_repo, script_path):
        """Test that providing only --email requires --name or interactive input."""

        git = temp_repo.git()

        # Initial config values.
        git.config("--local", "user.name", "John Doe")
        git.config("--local", "user.email", "john.doe@example.com")

        # Create an initial commit.
        temp_repo.write("test.txt", "initial content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --email flag and supply name via stdin.
        result = temp_repo.run(
            script_path, "--email", "jane@example.com", input="Jane Smith\n"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the author was changed.
        author = git.log("-1", "--pretty=format:%an <%ae>").strip()
        assert author == "Jane Smith <jane@example.com>"

    # Note: Testing with ref parameter is challenging because it requires
    # an interactive rebase which cannot be automated in tests.

    def test_rejects_name_without_value(self, temp_repo, script_path):
        """Test that --name flag requires a value."""

        git = temp_repo.git()

        # Create an initial commit.
        temp_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --name flag but with no value.
        result = temp_repo.run(script_path, "--name")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "--name requires a value" in result.stderr

    def test_rejects_email_without_value(self, temp_repo, script_path):
        """Test that --email flag requires a value."""

        git = temp_repo.git()

        # Create an initial commit.
        temp_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Provide only --email flag but with no value.
        result = temp_repo.run(script_path, "--email")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "--email requires a value" in result.stderr

    def test_rejects_unknown_option(self, temp_repo, script_path):
        """Test that unknown options are rejected."""

        git = temp_repo.git()

        # Create an initial commit.
        temp_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Call the script with an unsupported option.
        result = temp_repo.run(script_path, "--unknown")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "unknown option '--unknown'" in result.stderr

    def test_rejects_multiple_ref_arguments(self, temp_repo, script_path):
        """Test that multiple positional arguments are rejected."""

        git = temp_repo.git()

        # Create an initial commit.
        temp_repo.write("test.txt", "content")
        git.add("test.txt")
        git.commit("-m", "initial commit")

        # Call the script with multiple positional arguments.
        result = temp_repo.run(script_path, "HEAD", "HEAD~1")

        # Verify error exit code.
        assert result.returncode == 1

        # Verify error message.
        assert "unexpected argument" in result.stderr
