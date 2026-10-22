# Appian dialog

Use `page.dialog(name="Edit")` or `page.dialog(text="Confirm changes")` to scope
supported actions. Names and text match exactly by default; visible dialogs are
the default search boundary.

```python
dialog = page.dialog(name="Edit")
dialog.wait_until_visible()
dialog.textbox(label="Vendor Name").fill("Example vendor")
dialog.date(label="Start Date").fill("10/18/2026")
dialog.grid(header="Vendor Details").row(row_number=1).cell(column_name="Vendor Name").textbox(label="Vendor Name").fill("Example vendor")
dialog.button(name="Submit").click()
dialog.wait_until_hidden()
```

Direct scoped factories are `button`, `textbox`, `date`, and `grid`.
`buttons[0]`/`buttons.first` and `page.dialogs[0]`/`page.dialogs.first` use zero-based
collection positions. Grid lookup waits by default; `wait=False` enables optional
checks. Grid cell components retain the owning page for synchronization.

::: robo_appian.appian.components.appian_dialog.AppianDialog
    options:
      members: true
