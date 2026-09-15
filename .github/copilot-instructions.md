# Copilot instructions

## Project intent
This repo is a static 3D asset library. The objective is to catalog, preview, and download `.glb` models with minimal operational complexity.

## Rules
- Follow Spec-Driven Development: keep specs, architecture, and backlog aligned.
- Prefer surgical edits over broad refactors.
- Do not add backend/database complexity unless explicitly required.
- Keep paths relative to the project or script, never dependent on the caller's working directory.
- Preserve static hosting compatibility.
- Update documentation when behavior changes.
- Keep tests minimal but meaningful; validate the changed behavior.
- Keep metadata and naming consistent.
- Avoid hidden admin/auth patterns or insecure shortcuts.

## Important project facts
- `models/` contains the raw 3D files.
- `assets.json` is the catalog consumed by the web app.
- `generate_assets_data.py` is the catalog maintenance script.
- The UI is a static HTML page; keep it lightweight and resilient.
- Prefer simplicity and maintainability over speculative features.
