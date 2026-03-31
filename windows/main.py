import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import customtkinter as ctk
from core import preferences, proxy
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from ui.cmd_editor import CmdEditorWindow
from ui.tray import start_tray

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
            proxy.start(p["proxy_ip"], p["proxy_port"], p["cmd_args"] if p["use_cmd"] else "")
            self.main_frame.refresh()

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
