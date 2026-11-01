"""Check that the skill, its subagent and its evals stay loadable and consistent.

A host reads SKILL.md and agent frontmatter as YAML, so these tests parse it the same way.
They also resolve every file path the skill names: relative paths must exist in this
repository, and paths into another skill must name a companion skill the README declares.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
AGENTS = sorted((ROOT / "agents").glob("*.md"))
README = ROOT / "README.md"

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BACKTICKED = re.compile(r"`([^`\n]+)`")
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")
PATH_SUFFIXES = (".md", ".json", ".py", ".sh", ".txt", ".yaml", ".yml", ".toml")
COMPANION_PATH = re.compile(r"^~/\.claude/skills/([^/]+)/(.+)$")
VERDICTS = re.compile(r"exactly (\w+), (\w+), or (\w+)")


def split_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    assert match, f"{path.relative_to(ROOT)} has no YAML frontmatter block"
    meta = yaml.safe_load(match.group(1))
    assert isinstance(meta, dict), f"{path.relative_to(ROOT)} frontmatter is not a mapping"
    return meta, match.group(2)


def path_like(token: str) -> bool:
    return token.endswith(PATH_SUFFIXES) and " " not in token


def declared_companions() -> set[str]:
    """Skill names listed under the README's companion skills heading."""
    text = README.read_text(encoding="utf-8")
    section = re.search(r"^## Required companion skills\n(.*?)(?=^## |\Z)", text, re.DOTALL | re.MULTILINE)
    assert section, "README.md has no '## Required companion skills' section"
    return set(re.findall(r"^- `([^`]+)`", section.group(1), re.MULTILINE))


def test_repository_has_one_skill_and_one_agent() -> None:
    assert [p.name for p in SKILLS] == ["cto-filter"]
    assert [p.name for p in AGENTS] == ["communication-filter.md"]


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_frontmatter(skill: Path) -> None:
    meta, body = split_frontmatter(skill / "SKILL.md")
    assert meta.get("name") == skill.name
    assert NAME_PATTERN.match(meta["name"]) and len(meta["name"]) <= 64
    description = meta.get("description")
    assert isinstance(description, str) and description.strip()
    assert len(description) <= 1024
    assert body.strip()


@pytest.mark.parametrize("agent", AGENTS, ids=lambda p: p.stem)
def test_agent_frontmatter(agent: Path) -> None:
    meta, body = split_frontmatter(agent)
    assert meta.get("name") == agent.stem
    assert NAME_PATTERN.match(meta["name"])
    assert isinstance(meta.get("description"), str) and meta["description"].strip()
    assert isinstance(meta.get("tools"), str) and meta["tools"].strip()
    assert body.strip()


@pytest.mark.parametrize("agent", AGENTS, ids=lambda p: p.stem)
def test_agent_preloads_skills_that_ship_here(agent: Path) -> None:
    meta, _ = split_frontmatter(agent)
    preloaded = meta.get("skills")
    assert isinstance(preloaded, list) and preloaded
    for name in preloaded:
        assert (ROOT / "skills" / name / "SKILL.md").is_file(), f"{agent.name} preloads missing skill {name}"


def test_agent_and_skill_agree_on_verdict_labels() -> None:
    _, skill_body = split_frontmatter(ROOT / "skills" / "cto-filter" / "SKILL.md")
    _, agent_body = split_frontmatter(ROOT / "agents" / "communication-filter.md")
    skill_verdicts = VERDICTS.search(skill_body)
    agent_verdicts = VERDICTS.search(agent_body)
    assert skill_verdicts and agent_verdicts
    assert skill_verdicts.groups() == agent_verdicts.groups() == ("READY", "REVISE", "STOP")


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_evals_match_the_skill_creator_format(skill: Path) -> None:
    data = json.loads((skill / "evals" / "evals.json").read_text(encoding="utf-8"))
    assert data["skill_name"] == skill.name
    cases = data["evals"]
    assert isinstance(cases, list) and cases
    ids = [case["id"] for case in cases]
    assert all(isinstance(i, int) for i in ids)
    assert len(ids) == len(set(ids)), "eval ids must be unique"
    for case in cases:
        assert isinstance(case["prompt"], str) and case["prompt"].strip(), case["id"]
        assert isinstance(case["expected_output"], str) and case["expected_output"].strip(), case["id"]
        assert isinstance(case["files"], list), case["id"]
        for name in case["files"]:
            assert (skill / name).is_file(), f"eval {case['id']} names missing file {name}"
        expectations = case["expectations"]
        assert isinstance(expectations, list) and expectations, case["id"]
        assert all(isinstance(e, str) and e.strip() for e in expectations), case["id"]


def referencing_files() -> list[Path]:
    return [skill / "SKILL.md" for skill in SKILLS] + AGENTS


@pytest.mark.parametrize("source", referencing_files(), ids=lambda p: str(p.relative_to(ROOT)))
def test_named_paths_resolve(source: Path) -> None:
    _, body = split_frontmatter(source)
    companions = declared_companions()
    tokens = [t for t in BACKTICKED.findall(body) if path_like(t)]
    tokens += [t for t in MARKDOWN_LINK.findall(body) if "://" not in t and not t.startswith("#")]
    companion_files = set()
    for token in tokens:
        match = COMPANION_PATH.match(token)
        if match:
            assert match.group(1) in companions, f"{token} points into undeclared companion skill"
            companion_files.add(Path(match.group(2)).name)
    for token in tokens:
        if COMPANION_PATH.match(token):
            continue
        if "/" not in token and token in companion_files:
            continue
        assert not token.startswith(("/", "~")), f"{token} is an absolute path outside a companion skill"
        assert (source.parent / token).exists(), f"{source.relative_to(ROOT)} names missing path {token}"


def test_readme_declares_de_ai_as_companion() -> None:
    assert "de-ai" in declared_companions()


def test_no_ds_store_is_tracked() -> None:
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert not [line for line in tracked.splitlines() if Path(line).name == ".DS_Store"]


def companion_references() -> list[tuple[str, str]]:
    found = []
    for source in referencing_files():
        _, body = split_frontmatter(source)
        for token in BACKTICKED.findall(body):
            match = COMPANION_PATH.match(token)
            if match and (match.group(1), match.group(2)) not in found:
                found.append((match.group(1), match.group(2)))
    return found


@pytest.mark.parametrize(("companion", "relative"), companion_references(), ids=lambda v: v)
def test_companion_files_exist_when_installed(companion: str, relative: str) -> None:
    installed = Path.home() / ".claude" / "skills" / companion
    if not installed.is_dir():
        pytest.skip(f"companion skill {companion} is not installed at {installed}")
    assert (installed / relative).is_file(), f"{companion} no longer has {relative}"
