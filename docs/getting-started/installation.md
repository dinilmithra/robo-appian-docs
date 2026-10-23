# Install RoboAppian

RoboAppian is for automation engineers building tests for Appian applications.
Use RoboTest Studio if you prefer to record and review supported workflows visually.

1. Use a Python version supported by the package release you are installing.
2. Open the terminal in your test project and add the published package with Poetry.
3. Install the browser your team uses.
4. Ask your project owner for the application URL, approved data and access instructions.

```shell
poetry add robo-appian
poetry run playwright install chromium
```

Use Firefox or WebKit in place of Chromium when your project requires it.
A package installation does not grant access to your application or bypass sign-in.

Continue with [your first workflow](quick-start.md).
