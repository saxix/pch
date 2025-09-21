import pytest
from pch.check_run_command import check_run_command

def test_check_bash_command_success(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text("content")
    ret = check_run_command(["echo", str(p)])
    assert ret == 0

def test_check_bash_command_fail(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text("content")
    ret = check_run_command(["false", str(p)])
    assert ret == 1

def test_check_bash_command_no_command():
    with pytest.raises(SystemExit):
        check_run_command([])

def test_check_bash_command_no_files():
    ret = check_run_command(["echo"])
    assert ret == 0
