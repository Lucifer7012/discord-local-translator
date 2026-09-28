# Changelog

> [中文版本见本文末尾](#中文版本)。

This file records project-level change summaries.

Rules:

- Do not record API keys, passwords, tokens, cookies, or any real secrets.
- Update this file after each meaningful code or documentation change.
- If current status or handoff expectations change, also update `docs/PROJECT_STATUS.md` and `docs/HANDOFF.md`.
- Sync summary notes to `C:\Users\OgCloud\Desktop\Codex-Worklog\WORKLOG.md`.

## 2026-09-28

### Persistent always-on-top window control

- Added a toggle button to keep the main translator window above other applications until manually disabled.

### Direct translation, pause control, and GPT-6 Sol accurate mode

- Added direct translation for text entered in the original-text box.
- Added pause/resume control for clipboard-triggered automatic translation.
- Changed accurate mode to `gpt-6-sol` while keeping fast mode on `gpt-5.6-sol`.

## 2026-09-14

### Default to fast mode with GPT-5.6 Sol

- Changed the default startup mode to `极速模式`.
- Replaced `gpt-5.4-mini` with `gpt-5.6-sol` for fast-mode translations.
- Updated the code fallback and configuration examples to use the new default.

## 2026-07-02

### Switch translator gateway to apilink

- Updated the local `.env` to use `https://apilink.olinkdata.com/v1`.
- Synced `.env.example`, `README.md`, `docs/HOME_PC_SETUP.md`, and `docs/PROJECT_STATUS.md` to the same gateway so documented setup matches the current machine.

## 2026-06-29

### Skip numeric and random-code clipboard copies more reliably

- Extended the clipboard auto-translation filter to ignore compact code-like strings in addition to pure digits and `VM` + digits.
- Updated the README troubleshooting text to mention the new code-string skip behavior.

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

---

# 中文版本
## 变更日志

以下为本文件下方的完整中文翻译；英文项目变更记录见上方。

## 维护规则

- 不要记录 API Key、密码、Token、Cookie 或其他真实机密。
- 每次有意义的代码或文档修改后更新此文件。
- 如果当前状态或交接要求发生变化，也要更新 `docs/PROJECT_STATUS.md` 和 `docs/HANDOFF.md`。
- 将摘要同步到 `C:\Users\OgCloud\Desktop\Codex-Worklog\WORKLOG.md`。

## 2026-09-28

### 主窗口持久置顶

- 增加按钮，让主翻译窗口持续显示在其他软件上方，直到手动取消。

### 直接翻译、暂停控制和 GPT-6 Sol 准确模式

- 增加直接翻译原文框内容的功能。
- 增加剪贴板自动翻译暂停/恢复控制。
- 准确模式改为 `gpt-6-sol`，极速模式继续使用 `gpt-5.6-sol`。

## 2026-09-14

### 默认使用极速模式和 GPT-5.6 Sol

- 默认启动模式改为 `极速模式`。
- 极速模式从 `gpt-5.4-mini` 改为 `gpt-5.6-sol`。
- 更新代码回退值和配置示例。

## 2026-07-02

### 切换到 apilink 中转地址

- 本机 `.env` 使用 `https://apilink.olinkdata.com/v1`。
- 同步仓库示例、README、家用电脑安装说明和项目状态。

## 2026-06-29

### 更可靠地跳过数字和随机码

- 自动翻译过滤器现在会跳过紧凑随机码，以及纯数字和 `VM` 加数字。
- 更新 README 的故障排查说明，记录新的随机码跳过规则。

## 2026-06-22

### 将文档和配置示例切换到 olapi

- 本机 `.env` 使用 `https://olapi.olinkdata.com/v1`。
- 同步 `.env.example`、README、家用电脑安装说明和项目状态，使文档中的配置保持一致。

## 2026-06-15

### 重叠翻译时的回复反馈

- 新翻译在上一条尚未完成时触发，现在会显示明确的忙碌状态提示。
- 修复 F8 回复翻译在自动翻译进行时看起来没有反应的问题。

### 分开记录不同电脑

- 增加 `docs/MACHINE_NOTES.md`，分别记录公司电脑和家用电脑的配置差异。
- 在交接说明、项目状态和 README 中链接机器备注，避免把一台电脑的启动状态误写成所有电脑都相同。

## 2026-06-11

### 准确和极速翻译模式

- 在主窗口增加可见的翻译模式切换。
- 增加 `准确模式` 和 `极速模式`，可以在 `gpt-5.5` 与 `gpt-5.4-mini` 之间切换。
- 增加准确模型、快速模型和启动模式的可选环境变量。

### 准确和极速翻译文档同步

- 同步 README 和安装说明，记录完整的 `.env` 配置结构和自定义中转示例。
- 同步 `.env.example`，使用与当前本机配置一致的自定义中转地址。

### GitHub 和多电脑使用准备

- 让项目可以独立用于 GitHub 和多电脑同步。
- 默认从仓库本地 `.env` 读取配置，同时保留旧路径回退。
- 增加 `.env.example`、`.gitignore`、`FEATURE_LOG.md`、`agent.md` 和结构化文档。
- 重写 README，加入安装、使用、故障排查和快捷键说明。
- 增加 `docs/HOME_PC_SETUP.md`，另一台电脑可以直接克隆并运行项目。
- 更新 `start_translator.bat`，让启动更顺畅；增加 `start_translator_debug.bat`。

### 最近的助手易用性更新

- 翻译弹窗支持滚动和标题栏拖动。
- 自动翻译跳过纯数字和 `VM` 加数字。
- 调整剪贴板轮询和翻译请求流程，使响应更快。

## 2026-05-14

### 启动稳定性

- 增加单实例保护，避免重复启动辅助程序实例。
- 为最初使用的电脑设置 Windows 登录后自动启动。

## 2026-05-13

### 初始版本

- 增加 Discord 消息翻译成中文。
- 增加中文回复翻译成检测到或手动选择的语言。
- 增加浮动翻译结果和主控制窗口。
