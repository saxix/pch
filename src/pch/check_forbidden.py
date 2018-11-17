import re

import argparse
import sys
from pathlib import Path

from .utils import is_release, get_release, RexList
from distutils.version import LooseVersion, StrictVersion


def compile(perl_pattern):
    separator = perl_pattern[0]
    perl_pattern = perl_pattern.replace(r'\%s' % separator, chr(0))
    __, pattern, perl_options = perl_pattern.split(separator)
    pattern = pattern.replace(chr(0), separator)
    options = 0
    for opt in perl_options:
        if opt == 'i':
            options += re.IGNORECASE
        if opt == 'm':
            options += re.MULTILINE
        if opt == 's':
            options += re.DOTALL

    return re.compile(f'({pattern}.*)', options)


def check_forbidden(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help="")
    parser.add_argument('-p', '--pattern', action="append")
    parser.add_argument('-f', '--file', action="store")
    args = parser.parse_args(argv)
    rules = args.pattern or []
    targets = RexList([compile(p) for p in rules])
    if args.file:
        with Path(args.file).open() as f:
            for i, line in enumerate(f.readlines()):
                try:
                    targets.append(line[:-1])
                except Exception as e:
                    print(f"Error processing {args.file} at line {i}")
                    print(f"Cannot add regex: {e}")
                    sys.exit(1)

    for filename in args.filenames:
        content = Path(filename).read_text()
        for rex in targets:
            m = rex.search(content)
            if m:
                print(f"{filename} contains forbidden match '{rex.pattern}': `{m.group(0)}`")
                return 1
    return 0


if __name__ == '__main__':
    exit(check_forbidden())
