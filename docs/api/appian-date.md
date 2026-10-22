# Appian Date

Use `AppianPage.date(...)` for Appian date fields. A date can be identified by its label, placeholder, or nearby header text.

```python
page.date(label="Start Date").fill(value="10/07/2026").blur()
```

```python
page.date(placeholder="mm/dd/yyyy").fill(value="10/07/2026").blur()
```

```python
page.date(header="Start Date").fill(value="10/07/2026").blur()
```

`AppianDate.fill()` normalizes the value, retains focus and returns the same date component. The testcase explicitly uses `.blur()` to remove focus and commit dates that validate on focus-out. Tab remains an optional keyboard navigation action. Neither `fill()` nor `fill_locator()` forces blur. Key actions wait for Appian processing.

::: robo_appian.appian.components.appian_date.AppianDate
    options:
      show_root_heading: true
      members_order: source
      members:
        - normalize
        - fill
        - blur
        - key
        - press_key
        - fill_locator

## Exact matching and visibility

By default, robo-appian uses a visible component whose displayed name or label exactly matches what you provide. Keep `exact=True` and `visible=True` for normal business automation. Use `exact=False` only when you intentionally want a partial name or label match. Change `visible` only when your scenario specifically requires a component that is not currently visible.


## Timeout

`timeout` is expressed in seconds. Leave `timeout=None` to use the normal configured wait time, or provide a positive value when this particular action needs a different wait time.


## Explicit keyboard navigation

`page.date(label="Start Date").press_key("Tab")` reproduces an observed
navigation action. When a value is supplied, it is normalized and entered without
blur before the key. Use `.blur()` to remove focus without pressing a key, or Tab for keyboard navigation.

The inherited `page.date(label="Start Date").key(key="Tab")` alias also reproduces explicit navigation. Date fill returns the same date instance and never implicitly blurs.

Explicit date commit example:

```python
page.date(label="Start Date").fill(value="10/21/2026").blur()
```

`blur()` returns the same textbox/date component and waits for Appian processing.
It removes focus without synthesizing Tab or moving to the next control.
