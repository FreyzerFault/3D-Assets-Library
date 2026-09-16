# Implement Task

## Objective

Implement the requested task in the project while preserving existing behavior.

## Workflow

1. Read `docs/task.md` and identify the target task and acceptance criteria.
2. Read `docs/architecture.md` and `docs/specifications.md` for relevant constraints.
3. Inspect the existing implementation and related tests before changing code.
4. Create a concise implementation plan.
5. Modify only the files necessary to implement the task.
6. Follow the project's existing architecture, conventions, and naming.
7. Add or update tests for the changed behavior.
8. Run the relevant tests and checks.
9. Fix failures caused by the implementation.
10. Update relevant documentation when the task changes documented behavior.
11. Report the files changed, tests run, and any remaining issues.

## Rules

- Do not rewrite unrelated code.
- Do not introduce new dependencies unless necessary and justified.
- Do not silently change requirements.
- Preserve backward compatibility unless the task explicitly requires a breaking change.
- If requirements are ambiguous or conflicting, stop and ask before making risky changes.
