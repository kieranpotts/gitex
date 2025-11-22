"""
Helper functions for tests.
"""

import os
import subprocess
import tempfile

# https://github.com/gitpython-developers/GitPython
# https://gitpython.readthedocs.io/en/stable/tutorial.html
from git import Repo


class TestRepo:
    """Class to create and manage a temporary Git repository for testing purposes."""

    def __init__(self):
        self._dir = tempfile.mkdtemp()
        self._repo = Repo.init(self._dir, b="main")
        self._files = []

        self.git = self._repo.git

        self.cd()

    def cd(self):
        """Change to the test repo's root working directory."""

        os.chdir(self._dir)
        print(f"The current work directory has switched to {self._dir}")

    def dir(self):
        """Get the full path to the temporary repository's root directory."""

        return self._dir

    def dirname(self):
        """Get the directory name of the temporary repository"""

        system_tmpdir = tempfile.gettempdir()

        return self._dir[len(system_tmpdir) + 1 :]

    def run(self, bin, *args, input=None):
        """
        Run a git extension script and return the subprocess result.

        Args:
            bin: Path to the script to run.
            *args: Optional arguments to pass to the script.
            input: Optional input to pass to the script via stdin.

        Returns:
            subprocess.CompletedProcess with returncode, stdout, stderr
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
