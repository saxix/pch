from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path
from typing import Any, Generator

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pch.utils import Color, RexList


def clean(s):
    return s.replace("\n", "")


def compile_re(perl_pattern: str) -> re.Pattern:
    separator = perl_pattern[0]
    perl_pattern = perl_pattern.replace(r"\%s" % separator, chr(0))
    __, pattern, perl_options = perl_pattern.split(separator)
    pattern = pattern.replace(chr(0), separator)
    options = 0
    for opt in perl_options:
        if opt == "i":
            options += re.IGNORECASE
        if opt == "m":
            options += re.MULTILINE
        if opt == "s":
            options += re.DOTALL

    return re.compile(f"{pattern}", options)


def is_valid(filename: str | Path, include: list[str], exclude: list[str]) -> bool:
    if not include and not exclude:
        return True

    if include and exclude:
        return filename in exclude and filename not in exclude

    if exclude:
        return filename not in exclude

    return filename in include


def selector(bases: list[str], includes: list[str], excludes: list[str]) -> Generator[str, None, None]:
    for filename in bases:
        if Path(filename).is_file():
            if is_valid(filename, includes, excludes):
                yield filename
        elif Path(filename).is_dir():
            for entry in Path(filename).glob("*"):
                if is_valid(entry, includes, excludes):
                    yield str(entry)


def check_forbidden(argv: Any | None = None) -> int:  # noqa: PLR0912, C901
    """Check source code for forbidden text."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="list of filenames to check")
    parser.add_argument("-p", "--pattern", action="append", help="regex pattern to check")
    parser.add_argument("-c", "--config", action="store", help="path to config file")
    parser.add_argument("-e", "--exclude", nargs="*", action="store", help="list of filenames to exclude")
    parser.add_argument("-i", "--include", nargs="*", action="store", help="list of filenames to include")
    parser.add_argument("-v", "--verbosity", default=0, action="store", type=int, help="verbosity level")
    args = parser.parse_args(argv)
    rules = RexList([compile_re(p) for p in args.pattern or []])
    includes = RexList([fnmatch.translate(e) for e in args.include]) if args.include else []
    excludes = RexList([fnmatch.translate(e) for e in args.exclude]) if args.exclude else []
    targets: list[str] = []
    verbosity = int(args.verbosity)

    if args.config:
        try:
            with Path(args.config).open("r") as f:
                for i, line in enumerate(f.readlines()):
                    try:
                        pattern = line[:-1]
                        if pattern:
                            targets.append(pattern)
                    except re.PatternError as e:
                        sys.stdout.write(f"Error processing {args.config} at line {i}\n")
                        sys.stdout.write(f"Cannot add regex: {e}\n")
                        sys.exit(1)
        except FileNotFoundError:
            sys.stdout.write(f"check-forbidden: {args.config} does not exists.\n")
            return 1
    else:
        targets = args.filenames
    if verbosity > 2:
        sys.stdout.write(f"{Color.BLUE + Color.BOLD}Processing: {targets}{Color.NORMAL}\n")

    return_code = 0
    for filename in selector(targets, includes, excludes):
        if verbosity > 1:
            sys.stdout.write(f"{Color.BLUE + Color.BOLD}Processing: {filename}{Color.NORMAL}\n")
        try:
            content = Path(filename).read_text()
            for rex in rules:
                if m := rex.search(content):
                    sys.stdout.write(
                        f"{Color.NORMAL}{filename}: "
                        f"{Color.YELLOW}contains forbidden match '{rex.pattern}': "
                        f"{Color.RED}`{clean(m.group(0))}`\n"
                    )
                    return_code = 1
        except UnicodeDecodeError:
            pass
        except OSError as e:
            sys.stderr.write(f"Error reading {Path(filename).absolute()}: {e}\n")
            return_code = 1
    return return_code


if __name__ == "__main__":
    sys.exit(check_forbidden())
