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

        repo = TestRepo()

        # Verify directory was created.
        assert os.path.isdir(repo.dir())

        # Verify it's a Git repository.
        assert os.path.isdir(os.path.join(repo.dir(), ".git"))

        # Verify git object is accessible.
        assert repo.git is not None

    def test_cd(self):
        """Test changing to the repository directory."""

        repo = TestRepo()
        repo_dir = repo.dir()

        # Change to a different directory.
        os.chdir(tempfile.gettempdir())
        assert os.getcwd() != repo_dir

        # Use cd() to change back.
        repo.cd()

        # Verify current directory is the repo directory.
        assert os.getcwd() == repo_dir

    def test_dir(self):
        """Test getting the repository directory path."""

        repo = TestRepo()
        dir_path = repo.dir()

        # Verify it's an absolute path.
        assert os.path.isabs(dir_path)

        # Verify it's a directory.
        assert os.path.isdir(dir_path)

        # Verify it's in the system temp directory.
        assert dir_path.startswith(tempfile.gettempdir())

    def test_dirname(self):
        """Test getting the repository directory name."""

        repo = TestRepo()
        dirname = repo.dirname()

        # Verify it's just the directory name, not a full path.
        assert "/" not in dirname
        assert "\\" not in dirname

        # Verify it matches the last component of dir().
        assert repo.dir().endswith(dirname)

    def test_exists_file(self):
        """Test checking if a file exists."""

        repo = TestRepo()

        # File doesn't exist yet.
        assert not repo.exists("test.txt")

        # Create a file.
        repo.write("test.txt", "Content")

        # File now exists.
        assert repo.exists("test.txt")

    def test_files(self):
        """Test getting the list of files written to the repository."""

        repo = TestRepo()

        # Initially no files.
        assert repo.files() == []

        # Write a file.
        repo.write("file1.txt", "Content 1")
        assert repo.files() == ["file1.txt"]

        # Write more files.
        repo.write("file2.txt", "Content 2")
        repo.mkdir("subdir")
        repo.write("subdir/file3.txt", "Content 3")
        assert repo.files() == ["file1.txt", "file2.txt", "subdir/file3.txt"]

    def test_exists_directory(self):
        """Test checking if a directory exists."""

        repo = TestRepo()

        # Directory doesn't exist yet.
        assert not repo.exists("subdir")

        # Create a directory.
        repo.mkdir("subdir")

        # Directory now exists.
        assert repo.exists("subdir")

    def test_isdir(self):
        """Test checking if something is a directory."""

        repo = TestRepo()

        # Directory doesn't exist.
        assert not repo.isdir("subdir")

        # Create a directory.
        repo.mkdir("subdir")

        # Directory exists and is a directory.
        assert repo.isdir("subdir")

        # Create a file.
        repo.write("file.txt", "Content")

        # File exists but is not a directory.
        assert not repo.isdir("file.txt")

    def test_mkdir(self):
        """Test creating a directory."""

        repo = TestRepo()

        # Create a directory.
        dir_path = repo.mkdir("subdir")

        # Verify it exists.
        assert os.path.isdir(dir_path)

        # Verify it's in the repo.
        assert dir_path.startswith(repo.dir())

        # Verify nested directory creation.
        nested_path = repo.mkdir("parent/child")
        assert os.path.isdir(nested_path)

    def test_path(self):
        """Test getting the full path to a file."""

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

        repo = TestRepo()

        # Write a file.
        repo.write("test.txt", "Hello, World!")

        # Read it back.
        read_content = repo.read("test.txt")

        # Verify content matches.
        assert read_content == "Hello, World!"

    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist raises an error."""

        repo = TestRepo()

        # Attempt to read a nonexistent file.
        with pytest.raises(FileNotFoundError):
            repo.read("nonexistent.txt")

    def test_remove(self):
        """Test removing a file."""

        repo = TestRepo()

        # Create a file.
        repo.write("test.txt", "content")
        assert repo.exists("test.txt")

        # Remove it.
        repo.remove("test.txt")

        # Verify it's gone.
        assert not repo.exists("test.txt")

    def test_remove_nonexistent_file(self):
        """Test removing a file that doesn't exist raises an error."""

        repo = TestRepo()

        # Attempt to remove a nonexistent file.
        with pytest.raises(FileNotFoundError):
            repo.remove("nonexistent.txt")

    def test_run(self):
        """Test running a script."""

        repo = TestRepo()

        # Create a simple script.
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

    def test_write(self):
        """Test writing a file."""

        repo = TestRepo()

        # Write a file.
        repo.write("test.txt", "Test content")

        # Verify it exists.
        assert repo.exists("test.txt")

        # Verify content is correct.
        file_path = repo.path("test.txt")
        with open(file_path, "r") as f:
            assert f.read() == "Test content"

    def test_write_nested_file(self):
        """Test writing a file in a subdirectory."""

        repo = TestRepo()

        # Create subdirectory.
        repo.mkdir("subdir")

        # Write a file in the subdirectory.
        repo.write("subdir/test.txt", "Content")

        # Verify it exists.
        assert repo.exists("subdir/test.txt")

    def test_write_overwrite(self):
        """Test overwriting an existing file."""

        repo = TestRepo()

        # Write a file.
        repo.write("test.txt", "Original content")

        # Overwrite it.
        repo.write("test.txt", "Updated content")

        # Verify new content.
        assert repo.read("test.txt") == "Updated content"

    def test_git_integration(self):
        """Test that Git operations work correctly."""

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
