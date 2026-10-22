# Appian column

Use `grid.column(name="Status")` or `grid.column(column_number=3)` to resolve a
column, then find a cell by row name or one-based row number. `appian_column` is
also available on the grid.

```python
column = page.grid(header="Manage Vendors").column(name="Vendor Name")
value = column.cell(row_name="30000").text()
```

Named matching is exact by default. Column numbers are one-based and refer to
rendered structure. See [Grid](appian-grid.md) for row-oriented and direct-cell alternatives.

::: robo_appian.appian.data.appian_column.AppianColumn
    options:
      members: true
