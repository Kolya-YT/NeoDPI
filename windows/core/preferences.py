import json
import os
import sys

if getattr(sys, 'frozen', False):
    # Running as PyInstaller EXE — save prefs next to the exe
    _PREFS_DIR = os.path.dirname(sys.executable)
else:
    _PREFS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

PREFS_FILE = os.path.join(_PREFS_DIR, "neodpi_preferences.json")

# Support both PyInstaller bundle and normal run
if getattr(sys, 'frozen', False):
    # Running as PyInstaller EXE
    _BASE = sys._MEIPASS
    STRATEGIES_FILE = os.path.join(_BASE, "assets", "proxytest_strategies.list")
    BYEDPI_EXE = os.path.join(_BASE, "bin", "byedpi.exe")
else:
    _BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    STRATEGIES_FILE = os.path.join(_BASE, "app", "src", "main", "assets", "proxytest_strategies.list")
    BYEDPI_EXE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "byedpi.exe")

DEFAULTS = {
    "proxy_ip": "127.0.0.1",
    "proxy_port": "1080",
    "cmd_args": "",
    "use_cmd": False,
    "autostart": False,
    "theme": "dark",
    "history": None,  # None = not initialized yet
}

def _ensure_dir():
    os.makedirs(os.path.dirname(PREFS_FILE), exist_ok=True)

def _load_default_history() -> list:
    history = [
        {"text": "-K t,h -s1 -d1 -a1 -At,r,s -f-1 -r1+s -a1", "pinned": True, "name": "Telegram"},
        {"text": "-f1+nme -t6 -s1:6+sm -a1 -As -s5:12+sm -a1 -As -d3 -q7 -r6 -Mh -a1", "pinned": True, "name": "YouTube"},
        {"text": "-Qr -f-204 -K t,h -s1:5+sm -a1 -As -d1 -s3+s -s5+s -q7 -a1 -As -o2 -f-43 -a1", "pinned": True, "name": "Discord"},
        {"text": "-f-200 -Qr -s3:5+sm -a1 -As -d1 -s4+sm -s8+sh -f-300 -d6+sh -a1 -At,r,s -o2 -f-30 -As -r5 -Mh -r6+sh -f-250 -s2:7+s -s3:6+sm -a1", "pinned": True, "name": "Универсальная"},
    ]
    try:
        if os.path.exists(STRATEGIES_FILE):
            with open(STRATEGIES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not any(h["text"] == line for h in history):
                        history.append({"text": line, "pinned": False, "name": None})
    except Exception:
        pass
    return history

def load() -> dict:
    _ensure_dir()
    if not os.path.exists(PREFS_FILE):
        prefs = {**DEFAULTS, "history": _load_default_history()}
        save(prefs)
        return prefs
    try:
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # First launch migration: history was None or missing
        if data.get("history") is None:
            data["history"] = _load_default_history()
            save(data)
        return {**DEFAULTS, **data}
    except Exception:
        return {**DEFAULTS, "history": _load_default_history()}

def save(prefs: dict):
    _ensure_dir()
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)
