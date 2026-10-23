# Choose and use components

Choose the component that matches how the application control behaves.

| Control | How to use it reliably |
| --- | --- |
| Textbox | Identify its field label, enter the required value, then send Enter or Tab only when the workflow needs it. |
| Date | Enter the required date and explicitly move focus away to commit it before checking the result. |
| Dropdown | Select an actual option. Placeholder prompts such as “Select a Value” are not selected business values. |
| Search dropdown | Enter the search text, wait for choices and select the intended result. Keep search text separate from the choice you expect. |
| Button or link | Use the visible name and confirm whether it opens a new page. |
| Menu | Follow its parent-to-child path, such as Admin Controls → Reference Management. |
| Tab | Choose its visible title and check the content after switching. |
| Checkbox or radio | Specify the intended selection and check the result. |
| Dialog | Confirm the intended dialog is open before using its supported controls. |
| Grid | Choose the correct grid, row and column before using a cell control. |
| Dataset | Identify the intended record and verify its required values. |

For grids, prefer a unique business row value and a clear column name. Use positions
when names cannot uniquely identify a cell. Position-based choices need review when
sorting, filtering or paging changes. Check duplicate values before approving a target.

Allow component actions to finish. Increasing the timeout can help a slow page,
but does not resolve a wrong label, missing permission or unexpected page.
