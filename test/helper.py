"""
Helper functions for tests.
"""

import os
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
