# Discord Local Translator

Windows desktop helper for Discord chat translation. It does not modify the Discord client itself. It watches copied text, translates foreign-language messages into Simplified Chinese, and can translate your Chinese reply back into the target language.

## What It Does

- Translate copied Discord messages to Simplified Chinese
- Detect and display the source language
- Translate your Chinese reply into the other person's language
- Copy translated output back to the clipboard automatically
- Show a floating translation popup near the mouse cursor
- Skip pure numeric codes and `VM` + numeric identifiers automatically

## Files

- `local_translator.py`: main app
- `start_translator.bat`: normal launcher for daily use
- `start_translator_debug.bat`: debug launcher that keeps the console open
- `.env.example`: environment variable template
- `docs/`: status, changelog, handoff, and setup docs

## Requirements

- Windows 10 or Windows 11
- Discord desktop app
- Python 3.11+ with Tkinter available
- An OpenAI-compatible chat completion API

## Quick Start

1. Clone this repository.
2. Copy `.env.example` to `.env`.
3. Fill in your API settings in `.env`.
4. Run `start_translator.bat`.
5. Open Discord desktop and start using the hotkeys below.

## Environment Variables

Create a local `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-5.5
ACCURATE_TRANSLATION_MODEL=gpt-5.5
FAST_TRANSLATION_MODEL=gpt-5.4-mini
TRANSLATION_MODEL_MODE=accurate
```

Optional:

```env
AI_API_KEY=your_api_key
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-5.5
```

Example for the current local custom gateway setup:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=http://43.166.202.16:3000/v1
OPENAI_MODEL=gpt-5.5
ACCURATE_TRANSLATION_MODEL=gpt-5.5
FAST_TRANSLATION_MODEL=gpt-5.4-mini
TRANSLATION_MODEL_MODE=accurate
```

The app will use:

1. `DISCORD_TRANSLATOR_ENV` if you set it
2. local repo `.env`
3. the legacy old path only as a backward-compatible fallback

## Hotkeys

- `Ctrl+C`: copy a foreign-language Discord message and auto-translate it
- `Ctrl+Alt+T`: manual backup translation for the current selected text
- `F8`: open the reply box, translate your Chinese reply, and prepare it for Discord
- `Ctrl+Alt+O`: show or hide the main window

## Translation Modes

The main window now supports two built-in translation modes:

- `准确模式`: prefers translation quality and uses the accurate model
- `极速模式`: prefers lower latency and uses the fast model

By default, the mode labels show the actual model names currently configured.

## Daily Usage

### Translate someone else's message

1. Select the message text in Discord.
2. Press `Ctrl+C`.
3. The floating popup will show the translation and detected language.

### Translate your own reply

1. Press `F8`.
2. Type your Chinese reply.
3. Press Enter to translate.
4. The translated result is copied and can be pasted back into Discord.

## Home PC Setup

Detailed setup steps for another computer are in [docs/HOME_PC_SETUP.md](docs/HOME_PC_SETUP.md).

## Notes

- The floating popup supports mouse wheel scrolling for long translations.
- Drag the popup by its title bar text.
- Very long or heavy model responses will still depend on your API provider speed.
- This project does not commit API keys, tokens, or passwords.

## Troubleshooting

- If double-click launch does nothing, run `start_translator_debug.bat` and read the error.
- If translation feels slow, switch to a faster model in `.env`.
- If hotkeys do not respond, another app may be occupying the same global hotkey.
- If the popup does not appear, make sure Discord is the foreground window and that copied text is not Chinese, pure digits, or `VM` + digits.
