# Contributing to AgentBroko

Thank you for helping build AgentBroko. Contributions may include new skills, fixes, documentation, tests, accessibility improvements, and platform support.

## Before you start

- Search existing issues and pull requests.
- Open an issue before a large feature or architecture change.
- Never include API keys, tokens, private media, voice recordings, generated videos, or proprietary model files.
- Confirm that code and assets you contribute can be distributed under the MIT License.

## Development setup

```bash
git clone https://github.com/sajidhossain8272/agentbroko.git
cd agentbroko
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e . pytest
agentbroko skills
python -m pytest
```

Install FFmpeg and FFprobe to exercise Video Forge rendering. See `docs/INSTALL.md`.

## Pull request process

1. Create a focused branch from `main`.
2. Keep changes scoped and follow existing patterns.
3. Add or update tests and documentation.
4. Run `python -m pytest` and the relevant CLI smoke tests.
5. Update `CHANGELOG.md` under `Unreleased` for user-visible changes.
6. Open a pull request using the repository template.

Maintainers may request changes. By submitting a contribution, you agree that it is your original work or appropriately licensed and that it may be distributed under this repository's MIT License.

## Adding a skill

A skill must be local-first, documented, testable, and discoverable through `agentbroko skills`. Read `docs/ADDING_A_SKILL.md` before implementation.

## Community standards

Participation is governed by `CODE_OF_CONDUCT.md`. Report security vulnerabilities privately as described in `SECURITY.md`.

