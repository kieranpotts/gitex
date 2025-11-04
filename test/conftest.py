# Sharing fixtures
# Ref: https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session

import pytest

from helper import TempRepo


@pytest.fixture(scope="function")
def temp_repo():
    """Create a temporary Git repository that is reset for each test
    function call."""

    repo = TempRepo()

    return repo
