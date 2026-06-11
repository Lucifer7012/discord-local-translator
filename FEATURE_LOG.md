# Feature Log

This file keeps a more detailed working log than `docs/CHANGELOG.md`.

## 2026-06-11

### Popup usability and presentation refresh

- Restyled the floating translation popup with a cleaner dark card layout, improved spacing, and more readable typography.
- Added popup controls for scaling the overlay text size up or down.
- Added a pin mode so the popup can stay on screen without auto-closing while remaining topmost.
- Changed popup placement to reuse the cursor position captured at copy time so the result stays closer to the source message.
- Replaced the permanent duplicate-text suppression with a short cooldown so the same copied line can be translated again after a few seconds.

### Accurate/fast translation mode switch

- Added a runtime translation mode switch to the main window.
- `准确模式` now targets the accurate model slot, currently intended for `gpt-5.5`.
- `极速模式` now targets the fast model slot, currently intended for `gpt-5.4-mini`.
- Added optional env keys so the accurate model, fast model, and startup mode can be changed without editing code.

### Config documentation sync

- Synced the setup docs so the full six-line `.env` structure is documented consistently.
- Updated `.env.example` to use the same custom gateway URL as the current local configuration.

### Repository hardening for GitHub and multi-computer use

- Switched the default config path from a machine-specific absolute path to the repo-local `.env`.
- Kept the old `chaoshan-translator` config path as a fallback so the current computer does not break.
- Added `.env.example`, `.gitignore`, and structured project docs.
- Added a dedicated home PC setup guide so the project can be cloned and used on another machine.
- Improved `start_translator.bat` so normal double-click launch prefers `pythonw` and runs in the background.
- Added `start_translator_debug.bat` for troubleshooting when setup fails.

### Documentation and collaboration scaffolding

- Added `docs/CHANGELOG.md`, `docs/PROJECT_STATUS.md`, `docs/HANDOFF.md`, and `agent.md`.
- Standardized the project handoff flow so future Codex sessions can continue from the same state.
- Prepared the repository for GitHub sync without exposing secrets.

## 2026-06-09

### Translation popup improvements

- Replaced the non-scrollable popup label with a scrollable text area.
- Added mouse wheel scrolling for long translations.
- Increased popup height and display duration for long content.
- Limited popup dragging to the title area to avoid interfering with text scrolling.
- Fixed title-text dragging so the popup can be moved by grabbing the visible title.

### Automatic translation filtering and speed tuning

- Added filtering for pure numeric messages.
- Added filtering for `VM` + digits so code-like identifiers no longer trigger translation.
- Reduced clipboard polling delay and removed unnecessary fixed waits after copy.
- Added a smaller response token cap to keep quick chat translations faster.

## 2026-05-14

### Startup and stability

- Added single-instance protection to avoid duplicate hotkey registration.
- Configured the tool for Windows auto-start on the original computer.

## 2026-05-13

### Initial build

- Built the first Windows desktop translator for Discord.
- Added translation to Chinese for copied foreign-language messages.
- Added reply translation from Chinese into the target language.
- Added floating translation output and a main control window.
