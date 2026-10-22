# Appian Dropdown

Use `page.dropdown(label=...)` to select a business option from a supported Appian
dropdown. Both regular and searchable dropdowns use the same selection API.
Placeholder prompts are excluded from selection and from `options()`.

## Identify the dropdown

```python
dropdown = page.dropdown(label="Field label")
```

The field label identifies the dropdown. Option text is supplied separately to
`select(value=...)`. Keep `exact=True` and `visible=True` unless the testcase
intentionally requires different matching.

```python
page.dropdown(label="Status")
page.dropdown(label="Stat", exact=False)
page.dropdown(label="Status", visible=False)
page.dropdown(label="Status", visible=None)
page.dropdowns[0]  # Component collections use zero-based Python indexes.
```

## Parameter meanings

| Parameter | Meaning |
| --- | --- |
| `search_text` | Text to enter into a searchable dropdown's search input. |
| `value` | Displayed name of the business option to select. |
| `index` | One-based position among business options, after any search filter. |
| `exact` on `select` | Whether the option name must match exactly; defaults to `True`. |

Supply either `value` or `index`. Supply `search_text` separately when filtering.
An index never includes a placeholder prompt. Indexes refer to the available,
rendered business options, not an application's entire remote dataset.

## Select without an explicit search

```python
# Select a specific business option.
page.dropdown(label="Status").select(value="Active")

# Select the first business option.
page.dropdown(label="Status").select(index=1)

# Intentionally allow partial option-name matching.
page.dropdown(label="Status").select(value="Act", exact=False)
```

For a searchable dropdown, `select(value=...)` may use the search input to locate
that named option. The supplied `value` still means the option to select, not an
independent search query. Unchained `select(index=1)` clears a retained search
filter before selecting from the unfiltered rendered options.

## Search and select

```python
# Search and select by position in one call.
page.dropdown(label="Field label").select(search_text="02B", index=1)

# Search and select a specific option by name.
page.dropdown(label="Field label").select(
    search_text="02B", value="02B Research"
)

# Search and intentionally allow partial option-name matching.
page.dropdown(label="Field label").select(
    search_text="02B", value="Research", exact=False
)
```

Use only values approved for your application. The example names above are
illustrative; the library does not invent business expectations or choose a
replacement when a requested option is unavailable.

## Fluent search entry

```python
page.dropdown(label="Field label").fill(search_text="02B").select(index=1)

page.dropdown(label="Field label").fill(search_text="02B").select(
    value="02B Research"
)
```

`fill(search_text=...)` opens the dropdown, fills its search input, waits for
Appian processing and returns the same dropdown. It does not select a business
value or blur the control. The next selection on that instance retains the
filter. An explicit `search_text` on `select` overrides the filled filter.

After a successful selection, a later unchained `select(index=1)` returns to the
normal unfiltered behavior. Keep the returned component if separating the calls:

```python
dropdown = page.dropdown(label="Field label")
dropdown.fill(search_text="02B")
dropdown.select(index=1)
```

A newly created `page.dropdown(...)` instance does not inherit another instance's
pending search. Use the same instance or supply `search_text` directly.

## Clear the search filter

```python
page.dropdown(label="Field label").fill(search_text="").select(index=1)
page.dropdown(label="Field label").select(search_text="", index=1)
```

Clearing search resets the filter; it does not clear the selected business value.
For indexed selection, omitted, `None`, empty and whitespace-only `search_text`
use unfiltered options unless a preceding `fill(...)` on the same instance
supplies the filter. Search entry requires a dropdown with a supported search
input. Use `select(...)` directly for a regular dropdown.

## Read options and current state

```python
dropdown = page.dropdown(label="Status")

options = dropdown.options()       # Opens the list; excludes placeholder prompts.
current = dropdown.value()         # Displayed text, including a prompt if shown.
is_prompt = dropdown.is_placeholder()
is_active = dropdown.is_selected("Active")
visible = dropdown.is_visible()
enabled = dropdown.is_enabled()
disabled = dropdown.is_disabled()
```

`options()` returns the currently rendered business options, including any active
filter; it does not fetch every page of a remote option dataset. A placeholder
never satisfies `is_selected(...)`. `is_selected` reads current state rather than
waiting for a different selection to appear.

## Keyboard navigation

```python
dropdown = page.dropdown(label="Field label")
dropdown.key(key="ArrowDown")
dropdown.key(key="Enter")
dropdown.key(key="Tab")
```

`key(...)` and `press_key(...)` are equivalent and return the same dropdown.
Supported keys are `Enter`, `Tab`, `Shift+Tab`, `Escape`, `ArrowUp`, `ArrowDown`,
`ArrowLeft`, `ArrowRight`, `Home`, `End`, `PageUp` and `PageDown`. Use keyboard
navigation only when it is part of the intended scenario. The automatic
placeholder exclusion belongs to `select(...)`; raw keyboard navigation follows
the application's own behavior.

## Timeout and synchronization

```python
dropdown = page.dropdown(label="Owner", timeout=15)  # Seconds.
if dropdown.is_enabled(timeout=8):
    dropdown.select(value="Example User")
```

The component owns waits for search entry, option availability and selection
completion. Leave `timeout=None` to use the configured runtime timeout. Do not
add fixed sleeps. Filling a search or selecting an option does not force blur;
use `key(key="Tab")` when the testcase explicitly needs to advance focus.

## Grid cells

```python
page.grid(label="Items").cell(
    row_name="Item 1001", column_name="Status"
).dropdowns[0].select(value="Active")
```

Component collection indexes such as `dropdowns[0]` are zero-based. Option indexes
such as `select(index=1)` are one-based.

## Invalid calls and older calling styles

```python
# Invalid: search entry must use search_text.
dropdown.fill(value="02B")

# Invalid: choose one selection target, value OR index.
dropdown.select(value="02B", index=1)

# Invalid: search alone does not identify an option to select.
dropdown.select(search_text="02B")
```

Use `fill(search_text="02B")` to search without selecting, or
`select(search_text="02B", index=1)` to search and select. The former
`select(value="02B", index=1)` search shorthand is not supported.

Existing positional aliases remain available: `select("Active")`, `select(1)`
and `select(index="1")`. Prefer named arguments in new business flows.

## API reference

::: robo_appian.appian.components.appian_dropdown.AppianDropdown
    options:
      show_root_heading: true
      members_order: source
      members:
        - wait_until_visible
        - is_visible
        - is_disabled
        - is_enabled
        - value
        - is_placeholder
        - is_selected
        - options
        - fill
        - select
        - key
        - press_key
