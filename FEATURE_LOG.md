# Feature Log

> [中文版本见本文末尾](#中文版本)。

This file keeps a more detailed working log than `docs/CHANGELOG.md`.

## 2026-09-28

### Persistent always-on-top window control

- Added a `窗口置顶` / `取消置顶` button to keep the main translator window above other applications until manually disabled.
- Preserved the existing temporary focus behavior when persistent topmost mode is off.

### Direct translation and clipboard auto-translation pause

- Added a `翻译原文` action for translating text entered directly in the original-text box.
- Added `暂停自动翻译` / `恢复自动翻译` to pause clipboard-triggered translations while copying Discord content; manual translation and F8 reply translation remain available.
- Changed the accurate-mode model from `gpt-5.5` to the requested `gpt-6-sol`.

## 2026-09-14

### Fast mode is now the startup default

- Changed the startup translation mode from `accurate` to `fast`.
- Replaced the fast-mode model `gpt-5.4-mini` with `gpt-5.6-sol` in the runtime config and code fallback.
- Updated setup examples and verified a live translation request through the configured gateway.

## 2026-07-02

### Gateway switch from olapi to apilink

- Switched the active translator `.env` base URL from `https://olapi.olinkdata.com/v1` to `https://apilink.olinkdata.com/v1`.
- Synced `.env.example`, `README.md`, `docs/HOME_PC_SETUP.md`, and `docs/PROJECT_STATUS.md` so future machines use the same endpoint by default.

## 2026-06-29

### Clipboard filter for random code strings

- Extended the auto-translation skip logic beyond pure digits and `VM` + digits.
- Added compact code-like token filtering for copied strings such as `MOCJiQUwSu` and similar mixed-case identifiers.
- Synced the README wording so the documented skip behavior matches the installed plugin.

## 2026-06-22

### Gateway switch to olapi

- Switched the active translator `.env` from the old `43.166.202.16:3000` gateway to `https://olapi.olinkdata.com/v1`.
- Updated the repository examples and setup documents so new machines will use the same gateway by default.

## 2026-06-15

### Busy-state feedback for overlapping translations

- Investigated a case where the reply translation window accepted Chinese input but produced no visible result.
- Confirmed the root cause was the shared `self.busy` guard: auto-translation was still running, so reply translation returned early without any message.
- Added an explicit busy-state warning so overlapping requests now explain that the previous translation is still in progress.

### Separate company/home machine tracking

- Added `docs/MACHINE_NOTES.md` so startup state and other local setup details can be recorded per machine.
- Recorded that the company PC currently has Windows startup enabled through a Startup shortcut.
- Left the home PC startup state explicitly unconfirmed until that machine is configured.

## 2026-06-14

### Popup placement tuning and local startup setup

- Tuned the translation popup so it prefers showing above the captured copy anchor instead of dropping below the source line.
- Reset popup scaling to the default size whenever a new translation popup opens, so previous manual zoom does not affect the next message.
- Adjusted the reply prompt to prefer showing above the mouse cursor as well.
- Enabled Windows auto-start on the current machine by placing a shortcut to `start_translator.bat` in the user's Startup folder.

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

---

# 中文版本
## 功能日志

以下为本文件下方的完整中文翻译；英文详细记录见上方。

## 2026-09-28

### 主窗口持久置顶

- 增加 `窗口置顶` / `取消置顶` 按钮，让主翻译窗口持续显示在其他软件上方，直到手动取消。
- 未开启持久置顶时，保留原有的临时置前行为。

### 直接翻译和剪贴板自动翻译暂停

- 增加 `翻译原文` 按钮，可直接翻译原文框中输入的文字。
- 增加 `暂停自动翻译` / `恢复自动翻译`，复制 Discord 文本时可以暂时阻止自动翻译；手动翻译和 F8 回复翻译仍然可用。
- 准确模式从 `gpt-5.5` 改为指定的 `gpt-6-sol`。

## 2026-09-14

### 默认启动极速模式

- 启动翻译模式从 `accurate` 改为 `fast`。
- 极速模式模型从 `gpt-5.4-mini` 改为 `gpt-5.6-sol`。
- 更新配置示例，并通过当前中转网关验证实时翻译请求。

## 2026-07-02

### 中转地址从 olapi 切换到 apilink

- 将本机 `.env` 的地址从 `https://olapi.olinkdata.com/v1` 切换为 `https://apilink.olinkdata.com/v1`。
- 同步更新 `.env.example`、`README.md`、家用电脑安装说明和项目状态，使以后配置的电脑默认使用相同地址。

## 2026-06-29

### 更可靠地过滤随机码

- 在纯数字和 `VM` 加数字之外，增加紧凑随机码过滤。
- 对类似 `MOCJiQUwSu` 的混合大小写标识符自动跳过翻译。
- 同步更新 README，使文档中的跳过规则与已安装插件一致。

## 2026-06-22

### 中转地址切换到 olapi

- 将本机 `.env` 从旧的 `43.166.202.16:3000` 中转地址切换到 `https://olapi.olinkdata.com/v1`。
- 更新仓库示例和安装说明，使新电脑默认使用相同地址。

## 2026-06-15

### 重叠翻译时增加忙碌提示

- 调查回复翻译窗口接收中文却没有可见结果的问题。
- 确认原因是共享的 `self.busy` 锁：自动翻译仍在进行时，回复翻译会提前返回且没有提示。
- 增加明确的忙碌状态提示，说明上一条翻译仍在进行。

### 公司电脑和家用电脑分开记录

- 增加 `docs/MACHINE_NOTES.md`，分别记录不同电脑的启动状态和本地配置。
- 记录当前公司电脑通过 Startup 快捷方式启用了 Windows 开机自启。
- 家用电脑的自启状态暂时保持未确认，等实际配置后再填写。

## 2026-06-14

### 弹窗位置调整和本地开机启动

- 调整翻译弹窗位置，优先显示在复制锚点上方，而不是掉到原文下方。
- 每次打开新翻译弹窗时恢复默认缩放，避免上一次手动缩放影响下一条消息。
- 调整回复框位置，使其也优先显示在鼠标光标上方。
- 将 `start_translator.bat` 的快捷方式放入当前用户 Startup 文件夹，启用 Windows 开机自启。

## 2026-06-11

### 弹窗易用性和界面更新

- 重新设计浮动翻译弹窗，使用更清晰的深色卡片布局、间距和字体。
- 增加放大和缩小覆盖文字的弹窗控制按钮。
- 增加固定模式，让弹窗保持显示且继续置顶，不自动关闭。
- 使用复制时记录的光标位置重新定位弹窗，使译文更靠近原消息。
- 将永久重复文本抑制改为短暂冷却，同一行文字等待几秒后可以再次翻译。

### 准确/极速翻译模式切换

- 在主窗口增加运行时翻译模式切换。
- `准确模式` 使用准确模型槽位，当前默认配置为 `gpt-5.5`。
- `极速模式` 使用快速模型槽位，当前默认配置为 `gpt-5.4-mini`。
- 增加可选环境变量，无需改代码即可调整准确模型、快速模型和启动模式。

### 配置文档同步

- 同步安装说明，使完整的六行 `.env` 配置结构保持一致。
- 更新 `.env.example`，使用与当前本机配置相同的中转地址。

### GitHub 和多电脑使用准备

- 将默认配置路径从机器专用的绝对路径改为仓库本地 `.env`。
- 保留旧的 `chaoshan-translator` 配置路径作为回退，避免当前电脑配置失效。
- 增加 `.env.example`、`.gitignore` 和结构化项目文档。
- 增加家用电脑安装说明，使项目可以在另一台电脑上克隆使用。
- 改进 `start_translator.bat`，普通双击启动时优先使用 `pythonw` 并在后台运行。
- 增加 `start_translator_debug.bat`，用于安装或配置失败时排查问题。

### 文档和协作基础结构

- 增加 `docs/CHANGELOG.md`、`docs/PROJECT_STATUS.md`、`docs/HANDOFF.md` 和 `agent.md`。
- 统一项目交接流程，使未来 Codex 会话可以从同一状态继续。
- 为 GitHub 同步准备仓库，同时避免暴露密钥。

## 2026-06-09

### 翻译弹窗改进

- 将不可滚动的弹窗标签替换为可滚动文本区域。
- 为长译文增加鼠标滚轮滚动。
- 增加长文本的弹窗高度和显示时长。
- 将拖动限制在标题区域，避免影响文本滚动。
- 修复标题文字拖动，现在可以抓住可见标题移动弹窗。

### 自动翻译过滤和速度调整

- 增加纯数字消息过滤。
- 增加 `VM` 加数字过滤，避免代码样式标识符触发翻译。
- 降低剪贴板轮询延迟，并移除复制后的不必要固定等待。
- 降低响应 Token 上限，让快速聊天翻译更快。

## 2026-05-14

### 启动和稳定性

- 增加单实例保护，避免重复注册全局快捷键。
- 为最初使用的电脑配置 Windows 开机自启。

## 2026-05-13

### 初始构建

- 构建第一个 Windows Discord 桌面翻译助手。
- 增加将复制的外语消息翻译成中文的功能。
- 增加将中文回复翻译成目标语言的功能。
- 增加浮动翻译结果和主控制窗口。
