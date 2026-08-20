# Adding an AgentBroko skill

1. Create a focused Python package under `src/` with a `main(argv)` CLI entrypoint.
2. Register the skill name and description in `src/agentbroko/cli.py`.
3. Route remaining arguments without hiding exit codes or errors.
4. Add tests and skill documentation.
5. Add required tools and licenses to `docs/TECH_STACK.md` and `docs/CREDITS.md`.
6. Update README, changelog, privacy, and terms when behavior or data handling changes.

Skills must work without mandatory paid APIs, avoid telemetry and secret collection, use explicit local paths, and clearly disclose any optional network behavior. Never auto-download executables or models without user confirmation.

