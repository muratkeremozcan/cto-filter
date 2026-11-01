# Source provenance

Extracted on 2026-10-31 from the author's personal assistant repository and generalized for public use.
The contract tests under `tests/`, CI, `pyproject.toml` and `ruff.toml` are new.

## Dependencies

- The skill loads two `de-ai` reference files through `~/.claude/skills/de-ai/...`. `de-ai`
  has its own repository, `muratkeremozcan/de-ai`. The README lists it as a required companion
  skill, and a test fails if the skill names a path into a companion skill the README does not
  declare.

## License

MIT. See `LICENSE`.
