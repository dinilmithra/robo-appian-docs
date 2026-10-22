# Verification, assertions and errors

An action records what the test does. A verification records the business outcome
that must be true. A successful click alone does not confirm a successful save.
Use the approved requirement to choose an expected value; observed values are
proposals until a reviewer approves them.

## Verify with semantic components

```python
from robo_appian import AppianPage

def test_vendor_status(page: AppianPage):
    page.goto("https://your-appian-site.example/suite/sites/app")
    page.wait_until(
        lambda: page.dataset(header="Basic Information", row_number=1)
                    .data(field="Status").value == "Approved",
        timeout=90,
        message="The request did not reach its approved expected status.",
    )
```

`page.wait_until` polls a callable immediately and then until it succeeds or its
seconds-based timeout expires. It retries transient assertion/lookup errors handled
by the public implementation. Components already synchronize actions; use a
condition wait for an eventual business outcome, not a fixed sleep.

Visibility/enabled/selected methods return state; calling them without asserting
or waiting does not necessarily fail a test. For an immediate condition, use
`assert component.is_visible()`. For an expected transition, use the component's
`wait_until_visible` where present, or `page.wait_until`.

## Public locator assertion helpers

`assert_text`, `assert_not_text`, `assert_visible`, `wait_visible` and `wait_hidden`
are exported through `robo_appian`. They operate on locator-compatible objects.
Their low-level timeout parameters and forwarded expectation kwargs use the
underlying browser units (milliseconds); do not confuse them with component
factory timeouts and `page.wait_until`, which use seconds. Most test workflows
should prefer semantic components and business values.

See [Assertions API](../api/assertions.md) for signatures. Do not pass an arbitrary
component wrapper to a locator assertion without checking its supported interface.

## Recorded verification types

| Clicked target in Add verification mode | Recorded assertion |
| --- | --- |
| Supported textbox, date or dropdown | `assert_value` |
| Grid cell text | `assert_text` |
| Supported button, link or menu | `assert_visible` |
| A distinct text outcome | `assert_visible` on semantic text |

Verification mode consumes the click; it checks the target rather than activating
its normal action. The captured assertion is appended to the step list. Select an
outcome appropriate at that point in the workflow. A final result assertion cannot
stand in for an intermediate error dialog that has already been dismissed.

The recorder does not currently export checkbox/radio state assertions or arbitrary
negative assertions. Use approved handwritten public API checks for those cases.

## Errors and evidence

`RoboAppianError` carries a message, optional `code` and `details`. Specialized
public classes include `RoboAppianNavigationError` and `RoboAppianTimeoutError`.
Some component readiness failures propagate an assertion from the underlying
expectation; not every component failure is wrapped in one error class. Preserve
failure evidence and the original traceback rather than treating all failures as
a business validation success.

See [Error API](../api/errors.md), [Snapshots](action-snapshots.md) and
[Troubleshooting](../getting-started/troubleshooting.md).
