import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path
from typing import Sequence

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pch.utils import Color, RexList, is_git_tracked


def check_minimized(argv: Sequence[str] | None = None) -> int:  # noqa: C901 PLR0912
    """Check javascript script for minimized version."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    parser.add_argument("-b", "--base", action="store", help="Base path of source code.")
    parser.add_argument("-i", "--ignore", action="append", help="Ignore files to check.")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Verbosity level.")

    args = parser.parse_args(argv)
    if args.ignore:
        ignored = RexList([fnmatch.translate(e) for e in args.ignore] if args.ignore else [])
    if args.base:
        base = args.base
    else:
        base = Path.cwd()
    return_code = 0
    for filename in args.filenames:
        try:
            if not Path(filename).exists():
                if args.verbosity >= 2:
                    sys.stdout.write(f"File {filename} does not exist\n")
                continue
            if filename in args.ignored:
                if args.verbosity >= 2:
                    sys.stdout.write(f"Ignoring {filename}\n")
                continue
            source = Path(filename).resolve()
            if source.name.endswith(".min.js"):
                continue
            if source.suffix != ".js":
                if args.verbosity >= 2:
                    sys.stdout.write(f"Not javascript file {filename}\n")
                continue
            minimized = source.with_suffix(".min.js")
            if not minimized.exists():
                sys.stdout.write(
                    f"{Color.RED + Color.BOLD}{source.relative_to(base)}: minimized not found.{Color.NORMAL}\n"
                )
                return_code = 1
            else:
                if source.stat().st_mtime > minimized.stat().st_mtime:
                    sys.stdout.write(
                        f"{Color.RED + Color.BOLD}{source.relative_to(base)}: outdated minimized.{Color.NORMAL}\n"
                    )
                    return_code = 1
                if not is_git_tracked(minimized):
                    sys.stdout.write(
                        f"{Color.RED + Color.BOLD}{minimized.relative_to(base)}: is not git tracked.{Color.NORMAL}\n"
                    )
                    return_code = 1

        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Error running command on {filename}: {e}\n")
            return_code = 1
    return return_code


if __name__ == "__main__":
    raise SystemExit(check_minimized())
