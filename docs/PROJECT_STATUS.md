# Project Status

> 中文版本见本文末尾。

Updated: 2026-09-28

Project: Discord Local Translator

Local path:

- `C:\Users\OgCloud\Documents\Codex\2026-05-13\discord`

GitHub:

- `https://github.com/Lucifer7012/discord-local-translator`

## Current purpose

This is a Windows desktop helper for Discord. It helps the user quickly translate copied foreign-language chat messages into Simplified Chinese and translate Chinese replies back into the conversation language.

## Current features

- Auto-translate copied Discord messages to Chinese
- Detect source language and show it in the popup
- Translate Chinese replies through the `F8` reply window
- Switch between `准确模式` and `极速模式` in the main window
- Auto-copy translated output
- Floating popup with scroll support for long content
- Popup title dragging for repositioning
- Main control window for status and manual actions
- Direct translation from text entered in the original-text box
- Pause/resume control for clipboard-triggered auto-translation
- Persistent always-on-top toggle for the main window
- Automatic skip rules for:
  - Chinese content
  - Pure digits
  - `VM` + digits
- Single-instance protection

## Current configuration behavior

- Priority 1: `DISCORD_TRANSLATOR_ENV`
- Priority 2: local repo `.env`
- Priority 3: legacy `chaoshan-translator` env path as fallback
- Optional model-specific settings:
  - `ACCURATE_TRANSLATION_MODEL`
  - `FAST_TRANSLATION_MODEL`
  - `TRANSLATION_MODEL_MODE`

## Current recommended local config

```env
OPENAI_BASE_URL=https://apilink.olinkdata.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
```

## Important files

- `local_translator.py`: main application
- `start_translator.bat`: normal launcher
- `start_translator_debug.bat`: debug launcher
- `.env.example`: configuration template
- `docs/HOME_PC_SETUP.md`: another-computer setup guide
- `docs/MACHINE_NOTES.md`: company PC vs home PC setup differences

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

## Machine-specific note

- This project now tracks machine differences separately in `docs/MACHINE_NOTES.md`.

---

# 中文版本
## 项目状态

以下为本文件下方的中文项目状态；英文版本见上方。

更新时间：2026-09-28

项目：Discord 本地翻译助手

GitHub：<https://github.com/Lucifer7012/discord-local-translator>

## 项目用途

这是一个 Windows 桌面辅助工具，用于把复制的 Discord 外语聊天翻译成简体中文，也可以把中文回复翻译成对方的语言。

## 当前功能

- 自动翻译复制的 Discord 消息
- 检测并显示原文语言
- 通过 F8 回复框翻译中文回复
- 在准确模式和极速模式之间切换
- 自动复制译文
- 支持长文本滚动的浮动窗口
- 可拖动浮动窗口标题栏
- 主窗口手动操作
- 直接翻译原文框中的文字
- 暂停/恢复剪贴板自动翻译
- 主窗口持久置顶
- 自动跳过中文、纯数字和 `VM` 加数字
- 单实例保护

## 配置读取规则

- 优先读取 `DISCORD_TRANSLATOR_ENV`
- 其次读取仓库本地 `.env`
- 最后使用旧 `chaoshan-translator` 配置作为兼容回退

可选模型配置：

- `ACCURATE_TRANSLATION_MODEL`
- `FAST_TRANSLATION_MODEL`
- `TRANSLATION_MODEL_MODE`

## 当前推荐配置

```env
OPENAI_BASE_URL=https://apilink.olinkdata.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
```

## 重要文件

- `local_translator.py`：主程序
- `start_translator.bat`：正常启动脚本
- `start_translator_debug.bat`：调试启动脚本
- `.env.example`：配置模板
- `docs/HOME_PC_SETUP.md`：另一台电脑的安装说明
- `docs/MACHINE_NOTES.md`：公司电脑与家用电脑的差异记录

## 已知限制

- 仅支持 Windows
- 主要针对 Discord 桌面版前台使用
- 翻译速度受 API 中转服务和模型影响
- 全局快捷键可能与其他软件冲突
- Discord 的自动粘贴行为可能受窗口焦点影响
