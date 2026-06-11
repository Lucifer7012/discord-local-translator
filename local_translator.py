import ctypes
import json
import os
import queue
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from tkinter import BOTH, END, LEFT, RIGHT, TOP, X, Y, BooleanVar, Frame, Label, StringVar, Text, Tk, Toplevel
from tkinter import messagebox, ttk


APP_TITLE = "Discord 本地翻译助手"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_PATH = SCRIPT_DIR / ".env"
LEGACY_ENV_PATH = Path(r"C:\Users\OgCloud\Documents\chaoshan-translator\.env")
MODEL_MODE_ACCURATE = "accurate"
MODEL_MODE_FAST = "fast"
DEFAULT_ACCURATE_MODEL = "gpt-5.5"
DEFAULT_FAST_MODEL = "gpt-5.4-mini"

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
WM_HOTKEY = 0x0312
WM_QUIT = 0x0012
KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_SPACE = 0x20
VK_INSERT = 0x2D
VK_F8 = 0x77
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001

HOTKEY_TRANSLATE_TO_CHINESE = 1
HOTKEY_TRANSLATE_REPLY = 2
HOTKEY_TOGGLE_WINDOW = 3

HOTKEYS = {
    HOTKEY_TRANSLATE_TO_CHINESE: (MOD_CONTROL | MOD_ALT, ord("T"), "Ctrl+Alt+T", "选中文本 -> 中文"),
    HOTKEY_TRANSLATE_REPLY: (0, VK_F8, "F8", "中文 -> 回复目标语言"),
    HOTKEY_TOGGLE_WINDOW: (MOD_CONTROL | MOD_ALT, ord("O"), "Ctrl+Alt+O", "显示/隐藏设置窗口"),
}

MAX_INPUT_CHARS = 8000
CHAT_MAX_TOKENS = 120
CLIPBOARD_POLL_INTERVAL_MS = 150

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
SINGLE_INSTANCE_MUTEX = "Local\\DiscordLocalTranslatorAssistant"


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.c_void_p),
        ("message", ctypes.c_uint),
        ("wParam", ctypes.c_size_t),
        ("lParam", ctypes.c_size_t),
        ("time", ctypes.c_ulong),
        ("pt", POINT),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("union", INPUT_UNION)]


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue

        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        values[key] = value

    return values


def normalize_chat_url(base_url: str) -> str:
    base_url = (base_url or "https://api.openai.com/v1").strip().rstrip("/")
    if base_url.endswith("/chat/completions"):
        return base_url
    return f"{base_url}/chat/completions"


def extract_json_object(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", text))


def is_nontranslatable_code_block(text: str) -> bool:
    lines = [line.strip() for line in re.split(r"[\r\n]+", text) if line.strip()]
    if not lines:
        return False
    return all(re.fullmatch(r"(?:VM)?\d+", line, flags=re.IGNORECASE) for line in lines)


def send_key(vk: int, key_up: bool = False) -> None:
    flags = KEYEVENTF_KEYUP if key_up else 0
    if vk in {VK_INSERT}:
        flags |= KEYEVENTF_EXTENDEDKEY
    user32.keybd_event(vk, 0, flags, 0)


def send_key_combo(*keys: int) -> None:
    for vk in keys:
        send_key(vk, False)
        time.sleep(0.015)
    for vk in reversed(keys):
        send_key(vk, True)
        time.sleep(0.015)


def send_ctrl_c() -> None:
    send_key_combo(VK_CONTROL, ord("C"))


def send_ctrl_a() -> None:
    send_key_combo(VK_CONTROL, ord("A"))


def send_ctrl_v() -> None:
    send_key_combo(VK_CONTROL, ord("V"))


def send_ctrl_insert() -> None:
    send_key_combo(VK_CONTROL, VK_INSERT)


def send_alt_t() -> None:
    send_key_combo(VK_MENU, ord("T"))


def get_cursor_position() -> tuple[int, int]:
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def get_window_title(hwnd: int) -> str:
    if not hwnd:
        return ""
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def is_discord_foreground() -> bool:
    hwnd = int(user32.GetForegroundWindow())
    title = get_window_title(hwnd).lower()
    return "discord" in title


def is_key_down(vk: int) -> bool:
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


def wait_for_hotkey_release(timeout: float = 1.0) -> None:
    deadline = time.time() + timeout
    keys = [VK_CONTROL, VK_MENU, VK_SPACE, VK_F8, ord("T")]
    while time.time() < deadline:
        if not any(is_key_down(vk) for vk in keys):
            return
        time.sleep(0.03)


def wait_for_clipboard_change(previous_sequence: int, timeout: float = 1.2) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if int(user32.GetClipboardSequenceNumber()) != previous_sequence:
            return True
        time.sleep(0.03)
    return False


class HotkeyListener(threading.Thread):
    def __init__(self, events: queue.Queue[tuple[int, int]]) -> None:
        super().__init__(daemon=True)
        self.events = events
        self.thread_id = 0
        self.failures: list[str] = []
        self.ready = threading.Event()

    def run(self) -> None:
        self.thread_id = kernel32.GetCurrentThreadId()
        try:
            for hotkey_id, (modifiers, vk, label, description) in HOTKEYS.items():
                ok = user32.RegisterHotKey(None, hotkey_id, modifiers, vk)
                if not ok:
                    self.failures.append(f"{label}（{description}）")

            self.ready.set()
            msg = MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == WM_HOTKEY:
                    self.events.put((int(msg.wParam), int(user32.GetForegroundWindow())))
                else:
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            for hotkey_id in HOTKEYS:
                user32.UnregisterHotKey(None, hotkey_id)
            self.ready.set()

    def stop(self) -> None:
        if self.thread_id:
            user32.PostThreadMessageW(self.thread_id, WM_QUIT, 0, 0)


class TranslatorClient:
    def __init__(self) -> None:
        configured_env_path = os.environ.get("DISCORD_TRANSLATOR_ENV", "").strip()
        if configured_env_path:
            env_path = Path(configured_env_path).expanduser()
        elif DEFAULT_ENV_PATH.exists():
            env_path = DEFAULT_ENV_PATH
        elif LEGACY_ENV_PATH.exists():
            env_path = LEGACY_ENV_PATH
        else:
            env_path = DEFAULT_ENV_PATH
        file_env = load_dotenv(env_path)

        self.env_path = env_path
        self.api_key = (
            os.environ.get("OPENAI_API_KEY")
            or os.environ.get("AI_API_KEY")
            or file_env.get("OPENAI_API_KEY")
            or file_env.get("AI_API_KEY")
            or ""
        )
        self.default_model = (
            os.environ.get("OPENAI_MODEL")
            or os.environ.get("AI_MODEL")
            or file_env.get("OPENAI_MODEL")
            or file_env.get("AI_MODEL")
            or DEFAULT_ACCURATE_MODEL
        )
        self.accurate_model = (
            os.environ.get("ACCURATE_TRANSLATION_MODEL")
            or file_env.get("ACCURATE_TRANSLATION_MODEL")
            or self.default_model
            or DEFAULT_ACCURATE_MODEL
        )
        self.fast_model = (
            os.environ.get("FAST_TRANSLATION_MODEL")
            or file_env.get("FAST_TRANSLATION_MODEL")
            or DEFAULT_FAST_MODEL
        )
        initial_mode = (
            os.environ.get("TRANSLATION_MODEL_MODE")
            or file_env.get("TRANSLATION_MODEL_MODE")
            or ""
        ).strip().lower()
        if initial_mode not in {MODEL_MODE_ACCURATE, MODEL_MODE_FAST}:
            initial_mode = (
                MODEL_MODE_FAST
                if self.default_model == self.fast_model
                else MODEL_MODE_ACCURATE
            )
        self.model_mode = initial_mode
        self.model = self.resolve_model_for_mode(self.model_mode)
        base_url = (
            os.environ.get("OPENAI_BASE_URL")
            or os.environ.get("AI_API_BASE_URL")
            or file_env.get("OPENAI_BASE_URL")
            or file_env.get("AI_API_BASE_URL")
            or "https://api.openai.com/v1"
        )
        self.chat_url = normalize_chat_url(base_url)

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def resolve_model_for_mode(self, mode: str) -> str:
        if mode == MODEL_MODE_FAST:
            return self.fast_model
        return self.accurate_model

    def set_model_mode(self, mode: str) -> None:
        self.model_mode = (
            mode if mode in {MODEL_MODE_ACCURATE, MODEL_MODE_FAST} else MODEL_MODE_ACCURATE
        )
        self.model = self.resolve_model_for_mode(self.model_mode)

    def chat(self, messages: list[dict[str, str]], timeout: int = 90) -> str:
        if not self.api_key:
            raise RuntimeError(
                f"没有找到 OPENAI_API_KEY。请确认 {self.env_path} 存在，或设置环境变量。"
            )

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": CHAT_MAX_TOKENS,
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            self.chat_url,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"接口返回 HTTP {exc.code}: {body[:500]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"无法连接翻译接口: {exc.reason}") from exc

        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"接口返回格式不符合 chat/completions: {response_data}") from exc

    def translate_to_chinese(self, text: str) -> dict:
        messages = [
            {
                "role": "system",
                "content": (
                    "你是 Discord 聊天翻译助手。检测用户消息的主要语言，并翻译成简体中文。"
                    "只返回严格 JSON，不要 Markdown，不要解释。"
                    "JSON 字段：source_language_zh, source_language_en, translation_zh。"
                    "source_language_zh 使用中文语言名，例如 英语、日语、韩语、西班牙语、俄语。"
                    "如果原文已经是中文，也要返回 source_language_zh=中文。"
                ),
            },
            {"role": "user", "content": text},
        ]
        content = self.chat(messages)
        return extract_json_object(content)

    def translate_reply(self, text: str, target_language: str) -> dict:
        messages = [
            {
                "role": "system",
                "content": (
                    "你是 Discord 聊天翻译助手。把用户的中文消息翻译成指定目标语言，"
                    "语气自然、适合聊天，不要额外解释。只返回严格 JSON，不要 Markdown。"
                    "JSON 字段：target_language_zh, target_language_en, translation。"
                    "如果用户文本里包含 URL、代码、用户名、表情或命令，尽量原样保留。"
                ),
            },
            {
                "role": "user",
                "content": f"目标语言：{target_language}\n\n要翻译的中文消息：\n{text}",
            },
        ]
        content = self.chat(messages)
        return extract_json_object(content)


class FloatingTranslation:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.window: Toplevel | None = None
        self.body_text: Text | None = None

    def show(self, title: str, body: str, duration_ms: int = 14000) -> None:
        self.close()

        x, y = get_cursor_position()
        screen_width = self.root.winfo_screenwidth()
        width = 560
        xpos = min(max(12, x + 18), max(12, screen_width - width - 18))
        ypos = max(24, y + 24)

        window = Toplevel(self.root)
        window.overrideredirect(True)
        window.attributes("-topmost", True)
        window.configure(bg="#202225")

        container = Frame(window, bg="#202225", padx=12, pady=10)
        container.pack(fill=BOTH, expand=True)

        header = Frame(container, bg="#202225")
        header.pack(fill=X)
        Label(
            header,
            text=title,
            bg="#202225",
            fg="#b9bbbe",
            font=("Microsoft YaHei UI", 9, "bold"),
            anchor="w",
        ).pack(side=LEFT, fill=X, expand=True)
        Label(
            header,
            text="×",
            bg="#202225",
            fg="#dcddde",
            font=("Microsoft YaHei UI", 11, "bold"),
            cursor="hand2",
        ).pack(side=RIGHT)
        header.winfo_children()[-1].bind("<Button-1>", lambda _event: self.close())
        header.bind("<Button-1>", self._start_move)
        header.bind("<B1-Motion>", self._move)
        title_widget = header.winfo_children()[0]
        title_widget.configure(cursor="fleur")
        title_widget.bind("<Button-1>", self._start_move)
        title_widget.bind("<B1-Motion>", self._move)

        body_frame = Frame(container, bg="#202225")
        body_frame.pack(fill=BOTH, expand=True, pady=(7, 0))

        scrollbar = ttk.Scrollbar(body_frame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        body_text = Text(
            body_frame,
            bg="#202225",
            fg="#ffffff",
            wrap="word",
            font=("Microsoft YaHei UI", 10),
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            yscrollcommand=scrollbar.set,
        )
        body_text.pack(side=LEFT, fill=BOTH, expand=True)
        body_text.insert("1.0", body)
        body_text.configure(state="disabled")
        scrollbar.configure(command=body_text.yview)
        body_text.bind("<MouseWheel>", self._on_mousewheel)
        body_text.bind("<Button-4>", self._on_mousewheel)
        body_text.bind("<Button-5>", self._on_mousewheel)
        self.body_text = body_text

        window.bind("<Escape>", lambda _event: self.close())
        window.geometry(f"{width}x120+{xpos}+{ypos}")
        window.update_idletasks()
        height = min(max(window.winfo_reqheight(), 100), 360)
        window.geometry(f"{width}x{height}+{xpos}+{ypos}")
        display_duration_ms = max(duration_ms, min(30000, 12000 + len(body) * 18))
        window.after(display_duration_ms, lambda expected=window: self.close(expected))

        self.window = window

    def _on_mousewheel(self, event):
        if not self.body_text:
            return "break"
        if getattr(event, "delta", 0):
            step = -1 * int(event.delta / 120)
        elif getattr(event, "num", None) == 4:
            step = -1
        else:
            step = 1
        self.body_text.yview_scroll(step, "units")
        return "break"

    def _start_move(self, event) -> None:
        if not self.window:
            return
        self.window._drag_start = (event.x_root, event.y_root)
        self.window._drag_origin = (self.window.winfo_x(), self.window.winfo_y())

    def _move(self, event) -> None:
        if not self.window:
            return
        start_x, start_y = getattr(self.window, "_drag_start", (event.x_root, event.y_root))
        origin_x, origin_y = getattr(self.window, "_drag_origin", (self.window.winfo_x(), self.window.winfo_y()))
        self.window.geometry(f"+{origin_x + event.x_root - start_x}+{origin_y + event.y_root - start_y}")

    def close(self, expected: Toplevel | None = None) -> None:
        if self.window and (expected is None or expected is self.window):
            self.window.destroy()
            self.window = None
            self.body_text = None


class TranslatorApp:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("760x560")
        self.root.minsize(620, 420)

        self.client = TranslatorClient()
        self.last_source_language_en = ""
        self.last_source_language_zh = ""
        self.busy = False
        self.hotkey_events: queue.Queue[tuple[int, int]] = queue.Queue()
        self.hotkey_listener: HotkeyListener | None = None
        self.floating = FloatingTranslation(root)
        self.last_app_clipboard_text = ""
        self.last_app_clipboard_sequence = 0
        self.last_seen_clipboard_sequence = int(user32.GetClipboardSequenceNumber())
        self.last_auto_clipboard_text = ""
        self.reply_paste_hwnd = 0
        self.reply_prompt: Toplevel | None = None
        self.model_mode_var = StringVar()

        self.status_var = StringVar()
        self.detected_var = StringVar(value="尚未检测")
        self.reply_target_var = StringVar(value="自动：上次对方语言，否则 English")
        self.auto_copy_var = BooleanVar(value=True)
        self.auto_clipboard_var = BooleanVar(value=True)

        self._build_ui()
        self.model_mode_var.set(self.format_model_mode_label(self.client.model_mode))
        self._set_initial_status()
        self._start_hotkey_listener()
        self._poll_hotkey_events()
        self._poll_clipboard()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill=BOTH, expand=True)

        header = ttk.Frame(outer)
        header.pack(fill=X)

        ttk.Label(header, text=APP_TITLE, font=("Microsoft YaHei UI", 14, "bold")).pack(
            side=LEFT
        )
        ttk.Button(header, text="隐藏窗口", command=self.hide_window).pack(side=RIGHT)

        config = ttk.Frame(outer)
        config.pack(fill=X, pady=(10, 6))
        ttk.Label(config, text="回复目标：").pack(side=LEFT)
        target_box = ttk.Combobox(
            config,
            textvariable=self.reply_target_var,
            values=[
                "自动：上次对方语言，否则 English",
                "English",
                "Japanese",
                "Korean",
                "Spanish",
                "French",
                "German",
                "Russian",
                "Thai",
                "Vietnamese",
            ],
            width=36,
        )
        target_box.pack(side=LEFT, padx=(4, 14))
        ttk.Label(config, text="模式:").pack(side=LEFT)
        self.model_mode_box = ttk.Combobox(
            config,
            textvariable=self.model_mode_var,
            values=[
                self.format_model_mode_label(MODEL_MODE_ACCURATE),
                self.format_model_mode_label(MODEL_MODE_FAST),
            ],
            state="readonly",
            width=24,
        )
        self.model_mode_box.pack(side=LEFT, padx=(4, 14))
        self.model_mode_box.bind("<<ComboboxSelected>>", self.on_model_mode_changed)
        ttk.Checkbutton(config, text="翻译后自动复制", variable=self.auto_copy_var).pack(
            side=LEFT
        )
        ttk.Checkbutton(config, text="复制外语后自动翻译", variable=self.auto_clipboard_var).pack(
            side=LEFT, padx=(12, 0)
        )

        hotkeys = ttk.Frame(outer)
        hotkeys.pack(fill=X, pady=(0, 8))
        ttk.Label(hotkeys, text="Ctrl+C：复制外语后自动翻译").pack(side=LEFT)
        ttk.Label(hotkeys, text="    F8：弹出中文回复框").pack(
            side=LEFT
        )

        detected = ttk.Frame(outer)
        detected.pack(fill=X, pady=(0, 8))
        ttk.Label(detected, text="最近检测语言：").pack(side=LEFT)
        ttk.Label(detected, textvariable=self.detected_var).pack(side=LEFT)

        panes = ttk.PanedWindow(outer, orient="vertical")
        panes.pack(fill=BOTH, expand=True)

        original_frame = ttk.Labelframe(panes, text="原文")
        self.original_text = Text(original_frame, wrap="word", height=8, undo=False)
        self.original_text.pack(fill=BOTH, expand=True, padx=8, pady=8)
        panes.add(original_frame, weight=1)

        result_frame = ttk.Labelframe(panes, text="译文")
        self.result_text = Text(result_frame, wrap="word", height=10, undo=False)
        self.result_text.pack(fill=BOTH, expand=True, padx=8, pady=8)
        panes.add(result_frame, weight=2)

        actions = ttk.Frame(outer)
        actions.pack(fill=X, pady=(10, 6))
        ttk.Button(
            actions,
            text="剪贴板/选中文本 -> 中文",
            command=lambda: self.translate_selection_to_chinese(show_main=True),
        ).pack(side=LEFT)
        ttk.Button(
            actions,
            text="中文 -> 回复语言",
            command=lambda: self.translate_reply(show_main=True, paste_result=False),
        ).pack(side=LEFT, padx=(8, 0))
        ttk.Button(actions, text="复制译文", command=self.copy_current_result).pack(
            side=LEFT, padx=(8, 0)
        )

        ttk.Label(outer, textvariable=self.status_var).pack(fill=X, side=TOP)

    def _set_initial_status(self) -> None:
        if self.client.configured:
            self.status_var.set(
                f"已读取配置：{self.client.env_path}，模型：{self.client.model}"
            )
        else:
            self.status_var.set(
                f"未找到 OPENAI_API_KEY。当前会启动，但翻译前需要配置：{self.client.env_path}"
            )

    def format_model_mode_label(self, mode: str) -> str:
        if mode == MODEL_MODE_FAST:
            return f"极速模式 ({self.client.fast_model})"
        return f"准确模式 ({self.client.accurate_model})"

    def on_model_mode_changed(self, _event=None) -> None:
        selected = self.model_mode_var.get().strip()
        target_mode = (
            MODEL_MODE_FAST
            if selected == self.format_model_mode_label(MODEL_MODE_FAST)
            else MODEL_MODE_ACCURATE
        )
        self.client.set_model_mode(target_mode)
        self.model_mode_var.set(self.format_model_mode_label(self.client.model_mode))
        if self.client.configured:
            self.status_var.set(f"已切换翻译模式，当前模型：{self.client.model}")

    def _start_hotkey_listener(self) -> None:
        self.hotkey_listener = HotkeyListener(self.hotkey_events)
        self.hotkey_listener.start()
        self.hotkey_listener.ready.wait(timeout=2)
        if self.hotkey_listener.failures:
            messagebox.showwarning(
                APP_TITLE,
                "以下快捷键被其他程序占用，按钮仍可使用：\n"
                + "\n".join(self.hotkey_listener.failures),
            )

    def _poll_hotkey_events(self) -> None:
        try:
            while True:
                hotkey_id, source_hwnd = self.hotkey_events.get_nowait()
                self.handle_hotkey(hotkey_id, source_hwnd)
        except queue.Empty:
            pass
        self.root.after(80, self._poll_hotkey_events)

    def _poll_clipboard(self) -> None:
        current_sequence = int(user32.GetClipboardSequenceNumber())
        if current_sequence != self.last_seen_clipboard_sequence:
            self.last_seen_clipboard_sequence = current_sequence
            if self.auto_clipboard_var.get() and not self.busy and is_discord_foreground():
                text = self.normalize_input_text(self.read_clipboard())
                should_translate = (
                    text
                    and text != self.last_app_clipboard_text
                    and text != self.last_auto_clipboard_text
                    and not contains_cjk(text)
                    and not is_nontranslatable_code_block(text)
                    and len(text) >= 3
                )
                if should_translate:
                    self.last_auto_clipboard_text = text
                    self.translate_text_to_chinese(text, show_main=False)
        self.root.after(CLIPBOARD_POLL_INTERVAL_MS, self._poll_clipboard)

    def handle_hotkey(self, hotkey_id: int, source_hwnd: int = 0) -> None:
        if hotkey_id == HOTKEY_TRANSLATE_TO_CHINESE:
            self.translate_selection_to_chinese(show_main=False, source_hwnd=source_hwnd)
        elif hotkey_id == HOTKEY_TRANSLATE_REPLY:
            self.open_reply_prompt(source_hwnd)
        elif hotkey_id == HOTKEY_TOGGLE_WINDOW:
            if self.root.state() == "withdrawn":
                self.show_window()
            else:
                self.hide_window()

    def close(self) -> None:
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.floating.close()
        self.root.destroy()

    def read_clipboard(self) -> str:
        try:
            return self.root.clipboard_get()
        except Exception:
            return ""

    def write_clipboard(self, text: str, remember: bool = False) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update_idletasks()
        self.last_app_clipboard_sequence = int(user32.GetClipboardSequenceNumber())
        if remember:
            self.last_app_clipboard_text = text

    def focus_source_window(self, source_hwnd: int) -> None:
        if source_hwnd:
            user32.SetForegroundWindow(source_hwnd)
            time.sleep(0.12)

    def normalize_input_text(self, text: str) -> str:
        text = (text or "").strip()
        if len(text) > MAX_INPUT_CHARS:
            text = text[:MAX_INPUT_CHARS]
            self.status_var.set(f"文本过长，已截取前 {MAX_INPUT_CHARS} 个字符。")
        return text

    def read_after_copy(self, copy_action, source_hwnd: int = 0) -> str:
        previous = self.read_clipboard()
        sentinel = f"__DISCORD_TRANSLATOR_COPY_SENTINEL_{time.time_ns()}__"
        self.write_clipboard(sentinel)
        previous_sequence = int(user32.GetClipboardSequenceNumber())
        wait_for_hotkey_release()
        self.focus_source_window(source_hwnd)
        copy_action()

        if not wait_for_clipboard_change(previous_sequence, timeout=0.9):
            self.write_clipboard(previous)
            return ""

        text = sentinel
        for _ in range(6):
            text = self.read_clipboard()
            if text != sentinel:
                break
            time.sleep(0.03)

        if text == sentinel:
            self.write_clipboard(previous)
            return ""

        return self.normalize_input_text(text)

    def grab_selected_text(self, source_hwnd: int = 0) -> str:
        clipboard_text = self.normalize_input_text(self.read_clipboard())
        clipboard_sequence = int(user32.GetClipboardSequenceNumber())
        clipboard_looks_external = (
            clipboard_text
            and clipboard_text != self.last_app_clipboard_text
            and clipboard_sequence != self.last_app_clipboard_sequence
        )

        text = self.read_after_copy(send_ctrl_c, source_hwnd)
        if text:
            return text
        text = self.read_after_copy(send_ctrl_insert, source_hwnd)
        if text:
            return text
        return clipboard_text if clipboard_looks_external else ""

    def grab_clipboard_text(self) -> str:
        clipboard_text = self.normalize_input_text(self.read_clipboard())
        if clipboard_text and clipboard_text != self.last_app_clipboard_text:
            return clipboard_text
        return ""

    def trigger_copy_then_read_clipboard(self, source_hwnd: int = 0) -> str:
        previous_sequence = int(user32.GetClipboardSequenceNumber())
        wait_for_hotkey_release()
        self.focus_source_window(source_hwnd)
        send_alt_t()
        if wait_for_clipboard_change(previous_sequence):
            return self.grab_clipboard_text()
        return ""

    def grab_focused_draft_text(self, source_hwnd: int = 0) -> str:
        def select_all_then_copy() -> None:
            send_ctrl_a()
            time.sleep(0.08)
            send_ctrl_c()

        return self.read_after_copy(select_all_then_copy, source_hwnd)

    def show_problem(self, message: str, show_main: bool) -> None:
        self.status_var.set(message)
        if show_main:
            self.show_window()
        else:
            self.floating.show("翻译助手", message, duration_ms=5000)

    def set_text_widget(self, widget: Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", END)
        widget.insert("1.0", value)
        widget.configure(state="normal")

    def show_window(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(350, lambda: self.root.attributes("-topmost", False))

    def hide_window(self) -> None:
        self.root.withdraw()

    def open_reply_prompt(self, source_hwnd: int = 0) -> None:
        if self.reply_prompt:
            self.reply_prompt.destroy()
            self.reply_prompt = None

        self.reply_paste_hwnd = source_hwnd
        x, y = get_cursor_position()
        width = 560
        screen_width = self.root.winfo_screenwidth()
        xpos = min(max(12, x + 18), max(12, screen_width - width - 18))
        ypos = max(24, y + 24)

        prompt = Toplevel(self.root)
        prompt.title("回复翻译")
        prompt.attributes("-topmost", True)
        prompt.geometry(f"{width}x170+{xpos}+{ypos}")
        prompt.configure(bg="#202225")
        prompt.protocol("WM_DELETE_WINDOW", lambda: self.close_reply_prompt())

        container = Frame(prompt, bg="#202225", padx=12, pady=10)
        container.pack(fill=BOTH, expand=True)

        Label(
            container,
            text=f"输入中文，回车翻译成 {self.resolve_reply_target()} 并粘贴到 Discord",
            bg="#202225",
            fg="#b9bbbe",
            anchor="w",
            font=("Microsoft YaHei UI", 9, "bold"),
        ).pack(fill=X)

        entry = Text(
            container,
            wrap="word",
            height=4,
            bg="#2f3136",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            font=("Microsoft YaHei UI", 11),
        )
        entry.pack(fill=BOTH, expand=True, pady=(8, 8))

        footer = Frame(container, bg="#202225")
        footer.pack(fill=X)
        Label(
            footer,
            text="Enter 发送到翻译，Shift+Enter 换行，Esc 关闭",
            bg="#202225",
            fg="#8e9297",
            anchor="w",
            font=("Microsoft YaHei UI", 8),
        ).pack(side=LEFT, fill=X, expand=True)
        ttk.Button(footer, text="翻译并粘贴", command=lambda: self.submit_reply_prompt(entry)).pack(side=RIGHT)

        def on_return(event):
            if event.state & 0x0001:
                return None
            self.submit_reply_prompt(entry)
            return "break"

        entry.bind("<Return>", on_return)
        prompt.bind("<Escape>", lambda _event: self.close_reply_prompt())
        prompt.after(120, entry.focus_force)
        self.reply_prompt = prompt

    def close_reply_prompt(self) -> None:
        if self.reply_prompt:
            self.reply_prompt.destroy()
            self.reply_prompt = None

    def submit_reply_prompt(self, entry: Text) -> None:
        text = entry.get("1.0", END).strip()
        if not text:
            return
        if not contains_cjk(text):
            self.show_problem("输入内容不像中文，请输入中文后再翻译。", False)
            return
        self.close_reply_prompt()
        self.translate_reply_text(text, show_main=False, paste_result=True, source_hwnd=self.reply_paste_hwnd)

    def translate_selection_to_chinese(self, show_main: bool = False, source_hwnd: int = 0) -> None:
        if self.busy:
            return

        text = self.grab_clipboard_text()
        if not text:
            text = self.trigger_copy_then_read_clipboard(source_hwnd)
        if not text:
            self.show_problem("没有拿到消息。请先选中 Discord 消息并按 Ctrl+C，再按 Ctrl+Alt+T。", show_main)
            return

        self.translate_text_to_chinese(text, show_main)

    def translate_text_to_chinese(self, text: str, show_main: bool = False) -> None:
        if self.busy:
            return
        self._start_worker(
            "正在翻译成中文...",
            text,
            self._worker_to_chinese,
            show_main=show_main,
            paste_result=False,
        )

    def translate_reply_text(
        self,
        text: str,
        show_main: bool = False,
        paste_result: bool = True,
        source_hwnd: int = 0,
    ) -> None:
        if self.busy:
            return
        target = self.resolve_reply_target()
        self._start_worker(
            f"正在翻译成 {target}...",
            text,
            self._worker_reply,
            target,
            source_hwnd,
            show_main=show_main,
            paste_result=paste_result,
        )

    def translate_reply(
        self,
        show_main: bool = False,
        paste_result: bool = True,
        source_hwnd: int = 0,
    ) -> None:
        if self.busy:
            return

        text = self.grab_clipboard_text() if not paste_result else self.grab_focused_draft_text(source_hwnd)
        if not text:
            self.show_problem(
                "没有拿到中文。请先复制中文，再按 F8。",
                show_main,
            )
            return
        if not contains_cjk(text):
            self.show_problem(
                "当前读到的内容不像中文。请先复制你的中文回复，再按 F8。",
                show_main,
            )
            return

        target = self.resolve_reply_target()
        self._start_worker(
            f"正在翻译成 {target}...",
            text,
            self._worker_reply,
            target,
            source_hwnd,
            show_main=show_main,
            paste_result=paste_result,
        )

    def resolve_reply_target(self) -> str:
        selected = self.reply_target_var.get().strip()
        if selected.startswith("自动"):
            if self.last_source_language_en and self.last_source_language_en.lower() not in {
                "chinese",
                "simplified chinese",
                "traditional chinese",
                "unknown",
            }:
                return self.last_source_language_en
            return "English"
        return selected or "English"

    def _start_worker(
        self,
        status: str,
        text: str,
        func,
        *args,
        show_main: bool,
        paste_result: bool,
    ) -> None:
        self.busy = True
        self.status_var.set(status)
        self.set_text_widget(self.original_text, text)
        self.set_text_widget(self.result_text, "")
        if show_main:
            self.show_window()
        elif not paste_result:
            self.hide_window()
            self.floating.show("翻译中", status, duration_ms=6000)
        else:
            self.hide_window()

        thread = threading.Thread(target=func, args=(text, *args, show_main, paste_result), daemon=True)
        thread.start()

    def _worker_to_chinese(self, text: str, show_main: bool, paste_result: bool) -> None:
        try:
            result = self.client.translate_to_chinese(text)
            self.root.after(0, lambda: self._finish_to_chinese(result, show_main))
        except Exception as exc:
            self.root.after(0, lambda: self._finish_error(exc))

    def _worker_reply(
        self,
        text: str,
        target: str,
        source_hwnd: int,
        show_main: bool,
        paste_result: bool,
    ) -> None:
        try:
            result = self.client.translate_reply(text, target)
            self.root.after(0, lambda: self._finish_reply(result, show_main, paste_result, source_hwnd))
        except Exception as exc:
            self.root.after(0, lambda: self._finish_error(exc))

    def _finish_to_chinese(self, result: dict, show_main: bool) -> None:
        source_zh = str(result.get("source_language_zh") or "未知语言")
        source_en = str(result.get("source_language_en") or "Unknown")
        translation = str(result.get("translation_zh") or "").strip()

        if source_en.lower() not in {"unknown", "chinese", "simplified chinese", "traditional chinese"}:
            self.last_source_language_en = source_en
            self.last_source_language_zh = source_zh

        self.detected_var.set(f"{source_zh} ({source_en})")
        self.set_text_widget(
            self.result_text,
            f"检测语言：{source_zh} ({source_en})\n\n{translation}",
        )
        if self.auto_copy_var.get() and translation:
            self.write_clipboard(translation, remember=True)
            self.status_var.set("已翻译成中文，译文已复制。")
        else:
            self.status_var.set("已翻译成中文。")
        self.busy = False
        self.floating.show(f"{source_zh} ({source_en}) -> 中文", translation)
        if show_main:
            self.show_window()

    def _finish_reply(self, result: dict, show_main: bool, paste_result: bool, source_hwnd: int = 0) -> None:
        target_zh = str(result.get("target_language_zh") or "目标语言")
        target_en = str(result.get("target_language_en") or self.resolve_reply_target())
        translation = str(result.get("translation") or "").strip()

        self.set_text_widget(
            self.result_text,
            f"目标语言：{target_zh} ({target_en})\n\n{translation}",
        )
        if self.auto_copy_var.get() and translation:
            self.write_clipboard(translation, remember=True)
            if paste_result:
                time.sleep(0.12)
                self.focus_source_window(source_hwnd)
                send_ctrl_v()
                self.status_var.set("已翻译成回复语言，已尝试替换 Discord 里选中的中文。")
            else:
                self.status_var.set("已翻译成回复语言，译文已复制，可回到 Discord 粘贴发送。")
        else:
            self.status_var.set("已翻译成回复语言。")
        self.busy = False
        if paste_result:
            self.floating.show(
                f"已翻译成 {target_en}",
                "已复制并尝试粘贴到 Discord 输入框。",
                duration_ms=3000,
            )
        else:
            self.floating.show(f"已翻译成 {target_en}", translation, duration_ms=8000)
        if show_main:
            self.show_window()

    def _finish_error(self, exc: Exception) -> None:
        self.set_text_widget(self.result_text, f"翻译失败：\n{exc}")
        self.status_var.set("翻译失败。")
        self.busy = False
        self.show_window()

    def copy_current_result(self) -> None:
        text = self.result_text.get("1.0", END).strip()
        if not text:
            self.status_var.set("当前没有可复制的译文。")
            return

        lines = text.splitlines()
        if len(lines) >= 3 and lines[1].strip() == "":
            text = "\n".join(lines[2:]).strip()
        self.write_clipboard(text, remember=True)
        self.status_var.set("已复制译文。")


def main() -> int:
    if sys.platform != "win32":
        print("这个助手使用 Windows 全局快捷键 API，只支持 Windows。", file=sys.stderr)
        return 1

    mutex = kernel32.CreateMutexW(None, False, SINGLE_INSTANCE_MUTEX)
    if mutex and kernel32.GetLastError() == 183:
        return 0

    root = Tk()
    TranslatorApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
