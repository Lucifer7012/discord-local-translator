# Discord Local Translator

> 中文版本见本文末尾。

Windows desktop helper for Discord chat translation. It does not modify the Discord client itself. It watches copied text, translates foreign-language messages into Simplified Chinese, and can translate your Chinese reply back into the target language.

## What It Does

- Translate copied Discord messages to Simplified Chinese
- Detect and display the source language
- Translate your Chinese reply into the other person's language
- Copy translated output back to the clipboard automatically
- Show a floating translation popup near the mouse cursor
- Skip pure numeric codes, `VM` + numeric identifiers, and compact random-code strings automatically

## Files

- `local_translator.py`: main app
- `start_translator.bat`: normal launcher for daily use
- `start_translator_debug.bat`: debug launcher that keeps the console open
- `.env.example`: environment variable template
- `docs/`: status, changelog, handoff, and setup docs

Chinese translations are included at the end of this file and the corresponding Markdown files.

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
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
```

Optional:

```env
AI_API_KEY=your_api_key
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-6-sol
```

Example for the current local custom gateway setup:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://apilink.olinkdata.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
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

The main window also has `翻译原文` for translating text entered directly in the original-text box, and `暂停自动翻译` / `恢复自动翻译` for temporarily stopping clipboard-triggered translations while you copy Discord content.

Use `窗口置顶` to keep the main window above other applications; click it again to cancel.

## Translation Modes

The main window now supports two built-in translation modes:

- `准确模式`: prefers translation quality and uses `gpt-6-sol` by default
- `极速模式`: prefers lower latency and uses `gpt-5.6-sol` by default

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

For machine-specific differences such as startup status, see [docs/MACHINE_NOTES.md](docs/MACHINE_NOTES.md).

## Notes

- The floating popup supports mouse wheel scrolling for long translations.
- Drag the popup by its title bar text.
- Very long or heavy model responses will still depend on your API provider speed.
- This project does not commit API keys, tokens, or passwords.

## Troubleshooting

- If double-click launch does nothing, run `start_translator_debug.bat` and read the error.
- If translation feels slow, switch to a faster model in `.env`.
- If hotkeys do not respond, another app may be occupying the same global hotkey.
- If the popup does not appear, make sure Discord is the foreground window and that copied text is not Chinese, pure digits, `VM` + digits, or compact code-like strings such as `MOCJiQUwSu`.

---

# 中文版本
## Discord 本地翻译助手

Windows 桌面翻译工具，用于 Discord 聊天翻译。它不会修改 Discord 客户端，而是监听复制的文本，把外语消息翻译成简体中文，也可以把中文回复翻译成对方使用的语言。

> 英文版见本文上方。

## 功能

- 将复制的 Discord 消息翻译成简体中文
- 检测并显示原文语言
- 将中文回复翻译成对方的语言
- 自动把译文复制到剪贴板
- 在鼠标附近显示浮动翻译窗口
- 自动跳过纯数字、`VM` 加数字以及紧凑随机码

## 文件

- `local_translator.py`：主程序
- `start_translator.bat`：日常启动脚本
- `start_translator_debug.bat`：保留控制台窗口的调试启动脚本
- `.env.example`：环境变量模板
- `docs/`：状态、变更、交接和安装说明

英文原始内容保留在本文件及各对应 Markdown 文件的上方；中文版本统一放在同一文件末尾。

## 环境要求

- Windows 10 或 Windows 11
- Discord 桌面版
- Python 3.11 或更高版本，并启用 Tkinter
- 一个兼容 OpenAI Chat Completions 接口的 API

## 快速开始

1. 克隆此仓库。
2. 将 `.env.example` 复制为 `.env`。
3. 在 `.env` 中填写 API 配置。
4. 运行 `start_translator.bat`。
5. 打开 Discord，使用下面的快捷键。

## 配置示例

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
```

当前本机中转配置示例：

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://apilink.olinkdata.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
```

配置读取优先级：

1. `DISCORD_TRANSLATOR_ENV` 环境变量指定的文件
2. 仓库本地 `.env`
3. 旧项目配置路径，仅作为兼容回退

## 快捷键和按钮

- `Ctrl+C`：复制 Discord 外语消息并自动翻译
- `Ctrl+Alt+T`：手动翻译当前选中的文本
- `F8`：打开中文回复框并翻译回复
- `Ctrl+Alt+O`：显示或隐藏主窗口
- `翻译原文`：翻译主窗口原文框中的内容
- `暂停自动翻译` / `恢复自动翻译`：暂停或恢复剪贴板自动触发
- `窗口置顶` / `取消置顶`：让主窗口保持在其他软件上方或取消置顶

## 翻译模式

- `准确模式`：默认使用 `gpt-6-sol`
- `极速模式`：默认使用 `gpt-5.6-sol`

## 日常使用

### 翻译别人发送的消息

1. 在 Discord 中选中消息文本。
2. 按 `Ctrl+C`。
3. 浮动窗口会显示译文和检测到的语言。

### 翻译自己的回复

1. 按 `F8`。
2. 输入中文回复。
3. 按 Enter 翻译。
4. 译文会复制到剪贴板，可返回 Discord 粘贴。

## 家用电脑安装

请查看 [家用电脑安装说明（见对应文件末尾）](docs/HOME_PC_SETUP.md#中文版本)。机器差异请查看 [机器备注（见对应文件末尾）](docs/MACHINE_NOTES.md#中文版本)。

## 注意事项

- 浮动窗口支持长文本滚动。
- 可以拖动浮动窗口标题栏。
- 响应速度取决于 API 中转服务和模型速度。
- 仓库不会提交 API Key、Token 或密码。

## 故障排查

- 双击无法启动时，运行 `start_translator_debug.bat` 查看错误。
- 翻译速度慢时，可在 `.env` 中切换模型。
- 快捷键无响应时，可能被其他软件占用。
- 浮动窗口不出现时，确认 Discord 在前台，并确认复制内容不是中文、纯数字、`VM` 加数字或随机码。
