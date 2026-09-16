---
name: implement-task
description: Brief description of what this skill does
---

# implement-task

Implement the requested task in the project while preserving existing behavior.

## Usage

When tests are success completely and there's no review to make.

## Steps

## Objective

1. Read `docs/task.md` and identify the target task and acceptance criteria.
2. If there's no task pending, create another one from the Backlog or identify it yourself from Specifications
3. Analyze the task and rewrite it if needed, or fragment it in more tasks if too complex or risky.
4. Read `docs/architecture.md` and `docs/specifications.md` for relevant constraints.
5. Inspect the existing implementation and related tests before changing code.
6. Create a concise implementation plan.
7. Modify only the files necessary to implement the task.
8. Follow the project's existing architecture, conventions, and naming.
9. Add or update tests for the changed behavior.
10. Run the relevant tests and checks.
11. Fix failures caused by the implementation.
12. Update relevant documentation when the task changes documented behavior.
13. Report the files changed, tests run, and any remaining issues.

## Rules

- Do not rewrite unrelated code.
- Do not introduce new dependencies unless necessary and justified.
- Do not silently change requirements.
- Preserve backward compatibility unless the task explicitly requires a breaking change.
- If requirements are ambiguous or conflicting, stop and ask before making risky changes.
