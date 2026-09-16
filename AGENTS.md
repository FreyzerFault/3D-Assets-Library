# AGENTS.md

## Project context

This repository is a lightweight static 3D asset library. The goal is to catalog, preview, and download `.glb` models without adding unnecessary backend complexity.

## Core principles

- Follow SDD: keep documentation, architecture, and backlog aligned.
- Prefer simple, robust, maintainable solutions over speculative architecture.
- Do small, surgical changes. Avoid broad refactors unless required.
- Preserve the static-first philosophy: no backend unless explicitly requested.
- Keep the project easy to understand by humans and by agentic tools.
- Apply SOLID principles whenever modifying code: keep responsibilities separated, dependencies clear, and behavior predictable.
- Aim for strong code organization and readability so the logic is understandable quickly by a human reviewer.

## Editing files vs running commands

- Use the file tools (`read_files`, `editor`, `search_codebase`) for every file read and edit. Do not modify files through shell commands.
- Never use shell heredocs, output redirection, or inline interpreter one-liners to write file content. They are brittle, they fail on Windows/PowerShell, and they obscure what changed.
- Use the terminal only when a real process is required: running tests, git operations, dependency installs, listing directories.
- Keep terminal commands single, short and quotable. Do not chain long sequences with `;` when a file edit would do the job.
- When verifying a change, read the file back with `read_files` instead of echoing it through the shell.
- If a shell command fails twice with the same error, stop retrying it and switch to a file tool.

## Required behavior for agents

- Prefer file and path operations relative to the project root or script location, not the execution directory.
- When touching generator logic, keep `assets.json` paths relative to the repo, not absolute filesystem paths.
- Validate changes with the smallest existing test or smoke check that covers the behavior.
- After each task is completed, update `docs/task.md` and any documentation that contains information related to the task or affected project area, so the SDD docs remain current.
- When a task is finished, move its entry from `docs/task.md` to `docs/task_archive.md` with its DoD met and verifiable evidence. Keep the active queue accurate and free of completed work.
- If behavior or requirements change, update README, docs/SPECIFICATIONS.md, docs/ARCHITECTURE.md, and docs/task.md when relevant.
- Do not add complexity, dependencies, or frameworks without a clear reason.
- Favor reproducible scripts and deterministic output.
- Run the full test suite after completing any task. If tests fail, follow this triage order before proceeding:
  1. Re-run the tests to rule out transient issues.
  2. Inspect whether the failing tests are incorrect (false positives/negatives) and fix the tests if they need correction or clarification.
  3. If tests are correct, prioritize fixing the code (bugs) until the suite passes.
  4. Only continue with new tasks after the entire test suite is passing.

  This policy ensures regressions are caught early and that agentic changes remain safe and reversible.

- After completing a task, create a descriptive git commit with a clear summary of the work completed.
- If the codebase has diverged substantially since the last meaningful commit, create one descriptive commit for the related changes or split the work into multiple commits when the edits are unrelated, keeping each commit focused and understandable.
- When tests are updated, always compute project coverage via the repository script (scripts/record_metrics.py) and append the resulting metrics entry to docs/metrics_log.md. The metrics schema and guidance live in docs/METRICS.md.
- Review and update docs/METRICS.md whenever a milestone or major hito is completed so the metrics definitions remain accurate and actionable.
- Organize code in clear sections using `#region [DESCRIPTIVE REGION NAME]` blocks when the file grows beyond a small script.
- Encapsulate logic in small, clear functions and helper scripts instead of keeping everything in one massive script.
- Use self-explanatory variable and function names; do not rely on comments to compensate for unclear naming.
- Add comments only when they clarify a non-obvious decision or requirement, and avoid redundant explanations.

## Non-goals

- Do not introduce hidden admin/auth tricks or insecure ownership checks.
- Do not add a backend or database unless explicitly required.
- Do not add large, speculative features before the basic catalog flow is stable.

## Working rules

- Keep naming and metadata consistent.
- Keep `generate_assets_data.py` resilient against duplicate or missing files.
- Keep `assets.json` valid JSON and readable.
- Keep documentation concise and aligned with the actual state of the project.

## Critical project facts

- Models live in `models/`.
- Use `models/large/` for files over 100 MB and `models/projects/` for source or Blender work files, while `models/2gb-plus/` is reserved for >2 GB assets handled outside the repo or via LFS.
- Catalog lives in `assets.json`.
- The script `generate_assets_data.py` is the maintenance entry point.
- The web UI is static and loads `assets.json` from the browser.
- The project is designed for static hosting, not for a production multi-user app.
- The SDD documentation for the project lives in `docs/`.
- When you work on architecture, check `docs/ARCHITECTURE.md`.
- When you work on metrics, check `docs/METRICS.md`.
- When you work on specifications, check `docs/SPECIFICATIONS.md`.
- When you work on testing, check `docs/TESTING.md`.
- When you work on tasks, check `docs/task.md` (active queue) and `docs/task_archive.md` (completed work).
