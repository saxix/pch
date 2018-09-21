import argparse

from .utils import is_release, get_release


def check_version_release_match(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', help="")
    parser.add_argument('--version-attr', default='__version__', help="")
    parser.add_argument('--releases', default='release', help="")
    args = parser.parse_args(argv)

    if is_release(args.releases):
        pkg = __import__(args.package)
        pkg_version = getattr(pkg, args.version_attr)
        release = get_release()
        if int(release != pkg_version):
            print("Package version '{}' and branch nane '{}' do not match".format(pkg_version,
                                                                              release))
            return 1
    return 0


if __name__ == '__main__':
    exit(check_version_release_match())
