# Releasing

Maintainers should release from a clean, reviewed commit.

1. Update versions in `pyproject.toml`, `package.json`, and package `__init__.py` files.
2. Move relevant changelog entries from `Unreleased` into a dated release.
3. Run tests and CLI smoke checks on supported platforms.
4. Run `npm pack --dry-run --cache .npm-cache` and inspect the file list.
5. Tag the release and publish GitHub release notes.
6. Publish packages using short-lived granular credentials or trusted publishing.

Never paste tokens into issues, commits, logs, chat, or command history. Revoke any exposed token immediately.

