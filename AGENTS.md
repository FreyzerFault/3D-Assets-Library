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

## Required behavior for agents

- Prefer file and path operations relative to the project root or script location, not the execution directory.
- When touching generator logic, keep `assets.json` paths relative to the repo, not absolute filesystem paths.
- Validate changes with the smallest existing test or smoke check that covers the behavior.
- After each task is completed, update `docs/task.md` and any documentation that contains information related to the task or affected project area, so the SDD docs remain current.
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
- Catalog lives in `assets.json`.
- The script `generate_assets_data.py` is the maintenance entry point.
- The web UI is static and loads `assets.json` from the browser.
- The project is designed for static hosting, not for a production multi-user app.
- The SDD documentation for the project lives in `docs/`.
