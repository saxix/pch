import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path
from typing import Sequence, Any, TYPE_CHECKING

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pch.utils import Color, RexList, is_git_tracked, check_color

if TYPE_CHECKING:
    from re import Pattern


class MinimizedError(Exception):
    message = ""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __str__(self) -> str:
        return self.message % self.filename


class DoesNotExistError(MinimizedError):
    message = f"%s {Color.RED1} does not exist{Color.NORMAL}"


class IgnoredFileError(MinimizedError):
    message = f"%s {Color.YELLOW1} ignored{Color.NORMAL}"


class NotJavascriptError(MinimizedError):
    message = f"%s {Color.RED1} Not javascript file {Color.NORMAL}"


class MissingMinimizedError(MinimizedError):
    message = f"%s {Color.RED} minimized not found {Color.NORMAL}"


class OutdatedMinimizedError(MinimizedError):
    message = f"%s {Color.RED} outdated minimized.{Color.NORMAL}"


class NotInGitError(MinimizedError):
    message = f"%s {Color.RED1} is not git tracked.{Color.NORMAL}"


"""
    verbosity level:
        0: only errors
        1: ignored
"""
VERBOSITY_RULES = 1
VERBOSITY_IGNORED = 2


def check_minimized(argv: Sequence[str] | None = None) -> int:  # noqa: C901 PLR0912 PLR0915
    """Check javascript script for minimized version."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    parser.add_argument("-b", "--base", action="store", help="Base path of source code.")
    parser.add_argument("-i", "--ignore", action="append", help="Ignore files to check.")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Verbosity level.")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, help="Quiet mode.")
    parser.add_argument("-c", "--no-color", action="store_true", default=False, help="Disable color")
    args = parser.parse_args(argv)
    ignored: Sequence[str]
    if args.base:
        base = Path(args.base)
    else:
        base = Path.cwd()
    if args.ignore:
        ignored_rules: list[str | Pattern[Any]] = []
        for i in args.ignore:
            if i.startswith("/"):
                ignored_rules.append(fnmatch.translate(i))
            elif i.startswith("@"):
                ignored_rules.append(i[1:])
            else:
                ignored_rules.append(fnmatch.translate(i))
        ignored = RexList(ignored_rules)
    else:
        ignored = []
    return_code = 0
    if args.quiet:
        args.verbosity = -1

    if args.verbosity >= 1:
        sys.stdout.write(f"Base path   : {str(base)}\n")
        sys.stdout.write(f"Ignore rules: {str(ignored)}\n")
        sys.stdout.write("\n")

    for filename in args.filenames:
        source = Path(filename).resolve()
        if source.name.endswith(".min.js"):
            continue
        try:
            if not source.exists():
                raise DoesNotExistError(filename)
            if filename in ignored:
                raise IgnoredFileError(filename)
            if source.suffix != ".js":
                raise NotJavascriptError(filename)
            minimized = source.with_suffix(".min.js")
            if not minimized.exists():
                raise MissingMinimizedError(filename)
            if source.stat().st_mtime > minimized.stat().st_mtime:
                raise OutdatedMinimizedError(filename)
            if not is_git_tracked(minimized):
                raise NotInGitError(filename)
        except IgnoredFileError as e:
            if args.verbosity >= 2:
                sys.stderr.write(str(e) + "\n")
            continue
        except MinimizedError as e:
            return_code = 1
            if args.verbosity >= 0:
                sys.stderr.write(check_color(args.no_color, str(e)) + "\n")
            continue
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Error running command on {filename}: {e}\n")
            return_code = 1
        else:
            if args.verbosity >= 3:
                sys.stdout.write(f"{filename} {Color.GREEN}Ok{Color.NORMAL}\n")
    return return_code


if __name__ == "__main__":
    raise SystemExit(check_minimized())
