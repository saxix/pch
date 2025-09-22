# pch


[![Pypi](https://badge.fury.io/py/pch.svg)](https://badge.fury.io/py/pch)
[![coverage](https://codecov.io/github/saxix/pch/coverage.svg?branch=develop)](https://codecov.io/github/saxix/pch?branch=develop)
[![Test](https://github.com/saxix/pch/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/pch/actions/workflows/test.yml)

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit

### Usage

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/saxix/pch
    rev: v1.4.0
    hooks:
    -   id: check-untracked
    # -   id: ...
```

### Hooks available

- `check-untracked` - Prevent missing files in commit.
  This hook will check if there are any files that are not tracked by git and will fail the commit if there are any.
  It's useful to prevent forgetting to add new files to the commit.

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-untracked
  ```

- `check-missed-migrations` - As `check-untracked` but specific for Django migrations.
  This hook will check if there are any new migrations that are not tracked by git and will fail the commit if there are any.
  It's useful to prevent forgetting to add new migrations to the commit.

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-missed-migrations
  ```

- `check-forbidden` - Check files for forbidden patterns

  Example with a single pattern:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-forbidden
          args: ["--pattern", "/import pdb/i"]
  ```

  Example with a `ini` file:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-forbidden
          args: ["--ini", "forbidden.ini"]
  ```

  Example with multiple patterns:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-forbidden
          args: ["--pattern", "/import pdb/i", "--pattern", "/console.log/i"]
  ```

- `check-run-command` - Run a bash command on files.

  Run `pylint` on all python files:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-run-command
          name: Run pylint
          files: \.py$
          exclude: ^setup\.py$
          args: [ "pylint" ]
  ```

  Run multiple commands:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-run-command
          name: Run mypy and ruff
          files: \.py$
          exclude: ^setup\.py$
          args: [ "mypy", "&&", "ruff" ]
  ```

- `check-minimized` - Check if a javascript file has the minimized version added to git.

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      hooks:
      -   id: check-minimized
          files: (\.js)$
          args:
          - -i
          - "*.min.js"

    ```

- `check-tailwind` - Check if tailwind css has been compiled for production.

  Example:
  ```yaml
  -   repo: https://github.com/saxix/pch
      rev: v1.4.0
      files: src/app/theme/static_src/src/styles.scss
      hooks:
      -   id: check-tailwind
          args: ["--output-file", "path/to/your/tailwind.css"]
  ```

### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pch`
