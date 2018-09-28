import argparse
import os

from isort import isort


def imports_incorrect(filename):
    return isort.SortImports(filename, check=True, show_diff=False).incorrectly_sorted


def sort_imports(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument('--check-only', action='store_true', dest='check_only', default=False)
    parser.add_argument('--diff', action='store_true', dest='show_diff', default=False)
    args = parser.parse_args(argv)

    return_value = 0

    for filename in args.filenames:
        if imports_incorrect(filename):
            return_value = 1
            if not args.check_only:
                isort.SortImports(filename)
                print(f"FIXED: {os.path.abspath(filename)}")
    return return_value


if __name__ == '__main__':
    exit(main())
