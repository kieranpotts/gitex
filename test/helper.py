"""
Helper functions for tests.
"""

import os
import subprocess
import tempfile

# https://github.com/gitpython-developers/GitPython
# https://gitpython.readthedocs.io/en/stable/tutorial.html
from git import Repo


class TempRepo:
    """Class to create and manage a temporary Git repository for testing purposes."""

    def __init__(self):
        self._cwd = tempfile.mkdtemp()
        self._repo = Repo.init(self._cwd, b="main")
        self._files = []

        self.cd_repo()

    def cd_repo(self):
        os.chdir(self._cwd)
        print(f"The current work directory has switched to {self._cwd}")

    def cwd(self):
        return self._cwd

    def dirname(self):
        """Get the directory name of the temporary repository"""

        system_tmpdir = tempfile.gettempdir()

        return self._cwd[len(system_tmpdir) + 1 :]

    def git(self):
        return self._repo.git

    def run(self, script_path, *args, input=None):
        """
        Run a git extension script and return the subprocess result.

        Args:
            script_path: Path to the script to run.
            *args: Optional arguments to pass to the script.
            input: Optional input to pass to the script via stdin.

        Returns:
            subprocess.CompletedProcess with returncode, stdout, stderr
        """

        return subprocess.run(
            [script_path, *args],
            cwd=self._cwd,
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

        file_path = os.path.join(self._cwd, filename)
        with open(file_path, "w") as f:
            f.write(content)
        self._files.append(filename)
