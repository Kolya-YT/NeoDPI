import subprocess
import shlex
import os
import sys
import time
import threading
import winreg
import ctypes

if getattr(sys, 'frozen', False):
    BYEDPI_EXE = os.path.join(sys._MEIPASS, "bin", "byedpi.exe")
    STRATEGIES_FILE = os.path.join(sys._MEIPASS, "assets", "proxytest_strategies.list")
else:
    BYEDPI_EXE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "byedpi.exe")
    STRATEGIES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "app", "src", "main", "assets", "proxytest_strategies.list")

_process: subprocess.Popen | None = None


def is_running() -> bool:
    return _process is not None and _process.poll() is None


def _load_strategies() -> list:
    strategies = []
    if os.path.exists(STRATEGIES_FILE):
        with open(STRATEGIES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    strategies.append(line)
    return strategies


def _build_auto_args(strategies: list) -> list:
    if not strategies:
        return []
    args = []
    try:
        args += shlex.split(strategies[0])
    except ValueError:
        args += strategies[0].split()
    for strategy in strategies[1:]:
        args += ["-A", "t,r,s"]
        try:
            args += shlex.split(strategy)
        except ValueError:
            args += strategy.split()
    return args


def _set_system_proxy(ip: str, port: str, enable: bool):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_SET_VALUE
        )
        if enable:
            proxy_str = f"socks={ip}:{port}"
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy_str)
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ,
                              "localhost;127.*;10.*;172.16.*;192.168.*;<local>")
            print(f"[proxy] System proxy enabled: {proxy_str}")
        else:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "")
            print("[proxy] System proxy disabled")
        winreg.CloseKey(key)
        ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)
        ctypes.windll.wininet.InternetSetOptionW(0, 37, 0, 0)
    except Exception as e:
        print(f"[proxy] Failed to set system proxy: {e}")


def start(ip: str, port: str, extra_args: str = "") -> bool:
    global _process
    if is_running():
        return True

    cmd = [BYEDPI_EXE, "-i", ip, "-p", port]

    if extra_args.strip():
        try:
            cmd += shlex.split(extra_args)
        except ValueError:
            cmd += extra_args.split()
    else:
        strategies = _load_strategies()[:10]
        if strategies:
            cmd += _build_auto_args(strategies)
            print(f"[proxy] Auto mode: {len(strategies)} strategies")
        else:
            print("[proxy] No strategies found")

    print(f"[proxy] Starting: {' '.join(cmd[:8])}{'...' if len(cmd) > 8 else ''}")

    try:
        _process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )

        def _log(stream, prefix):
            for line in stream:
                print(f"[byedpi {prefix}] {line.decode(errors='replace').rstrip()}")

        threading.Thread(target=_log, args=(_process.stdout, "out"), daemon=True).start()
        threading.Thread(target=_log, args=(_process.stderr, "err"), daemon=True).start()

        time.sleep(0.4)
        if _process.poll() is not None:
            print(f"[proxy] Exited immediately with code {_process.returncode}")
            return False

        print(f"[proxy] Started OK (pid={_process.pid})")
        _set_system_proxy(ip, port, True)
        return True
    except Exception as e:
        print(f"[proxy] Failed to start: {e}")
        return False


def stop():
    global _process
    _set_system_proxy("", "", False)
    if _process and _process.poll() is None:
        _process.terminate()
        try:
            _process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _process.kill()
    _process = None
    print("[proxy] Stopped")
