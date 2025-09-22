import argparse
import sys
from pathlib import Path
from typing import Sequence

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pch.utils import Color, is_git_tracked


def check_tailwind(argv: Sequence[str] | None = None) -> int:
    """Check django-tailwind produced production css instead of development version."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="")
    parser.add_argument("-o", "--output-file", action="store")
    parser.add_argument("-l", "--lines", action="store", default=2, type=int)
    args = parser.parse_args(argv)
    base = Path.cwd()

    return_code = 0
    dest = base / Path(args.output_file)
    chunk_size = 1024
    if dest.exists():
        with dest.open("rb") as f:
            count = 0
            for chunk in iter(lambda: f.read(chunk_size), b""):
                count += chunk.count(b"\n")
            if count > args.lines:
                sys.stdout.write(
                        f"{Color.RED + Color.BOLD}{dest.relative_to(base)}: "
                        f"does not look like a production file.{Color.NORMAL}\n"
                    )
                return_code = 1
        if not is_git_tracked(dest):
            sys.stdout.write(f"{Color.RED + Color.BOLD}{dest.relative_to(base)}: is not git tracked.{Color.NORMAL}\n")
            return_code = 1

    else:
        sys.stdout.write(f"{Color.RED + Color.BOLD}{dest.relative_to(base)}: not found.{Color.NORMAL}\n")
        return_code = 1

    return return_code


if __name__ == "__main__":
    raise SystemExit(check_tailwind())
