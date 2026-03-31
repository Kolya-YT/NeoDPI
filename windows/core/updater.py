import threading
import urllib.request
import json
import os
import sys
import subprocess

GITHUB_API = "https://api.github.com/repos/Kolya-YT/NeoDPI/releases/latest"
CURRENT_VERSION = "1.0.6"

def _get_latest() -> dict | None:
    try:
        req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "NeoDPI"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return None

def _version_tuple(v: str):
    return tuple(int(x) for x in v.lstrip("v").split("."))

def check_update(on_update_available):
    """Check for updates in background thread. Calls on_update_available(version, url) if found."""
    def _check():
        data = _get_latest()
        if not data:
            return
        latest = data.get("tag_name", "").lstrip("v")
        if not latest:
            return
        try:
            if _version_tuple(latest) > _version_tuple(CURRENT_VERSION):
                # Find Windows EXE asset
                url = None
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        url = asset["browser_download_url"]
                        break
                on_update_available(latest, url or data.get("html_url", ""))
        except Exception:
            pass

    threading.Thread(target=_check, daemon=True).start()

def download_and_install(url: str, on_progress=None):
    """Download new EXE and replace current one."""
    def _download():
        try:
            dest = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "NeoDPI_new.exe")
            req = urllib.request.Request(url, headers={"User-Agent": "NeoDPI"})
            with urllib.request.urlopen(req) as r:
                total = int(r.headers.get("Content-Length", 0))
                downloaded = 0
                chunk = 8192
                with open(dest, "wb") as f:
                    while True:
                        data = r.read(chunk)
                        if not data:
                            break
                        f.write(data)
                        downloaded += len(data)
                        if on_progress and total:
                            on_progress(int(downloaded / total * 100))

            # Replace current exe with new one via batch script
            current = sys.executable if getattr(sys, 'frozen', False) else dest
            bat = dest + "_update.bat"
            with open(bat, "w") as f:
                f.write(f'@echo off\ntimeout /t 2 /nobreak >nul\nmove /y "{dest}" "{current}"\nstart "" "{current}"\ndel "%~f0"\n')
            subprocess.Popen(["cmd", "/c", bat], creationflags=subprocess.CREATE_NO_WINDOW)
            if on_progress:
                on_progress(100)
        except Exception as e:
            print(f"[updater] Download failed: {e}")

    threading.Thread(target=_download, daemon=True).start()
