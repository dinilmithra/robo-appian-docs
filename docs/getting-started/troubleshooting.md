# Troubleshooting

| Problem | What to do |
| --- | --- |
| Control cannot be found | Confirm the current page, visible label, permissions and correct component type. |
| Test opens a warning or sign-in page | Complete the approved entry flow for the new browser session. Direct navigation does not bypass authentication. |
| Menu is missing | Check window size, permissions and the required parent menu. |
| Several controls have the same label | Identify the intended dialog, grid or business record and ask your automation team to refine the target. |
| Search result is wrong | Check the entered search text separately from the selected option. |
| Date change is not applied | Call `blur()` immediately after filling the date; do not use Tab to commit it. |
| Grid row changes between runs | Use a unique business value where available; review sorting, filters and paging. |
| Browser is invisible | Check the project's execution setting for headless mode. |
| No evidence is available | Check capture settings and selected formats before another run. |
| Timeout | Check entry steps and labels first; increase the wait only for genuine application slowness. |

Share the testcase name, failed step, expected result, error message and available
evidence with your automation support team. Remove secrets before sharing.
