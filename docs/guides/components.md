# Choose and use components

Choose the component that matches how the application control behaves.

| Control | How to use it reliably |
| --- | --- |
| Textbox | Identify its field label, enter the required value, then send Enter or Tab only when the workflow needs it. |
| Date | Fill the date and immediately call `blur()` to commit it before checking the result. |
| Dropdown | Select an actual option. Placeholder prompts such as “Select a Value” are not selected business values. |
| Search dropdown | Enter the search text, wait for choices and select the intended result. Keep search text separate from the choice you expect. |
| Button or link | Use the visible name and confirm whether it opens a new page. |
| Menu | Follow its parent-to-child path, such as Admin Controls → Reference Management. |
| Tab | `select()` waits for the selected marker; separately verify the required tab content. |
| Checkbox or radio | Specify the intended selection and check the result. |
| Dialog | Confirm the intended dialog is open before using its supported controls. |
| Grid | Choose the correct grid, row and column before using a cell control. |
| Dataset | Identify the intended record and verify its required values. |

For grids, prefer a unique business row value and a clear column name. Use positions
when names cannot uniquely identify a cell. Position-based choices need review when
sorting, filtering or paging changes. Check duplicate values before approving a target.

Allow component actions to finish. Increasing the timeout can help a slow page,
but does not resolve a wrong label, missing permission or unexpected page.

Tab selection confirms the tab's selected state, not the readiness of every control
in its content. Use an explicit business-content check after selection. For a tab
selected by another action, `wait_until_selected()` waits without clicking again.

## Wait for a dialog to close

Keep the dialog reference before clicking the action that closes it:

```python
dialog = page.dialog(name="Confirm request")
dialog.button(name="Confirm").click()
dialog.wait_until_closed(timeout=90)
```

The wait completes when the matching dialog is hidden or removed. It does not
click a close button. A still-visible dialog raises an error after the timeout,
which is in seconds. Omit the argument to use the dialog/framework default.
Verify the expected business result separately after the dialog closes.

If the dialog may already be closed when you obtain the reference, avoid the
constructor's initial visibility wait:

```python
page.dialog(name="Confirm request", visible=None).wait_until_closed()
```

Use a unique name or text to identify the intended dialog. The live locator follows
rerenders; an unnamed wait covers all matching dialogs.
