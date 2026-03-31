import customtkinter as ctk
from core import proxy, preferences

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, on_settings, on_editor, **kwargs):
        super().__init__(master, **kwargs)
        self.on_settings = on_settings
        self.on_editor = on_editor
        self.prefs = preferences.load()
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)

        # Status card
        self.status_card = ctk.CTkFrame(self, corner_radius=16, fg_color=("#5976DF", "#5976DF"))
        self.status_card.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.status_card.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.status_card, text="Отключено",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="white"
        )
        self.status_label.grid(row=0, column=0, pady=(16, 4))

        self.proxy_addr_label = ctk.CTkLabel(
            self.status_card, text=self._proxy_addr(),
            font=ctk.CTkFont(size=12), text_color="white"
        )
        self.proxy_addr_label.grid(row=1, column=0, pady=(0, 16))

        # Toggle button
        self.toggle_btn = ctk.CTkButton(
            self, text="Старт", height=48,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._toggle
        )
        self.toggle_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Bottom buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="⚙ Настройки", command=self.on_settings).grid(
            row=0, column=0, padx=(0, 5), sticky="ew"
        )
        ctk.CTkButton(btn_frame, text="✎ Редактор", command=self.on_editor).grid(
            row=0, column=1, padx=(5, 0), sticky="ew"
        )

    def _proxy_addr(self):
        p = preferences.load()
        return f"{p['proxy_ip']}:{p['proxy_port']}"

    def _toggle(self):
        if proxy.is_running():
            proxy.stop()
            self._set_stopped()
        else:
            p = preferences.load()
            # Always use cmd_args if set, use_cmd just controls whether settings are editable
            args = p.get("cmd_args", "")
            ok = proxy.start(p["proxy_ip"], p["proxy_port"], args)
            if ok:
                self._set_running()
            else:
                self._set_stopped(error=True)

    def _set_running(self):
        self.status_label.configure(text="Подключено (Proxy)")
        self.status_card.configure(fg_color=("#2e7d32", "#2e7d32"))
        self.toggle_btn.configure(text="Стоп", fg_color=("#c62828", "#c62828"))
        self.proxy_addr_label.configure(text=self._proxy_addr())

    def _set_stopped(self, error=False):
        self.status_label.configure(text="Ошибка запуска" if error else "Отключено")
        self.status_card.configure(fg_color=("#c62828", "#c62828") if error else ("#5976DF", "#5976DF"))
        self.toggle_btn.configure(text="Старт", fg_color=("#1f538d", "#1f538d"))

    def refresh(self):
        self.proxy_addr_label.configure(text=self._proxy_addr())
        if proxy.is_running():
            self._set_running()
        else:
            self._set_stopped()
