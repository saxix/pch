
import argparse
import subprocess
import sys
from typing import Sequence


def check_run_command(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='The bash command to run.')
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    if not args.command:
        print("Error: command not specified.", file=sys.stderr)
        return 1

    return_code = 0
    for filename in args.filenames:
        try:
            subprocess.check_call([*args.command.split(), filename])
        except subprocess.CalledProcessError as e:
            print(f"Error running command on {filename}: {e}", file=sys.stderr)
            return_code = 1
    return return_code


if __name__ == '__main__':
    raise SystemExit(check_run_command())
