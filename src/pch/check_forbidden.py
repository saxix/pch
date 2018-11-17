import re

import argparse
import sys
import os
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

    print(Path(os.curdir).absolute())
    if args.file:
        try:
            with Path(args.file).open("r") as f:
                for i, line in enumerate(f.readlines()):
                    try:
                        pattern = line[:-1]
                        if pattern:
                            targets.append(pattern)
                    except Exception as e:
                        print(f"Error processing {args.file} at line {i}")
                        print(f"Cannot add regex: {e}")
                        sys.exit(1)
        except FileNotFoundError as e:
            print(f"check-forbidden: {args.file} does not exists. Check your '.pre-commit-config.yaml'")
            return 1

    return_code = 0
    for filename in args.filenames:
        if args and filename == args.file or filename == '.pre-commit-config.yaml':
            continue
        try:
            content = Path(filename).read_text()
            for rex in targets:
                m = rex.search(content)
                if m:
                    print(f"{filename} contains forbidden match '{rex.pattern}': `{m.group(0)}`")
                    return_code = 1
        except UnicodeDecodeError:
            pass
        except Exception as e:
            print(f"Error reading {Path(filename).absolute()}: {e}")
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(check_forbidden())
