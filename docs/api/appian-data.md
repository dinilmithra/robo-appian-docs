# Appian data values and collections

`AppianData` wraps a business field value. `AppianDataCollection` exposes matching
values in display order. Normal consumers obtain these from `dataset.data(...)`.

```python
status = page.dataset(header="Basic Information", row_number=1).data(field="Status")
value = status.value
first_value = status.first.value
same_first_value = status[0].value
```

Direct collection `.value` requires exactly one result. `.first` and `[0]` select
an intended first match; they are not uniqueness checks. A displayed field with
an empty value can return an empty string. Business `field_number` and row numbers
are one-based, while Python collection selection is zero-based.

::: robo_appian.appian.data.appian_data.AppianData
    options:
      members: true

::: robo_appian.appian.data.appian_data.AppianDataCollection
    options:
      members: true
