from setuptools import find_packages
from setuptools import setup


setup(
    name='pch',
    description='Extra hooks for pre-commit.',
    url='https://github.com/saxix/pre-commit-hooks',
    version='0.1',
    author='Stefano Apostolico',
    author_email='s.apostolico@gmail.com',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['cfgv', 'pre-commit', 'isort'],
    entry_points={
        'console_scripts': [
            'check-missed-migrations = pch.check_missed_migrations:check_missed_migrations',
            'check-untracked = pch.check_untracked:check_untracked',
            'check-env-template = pch.check_env_template:check_env_template',
            'check-version-release-match = pch.check_version_release_match:check_version_release_match',
            'check-forbidden = pch.check_forbidden:check_forbidden',
            'sort-imports = pch.sort_imports:sort_imports',
        ],
    },
)
