# Verify business outcomes

Decide what must be true after an action before you run the test.

| Scenario | Useful check |
| --- | --- |
| Submit a form | The required confirmation and resulting state are shown. |
| Leave a required field empty | The approved validation message appears and submission is blocked. |
| Update a record | The intended record shows the approved new values. |
| Filter a grid | The required records are present and displayed values match the filter. |
| Use a restricted role | Access matches the approved permission requirement. |

These are examples of test design, not promises about your application.
Use your requirements to decide the actual expected messages and values.

Review failures with [evidence](action-snapshots.md). A screenshot supports investigation;
it does not replace an explicit expected-result check.
