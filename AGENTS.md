# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **content + packaging project**, not a deployable app. It is a Chinese
writing "Agent Skill" / Codex plugin (`no-ai-slop-cn`). There is **no web server, database, or
long-running service** — nothing listens on a port.

### Services / how to run

The only runnable program is the plugin build/validation script (Python 3.12 stdlib only, no
third-party dependencies):

- Validate only (no artifacts kept): `python3 scripts/build_plugin.py --check`
- Full build (writes `dist/no-ai-slop-cn-plugin-<version>.zip`): `python3 scripts/build_plugin.py`

`dist/` is gitignored. This build script is exactly what CI runs (see
`.github/workflows/plugin.yml`), so a green `python3 scripts/build_plugin.py` locally means CI
should pass.

### Lint / test / build

- There is no separate linter and no automated test runner (`pytest` etc.). The build script IS
  the test suite: it validates the plugin manifest, required source files, `SKILL.md` YAML front
  matter + version consistency, the 30 + 8 regression case headings in `tests.md`, and the
  research-link count in `research.md`. Run it after editing any of the spec files
  (`SKILL.md`, `eval.md`, `research.md`, `tests.md`, `.codex-plugin/plugin.json`,
  `agents/openai.yaml`).
- `tests.md` and `eval.md` define **functional** LLM-driven test cases for the skill itself;
  these are run by an AI agent host (Cursor / Claude Code / Codex), not by any local process.

### Gotchas

- Use `python3` (the `python` alias is not installed on this VM). Python 3.12 is already present.
- No package install step is needed — the script imports only stdlib (`argparse`, `json`,
  `shutil`, `zipfile`, `pathlib`).
