# Pytest integration

Installed `robo-appian` and `robo-automation` expose their pytest plugins through
package entry points. Pytest discovers the installed plugins automatically.
Refresh editable installs after entry-point changes; use `pytest --trace-config`
to inspect plugin discovery.

## Public fixtures

| Fixture | Purpose |
| --- | --- |
| `page` | Public AppianPage for normal tests |
| `appian_page` | AppianPage before a consumer's optional page policy override |
| `appian_runtime` | Appian context/page creation, measurements and resource helpers |
| `wait_time` | Configured timeout in seconds, default 90 |
| `context_options` | Per-test context settings; empty by default |
| `context_page_handler` | Optional callback for newly created generic pages |
| `storage_state` | Compatibility input, defaults to None; fresh-session projects must not override it with reusable authentication |
| `robo_runtime_config` and configuration-group fixtures | Generic runtime policy; see runtime configuration |

```python
from robo_appian import AppianPage

def test_example(page: AppianPage):
    page.goto("https://your-appian-site.example/")
    page.text("Dashboard").wait_until_visible()
```

## Fresh browser per testcase

In the consumer project's `pytest.ini`:

```ini
[pytest]
robo_browser_scope = function
robo_env_file = .env
testpaths = tests
```

`robo_browser_scope` accepts `function` or `session`. The library default is
`session`; use `function` for a fresh browser per testcase. Driver, browser and Appian runtime
lifetimes follow this setting. Context and page fixtures remain per-test and
library cleanup closes resources. The `.env` setting is opt-in and supported by
the current workspace library. See [Runtime configuration](runtime-configuration.md).

## Application authentication policy

Direct URL navigation does not bypass security banners or SSO. The recorder
consumer currently has no automatic authentication hook; generated steps must
include supported landing actions or another consumer policy must establish the
required application state. No manual playback sign-in pause is implemented.

For an application that has approved public Login/Logout flows, override `page`
in that consumer's own `conftest.py`. The following is an integration template;
`Login` and `Logout` must be supplied by the application:

```python
import pytest
from application import Login, Logout

@pytest.fixture
def page(appian_page):
    authenticated = False
    try:
        Login.sign_in(appian_page)
        authenticated = True
        yield appian_page
    finally:
        if authenticated:
            Logout.sign_out(appian_page)
```

Use the actual method names of the application's hooks. Logout belongs in cleanup;
the lower-layer fixtures still close pages, contexts and browsers if setup or logout
fails. Preserve the original test failure when designing reporting and cleanup.
Do not cache cookies or authentication state when fresh authentication is required.
Application flows must use public RoboAppian interactions, not direct Playwright APIs.

## Parallel workers

pytest-xdist is optional and is not provisioned by the recorder itself. If installed,
run `poetry run pytest -n 2` and ensure test data and server-side actions are suitable
for concurrent execution. Assign credentials per worker through consumer policy;
do not force workers to share a saved authenticated context. Application Login/Logout
and data cleanup must remain worker-aware. Correlation logs and evidence retain
worker and attempt identifiers.

## Fixture overrides

An application may override `wait_time`, `context_options`, and supported runtime
configuration fixtures before their dependents are created. For example:

```python
import pytest

@pytest.fixture(scope="session")
def wait_time():
    return 90

@pytest.fixture
def context_options():
    return {"viewport": {"width": 1440, "height": 900}}
```

Keep session-dependent inputs compatible with a session browser. Override policy
rather than replacing generic lifecycle ownership. A dedicated `headless` fixture
is proposed but **not implemented**; use `.env` or process environment today.
See [Headless execution](headless-execution.md). Some environment-backed operations
read `WAIT_TIME` directly; keep the project setting aligned with timeout overrides.

## Run and diagnose

```powershell
poetry run pytest .\tests\generated\test_scenario_01.py -v -s
poetry run pytest --trace-config
poetry run pytest --fixtures -q
```

Use the consumer's interpreter in VS Code. Avoid registering a second copy of an
already-discovered plugin. See [Troubleshooting](../getting-started/troubleshooting.md)
for editable installation, SSO, stale generated tests and export blockers.
