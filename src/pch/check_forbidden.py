import re

import argparse
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

    return re.compile(pattern, options)


def check_forbidden(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help="")
    parser.add_argument('-p', '--pattern', action="append")
    args = parser.parse_args(argv)

    targets = RexList([compile(p) for p in args.pattern])
    for filename in args.filenames:
        content = Path(filename).read_text()
        for rex in targets:
            if rex.search(content):
                print(f"{filename} contains forbidden match '{rex.pattern}'")
                return 1
    return 0


if __name__ == '__main__':
    exit(check_forbidden())
