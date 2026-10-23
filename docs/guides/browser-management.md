# Browser Management

`robo-appian` depends on the browser automation runtime and provides a platform-independent command for provisioning framework-managed browser binaries.

## Install all browsers

```bash
python -m playwright install
```

Equivalent explicit form:

```bash
python -m playwright install
```

## Install one browser

```bash
python -m playwright install firefox
python -m playwright install chromium
python -m playwright install webkit
```

Internally, the command runs the equivalent of:

```text
<current-python> -m playwright install [browser]
```

It does not rely on a platform-specific `playwright` executable being on `PATH`.

## Runtime browser selection

Browser installation and browser execution are separate decisions.

The generic lifecycle selects a browser from the automation configuration. The common setting is:

```text
BROWSER=firefox
```

Supported browser engine names are:

- `chromium`
- `firefox`
- `webkit`

If no value is configured, the generic lifecycle defaults to Chromium.

For a visible local browser session:

```text
HEAD_LESS=false
```

## CI guidance

Install the browser during environment/bootstrap setup, not inside individual tests. For example:

```bash
pip install robo-appian
python -m playwright install firefox
pytest
```

On Linux, the selected browser may also require operating-system libraries provided by the runner/container image.

## Headless and visible tests

Pytest defaults to a visible browser (`HEAD_LESS=N`). Set `HEAD_LESS=Y` to run
headless. See [Headless execution](headless-execution.md) for `.env`, shell, CI,
VS Code, precedence and fixture guidance. Interactive recorder browsers stay visible.
