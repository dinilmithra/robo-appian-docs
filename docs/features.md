# Feature guide

This guide describes the features present in the attached workspace source. API
reference pages render signatures from source. Examples use illustrative labels
and URLs: replace them with approved application values and expected outcomes.

## Learn and run

| Feature | Documentation |
| --- | --- |
| Install Python package and browser binaries | [Installation](getting-started/installation.md), [Browser management](guides/browser-management.md) |
| First pytest test and business flows | [Quick start](getting-started/quick-start.md), [Business flows](getting-started/ba-workflow.md) |
| Visible/headless, shell, project file, CI, VS Code | [Headless execution](guides/headless-execution.md) |
| Fresh browser lifecycle, fixture configuration, worker isolation | [Pytest integration](guides/pytest-integration.md) |
| Timeouts, environment settings, logs, performance and diagnostics | [Runtime configuration](guides/runtime-configuration.md) |

## Interact with Appian

| Feature | Documentation |
| --- | --- |
| Navigation, reload, upload, polling, processing wait, page identity | [Page API](api/appian-page.md), [Component recipes](guides/component-recipes.md) |
| Text entry and searchable suggestions | [Textbox](api/appian-textbox.md) |
| Normalized dates committed through blur | [Date](api/appian-date.md) |
| Named dropdown options and selection | [Dropdown](api/appian-dropdown.md) |
| Radio groups and checkboxes | [Radio](api/appian-radio-select.md), [Checkbox](api/appian-checkbox.md) |
| Buttons, links, tabs and menu paths | [Button](api/appian-button.md), [Link](api/appian-link.md), [Tab](api/appian-tab.md), [Menu](api/appian-menu.md) |
| Scoped dialog fields, buttons and grids | [Dialog](api/appian-dialog.md) |
| Exact/partial matching, visibility and indexed component access | [Component recipes](guides/component-recipes.md), [Locator](api/appian-locator.md) |
| Read-only text and repeated matches | [Text](api/appian-text.md) |
| Grids, matching rows, columns, cells, counts and cell components | [Grid](api/appian-grid.md), [Row](api/appian-row.md), [Column](api/appian-column.md), [Cell](api/appian-cell.md) |
| Summary/list/grid business data and value collections | [Dataset](api/appian-dataset.md), [Data values](api/appian-data.md) |
| Scoping and component extension types | [Scope](api/appian-scope.md), [Input base](api/appian-input-component.md) |

## Verify and investigate

| Feature | Documentation |
| --- | --- |
| Business expectations, condition waits and assertion helpers | [Verification and errors](guides/verification.md), [Assertions API](api/assertions.md) |
| PNG, HTML, metadata and failure evidence | [Action and failure snapshots](guides/action-snapshots.md) |
| Context/page lifecycle, measurements and correlation helpers | [Runtime API](api/runtime.md) |
| Navigation/timeout errors and structured details | [Errors](api/errors.md), [Troubleshooting](getting-started/troubleshooting.md) |

## Boundaries

Semantic components are Appian-specific. A generic non-Appian page may contain
unsupported widgets even if a recorder observes its HTML. Recording actions does
not infer business requirements or expected outcomes. Document/Jira ingestion,
automatic business-test design, a no-code test-management service, a generic web
adapter, and a public `headless` fixture override are not implemented here.

Handwritten public APIs can support operations that the recorder cannot export.
For example, file upload and explicit popup handling are public features, while
recorded popup/iframe workflows remain blocked. Grid APIs are the current table
interface; there is no `page.table` factory in this source, and historical table
parity is not asserted.
