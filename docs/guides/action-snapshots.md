# Action and Failure Snapshots

Snapshots provide visual evidence of what happened while an automation test was running. They are useful when reviewing test results or investigating a failure.

Configure snapshot capture using:

```text
CAPTURE_ACTION_SNAPSHOTS=N
ENABLE_FAILURE_SNAPSHOT=Y
CAPTURE_FAILURE_HTML_SNAPSHOT=Y
CAPTURE_FAILURE_IMAGE_SNAPSHOT=Y
CAPTURE_FAILURE_JSON_SNAPSHOT=Y
CAPTURE_EXECUTION_HTML_SNAPSHOT=Y
CAPTURE_EXECUTION_IMAGE_SNAPSHOT=Y
CAPTURE_EXECUTION_JSON_SNAPSHOT=Y
SNAPSHOT_FULL_PAGE=N
ARTIFACTS_ROOT=artifacts
EXECUTION_SNAPSHOT_PATH=${ARTIFACTS_ROOT}/snapshots
```

| Setting | Purpose |
| --- | --- |
| `CAPTURE_ACTION_SNAPSHOTS` | Enable normal after-only snapshots for supported automation actions. |
| `ENABLE_FAILURE_SNAPSHOT` | Capture screenshot evidence when a test fails. |
| `CAPTURE_FAILURE_HTML_SNAPSHOT` | HTML for enabled failure evidence |
| `CAPTURE_FAILURE_IMAGE_SNAPSHOT` | PNGs for enabled failure evidence |
| `CAPTURE_FAILURE_JSON_SNAPSHOT` | JSON metadata for enabled failure evidence |
| `CAPTURE_EXECUTION_HTML_SNAPSHOT` | Include live HTML DOM; default `Y`. Set `N` to skip HTML files. |
| `SNAPSHOT_FULL_PAGE` | Capture the full page instead of only the visible area. |
| `EXECUTION_SNAPSHOT_PATH` | Folder where snapshot evidence is stored. The standard project setting is `${ARTIFACTS_ROOT}/snapshots`. |

## Recommended configuration

For normal automation execution, failure snapshots provide useful evidence without capturing screenshots for every action:

```text
CAPTURE_ACTION_SNAPSHOTS=N
ENABLE_FAILURE_SNAPSHOT=Y
CAPTURE_FAILURE_HTML_SNAPSHOT=Y
CAPTURE_FAILURE_IMAGE_SNAPSHOT=Y
CAPTURE_FAILURE_JSON_SNAPSHOT=Y
CAPTURE_EXECUTION_HTML_SNAPSHOT=Y
CAPTURE_EXECUTION_IMAGE_SNAPSHOT=Y
CAPTURE_EXECUTION_JSON_SNAPSHOT=Y
SNAPSHOT_FULL_PAGE=N
ARTIFACTS_ROOT=artifacts
EXECUTION_SNAPSHOT_PATH=${ARTIFACTS_ROOT}/snapshots
```

Enable action snapshots when additional evidence is useful while developing or troubleshooting a test:

```text
CAPTURE_ACTION_SNAPSHOTS=Y
```

## Snapshot files

Snapshot evidence is stored under `EXECUTION_SNAPSHOT_PATH` and organized by evidence type:

```text
${EXECUTION_SNAPSHOT_PATH}/
├── screenshots/
├── html/
└── metadata/
```

Action PNGs follow `CAPTURE_EXECUTION_IMAGE_SNAPSHOT`; failure PNGs follow
`CAPTURE_FAILURE_IMAGE_SNAPSHOT`.
HTML can separately be disabled using `CAPTURE_EXECUTION_HTML_SNAPSHOT=N`; JSON metadata
for action evidence follows `CAPTURE_EXECUTION_JSON_SNAPSHOT`. Failure JSON follows `CAPTURE_FAILURE_JSON_SNAPSHOT`. The
`screenshots/` directory is created only when images are enabled; existing PNG
files from earlier runs are not deleted by this setting.

`CAPTURE_EXECUTION_HTML_SNAPSHOT` defaults to `Y`. Disabling HTML keeps PNG images
and enabled JSON metadata. Existing artifacts are not deleted by format settings.

## Exact configuration names

PNG images are controlled by `CAPTURE_EXECUTION_IMAGE_SNAPSHOT`. HTML is controlled
separately by `CAPTURE_EXECUTION_HTML_SNAPSHOT`. See [Runtime configuration](runtime-configuration.md) for source-backed
defaults and [Verification](verification.md) for business assertions.

## Execution capture modes

`ENABLE_EXECUTION_SNAPSHOT=Y` enables normal after-only action capture.
`ENABLE_EXECUTION_BEFORE_AFTER_SNAPSHOT=Y` independently enables both phases,
even if the normal switch is `N`. With both enabled, each phase is captured once.
Disable both switches to turn execution action evidence off. Failure evidence
remains independently controlled by `ENABLE_FAILURE_SNAPSHOT`.

HTML, PNG and JSON formats use their corresponding `CAPTURE_EXECUTION_*` flags.
Failure formats use `CAPTURE_FAILURE_*`. Supported execution/failure requests
share the unified evidence service to avoid duplicate captures for the same event.
Evidence collection is diagnostic and must not replace the business failure.

Recording-time capture belongs to RoboTest Studio; see its
[evidence guide](https://dinilmithra.github.io/robo-test-studio-docs/evidence/).
