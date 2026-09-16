---
name: project-review
description: Brief description of what this skill does
---

# project-review

Review the current project state, identify important issues, and provide actionable recommendations without modifying the project.

## Usage

When tests are ran successfully and before implementing a new task.

## Steps

1. Read `docs/task.md` for current and pending work.
2. Read `docs/ARCHITECTURE.md` to understand the intended structure.
3. Read `docs/SPECIFICATIONS.md` for project requirements.
4. Read `docs/TESTING.md` for verification expectations.
5. Read `docs/METRICS.md` and `docs/metrics_log.md` when evaluating project progress or performance.
6. Inspect relevant source files and configuration.
7. Compare the current implementation against documented requirements and architecture.
8. Identify:
   - Incomplete or blocked tasks
   - Architectural inconsistencies
   - Bugs or likely failure points
   - Missing tests
   - Performance or maintainability concerns
   - Documentation that is outdated or missing
9. Prioritize findings by impact and urgency.
10. Produce a concise review with evidence from the project files.
11. Do not modify files unless explicitly requested.

## Output

### Current State

Brief description of the project's current state.

### Findings

For each finding:

- **Issue**
- **Evidence**
- **Impact**
- **Recommended action**

### Next Steps

A short, prioritized list of suggested actions.
Break them down into small tasks and sort then according to the docs/task.md file.
