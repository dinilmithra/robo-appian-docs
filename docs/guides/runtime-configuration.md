# Runtime configuration, logs and evidence

RoboAppian delegates generic browser lifecycle and infrastructure to
`robo-automation`. Application interactions use public RoboAppian APIs. This page
describes the current workspace defaults; use [Headless execution](headless-execution.md)
for environment precedence and project `.env` loading.

## Browser and test lifecycle

| Setting | Default | Meaning |
| --- | --- | --- |
| `HEAD_LESS` | `N` | Visible pytest browser; `Y` runs headless |
| `BROWSER` | `chromium` | Browser engine: chromium, firefox or webkit |
| `WAIT_TIME` | `90` | Generic component timeout in seconds |
| pytest `robo_browser_scope` | `session` | Library browser/driver scope; use `function` for a fresh browser per testcase |
| pytest `robo_env_file` | Empty | Opt-in simple environment file relative to pytest root |
| `ENABLE_BROWSER_LAUNCH_DELAY` | `N` | Opt-in launch-slot throttling; unrelated to component synchronization |
| `BROWSER_LAUNCH_INTERVAL_SECONDS` | `0` | Launch-slot interval when throttling is enabled |
| `CACHE_PATH` | `artifacts/runtime/cache` | Launch coordination files when throttling is enabled |

Set `robo_browser_scope=function` for a fresh browser per testcase. Contexts and pages have per-test
lifetimes even when another consumer retains the session-scoped browser default.
Appian runtime follows the configured browser scope. No authentication state is
saved by default. Changing headless settings after launch cannot affect the
already-created browser.

Component factory and `page.wait_until` timeout overrides use seconds. Low-level
locator assertion helpers forward browser milliseconds. A consumer can override
`wait_time`; environment-backed operations may still resolve `WAIT_TIME` directly,
so keep the project setting aligned rather than assuming one fixture replaces
every configuration reader.

## Typed configuration fixtures

Supported configuration fixtures include `robo_runtime_config`, `robo_logging_config`,
`robo_diagnostics_config`, `robo_performance_config`, `robo_snapshot_config` and
`robo_artifact_paths`. These allow policy overrides before dependent services are
created. Runtime configuration groups cover logging, artifacts, diagnostics,
performance, snapshots and timeouts. It does not contain a browser `headless`
field. A public `headless` fixture remains proposed, not implemented.

Ordinary tests should request `page` and `wait_time`. Advanced consumers can request
`appian_runtime`, which exposes context/page creation and measurement through the
Appian boundary. Do not close library-owned resources inside a business testcase.

## Artifact paths

| Setting | Default |
| --- | --- |
| `ARTIFACTS_ROOT` | `artifacts` |
| `PYTEST_PARALLEL_LOG_PATH` | `artifacts/logs/worker` |
| `TESTCASE_LOG_PATH` | `artifacts/logs/testcases` |
| `PERF_MONITOR_PATH` | `artifacts/logs/performance` |
| `BROWSER_DIAGNOSTICS_PATH` | `artifacts/browser-actions` |
| `EXECUTION_SNAPSHOT_PATH` | `artifacts/snapshots` |

Relative paths resolve under the consumer pytest root. Path settings support
`${VAR}` references; missing, blank or cyclic referenced values cause an error.
Changing `ARTIFACTS_ROOT` alone does not rewrite every default subpath: set the
individual path variables when moving all evidence together. For example, define
`ARTIFACTS_ROOT=artifacts` before using `EXECUTION_SNAPSHOT_PATH=${ARTIFACTS_ROOT}/snapshots`.

## Logging

| Setting | Default |
| --- | --- |
| `PYTEST_LOG_LEVEL` | `INFO` |
| `PYTEST_LOG_CLI_LEVEL`, `PYTEST_LOG_CLI_FORMAT`, `PYTEST_LOG_CLI_DATE_FORMAT` | Unset |
| `PYTEST_PARALLEL_LOG_TO_FILE` | `N` |
| `TESTCASE_LOG_ENABLED` | `Y` |

Logs correlate worker, testcase, process and attempt information. Testcase IDs
and per-attempt process IDs help match logs, performance and snapshots. Public
Appian helpers include `current_automation_context`, `automation_context_for`,
`automation_test_case_id` and `automation_test_log_path`; see [Runtime API](../api/runtime.md).
Browser launch logs include the effective headless setting. Test collection output
alone cannot identify headless execution.

## Performance

| Setting | Default |
| --- | --- |
| `PERF_MONITOR_ENABLED` | `Y` |
| `PERF_MONITOR_ACTIONS` | `Y` |
| `PERF_MONITOR_FRAMEWORK` | `Y` |
| `PERF_MONITOR_CONSOLE` | `N` |
| `PERF_MONITOR_INTERVAL` | `1.0` seconds |
| `PERF_MONITOR_FLUSH_EVERY` | `20` |
| `PERF_MONITOR_THRESHOLD_MS` | `500.0` |
| `PERF_MONITOR_SLOW_MS` | `2000.0` |
| `PERF_MONITOR_SUMMARY_LIMIT` | `50` |
| `PERF_MONITOR_RUN_ID` | `run-unknown`; controller may assign one for parallel monitoring |

Performance instrumentation measures supported actions and framework operations.
AppianRuntime exposes `measure` and `record_duration` for application flow timing.
Monitoring is diagnostic; thresholds are not business expectations or substitutes
for assertions.

## Browser diagnostics

`ENABLE_BROWSER_DIAGNOSTICS=N` disables diagnostics by default. When enabled,
`BROWSER_DIAGNOSTICS_CONSOLE`, `BROWSER_DIAGNOSTICS_PAGE_ERRORS`,
`BROWSER_DIAGNOSTICS_NETWORK` and `BROWSER_DIAGNOSTICS_NAVIGATION` each default to
`Y`. Their output uses `BROWSER_DIAGNOSTICS_PATH`. Diagnostics describe browser
activity; they are separate from snapshots and business acceptance checks.

## Execution snapshot policy

| Setting | Default | Purpose |
| --- | --- | --- |
| `ENABLE_EXECUTION_SNAPSHOT` | `N` | Normal after-only execution evidence |
| `ENABLE_EXECUTION_BEFORE_AFTER_SNAPSHOT` | `N` | Independently enable both phases |
| `CAPTURE_EXECUTION_HTML_SNAPSHOT` | `Y` | HTML format |
| `CAPTURE_EXECUTION_IMAGE_SNAPSHOT` | `Y` | PNG format for enabled execution capture |
| `CAPTURE_EXECUTION_JSON_SNAPSHOT` | `Y` | JSON metadata format |
| `ENABLE_FAILURE_SNAPSHOT` | `Y` | Independent failure evidence |
| `CAPTURE_FAILURE_HTML_SNAPSHOT` | `Y` | Failure HTML |
| `CAPTURE_FAILURE_IMAGE_SNAPSHOT` | `Y` | Failure PNG |
| `CAPTURE_FAILURE_JSON_SNAPSHOT` | `Y` | Failure metadata |

Explicit canonical settings take precedence over legacy aliases. The paired
execution switch overrides the normal switch when enabled. Format flags remain
independent. Both execution switches disabled means no execution action capture;
it does not disable failure evidence. See [snapshots](action-snapshots.md).

Recording UI settings and recording-time snapshots are documented in
[RoboTest Studio](https://dinilmithra.github.io/robo-test-studio-docs/).
Application credentials, workflow policy, test data and reports belong to the
consumer suite.
