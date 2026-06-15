# Machine Notes

This file records machine-specific setup differences for the Discord Local Translator.

Do not store API keys, passwords, tokens, cookies, or any real secrets here.

## Company PC

Role:

- Current main work machine

Startup status:

- Enabled

Startup shortcut:

- `C:\Users\OgCloud\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Discord 本地翻译助手.lnk`

Shortcut target behavior:

- Launches `pythonw.exe`
- Runs `C:\Users\OgCloud\Documents\Codex\2026-05-13\discord\local_translator.py`
- Working directory: `C:\Users\OgCloud\Documents\Codex\2026-05-13\discord`

Config notes:

- Uses the repo-local `.env`
- Current model setup is documented in `docs/PROJECT_STATUS.md`

## Home PC

Role:

- Secondary personal machine

Startup status:

- Not yet confirmed in this repo record

Setup expectation:

- Clone the repo
- Create local `.env` from `.env.example`
- Decide separately whether Windows startup should be enabled

When home PC setup is finished, update this file instead of overwriting the company PC notes.
