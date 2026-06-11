# Home PC Setup

Use this guide to run the Discord Local Translator on another Windows computer.

## 1. Install prerequisites

- Install Python 3.11 or newer
- Make sure `python` is available in Command Prompt or PowerShell
- Install Discord desktop
- Make sure you have a working OpenAI-compatible API key

Check Python:

```powershell
python --version
```

## 2. Download the project

Clone the GitHub repo:

```powershell
git clone https://github.com/Lucifer7012/discord-local-translator.git
cd discord-local-translator
```

If you do not want to use Git, you can also download the repo ZIP from GitHub and extract it.

## 3. Create your config

Copy the template:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and fill these values:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=http://43.166.202.16:3000/v1
OPENAI_MODEL=gpt-5.5
ACCURATE_TRANSLATION_MODEL=gpt-5.5
FAST_TRANSLATION_MODEL=gpt-5.4-mini
TRANSLATION_MODEL_MODE=accurate
```

Tip:

- Use a lighter/faster model if response speed matters more than nuance.
- Keep `.env` local only. Do not upload it.
- If you do not use the same custom gateway, replace `OPENAI_BASE_URL` with your own compatible endpoint.

## 4. Start the translator

Normal mode:

```powershell
.\start_translator.bat
```

Debug mode if normal launch does not work:

```powershell
.\start_translator_debug.bat
```

## 5. Use it in Discord

- Select a foreign-language message and press `Ctrl+C`
- Press `F8` to open the Chinese reply box
- Press `Ctrl+Alt+O` to show or hide the main window

## 6. Optional auto-start

If you want it to start automatically after Windows login:

1. Press `Win + R`
2. Run `shell:startup`
3. Create a shortcut to `start_translator.bat`

## 7. Troubleshooting

- No response after copying:
  - Make sure Discord is the foreground window
  - Make sure the copied content is not Chinese, pure digits, or `VM` + digits
- Launch failure:
  - Run `start_translator_debug.bat`
  - Confirm `python --version` works
- Slow translation:
  - Switch to a faster model in `.env`
  - Check your API provider latency
