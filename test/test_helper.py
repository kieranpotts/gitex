"""
Test suite for the TestRepo helper class.
"""

import os
import tempfile

import pytest

from helper import TestRepo


class TestTestRepo:
    """Test cases for the TestRepo helper class."""

    def test_initialization(self):
        """Test that TestRepo initializes correctly."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Verify directory was created.
        assert os.path.isdir(repo.dir())

        # Verify it's a Git repository.
        assert os.path.isdir(os.path.join(repo.dir(), ".git"))

        # Verify git interface is accessible.
        assert repo.git is not None

    def test_git_integration(self):
        """Test that Git operations work correctly."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Minimal required Git configuration to be able to make commit objects.
        repo.git.config("--local", "user.name", "John Doe")
        repo.git.config("--local", "user.email", "john.doe@example.com")

        # Create and commit a file.
        repo.write("file.txt", "Content")
        repo.git.add("file.txt")
        repo.git.commit("-m", "test commit")

        # Verify commit was created.
        log = repo.git.log("--oneline")
        assert "test commit" in log

        # Verify file is tracked.
        ls_files = repo.git.ls_files()
        assert "file.txt" in ls_files

    def test_cd(self):
        """Test changing to the repository directory."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Change to the test repo's root directory.
        repo_dir = repo.dir()

        # Change to a different directory.
        os.chdir(tempfile.gettempdir())
        assert os.getcwd() != repo_dir

        # Use cd() to change back to the repo directory.
        repo.cd()

        # Verify current directory is the repo directory.
        assert os.getcwd() == repo_dir

    def test_dir(self):
        """Test getting the repository directory path."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Change to the test repo's root directory.
        repo_dir = repo.dir()

        # Verify it's an absolute path.
        assert os.path.isabs(repo_dir)

        # Verify it's a directory.
        assert os.path.isdir(repo_dir)

        # Verify it's in the system temp directory.
        assert repo_dir.startswith(tempfile.gettempdir())

    def test_dirname(self):
        """Test getting the repository directory name."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Get the basename of the repository's root directory.
        dirname = repo.dirname()

        # Verify it's just the directory name, not a full path.
        assert "/" not in dirname
        assert "\\" not in dirname

        # Verify it matches the last component of dir().
        assert repo.dir().endswith(dirname)

    def test_written_file_exists(self):
        """Test checking if a file exists."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Verify file doesn't exist yet.
        assert not repo.exists("test.txt")

        # Create a file.
        repo.write("test.txt", "Content")

        # Verify file now exists.
        assert repo.exists("test.txt")

        # Verify the file is a file, not a directory.
        assert not repo.isdir("test.txt")

    def test_written_subdirectory_exists(self):
        """Test checking if a directory exists."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Verify a sub-directory doesn't exist yet.
        assert not repo.exists("subdir")

        # Create a sub-directory.
        repo.mkdir("subdir")

        # Verify the sub-directory now exists.
        assert repo.exists("subdir")

        # Verify the sub-directory is a directory and not a file.
        assert repo.isdir("subdir")

    def test_writing_multiple_files_and_subdirectories(self):
        """Test getting the list of files written to the repository."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Verify no written files initially.
        assert repo.files() == []

        # Write a file.
        repo.write("file1.txt", "Content 1")

        # Verify the new file exists.
        assert repo.files() == ["file1.txt"]

        # Write more files, including into sub-directories.
        repo.write("file2.txt", "Content 2")
        repo.mkdir("subdir")
        repo.write("subdir/file3.txt", "Content 3")

        # Verify all the expected files exist.
        assert repo.files() == ["file1.txt", "file2.txt", "subdir/file3.txt"]

    def test_write_overwrite(self):
        """Test overwriting an existing file."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Write a file.
        repo.write("test.txt", "Original content")

        # Overwrite it.
        repo.write("test.txt", "Updated content")

        # Verify new content.
        assert repo.read("test.txt") == "Updated content"

    def test_path(self):
        """Test getting the full path to a file."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Get path to a file.
        file_path = repo.path("test.txt")

        # Verify it's an absolute path.
        assert os.path.isabs(file_path)

        # Verify it's in the repo directory.
        assert file_path.startswith(repo.dir())

        # Verify it ends with the filename.
        assert file_path.endswith("test.txt")

    def test_read(self):
        """Test reading a file."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Write a file.
        repo.write("test.txt", "Hello, World!")

        # Read it back.
        read_content = repo.read("test.txt")

        # Verify content matches.
        assert read_content == "Hello, World!"

    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist raises an error."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Attempt to read a nonexistent file.
        with pytest.raises(FileNotFoundError):
            repo.read("nonexistent.txt")

    def test_remove(self):
        """Test removing a file."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Create a file.
        repo.write("test.txt", "Content")
        assert repo.exists("test.txt")

        # Remove it.
        repo.remove("test.txt")

        # Verify it's gone.
        assert not repo.exists("test.txt")

    def test_remove_nonexistent_file(self):
        """Test removing a file that doesn't exist raises an error."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Attempt to remove a nonexistent file.
        with pytest.raises(FileNotFoundError):
            repo.remove("nonexistent.txt")

    def test_run(self):
        """Test running a script."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Create a simple script. Set permissions.
        script_path = repo.path("test.sh")
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\necho 'Hello from script'\n")
        os.chmod(script_path, 0o755)

        # Run it.
        result = repo.run(script_path)

        # Verify success.
        assert result.returncode == 0
        assert "Hello from script" in result.stdout

    def test_run_with_arguments(self):
        """Test running a script with arguments."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Create a script that echoes arguments.
        script_path = repo.path("echo.sh")
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\necho $1 $2\n")
        os.chmod(script_path, 0o755)

        # Run it with arguments.
        result = repo.run(script_path, "foo", "bar")

        # Verify arguments were passed.
        assert result.returncode == 0
        assert "foo bar" in result.stdout

    def test_run_with_input(self):
        """Test running a script with stdin input."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Create a script that reads from stdin.
        script_path = repo.path("read.sh")
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\nread line\necho $line\n")
        os.chmod(script_path, 0o755)

        # Run it with input.
        result = repo.run(script_path, input="test input\n")

        # Verify input was received.
        assert result.returncode == 0
        assert "test input" in result.stdout

    def test_run_with_env(self):
        """Test running a script with custom environment variables."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Create a script that uses an environment variable.
        script_path = repo.path("env.sh")
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\necho $TEST_VAR\n")
        os.chmod(script_path, 0o755)

        # Run it with a custom environment.
        env = os.environ.copy()
        env["TEST_VAR"] = "custom value"
        result = repo.run(script_path, env=env)

        # Verify environment variable was set.
        assert result.returncode == 0
        assert "custom value" in result.stdout

    def test_run_failure(self):
        """Test running a script that fails."""

        # Initialize component-under-test.
        repo = TestRepo()

        # Create a script that exits with error.
        script_path = repo.path("fail.sh")
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\nexit 1\n")
        os.chmod(script_path, 0o755)

        # Run it.
        result = repo.run(script_path)

        # Verify it failed.
        assert result.returncode == 1
