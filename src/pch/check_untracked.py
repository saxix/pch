from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from .utils import RexList, cmd_output


def check_untracked(argv: Any | None = None) -> int:
    """Check if there are unwanted untracked files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("directories", nargs="*", help="")
    parser.add_argument("--ignore", action="append", help="")

    args = parser.parse_args(argv)
    dirs = args.directories
    ignored = RexList()
    if args.ignore:
        ignored = RexList(args.ignore)

    if not dirs:
        dirs = [os.curdir]

    dirs = list(map(os.path.realpath, dirs))

    output = cmd_output("git", "ls-files", "--others", "--exclude-standard", *dirs)
    if output:
        results = output.split("\n")
        filenames = results - ignored
        if filenames:
            sys.stdout.write("\n".join(filenames))
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(check_untracked())
