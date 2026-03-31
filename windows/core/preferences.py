import json
import os

PREFS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "preferences.json")
STRATEGIES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               "app", "src", "main", "assets", "proxytest_strategies.list")

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
    history = [{"text": "-K t,h -s1 -d1 -a1 -At,r,s -f-1 -r1+s -a1", "pinned": True, "name": "Telegram"}]
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
