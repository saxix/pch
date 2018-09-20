# refs/heads/release/1.0b
from unittest import mock

import pytest

from pch.utils import get_current_branch, is_release


@pytest.mark.parametrize('branch,expected', [('refs/heads/release/1.0b', True),
                                    ('refs/heads/develop', False)])
def test_is_release(branch, expected):
    with mock.patch('pch.utils.cmd_output', lambda *a: branch):
        assert is_release() is expected


@pytest.mark.parametrize('branch', ['refs/heads/release/1.0b', 'refs/heads/test'])
def test_get_current_branch(branch):
    with mock.patch('pch.utils.cmd_output', lambda *a: branch):
        branch = get_current_branch()
    assert branch
