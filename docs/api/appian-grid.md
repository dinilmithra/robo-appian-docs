# Appian Grid

Use `page.grid(...)` to work with rows and cells in an Appian grid. The factory
waits for the matching grid before returning it, so callers can use it directly.

```python
items = page.grid(label="Items")
```

A grid can be identified by `label`, `header`, `row_name`, or `column_name`. Additional identifiers can narrow the match.

`label` matches only the grid's own accessible name. `header` matches
either a region's accessible name or header text, without requiring a heading
role. Header text can appear in a heading, nested span, paragraph, strong text,
or table caption. Text outside the grid resolves through its nearest
table-containing ancestor; a caption resolves to its own table. Ordinary cell
text is not treated as a header. A grid matched by both region and text paths
is returned only once:

```python
details = page.grid(header="Item Details")
```

## Count the displayed rows

```python
count = page.grid(label="Items").row_count()
```

`row_count()` returns the number of data rows currently displayed. It does not count the header and does not return the total number of records across other pages.

## Work with a row

Rows can be identified by visible text or by a one-based row number.
`row()` waits for the selected data row to become visible before returning it.
Appian's “No items available” placeholder is excluded from row selection.
The default timeout is inherited from the grid (or browser/context when unset).
Use `row(..., timeout=90)` to override it in seconds, or `row(..., wait=False)`
for a live optional-row lookup without waiting. With `visible=False` or
`visible=None`, row readiness waits for attachment rather than visibility.
A visible table alone does not guarantee that a requested data row exists:


```python
items = page.grid(label="Items")

row = items.row(name="Item 1001")
row.click()
```

## Work with a cell

`row(...).cell(...)` also waits for the selected cell to become visible before
returning it. The chain therefore waits for the data row, then the cell;
component actions such as `.link(...).click()` retain their own action waits.
Cell lookup supports `timeout` in seconds and `wait=False` as well.
Hidden/unfiltered cells wait for attachment.

A cell can be found directly from the grid:

```python
cell = items.cell(
    row_name="Item 1001",
    column_name="Status",
)
```

Names and one-based numbers can be mixed:

```python
items.cell(row_name="Item 1001", column_number=3)
items.cell(row_number=1, column_name="Status")
items.cell(row_number=1, column_number=3)
```

You can also start from a row or column:

```python
items.row(name="Item 1001").cell(column_name="Owner")
items.column(name="Status").cell(row_name="Item 1001")
```

## Use components inside a cell

Cells expose the same Appian component style used elsewhere:

```python
items.cell(
    row_name="Item 1001",
    column_name="Action",
).buttons[0].click()

items.cell(
    row_name="Item 1001",
    column_name="Status",
).dropdowns[0].select(value="Active")
```

## Matching options

`exact=True` and `visible=True` are the defaults. Use `exact=False` for an intentional partial match and `visible=None` when visibility should not filter the result.

```python
page.grid(label="Items", exact=False)
page.grid(label="Items", visible=None)
```

Check whether a matching grid is visible now:

```python
items = page.grid(label="Items", wait=False)
if items.is_visible():
    print("Items grid is visible")
```

`is_visible()` itself returns immediately. Use `wait=False` on the factory to
probe an optional grid without waiting. By default `page.grid()` already waits.

The default `visible=True` waits for a visible table. `visible=False` waits for
an attached hidden table, and `visible=None` waits for an attached table with
either visibility. A missing table never counts as a ready hidden grid.

Timeout values are in seconds. The grid uses the supplied `timeout`, or the
configured browser/context timeout when omitted. This
waits for the grid, not for a particular row to be added.

You can explicitly wait on a previously obtained component after a UI transition:

```python
items = page.grid(label="Items", wait=False)
items.wait_until_ready()
items.wait_until_visible(timeout=8)
```

## API

::: robo_appian.appian.data.appian_grid.AppianGrid
    options:
      show_root_heading: true
      members_order: source
      members:
        - is_visible
        - wait_until_visible
        - wait_until_ready
        - cell
        - appian_column
        - row
        - row_matching
        - column
        - row_count

## Unique row selection

Use `row(name="30000", exact=True, unique=True)` to require exactly one matching
row in one grid. Use `row_matching(column_name="Vendor #", value="30000")` when
the identifier must match a specific named column. This exact key-column lookup
always requires uniqueness. Neither searches unrendered pages or silently selects
the first duplicate. Named/numbered column and row selection, visibility filters,
timeouts, row counting and cell components remain supported.
