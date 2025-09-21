# pch


[![Pypi](https://badge.fury.io/py/pch.svg)](https://badge.fury.io/py/pch)
[![coverage](https://codecov.io/github/saxix/pch/coverage.svg?branch=develop)](https://codecov.io/github/saxix/pch?branch=develop)
[![Test](https://github.com/saxix/pch/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/pch/actions/workflows/test.yml)

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/saxix/pre-commit
        rev: v1.4.0  # Use the ref you want to point at
        hooks:
        -   id: check-untracked
        # -   id: ...


### Hooks available

- `check-untracked` - Prevent missing files in commit

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: <tag>
      hooks:
      -   id: check-untracked
  ```

- `check-missed-migrations` - As `check-untracked` but specific for Django migrations

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: <tag>
      hooks:
      -   id: check-missed-migrations
  ```

- `check-forbidden` - Check files for forbidden patterns

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: <tag>
      hooks:
      -   id: check-forbidden
          args: ["--pattern", "/import pdb/i"]
  ```

- `check-bash-command` - Run a bash command on files.

  Example:
  ```yaml
  - repo: local
    hooks:
      - id: check-run-command
        name: check-run-command
        entry: check-run-command
        language: python
        pass_filenames: true
        files: \.py$
        exclude: ^setup\.py$
        args: [ "pylint" ]
  ```


### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pch`

### Exampled in .pre-commit-hooks.yaml
