from unittest import mock

import pytest

import pch
from pch.check_version_release_match import check_version_release_match


@pytest.mark.parametrize('branch,expected', [('refs/heads/release/0.99', 1),
                                             ('refs/heads/develop', 0),
                                             ('refs/heads/release/1.0.0', 0),
                                             ('refs/heads/release/1.0', 0)])
def test_check_version_release_match(branch, expected):
    with mock.patch('pch.VERSION', '1.0.0'):
        with mock.patch('pch.utils.cmd_output', lambda *a: branch):
            assert check_version_release_match(["--package", "pch",
                                                "--version-attr", "VERSION"]) == expected
