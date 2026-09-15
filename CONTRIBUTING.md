# Contributing

Quick workflow for contributors and agents. Keep each change small and well-tested.

## Before you start

- Open the repository root in VS Code.
- Select the desired Python interpreter (use one with Python 3.11+ recommended).
- Install recommended extensions from .vscode/extensions.json for best DX.

## Local validation

Always run these checks locally before creating a PR.

1. Run tests
   python -m unittest discover -v

2. Run the generator (optional, when touching assets or metadata)
   python generate_assets_data.py --report
   - Inspect assets-report.json for warnings or errors.

3. Lint / format (if configured in the project)
   - Python: black, isort, flake8 (optional)
   - JS: prettier / eslint (optional)

## Documentation and tasks

- When a change touches code or docs, update docs/task.md and any relevant docs in docs/ (SPECIFICATIONS.md or ARCHITECTURE.md).
- If the change affects behavior that agents rely upon, update AGENTS.md and .github/copilot-instructions.md accordingly.

## Pull Requests

- Create a concise PR description explaining what changed and why.
- Reference the task in docs/task.md if applicable.
- CI will run tests and validate generated artifacts; fix issues before requesting review.

## When tests fail

Follow the project test policy in docs/TESTING.md:

1. Re-run tests to rule out transient failures.
2. If tests are incorrect, update tests with justification.
3. If tests are correct, fix the code until tests pass.
4. Do not merge until CI shows a green status.

## Contact

For questions about architecture or policies, open an issue or contact the maintainer listed in README.md.
