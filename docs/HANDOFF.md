# Handoff

This file is the quick resume entry for future Codex sessions or another computer.

## Read first in a new session

- `docs/HANDOFF.md`
- `docs/PROJECT_STATUS.md`
- `docs/CHANGELOG.md`
- `FEATURE_LOG.md`
- `agent.md`

Suggested opening prompt:

```text
请先读取 docs/HANDOFF.md、docs/PROJECT_STATUS.md、docs/CHANGELOG.md、FEATURE_LOG.md 和 agent.md，然后继续这个 Discord 翻译助手项目。不要记录任何 API Key、密码、Token。
```

## Current handoff summary

- The project is now prepared for GitHub sync and cross-computer use.
- The repo should use a local `.env` instead of relying on another project's config file.
- Popup scrolling, dragging, numeric skip rules, and translation speed tuning were already added.
- When changing behavior, remember to update the project docs and the desktop worklog.

## Cross-computer workflow

On another computer:

1. Clone the GitHub repo.
2. Copy `.env.example` to `.env`.
3. Fill in API settings.
4. Run `start_translator.bat`.
5. If it fails, run `start_translator_debug.bat`.

## Documentation contract

After each meaningful change, update:

- `docs/CHANGELOG.md`
- `docs/PROJECT_STATUS.md`
- `FEATURE_LOG.md`
- `agent.md` if workflow rules change

Also sync the summary into:

- `C:\Users\OgCloud\Desktop\Codex-Worklog\WORKLOG.md`
