# Appian Textbox

Use `AppianPage.textbox(...)` for ordinary text entry and searchable text-entry controls. Identify a textbox by its label, placeholder, or nearby header text.

```python
textbox = page.textbox(label="Title")
textbox.fill("Example request")
```

A placeholder can be used when that is the natural identifier for the field:

```python
page.textbox(placeholder="example@example.com").fill("user@example.com")
page.textbox(header="Item Description").fill("General details")
```

`fill(value)` replaces the current text and returns the same `AppianTextbox`, so calls can be chained. For a searchable textbox, use `fill(...).select(...)` to enter search text and choose a suggestion.

```python
page.textbox("Employee").fill("John").select("John Smith")
page.textbox("Employee").fill("John").select(index=2)
```

The same operation can be expressed in one call. Suggestion `index` values are 1-based.

```python
page.textbox("Employee").select(search_text="John", value="John Smith")
page.textbox("Employee").select(search_text="John", index=2)
page.textbox(placeholder="Start typing...").select(
    search_text="Example", value="Example Result"
)
```

`select(value=None, *, search_text=None, index=None, exact=True, timeout=None)` requires exactly one of `value` or `index`:

- `value` selects a visible suggestion by displayed text. Matching is exact by default; use `exact=False` for intentional partial matching.
- `index` selects by **1-based suggestion position**. `index=1` is the first visible suggestion and `index=2` is the second.
- `search_text` optionally enters the search criteria before selecting. Omit it when `fill()` has already entered the search text.
- `timeout` is expressed in seconds. `None` uses the component/framework timeout.

`value` and `index` are mutually exclusive. Calling `select()` with neither, with both, with an index below 1, or with blank search/value text raises a clear argument error. A searchable textbox with no results raises `LookupError`; an out-of-range suggestion index raises `IndexError`. After the suggestion is selected, `select()` waits for the action to complete and returns the same textbox.

Textbox **component collection indexing remains zero-based**:

```python
page.textboxes[0].fill("John").select(index=2)
```

Here `[0]` means the first textbox on the page, while `select(index=2)` means the second suggestion.

Common operations include `fill()`, `select()`, `clear()`, `click()`, `is_visible()`, `is_enabled()`, `is_disabled()`, `value()`, and `wait_until_ready()`.

::: robo_appian.appian.components.appian_textbox.AppianTextbox
    options:
      show_root_heading: true
      members_order: source
      members:
        - fill
        - blur
        - key
        - press_key
        - press_enter
        - select
        - clear
        - click
        - is_visible
        - is_disabled
        - is_enabled
        - value
        - wait_until_ready
## Date fields

Use `page.date(...)` for Appian date fields rather than `page.textbox(...)`.

```python
page.date(label="Start Date").fill("10/07/2026")
```


## Exact matching and visibility

By default, robo-appian uses a visible component whose displayed name or label exactly matches what you provide. Keep `exact=True` and `visible=True` for normal business automation. Use `exact=False` only when you intentionally want a partial name or label match. Change `visible` only when your scenario specifically requires a component that is not currently visible.


## Timeout

`timeout` is expressed in seconds. Leave `timeout=None` to use the normal configured wait time, or provide a positive value when this particular action needs a different wait time.


## Keyboard submission and navigation

```python
page.textbox(label="Search Vendors").press_key("Enter", value="Tester-")
page.textbox(label="Search Vendors").press_enter(value="Tester-")
page.textbox(label="Search Vendors").press_key("Tab")
page.textbox(label="Search Vendors").press_key("Shift+Tab")
```

`press_key(key, *, value=None)` supports Enter, Tab, Shift+Tab, Escape, arrow keys,
Home/End and PageUp/PageDown. Omitting the value preserves the text and caret;
`value=""` clears the field. Supplying a value enters it without an intermediate
blur before pressing the key. Both Appian readiness and completion are owned by
the component. `press_enter` is a convenience wrapper. Unsupported keys raise
ValueError before interaction. Dates normalize on fill and retain focus until an explicit key or another action moves focus.


## Fluent fill and key

```python
page.textbox(label="Search Vendors").fill(value="Tester-").key(key="Enter")
page.textbox(label="Search Vendors").key(key="Tab")
```

`key(key=...)` returns the same textbox and delegates to `press_key` with no value
replacement. A preceding `fill` retains focus without blur. The key
action resolves/focuses the field and waits for Appian completion. Direct
`press_key(key, value=...)` remains available when a value must be entered without
an intermediate blur.


### Explicit input focus changes

Input fills and selections no longer force blur. Textbox/date fill returns the same
component. Tests commit dates with `.fill(value=...).blur()`; `.key(key="Tab")`
(or `Shift+Tab`) is available for explicit keyboard navigation;
normal component synchronization remains in each action. Tab also invokes keyboard
handlers and advances focus, whereas DOM blur only removes focus. Date normalization
is unchanged. Generated date fills explicitly append `.blur()`; any recorded
key remains a separate explicit navigation action. Re-export existing tests and review the changed
source before running. Custom consumer input flows that relied on implicit blur
need explicit focus-changing steps before checking validation.

Explicit date commit example:

```python
page.date(label="Start Date").fill(value="10/21/2026").blur()
```

`blur()` returns the same textbox/date component and waits for Appian processing.
It removes focus without synthesizing Tab or moving to the next control.
