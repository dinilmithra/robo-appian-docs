# Component recipes

Use public RoboAppian components in application code. Components own readiness,
Appian rerender handling and action synchronization. Do not add fixed sleeps or
raw browser selectors to business flows.

## Match the business control

Most factories default to `exact=True` and `visible=True`. Use `exact=False` only
for intentional partial matching; use `visible=None` when attachment rather than
visible state is relevant. Factory signatures differ: inspect the API page before
passing a label, name, placeholder or header. Explicit component timeouts are in
seconds; the workspace default wait is 90 seconds.

```python
page.textbox(label="Description").fill("Example vendor")
page.textbox(placeholder="Search").fill("Example")
page.textbox(label="Description").clear()
page.textbox(label="Employee").select(search_text="Alex", value="Alex Example")
page.dropdown(label="Status").select(value="Active")
page.radio(label="Priority").select("High")
page.checkbox(label="Acknowledgement").check()
page.checkbox(label="Acknowledgement").uncheck()
page.checkbox(label="Acknowledgement").set_checked(True)
```

A searchable textbox selection is distinct from filling its search text. Record
both the search and intended selected option. Dropdowns expose `options`, `value`,
`is_selected(value)`, visibility and enabled state. Do not assume native HTML
select elements are equivalent to Appian dropdowns.

## Dates

```python
from robo_appian import AppianDate

page.date(label="Start Date").fill("2026-10-18")
page.date(label="End Date").fill("")
assert AppianDate.normalize("2026-10-18") == "10/18/2026"
```

Date fill normalizes recognized values and commits through blur/focus-out. No Tab
or additional key press is needed. Unknown date strings are retained rather than
validated as business dates; requirements must define valid dates and relationships.
Clearing a date is an intentional action and must be reviewed as such.

## Buttons, links, tabs and menus

```python
page.button(name="Submit").click()
page.link(name="Catalog").click()
page.tab(name="Details").select()
page.menu(name="User options").menu(name="Sign Out").click(opens_new_page=False)
choices = page.menu(name="User options").options()
```

Build menu paths by chaining `menu(...)`. `menu(index=1)` uses a one-based option
index; use names when stable. `click(opens_new_page=True)` returns the new AppianPage
and requires a popup. `False` returns the current page and does not wait for a popup;
it does not change the application's configured link target.

```python
other = page.menu(name="Applications").menu(name="Workspace").click(opens_new_page=True)
assert not page.same_page(other)
assert page.same_context(other)
```

## Dialogs and collections

```python
dialog = page.dialog(name="Edit")
dialog.wait_until_visible()
dialog.textbox(label="Vendor Name").fill("Example vendor")
dialog.date(label="Start Date").fill("10/18/2026")
dialog.button(name="Submit").click()
dialog.wait_until_hidden()
```

Direct dialog factories currently cover button, textbox, date and grid. Do not
assume dialog dropdown/link/text factories exist. Grids inside dialogs expose
supported cell components normally.

Page collections include `buttons`, `textboxes`, `dropdowns`, `checkboxes`, `radios`,
`links`, `tabs`, `dates`, `grids`, and `dialogs`. Cells provide corresponding
component collections and dialogs provide `buttons`. Component collection indexing
is zero-based, nonnegative, and exposes `.first`:

```python
page.buttons[0].is_visible()
page.dialogs.first.wait_until_visible()
```

A positional choice is appropriate only when the display order is intentional.
Use semantic names for important actions whenever possible.

## Grids and rows

```python
vendors = page.grid(header="Manage Vendors")
row = vendors.row(name="30000", exact=True, unique=True)
row.cell(column_name="Edit").button(name="EDIT").click()
count = vendors.row_count()
keyed = vendors.row_matching(column_name="Vendor #", value="30000")
value = keyed.cell(column_name="Vendor Name").text()
```

`row(name=...)` matches row text; `row_matching(...)` matches an exact value in an
exact named column. `unique=True` requires one grid and one matching row.
`row_matching` always requires uniqueness. Neither automatically searches other
pages. `row_count()` counts rendered data rows, excluding the header and recognized
empty placeholders. It is not the server total.

```python
vendors.row(row_number=1).cell(column_number=2).text()
vendors.column(name="Vendor Name").cell(row_number=1).text()
optional = page.grid(header="Optional Results", wait=False)
if optional.is_visible():
    print(optional.row_count())
```

Business row and column numbers are one-based. Grid factories wait by default;
use `wait=False` for immediate optional-grid checks. Rows and row cells have their
own readiness waits with `wait=False` and `timeout` options. A visible grid does
not imply a requested record has appeared. Scope duplicate controls by row and
column rather than clicking the first matching label on the page.

## Datasets and read-only data

```python
status = page.dataset(header="Basic Information", row_number=1).data(field="Status").value
activity = page.dataset(header="Recent Activities", row_number=1)
action = activity.data(field="Action").value
message = page.text("Request submitted successfully").value
```

Datasets cover detail/summary fields, repeated lists and grids. `data(field=...)`
returns a collection; direct `.value` requires exactly one item. Use `.first` or
`[0]` for an intentional collection selection. `field_number` and `row_number`
are one-based; Python collection indexes are zero-based. See the dataset guide
for field/row/column filters and duplicate-match behavior.

## Navigation, upload and explicit waits

```python
page.goto("https://your-appian-site.example/suite/sites/app")
page.reload()
page.upload("data/attachment.pdf", label="Attachment")
page.wait_for_appian_action_completed(timeout=90)
page.wait_until(
    lambda: page.textbox(label="Vendor Name").value == "Example vendor",
    timeout=90,
    message="Saved vendor name did not match the expected value.",
)
```

Upload accepts one path or a sequence, checks files exist, sets the upload control
and waits for Appian processing. It does not supply a separate business Submit.
Page navigation delegates to the framework's navigation behavior. Use `new_page`,
`open_pages`, `same_page`, and `same_context` for explicit page management through
the Appian boundary. Advanced attribute/ID lookups exist but should be maintained
in reusable mappings rather than author-written business steps.
