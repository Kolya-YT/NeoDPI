import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import customtkinter as ctk
from core import preferences, proxy
from core.updater import check_update, download_and_install, CURRENT_VERSION
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from ui.cmd_editor import CmdEditorWindow
from ui.tray import start_tray

class UpdateDialog(ctk.CTkToplevel):
    def __init__(self, master, version, url):
        super().__init__(master)
        self.title("Обновление")
        self.geometry("340x180")
        self.resizable(False, False)
        self.grab_set()
        self._url = url
        self._build(version)

    def _build(self, version):
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text=f"Доступна новая версия {version}!",
                     font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=(20, 4))
        ctk.CTkLabel(self, text=f"Текущая версия: {CURRENT_VERSION}",
                     text_color="gray").grid(row=1, column=0, pady=(0, 16))

        self.progress = ctk.CTkProgressBar(self, width=280)
        self.progress.set(0)
        self.progress.grid(row=2, column=0, padx=20, pady=(0, 12))
        self.progress.grid_remove()

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=4, column=0, padx=20, pady=12, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.update_btn = ctk.CTkButton(btn_frame, text="Обновить", command=self._start_update)
        self.update_btn.grid(row=0, column=0, padx=(0, 4), sticky="ew")
        ctk.CTkButton(btn_frame, text="Позже", fg_color="gray",
                      command=self.destroy).grid(row=0, column=1, padx=(4, 0), sticky="ew")

    def _start_update(self):
        self.update_btn.configure(state="disabled", text="Скачивание...")
        self.progress.grid()

        def on_progress(pct):
            self.after(0, lambda: self.progress.set(pct / 100))
            if pct >= 100:
                self.after(0, lambda: self.status_label.configure(text="Перезапуск..."))

        download_and_install(self._url, on_progress=on_progress)


class App(ctk.CTk):
    def __init__(self):
        self.prefs = preferences.load()
        ctk.set_appearance_mode(self.prefs.get("theme", "dark"))
        ctk.set_default_color_theme("blue")

        super().__init__()
        self.title("NeoDPI")
        self.geometry("360x280")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = MainWindow(
            self,
            on_settings=self._open_settings,
            on_editor=self._open_editor,
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self._tray = start_tray(self, on_show=self._show_window, on_quit=self._quit)

        if self.prefs.get("autostart") and not proxy.is_running():
            p = self.prefs
            proxy.start(p["proxy_ip"], p["proxy_port"], p.get("cmd_args", ""))
            self.main_frame.refresh()

        # Check for updates after 3 seconds
        self.after(3000, lambda: check_update(self._on_update_available))

    def _on_update_available(self, version, url):
        self.after(0, lambda: UpdateDialog(self, version, url))

    def _open_settings(self):
        SettingsWindow(self, on_save=self.main_frame.refresh)

    def _open_editor(self):
        CmdEditorWindow(self, on_apply=self.main_frame.refresh)

    def _on_close(self):
        if self._tray:
            self.withdraw()
        else:
            self._quit()

    def _show_window(self):
        self.deiconify()
        self.lift()

    def _quit(self):
        proxy.stop()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
