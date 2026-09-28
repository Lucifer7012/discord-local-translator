# Home PC Setup

> 中文版本见本文末尾。

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
OPENAI_BASE_URL=https://apilink.olinkdata.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
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
- Use `翻译原文` to translate text entered in the main window, and `暂停自动翻译` when copying Discord text without triggering automatic translation.

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

---

# 中文版本
## 家用电脑安装说明

以下为本文件下方的中文安装说明；英文版本见上方。

## 1. 安装前置环境

- 安装 Python 3.11 或更高版本
- 确认命令行可以运行 `python`
- 安装 Discord 桌面版
- 准备一个可用的 OpenAI 兼容 API Key

检查 Python：

```powershell
python --version
```

## 2. 下载项目

```powershell
git clone https://github.com/Lucifer7012/discord-local-translator.git
cd discord-local-translator
```

也可以直接从 GitHub 下载 ZIP 后解压，不使用 Git。

## 3. 创建配置

```powershell
Copy-Item .env.example .env
```

编辑 `.env`：

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://apilink.olinkdata.com/v1
OPENAI_MODEL=gpt-6-sol
ACCURATE_TRANSLATION_MODEL=gpt-6-sol
FAST_TRANSLATION_MODEL=gpt-5.6-sol
TRANSLATION_MODEL_MODE=fast
```

注意：

- 如果更看重速度，可以使用较轻量的模型。
- `.env` 只保存在本机，不要上传。
- 如果不使用本项目的中转服务，请替换为自己的兼容接口地址。

## 4. 启动翻译助手

日常启动：

```powershell
.\start_translator.bat
```

启动失败时使用调试模式：

```powershell
.\start_translator_debug.bat
```

## 5. 在 Discord 中使用

- 选中外语消息并按 `Ctrl+C`
- 按 `F8` 打开中文回复框
- 按 `Ctrl+Alt+O` 显示或隐藏主窗口
- 使用 `翻译原文` 翻译主窗口中的文字
- 复制 Discord 内容前可点击 `暂停自动翻译`
- 需要始终显示窗口时点击 `窗口置顶`

## 6. 设置开机自启

1. 按 `Win + R`
2. 输入 `shell:startup`
3. 在启动文件夹中创建指向 `start_translator.bat` 的快捷方式

## 7. 故障排查

- 复制后没有反应：确认 Discord 在前台，且复制内容不是中文、纯数字或 `VM` 加数字。
- 启动失败：运行 `start_translator_debug.bat`，并确认 `python --version` 正常。
- 翻译速度慢：切换 `.env` 中的模型，并检查 API 中转服务延迟。
