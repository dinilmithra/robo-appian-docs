# Command-Line Interface

The `appian` executable is supplied by the separately installed
`robo-test-studio` package. The component library supplies no console entry point.

## Component-only browser installation

Install browsers without the authoring library:

```text
python -m playwright install
python -m playwright install chromium
```

## `record`

Record using the separately installed RoboTest Studio authoring library:

```text
appian record --url "https://your-appian-host/suite/sites/your-site" --output recordings/request-01 --start-recording
```

Run `appian record --help` for recording options. Omit `--start-recording`
to open paused and start capture manually. `--channel chrome` or
`--channel msedge` selects an installed browser channel.
The command entry point and all recording logic are implemented in Studio.
Install Studio in the same environment through Poetry before using this command.
All authoring and UI commands use the same `appian` executable.

## Recording lifecycle commands

All commands are implemented by RoboTest Studio in the same environment. Their
options and validation are implemented only in Studio.

```text
appian review recordings/request-01/recording.json
appian validate recordings/request-01/recording.json
appian generate recordings/request-01/recording.json --output tests/generated/test_request_01.py
appian demo --output recordings/demo-01
```

Use `robo-appian COMMAND --help` for the selected command's options.
Launch the visual interface with `appian ui`.
