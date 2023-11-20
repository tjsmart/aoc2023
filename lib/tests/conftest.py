import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from .. import _helpers


@pytest.fixture
def rootdir():
    startingdir = Path.cwd()
    with patch.object(_helpers, "get_rootdir") as mock_get_rootdir, TemporaryDirectory() as tempd:
        rootdir = Path(tempd) / "aoc1994"
        rootdir.mkdir(exist_ok=True, parents=True)
        mock_get_rootdir.return_value = rootdir
        os.chdir(rootdir)
        yield rootdir

    os.chdir(startingdir)
