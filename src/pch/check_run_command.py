import argparse
import subprocess
import sys
from typing import Sequence

from pch.utils import safe_path


def check_run_command(argv: Sequence[str] | None = None) -> int:
    """Execute bash command."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to pass as arguments.")
    parser.add_argument("-c", "--command", help="The bash command to run.")
    args = parser.parse_args(argv)
    if not args.command:
        sys.stderr.write("Error: command not specified.]n")
        return 1
    return_code = 0
    for filename in args.filenames:
        try:
            subprocess.check_call([*args.command.split(), safe_path(filename)])  # noqa: S603
            return_code = 0
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Error running command on {filename}: {e}\n")
            return_code = 1
    return return_code


if __name__ == "__main__":
    raise SystemExit(check_run_command())
