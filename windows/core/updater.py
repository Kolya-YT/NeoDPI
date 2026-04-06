import threading
import urllib.request
import json
import os
import sys
import subprocess

GITHUB_API = "https://api.github.com/repos/Kolya-YT/NeoDPI/releases/latest"

def _get_current_version() -> str:
    # Try VERSION file next to exe or in bundle
    candidates = []
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(os.path.dirname(sys.executable), "VERSION"))
        candidates.append(os.path.join(sys._MEIPASS, "VERSION"))
    else:
        candidates.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION"))
    for path in candidates:
        if os.path.exists(path):
            return open(path).read().strip()
    return "1.0.7"

CURRENT_VERSION = _get_current_version()

def _get_latest() -> dict | None:
    try:
        req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "NeoDPI"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return None

def _version_tuple(v: str):
    try:
        return tuple(int(x) for x in v.lstrip("v").split("."))
    except Exception:
        return (0,)

def check_update(on_update_available):
    def _check():
        data = _get_latest()
        if not data:
            return
        latest = data.get("tag_name", "").lstrip("v")
        if not latest:
            return
        if _version_tuple(latest) > _version_tuple(CURRENT_VERSION):
            url = data.get("html_url", "")
            exe_url = None
            for asset in data.get("assets", []):
                if asset["name"].lower().endswith(".exe"):
                    exe_url = asset["browser_download_url"]
                    break
            on_update_available(latest, exe_url or url)

    threading.Thread(target=_check, daemon=True).start()

def download_and_replace(url: str, on_progress=None, on_done=None, on_error=None):
    def _download():
        try:
            if getattr(sys, 'frozen', False):
                current_exe = sys.executable
            else:
                on_error and on_error("Обновление доступно только для EXE версии")
                return

            dest = current_exe + ".new"
            req = urllib.request.Request(url, headers={"User-Agent": "NeoDPI"})
            with urllib.request.urlopen(req) as r:
                total = int(r.headers.get("Content-Length", 0))
                downloaded = 0
                with open(dest, "wb") as f:
                    while True:
                        chunk = r.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if on_progress and total:
                            on_progress(int(downloaded / total * 100))

            # Batch script to replace exe and restart
            bat = current_exe + "_update.bat"
            with open(bat, "w") as f:
                f.write(
                    f'@echo off\n'
                    f'timeout /t 2 /nobreak >nul\n'
                    f'move /y "{dest}" "{current_exe}"\n'
                    f'start "" "{current_exe}"\n'
                    f'del "%~f0"\n'
                )
            subprocess.Popen(["cmd", "/c", bat], creationflags=subprocess.CREATE_NO_WINDOW)
            on_done and on_done()

        except Exception as e:
            on_error and on_error(str(e))

    threading.Thread(target=_download, daemon=True).start()
