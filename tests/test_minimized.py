from pathlib import Path

from pch.check_minimized import check_minimized

JS_DIR = Path(__file__).parent / "js"


def test_check_ok():
    ret = check_minimized([str(JS_DIR / "ok.js")])
    assert ret == 0


def test_verbosity_ok(capsys):
    ret = check_minimized([str(JS_DIR / "ok.js"), "-vvvv"])
    captured = capsys.readouterr()
    assert ret == 0
    assert "Ignore rules" in captured.out


def test_check_missing(capsys):
    ret = check_minimized([str(JS_DIR / "missing.js"), "-vvvv"])
    captured = capsys.readouterr()
    assert ret == 1
    assert "missing.js: minimized not found." in captured.out
