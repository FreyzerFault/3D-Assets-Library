---
name: test-and-verify
description: Brief description of what this skill does
---

# test-and-verify

Verify that the current implementation works correctly and that recent changes have not introduced regressions.

## Usage

When big changes are made or a milestone is completed.

## Steps

1. Read `docs/testing.md` to identify the project's testing and verification procedures.
2. Inspect the relevant implementation and recent changes.
3. Identify the tests and checks relevant to the current task.
4. Run the smallest relevant test set first.
5. Run broader checks when appropriate.
6. Analyze every failure and determine whether it is caused by the current implementation.
7. Fix implementation issues when the cause is clear and within scope.
8. Re-run failed tests after each fix.
9. Confirm that the final test results are clean or clearly document unavoidable failures.
10. Report:

- Tests and checks executed
- Results
- Fixes made
- Remaining failures or risks

## Rules

- Do not modify tests merely to make them pass unless the test itself is demonstrably incorrect.
- Do not ignore failing tests.
- Do not make unrelated refactors while fixing verification failures.
