# Source provenance

Extracted on 2026-10-31 from the author's personal assistant repository and generalized for public use.
The contract tests under `tests/`, CI, `pyproject.toml` and `ruff.toml` are new.

## Dependencies

- The skill loads the `de-ai` voice references and its technical-writing reference through `~/.claude/skills/de-ai/...`. `de-ai`
  has its own repository, `muratkeremozcan/de-ai`. The README lists it as a required companion
  skill, and a test fails if the skill names a path into a companion skill the README does not
  declare.

On 2026-11-03, the technical clarity integration was added after comparing Lauren Tan's Unslop and technical-writing skills with `de-ai`.
The comparison, pinned upstream sources, and adoption decisions live in [de-ai's comparison](https://github.com/muratkeremozcan/de-ai/blob/main/docs/upstream-comparison.md).
The filter also checks that voice edits preserve conditions, completion states, ownership, uncertainty, and the requested decision.

## License

MIT. See `LICENSE`.
