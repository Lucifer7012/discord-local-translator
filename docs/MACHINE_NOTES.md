# Machine Notes

> 中文版本见本文末尾。

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

---

# 中文版本
## 机器备注

以下为本文件下方的机器备注（见对应文件末尾）；英文版本见上方。

不要在这里保存 API Key、密码、Token、Cookie 或任何真实机密。

## 公司电脑

角色：

- 当前主要工作电脑

开机自启：

- 已启用

启动快捷方式：

`C:\Users\OgCloud\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Discord 本地翻译助手.lnk`

快捷方式行为：

- 启动 `pythonw.exe`
- 运行 `C:\Users\OgCloud\Documents\Codex\2026-05-13\discord\local_translator.py`
- 工作目录为 `C:\Users\OgCloud\Documents\Codex\2026-05-13\discord`

配置备注：

- 使用仓库本地 `.env`
- 当前模型配置记录在 `docs/PROJECT_STATUS.md`

## 家用电脑

角色：

- 第二台个人电脑

开机自启：

- 当前仓库记录中尚未确认

预期设置：

- 克隆仓库
- 根据 `.env.example` 创建本地 `.env`
- 单独决定是否启用 Windows 开机自启

家用电脑配置完成后，请更新此文件，不要覆盖公司电脑的记录。
