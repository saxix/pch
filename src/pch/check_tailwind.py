import argparse
import fnmatch
import sys
from pathlib import Path
from typing import Sequence

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pch.utils import Color, is_git_tracked


def check_tailwind(argv: Sequence[str] | None = None) -> int:
    """Check django-tailwind produced production css instead of development version."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="")
    parser.add_argument("-d", "--output-dir", action="store")
    parser.add_argument("-l", "--lines", action="store", default=2, type=int)
    parser.add_argument("-i", "--ignore", action="store", default=None, type=str)
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Verbosity level.")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, help="Quiet mode.")

    args = parser.parse_args(argv)
    base = Path.cwd()

    if args.quiet:
        args.verbosity = -1

    return_code = 0
    for filename in args.filenames:
        if args.ignore and fnmatch.fnmatch(Path(filename).name, args.ignore):
            continue
        dest = base / Path(args.output_dir) / Path(filename).with_suffix(".css").name
        chunk_size = 1024
        out_msg = None
        if dest.exists():
            with dest.open("rb") as f:
                count = 0
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    count += chunk.count(b"\n")
                if count > args.lines:
                    out_msg = (f"{Color.RED + Color.BOLD}{dest.relative_to(base)}: "
                               f"does not look like a production file.{Color.NORMAL}\n")
                    return_code = 1
            if not is_git_tracked(dest):
                out_msg = f"{Color.YELLOW1 + Color.BOLD}{dest.relative_to(base)}: is not git tracked.{Color.NORMAL}\n"
                return_code = 1
            if args.verbosity >= 1  and not out_msg:
                out_msg = f"{filename} {Color.GREEN}Ok{Color.NORMAL} \n"
        else:
            out_msg = f"{Color.RED + Color.BOLD}{dest.relative_to(base)}: not found.{Color.NORMAL}\n"
            return_code = 1
        if args.verbosity >= 0 and out_msg:
            sys.stdout.write(out_msg)

    return return_code


if __name__ == "__main__":
    raise SystemExit(check_tailwind())
