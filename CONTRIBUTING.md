# Contributing to appstudy

Thanks for considering a contribution. appstudy is intentionally small: a
zero-dependency Python CLI. Keep it that way.

## Ground rules

- **Zero dependencies, always.** New features must use the standard library only.
- **Clean-room only.** Never add anything that downloads code, assets, or
  anything behind a login. If a feature would weaken the clean-room rules in
  the README, it does not belong here.
- **Tests for behaviour.** Every new feature or fix ships with a test in
  `tests/`. Run the suite before opening a PR:

  ```bash
  python3 -m unittest discover -s tests -v
  ```

## How to contribute

1. Fork the repo and create a branch: `git checkout -b feature/my-change`.
2. Make focused commits with clear messages.
3. Add or update tests and docs (`docs/` for behaviour changes, README for
   user-visible changes).
4. Open a pull request using the template, describing what changed and why.

## What makes a good PR

- One concern per PR.
- Fixture HTML in `examples/sample-site/` (or a new fixture folder) rather than
  live network calls in tests — tests must pass offline.
- No placeholder or TODO code; if it is not finished, it is not merged.

## Code style

- Python 3.10+, type hints on public functions, 4-space indent.
- Keep modules single-purpose: `extract` parses, `crawler` fetches,
  `analyze` models, `report` renders, `cli` wires it together.

## Questions?

Open an issue — bug reports and feature ideas are both welcome. See
[SUPPORT.md](SUPPORT.md) for where each kind of question goes.
