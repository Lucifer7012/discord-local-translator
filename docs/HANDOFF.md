# Handoff

> [中文版本见本文末尾](#中文版本)。

This file is the quick resume entry for future Codex sessions or another computer.

## Read first in a new session

- `docs/HANDOFF.md`
- `docs/MACHINE_NOTES.md`
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
- GitHub repo: `https://github.com/Lucifer7012/discord-local-translator`
- The repo should use a local `.env` instead of relying on another project's config file.
- Machine-specific differences should be recorded in `docs/MACHINE_NOTES.md`.
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

---

# 中文版本
## 项目交接说明

以下为本文件下方的中文交接说明；英文版本见上方。

## 新会话先读取

- `docs/HANDOFF.md`
- `docs/MACHINE_NOTES.md`
- `docs/PROJECT_STATUS.md`
- `docs/CHANGELOG.md`
- `FEATURE_LOG.md`
- `agent.md`

建议提示词：

```text
请先读取 docs/HANDOFF.md、docs/PROJECT_STATUS.md、docs/CHANGELOG.md、FEATURE_LOG.md 和 agent.md，然后继续这个 Discord 翻译助手项目。不要记录任何 API Key、密码、Token。
```

## 当前交接摘要

- 项目已准备好同步到 GitHub，并支持多台电脑使用。
- GitHub 仓库：<https://github.com/Lucifer7012/discord-local-translator>
- 项目应使用本地 `.env`，不依赖其他项目的配置文件。
- 机器差异应记录在 `docs/MACHINE_NOTES.md`。
- 已加入浮动窗口滚动、拖动、数字跳过、翻译速度调整、直接翻译、暂停自动翻译和窗口置顶。
- 修改行为后要同步更新项目文档和桌面总工作日志。

## 多电脑工作流程

1. 克隆 GitHub 仓库。
2. 将 `.env.example` 复制为 `.env`。
3. 填写 API 配置。
4. 运行 `start_translator.bat`。
5. 如果失败，运行 `start_translator_debug.bat`。

## 文档维护约定

每次重要修改后更新：

- `docs/CHANGELOG.md`
- `docs/PROJECT_STATUS.md`
- `FEATURE_LOG.md`
- 如果工作流程发生变化，再更新 `agent.md`

同时将摘要同步到：

`C:\Users\OgCloud\Desktop\Codex-Worklog\WORKLOG.md`
