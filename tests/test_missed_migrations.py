import tempfile
from pathlib import Path

from pch.check_missed_migrations import check_missed_migrations

MIGRATIONS_DIR = str(Path(__file__).parent / "migrations")


def test_check_ok():
    ret = check_missed_migrations([MIGRATIONS_DIR])
    assert ret == 0


def test_check_missing():
    with tempfile.NamedTemporaryFile(dir=str(MIGRATIONS_DIR), prefix="0002_", suffix=".py") as __:
        ret = check_missed_migrations([MIGRATIONS_DIR])
    assert ret == 1
