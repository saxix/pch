from pathlib import Path

import pytest

from pch.check_forbidden import check_forbidden

TEST_FILE = str(Path(__file__).parent.parent / 'README.md')


@pytest.mark.parametrize('word,expected', [('/.check-forbidden./', 1),
                                           ('/bbb/', 0),
                                           ('/forbidde\s/', 0),
                                           ('/Hooks/', 1),
                                           ('/hooks/i', 1),
                                           (r'/check.*/', 1),
                                           (r'/for..dden/', 1)
                                           ])
def test_check_forbidden(word, expected):
    ret = check_forbidden([TEST_FILE, "-p", word])
    assert ret == expected, ret


def test_check_forbidden_multi():
    ret = check_forbidden([TEST_FILE, "-p", "/xxx/", "-p", "/for/"])
    assert ret == 1
