from __future__ import annotations

import re
import shutil
import subprocess
from enum import Enum
from pathlib import Path
from typing import Any


class Color(str, Enum):
    BOLD = "\033[1m"
    UNDER = "\033[4m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    NORMAL = "\033[0m"
    DIM = "\033[2m"

    def __str__(self) -> str:
        return self.value


def cmd_output(*cmd: str, **kwargs: Any) -> str:
    retcode = kwargs.pop("retcode", 0)
    popen_kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
    popen_kwargs.update(kwargs)
    proc = subprocess.Popen(cmd, **popen_kwargs)  # type: ignore[call-overload] # noqa: S603
    stdout, stderr = proc.communicate()
    stdout = stdout.decode("UTF-8")
    if stderr is not None:
        stderr = stderr.decode("UTF-8")
    if retcode is not None and proc.returncode != retcode:
        raise subprocess.CalledProcessError(retcode, cmd, stdout, stderr)
    return stdout


class RexList(list):
    """list class where each entry is a valid regular expression.

    >>> r = RexList(["a.*"])
    >>> r.append("[0-9]*")
    >>> "1" in r
    True

    >>> ['abc', 'ccc', '10'] - r
    ['ccc']

    >>> ('abc', 'ccc', '10') - r
    ('ccc',)

    >>> "cc" in r
    False

    >>> "abc" in r
    True

    >>> print(r)
    ['a.*', '[0-9]*']

    >>> r[0] = '.*'

    >>> r[0] = '[0-'
    Traceback (most recent call last):
        ...
    ValueError: [0- is not a valid regular expression
    """

    def __init__(self, seq: list[str | re.Pattern] | None = None) -> None:
        regexx = []
        if seq:
            for el in seq:
                if isinstance(el, re.Pattern):
                    regexx.append(el)
                else:
                    regexx.append(re.compile(self._compile(el)))
        super().__init__(regexx)

    def __repr__(self) -> str:
        return str([r.pattern for r in self])

    def _compile(self, pattern: str) -> re.Pattern:
        try:
            return re.compile(pattern)
        except (TypeError, re.error):
            raise ValueError(str(pattern)) from None

    def __setitem__(self, i: Any, pattern: Any) -> None:
        rex = self._compile(pattern)
        super().__setitem__(i, rex)

    def append(self, pattern: str) -> None:
        rex = self._compile(pattern)
        super().append(rex)

    def __contains__(self, target: Any) -> bool:
        t = str(target)
        for rex in self:
            m = rex.match(t)
            if m and m.group():
                return True
        return False

    def __rsub__(self, other: Any) -> Any:
        if other and isinstance(other, (list | tuple)):
            t = type(other)
            return t([a for a in other if a not in self])
        return self


def safe_path(p: Path | str, base: Path | None = None) -> Path:
    base = Path.cwd() if base is None else Path(base)
    # Ensure 'p' is inside 'base' (prevent path traversal)
    return Path(p).resolve().relative_to(base.resolve())


def is_git_tracked(path: Path) -> bool:
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable not found in PATH")

    try:
        subprocess.run(  # noqa: S603
            [git, "ls-files", "--error-unmatch", str(safe_path(path))],
            capture_output=True,  # UP022 compliant
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def is_git_ignored(path: Path) -> bool:
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable not found in PATH")

    result = subprocess.run(  # noqa: S603
        [git, "check-ignore", str(safe_path(path))],
        capture_output=True,  # UP022 compliant
        check=False,  # we don’t want exceptions here
    )
    return result.returncode == 0
