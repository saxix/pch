import argparse
import os
import sys

from .utils import is_release, get_release
from distutils.version import LooseVersion, StrictVersion


def check_version_release_match(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', help="")
    parser.add_argument('--pythonpath', default='.', help="")
    parser.add_argument('--version-attr', default='__version__', help="")
    parser.add_argument('--releases', default='release', help="")
    parser.add_argument('--loose', action='store_true',
                        help="use LooseVersion instead of StrictVersion")
    parser.add_argument('--string', action='store_true',
                        help="use string comparision")
    args = parser.parse_args(argv)

    if args.string:
        Version = str
    elif args.loose:
        Version = LooseVersion
    else:
        Version = StrictVersion

    if is_release(args.releases):
        sys.path.append(os.path.abspath(args.pythonpath))
        pkg = __import__(args.package)
        try:
            pkg_version = Version(getattr(pkg, args.version_attr))
        except ValueError as e:
            print(f"Package {args.package} has an invalid version number: {e}")
            return 1
        try:
            release = Version(get_release())
        except ValueError as e:
            print(f"Branch has an invalid version number: {e}")
            return 1

        if release != pkg_version:
            print("Package version '{}' and branch name '{}' do not match".format(pkg_version,
                                                                                  release))
            return 1
    return 1


if __name__ == '__main__':
    exit(check_version_release_match())
