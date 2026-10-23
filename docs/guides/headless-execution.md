# Choose a visible or headless run

Use a visible browser while checking a new workflow. Use headless execution when
you want the test to run without a visible browser window.

| Project setting | Effect |
| --- | --- |
| `HEAD_LESS=N` | Visible execution; the library default. |
| `HEAD_LESS=Y` | Execution without a visible browser window. |
| `WAIT_TIME` | Maximum wait for supported operations, in seconds; default 90. |

Set these values in your test project's supported environment configuration before
starting the run. Project-specific settings may override the library default.
Changing an environment file does not update a browser that is already running.

Headless runs still need a suitable viewport. If a navigation control only appears
in a wide layout, ask your project owner to configure an appropriate execution size.

See the [runtime user guide](https://dinilmithra.github.io/robo-automation-docs/).
