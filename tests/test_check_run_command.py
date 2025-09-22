import tempfile
from pathlib import Path


from pch.check_run_command import check_run_command


def test_check_bash_command_success(tmp_path):
    with tempfile.NamedTemporaryFile(dir=Path(__file__).parent) as __:
        ret = check_run_command([__.name, "-c", "echo"])
    assert ret == 0


def test_check_bash_command_fail(tmp_path):
    with tempfile.NamedTemporaryFile(dir=Path(__file__).parent) as __:
        ret = check_run_command([__.name, "-c", "false"])
    assert ret == 1


def test_check_bash_command_no_files():
    with tempfile.NamedTemporaryFile() as __:
        ret = check_run_command(["xx", "-c", "echo"])
    assert ret == 0
