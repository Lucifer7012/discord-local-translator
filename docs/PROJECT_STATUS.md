# Project Status

Updated: 2026-06-11

Project: Discord Local Translator

Local path:

- `C:\Users\OgCloud\Documents\Codex\2026-05-13\discord`

## Current purpose

This is a Windows desktop helper for Discord. It helps the user quickly translate copied foreign-language chat messages into Simplified Chinese and translate Chinese replies back into the conversation language.

## Current features

- Auto-translate copied Discord messages to Chinese
- Detect source language and show it in the popup
- Translate Chinese replies through the `F8` reply window
- Auto-copy translated output
- Floating popup with scroll support for long content
- Popup title dragging for repositioning
- Main control window for status and manual actions
- Automatic skip rules for:
  - Chinese content
  - Pure digits
  - `VM` + digits
- Single-instance protection

## Current configuration behavior

- Priority 1: `DISCORD_TRANSLATOR_ENV`
- Priority 2: local repo `.env`
- Priority 3: legacy `chaoshan-translator` env path as fallback

## Important files

- `local_translator.py`: main application
- `start_translator.bat`: normal launcher
- `start_translator_debug.bat`: debug launcher
- `.env.example`: configuration template
- `docs/HOME_PC_SETUP.md`: another-computer setup guide

## Known limitations

- Windows only
- Designed for Discord desktop foreground usage
- Translation speed still depends heavily on the upstream API provider and model
- Global hotkeys may conflict with other applications
- Auto-paste behavior in Discord can still depend on client focus behavior

## Recommended next steps

- Keep using a lightweight model for faster translation
- If another computer will use the same repo, clone it and create a separate `.env`
- If startup convenience is needed on the home PC, create a shortcut to `start_translator.bat` in `shell:startup`
