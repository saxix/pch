import argparse
from pathlib import Path

from .utils import is_release, get_release, RexList
from distutils.version import LooseVersion, StrictVersion


def check_forbidden(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help="")
    parser.add_argument('-p', '--pattern', action="append")
    args = parser.parse_args(argv)

    targets = RexList(["\s%s\s" % p for p in args.pattern])
    for filename in args.filenames:
        content = Path(filename).read_text()
        for rex in targets:
            if rex.search(content):
                print(f"{filename} contains forbidden match '{rex.pattern}'")
                return 1
    return 0


if __name__ == '__main__':
    exit(check_forbidden())
