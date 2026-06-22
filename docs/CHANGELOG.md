# Changelog

This file records project-level change summaries.

Rules:

- Do not record API keys, passwords, tokens, cookies, or any real secrets.
- Update this file after each meaningful code or documentation change.
- If current status or handoff expectations change, also update `docs/PROJECT_STATUS.md` and `docs/HANDOFF.md`.
- Sync summary notes to `C:\Users\OgCloud\Desktop\Codex-Worklog\WORKLOG.md`.

## 2026-06-22

### Switch translator docs and config examples to olapi gateway

- Updated the local `.env` to use `https://olapi.olinkdata.com/v1`.
- Synced `.env.example`, `README.md`, `docs/HOME_PC_SETUP.md`, and `docs/PROJECT_STATUS.md` to the same gateway so the documented setup matches the current machine.

## 2026-06-15

### Busy-state reply translation feedback

- Added an explicit busy-state message when a new translation is triggered before the previous one finishes.
- Fixed the confusing case where `F8` reply translation could appear to do nothing while an auto-translation was still running.

### Separate machine records

- Added `docs/MACHINE_NOTES.md` to track company PC and home PC setup differences separately.
- Linked the new machine-specific note from handoff, status, and README so startup state is no longer described as if every computer is identical.

## 2026-06-11

### Accurate and fast translation modes

- Added a visible translation mode switch in the main window.
- Added `准确模式` and `极速模式` so the tool can switch between `gpt-5.5` and `gpt-5.4-mini`.
- Added optional env settings for accurate model, fast model, and startup mode.

### Accurate and fast translation docs sync

- Synced README and setup docs to the current full `.env` structure and custom gateway example.
- Synced `.env.example` to the same custom gateway base URL so the repo template matches the current local setup.

### GitHub and multi-computer preparation

- Made the project self-contained for GitHub and cross-computer usage.
- Switched default config loading to the repo-local `.env`, with legacy fallback preserved.
- Added `.env.example`, `.gitignore`, `FEATURE_LOG.md`, `agent.md`, and structured docs.
- Rewrote `README.md` with setup, usage, troubleshooting, and hotkey instructions.
- Added `docs/HOME_PC_SETUP.md` so another computer can clone and run the tool directly.
- Updated `start_translator.bat` for smoother background launch and added `start_translator_debug.bat`.

### Recent assistant usability updates

- Popup translations now support scrolling and title-bar dragging.
- Automatic translation now skips pure digits and `VM` + digits.
- Clipboard polling and translation request flow were tuned for faster response.

## 2026-05-14

### Startup stability

- Added single-instance protection to avoid duplicate helper instances.
- Set up the original machine for Windows login auto-start.

## 2026-05-13

### Initial release

- Added Discord message translation to Chinese.
- Added reply translation from Chinese into the detected or selected language.
- Added floating popup output and a main control window.
