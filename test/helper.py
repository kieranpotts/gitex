"""
Helper functions for tests.
"""

import os
import subprocess
import tempfile

# https://github.com/gitpython-developers/GitPython
# https://gitpython.readthedocs.io/en/stable/tutorial.html
from git import Repo as GitRepo


class TestRepo:
    """Class to create and manage a temporary Git repository for testing purposes."""

    def __init__(self):
        # /tmp/* directory in which the test repository will be created.
        self._dir = tempfile.mkdtemp()

        # Initialize a Git repository in the temporary directory.
        # Default branch = main.
        self._repo = GitRepo.init(self._dir, b="main")

        # Maintain a list of files that will be written to the test repo directory.
        self._files = []

        # Expose Git interface.
        self.git = self._repo.git

    def cd(self):
        """Change the current working directory to the test repository's root."""

        os.chdir(self._dir)
        print(f"The current work directory has switched to {self._dir}")

    def dir(self):
        """
        Get the full path to the temporary repository's root directory.

        Returns:
            The absolute path to the repository directory.
        """

        return self._dir

    def dirname(self):
        """
        Get the directory name of the temporary repository (basename only).

        Returns:
            The repo's directory basename without the full path to the /tmp directory.
        """

        system_tmpdir = tempfile.gettempdir()

        return self._dir[len(system_tmpdir) + 1 :]

    def exists(self, filename):
        """
        Check if a file or directory exists in the temporary repository.

        Args:
            filename: Name of the file or directory to check.

        Returns:
            True if the file or directory exists, False otherwise.
        """

        file_path = os.path.join(self._dir, filename)

        return os.path.exists(file_path)

    def files(self):
        """
        Get the list of files that have been written to the repository.

        Returns:
            A list of filenames that were created using the write() method.
        """

        return self._files

    def isdir(self, dirname):
        """
        Check if a directory exists in the temporary repository.

        Args:
            dirname: Name of the directory to check.

        Returns:
            True if the directory exists and is a directory, False otherwise.
        """

        dir_path = os.path.join(self._dir, dirname)

        return os.path.isdir(dir_path)

    def mkdir(self, dirname):
        """
        Create a directory in the temporary repository.

        Args:
            dirname: Name of the directory to create.

        Returns:
            The full path to the created directory.
        """

        dir_path = os.path.join(self._dir, dirname)
        os.makedirs(dir_path)

        return dir_path

    def path(self, filename):
        """
        Get the full path to a file or directory in the temporary repository.

        Args:
            filename: Name of the file or directory.

        Returns:
            The absolute path to the file or directory.
        """

        return os.path.join(self._dir, filename)

    def read(self, filename):
        """
        Read content from a file in the temporary repository.

        Args:
            filename: Name of the file to read.

        Returns:
            The content of the file as a string.
        """

        file_path = os.path.join(self._dir, filename)

        with open(file_path, "r") as f:
            return f.read()

    def remove(self, filename):
        """
        Remove a file from the temporary repository.

        Args:
            filename: Name of the file to remove.
        """

        file_path = os.path.join(self._dir, filename)
        os.remove(file_path)

    def run(self, bin, *args, input=None, env=None):
        """
        Run a git extension script and return the subprocess result.

        Args:
            bin: Path to the script to run.
            *args: Optional arguments to pass to the script.
            input: Optional input to pass to the script via stdin.
            env: Optional environment variables to pass to the script.

        Returns:
            subprocess.CompletedProcess with returncode, stdout, and stderr.
        """

        # Explicitly use bash to execute the script. This is required for the tests
        # to run in the dev container, and it should help resolve shebang
        # interpretation issues in other dev environments, too.
        return subprocess.run(
            ["bash", bin, *args],
            cwd=self._dir,
            capture_output=True,
            text=True,
            input=input,
            env=env,
        )

    def write(self, filename, content):
        """
        Write content to a file in the temporary repository.

        Args:
            filename: Name of the file to write.
            content: Content to write to the file.
        """

        file_path = os.path.join(self._dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        self._files.append(filename)
