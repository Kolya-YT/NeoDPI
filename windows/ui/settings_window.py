import customtkinter as ctk
from core import preferences

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, on_save=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Настройки")
        self.geometry("400x280")
        self.resizable(False, False)
        self.grab_set()
        self.on_save = on_save
        self.prefs = preferences.load()
        self._build()

    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        pad = {"padx": 20, "pady": 8}

        ctk.CTkLabel(self, text="IP прокси:").grid(row=0, column=0, sticky="w", **pad)
        self.ip_entry = ctk.CTkEntry(self)
        self.ip_entry.insert(0, self.prefs["proxy_ip"])
        self.ip_entry.grid(row=0, column=1, sticky="ew", **pad)

        ctk.CTkLabel(self, text="Порт:").grid(row=1, column=0, sticky="w", **pad)
        self.port_entry = ctk.CTkEntry(self)
        self.port_entry.insert(0, self.prefs["proxy_port"])
        self.port_entry.grid(row=1, column=1, sticky="ew", **pad)

        ctk.CTkLabel(self, text="Тема:").grid(row=2, column=0, sticky="w", **pad)
        self.theme_var = ctk.StringVar(value=self.prefs["theme"])
        ctk.CTkOptionMenu(self, values=["dark", "light", "system"], variable=self.theme_var).grid(
            row=2, column=1, sticky="ew", **pad
        )

        ctk.CTkLabel(self, text="Автозапуск:").grid(row=3, column=0, sticky="w", **pad)
        self.autostart_var = ctk.BooleanVar(value=self.prefs["autostart"])
        ctk.CTkSwitch(self, variable=self.autostart_var, text="").grid(row=3, column=1, sticky="w", **pad)

        ctk.CTkButton(self, text="Сохранить", command=self._save).grid(
            row=4, column=0, columnspan=2, padx=20, pady=16, sticky="ew"
        )

    def _save(self):
        p = preferences.load()
        p["proxy_ip"] = self.ip_entry.get().strip()
        p["proxy_port"] = self.port_entry.get().strip()
        p["theme"] = self.theme_var.get()
        p["autostart"] = self.autostart_var.get()
        preferences.save(p)
        ctk.set_appearance_mode(p["theme"])
        self._set_autostart(p["autostart"])
        if self.on_save:
            self.on_save()
        self.destroy()

    def _set_autostart(self, enable: bool):
        import sys, winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "NeoDPI"
        exe = sys.executable
        script = __file__.replace("ui\\settings_window.py", "main.py")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if enable:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{exe}" "{script}"')
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Autostart error: {e}")
