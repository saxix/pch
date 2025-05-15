from subprocess import CalledProcessError

import pytest

from pch.utils import cmd_output


@pytest.mark.parametrize(
    "cmd,retcode",
    [
        ("ls", 0),
    ],
)
def test_cmd_output(cmd, retcode):
    assert cmd_output(cmd, retcode=retcode)


def test_cmd_output_fail():
    with pytest.raises(CalledProcessError):
        assert cmd_output("ls", retcode="99")
