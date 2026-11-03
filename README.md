# cto-filter

A `cto-filter` skill that reviews workplace messages, documents, decks and emails before they
are sent, plus a `communication-filter` subagent that preloads it. The skill scores an artifact
against core communication gates, adds executive cold-read gates for leadership audiences, runs
the `de-ai` voice pass and returns a READY, REVISE or STOP verdict with a sendable rewrite.

- `skills/cto-filter/SKILL.md`: the skill.
- `skills/cto-filter/evals/evals.json`: behavioral eval cases in the skill-creator format.
- `agents/communication-filter.md`: a read-only Claude Code subagent that preloads the skill
  through its `skills:` frontmatter. Install it beside the skill, or it loads without the gates.
- `docs/source-provenance.md`: where the skill came from.

## Required companion skills

- `de-ai`: the voice layer. The skill loads `~/.claude/skills/de-ai/references/ai-tells.md`
  and `~/.claude/skills/de-ai/references/murat-voice.md` by absolute path, so `de-ai` must be
  installed at `~/.claude/skills/de-ai`. It lives in its own repository,
  `muratkeremozcan/de-ai`.
  For technical prose, it also loads `~/.claude/skills/de-ai/references/technical-writing.md`.
  Update the companion checkout with this change.

## Install

Clone this repository, then symlink `skills/cto-filter` into each skill discovery directory,
such as `~/.claude/skills/`, and `agents/communication-filter.md` into `~/.claude/agents/`.
Linking to the checkout keeps the installed skill current with every `git pull`.

## Tests

```bash
uv run pytest
```

The tests parse SKILL.md and agent frontmatter as YAML, check that names match their
directory or file, that the agent preloads a skill that ships here, that the skill and agent
use the same verdict labels, that `evals/evals.json` has every field the skill-creator eval
format needs, that every relative path the skill and agent name exists in this repository,
and that every path into another skill names a companion declared above. When a companion is
installed at `~/.claude/skills/<name>`, the tests also check that the referenced file exists
there; CI has no companions installed and skips that check.
