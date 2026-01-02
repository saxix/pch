import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path
from typing import Sequence, Any, TYPE_CHECKING

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pch.utils import Color, RexList, is_git_tracked

if TYPE_CHECKING:
    from re import Pattern


def check_minimized(argv: Sequence[str] | None = None) -> int:  # noqa: C901 PLR0912 PLR0915
    """Check javascript script for minimized version."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    parser.add_argument("-b", "--base", action="store", help="Base path of source code.")
    parser.add_argument("-i", "--ignore", action="append", help="Ignore files to check.")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Verbosity level.")
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
    if args.verbosity >= 1:
        sys.stdout.write(f"Base path   : {str(base)}\n")
        sys.stdout.write(f"Ignore rules: {str(ignored)}\n")

    for filename in args.filenames:
        source = Path(filename).resolve()
        if source.name.endswith(".min.js"):
            continue
        sys.stdout.write("\n")
        if args.verbosity >= 2:
            sys.stdout.write(f"{str(filename)}: ")

        try:
            if not source.exists():
                if args.verbosity >= 3:
                    sys.stdout.write(f"{Color.RED} does not exist{Color.NORMAL}")
                continue
            if filename in ignored:
                if args.verbosity >= 2:
                    sys.stdout.write(f"{Color.YELLOW} ignored{Color.NORMAL}")
                continue
            if source.suffix != ".js":
                if args.verbosity >= 2:
                    sys.stdout.write(f"Not javascript file {filename}")
                continue
            minimized = source.with_suffix(".min.js")
            if not minimized.exists():
                sys.stdout.write(
                    f"{Color.RED + Color.BOLD}{source.relative_to(base)}: minimized not found.{Color.NORMAL}"
                )
                return_code = 1
            elif source.stat().st_mtime > minimized.stat().st_mtime:
                sys.stdout.write(
                    f"{Color.RED + Color.BOLD}{source.relative_to(base)}: outdated minimized.{Color.NORMAL}"
                )
                return_code = 1
            elif not is_git_tracked(minimized):
                sys.stdout.write(
                    f"{Color.RED + Color.BOLD}{minimized.relative_to(base)}: is not git tracked.{Color.NORMAL}"
                )
                return_code = 1
            else:
                sys.stdout.write(f"{Color.GREEN}Ok{Color.NORMAL}")
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Error running command on {filename}: {e}\n")
            return_code = 1
    sys.stdout.write("\n")
    return return_code


if __name__ == "__main__":
    raise SystemExit(check_minimized())
