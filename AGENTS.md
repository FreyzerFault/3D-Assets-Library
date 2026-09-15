# AGENTS.md

## Project context
This repository is a lightweight static 3D asset library. The goal is to catalog, preview, and download `.glb` models without adding unnecessary backend complexity.

## Core principles
- Follow SDD: keep documentation, architecture, and backlog aligned.
- Prefer simple, robust, maintainable solutions over speculative architecture.
- Do small, surgical changes. Avoid broad refactors unless required.
- Preserve the static-first philosophy: no backend unless explicitly requested.
- Keep the project easy to understand by humans and by agentic tools.

## Required behavior for agents
- Prefer file and path operations relative to the project root or script location, not the execution directory.
- When touching generator logic, keep `assets.json` paths relative to the repo, not absolute filesystem paths.
- Validate changes with the smallest existing test or smoke check that covers the behavior.
- If behavior or requirements change, update README, SPECIFICATIONS.md, ARCHITECTURE.md, and task.md when relevant.
- Do not add complexity, dependencies, or frameworks without a clear reason.
- Favor reproducible scripts and deterministic output.

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
