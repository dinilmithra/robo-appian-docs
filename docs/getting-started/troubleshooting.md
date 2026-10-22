# Troubleshooting

Start from what you see in the failure.

## A field cannot be found

Check the text visible on the page.

```python
page.textbox(label="Description")
```

If the application label changed, update the automation to use the current label.

For radio questions, use the complete question text whenever possible:

```python
page.radio(
    label="Who owns this item?"
).select("For myself")
```

## A date is filled but Appian does not react

Use `page.date(...)` rather than a normal textbox:

```python
page.date(label="Start Date").fill("10/15/2026")
```

Focus-out is automatic. Do not add Tab just to trigger Appian validation.

## A radio option is not selected

Confirm both the full question and the visible choice text. Avoid searching globally for common values such as `Yes` or `No`.

## A button is found but cannot be clicked

Check whether the application currently shows the button as enabled. Appian button state is based on the native `disabled` state.

## The test times out

A timeout does not always mean the timeout value is too small. First check:

1. Is the expected page actually open?
2. Is the visible label text still correct?
3. Did the previous action finish successfully?
4. Is the control enabled/visible?

Increase a timeout only when the evidence shows that the application is genuinely slow.

## Another element intercepts pointer events

This means The browser found the target but another visible element is receiving the click. For supported Appian radio controls, `robo-appian` handles the associated label interaction internally. If you see this elsewhere, inspect the current UI rather than forcing the click immediately.

## Need more detail?

The consumer project may collect logs, screenshots, HTML and browser diagnostics. Use those artifacts to see the actual page state at the time of failure.

## Recorder and generated-test diagnosis

| Symptom | Check and resolution |
| --- | --- |
| Add and approve at least one explicit verification | Add verification while recording; click the intended outcome, pause, review and approve the new assertion. Approving actions alone is insufficient. |
| Step requires exact-content approval | Review changed values/mappings and approve again; changed entry URLs also invalidate approvals. |
| Semantic target is ambiguous | Resolve dialog/grid/row/column scope or re-record; do not simply clear the ambiguity flag. |
| Calendar UI needs owning date field | Re-record with the current recorder so the target is a named date field, or enter the date in that field. |
| SETTINGS missing; snapshot shows Security Warning | Fresh playback is at SSO. Capture supported landing actions using --start-recording; credentials/MFA still require consumer handling. |
| Review opens at entry page without executing | Expected: review is not replay. Navigate manually while paused. |
| New steps appear after the old workflow | Review appends. There is no insert/reorder feature; make a fresh recording for intermediate replacements. |
| Python generator refuses overwrite | Choose a new output filename; existing generated tests do not update automatically. |
| Browser invisible despite project setting | Check shell/VS Code inherited HEAD_LESS and the imported library path; see Headless execution. |
| Old behavior after editable install | Installing editable links to current local files; it does not copy new fixes into an old source checkout. Update source and restart browser/VS Code. |
| Windows recording save Access denied | Close file-locking programs; preserve the previous JSON and reported recovery temporary file. |
| Test passes mapping validation but fails at runtime | Structural validation cannot prove current UI state, data or expected business behavior. Inspect failure evidence and exact targets. |

See [Semantic recorder](../guides/recorder.md), [Headless execution](../guides/headless-execution.md),
and [Runtime configuration](../guides/runtime-configuration.md).

### Settings is present but a button assertion times out

Inspect the actual failure-page HTML before assuming authentication failed. Appian
navigation may render `<button>` without `type="button"`, alongside hidden duplicate
navigation markup. The updated native button component accepts omitted type and
filters visibility before choosing a match. Update the editable RoboAppian source
and rerun; the generated `page.button(name="SETTINGS")` call does not need
to change. If evidence instead shows SSO, resolve authentication separately.
