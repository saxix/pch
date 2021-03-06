pch
===

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
- `check-missed-migrations` - As `check-untracked` but spcific for Django migrations
- `check-env-template` - Check any entry in `.env` is pesent in `env.tpl`
    - Useful to keep in the source repository a template 
    for your `.env`     
- `check-forbidden` - Check filses for forbidden patterns
- `sort-imports` - Sort python imports using [isort](https://github.com/timothycrosley/isort)


### As a standalone package

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pch`
