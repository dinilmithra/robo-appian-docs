# Headless and visible browser execution

RoboAppian pytest tests use `robo-automation` to launch browsers. In this workspace,
the default is **visible**: `HEAD_LESS=N`. Use `HEAD_LESS=Y` for headless tests.
This setting applies when a new browser is created; changing it after launch does
not change an existing browser.

| Setting | Result |
| --- | --- |
| Unset or blank | Visible browser, using the library default |
| `HEAD_LESS=N` or `HEAD_LESS=false` | Visible browser |
| `HEAD_LESS=Y` or `HEAD_LESS=true` | Headless browser |

Use `Y` and `N` consistently in project configuration.

## Project environment file

In the consumer project, create `.env`:

```dotenv
HEAD_LESS=N
WAIT_TIME=90
```

Load this file with the following setting in `pytest.ini`:

```ini
[pytest]
robo_env_file = .env
```

Retain any other existing pytest settings. The path is relative to the pytest root.
This requires the workspace version of `robo-automation` with `robo_env_file` support;
older installed distributions may not recognize it. Other projects do not load
`.env` automatically unless configured or their own startup code loads it.

The loader accepts simple KEY=VALUE entries, optional surrounding quotes and
full-line `#` comments. It does not execute shell commands or support inline
comments. A missing explicitly configured file is a configuration error.

Set `HEAD_LESS=Y` in the file to run headless, then run the test normally:

```powershell
poetry run pytest .\tests\generated\test_vendor_date_01.py -v -s
```

## PowerShell override

From the consumer project's directory:

```powershell
# Run headless.
$env:HEAD_LESS = "Y"
poetry run pytest .\tests\generated\test_vendor_date_01.py -v -s

# Run with a visible browser.
$env:HEAD_LESS = "N"
poetry run pytest .\tests\generated\test_vendor_date_01.py -v -s

# Remove the shell override; the next pytest process uses .env or library defaults.
Remove-Item Env:HEAD_LESS -ErrorAction SilentlyContinue
```

These variables apply to the current shell and child processes.

## Bash override

For one pytest invocation:

```bash
HEAD_LESS=Y poetry run pytest tests/generated/test_vendor_date_01.py -v -s
HEAD_LESS=N poetry run pytest tests/generated/test_vendor_date_01.py -v -s
```

For the current shell and subsequent child processes:

```bash
export HEAD_LESS=Y
poetry run pytest tests/generated/test_vendor_date_01.py -v -s
unset HEAD_LESS
```

The same environment-variable approach works in CI: set `HEAD_LESS=Y` in the
runner environment before starting pytest. A visible browser requires a display
on the machine executing the tests.

## Configuration precedence

For the current implementation, the first available value wins:

1. Existing process environment, including shell or CI variables.
2. The explicitly configured project `.env` file.
3. Library default: `HEAD_LESS=N`.

A shell value of `Y` therefore overrides `N` in `.env`. Remove the shell variable
to return control to the file.

## VS Code test explorer

Select your test project's interpreter, for example `.venv/Scripts/python.exe`.
Use `robo_env_file = .env` in `pytest.ini` to load the environment file for both
test explorer and terminal pytest runs.

An environment variable inherited by VS Code takes precedence over `.env`.
Changing a variable in an integrated terminal does not update the environment of
an already-running VS Code test process. Remove stale inherited values and restart
VS Code when needed.

## Fixture override: proposed enhancement

A dedicated public `headless` fixture is **not implemented**. Defining a fixture
with that name currently does not configure the library's browser lifecycle.
Use the environment methods above today.

The recommended future design is a session-scoped library `headless` fixture,
requested explicitly by browser creation. A consumer override would take precedence
over the shell, project file and library default. A compatible scope must support
both session and per-test browser lifetimes. Environment changes inside a test
are too late after browser creation, and an autouse fixture alone does not establish
an explicit dependency on the browser fixture.

## Recorder versus test execution

`robo-appian recorder record`, `review`, and `demo` always launch a visible browser
for interaction. `HEAD_LESS` controls generated pytest execution, not the interactive
recorder. `--start-recording` controls when capture starts; it does not change
browser visibility. The recorder has no `--headless` option.

Headless mode does not bypass SSO. Each fresh session must still complete the
application's required security banner and authentication steps.

## Check the effective setting

Browser-launch logs include `headless=False` or `headless=True`. The presence of
pytest test output alone does not tell you whether the browser is visible.

From the consumer project, inspect the active environment and imported library:

```powershell
poetry run python -c "import os; import robo_automation.browser as b; print('HEAD_LESS:', os.getenv('HEAD_LESS')); print('Library:', b.__file__)"
```

This diagnostic runs outside pytest, so it shows the shell value and does not load
the pytest-configured `.env` file. `HEAD_LESS: None` can therefore be normal.

When using workspace source changes, install the sibling library as editable:

```powershell
poetry add --editable ..\robo-automation
```

The import path should then point into the workspace's `robo-automation` project.
An older site-packages installation can have different defaults even when its
version number matches, because workspace versions are not changed for these fixes.
