import sys


def pytest_configure():
    sys.path.append('tests/data')
    sys.path.append('src')
