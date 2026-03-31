import customtkinter as ctk
from core import preferences

class CmdEditorWindow(ctk.CTkToplevel):
    def __init__(self, master, on_apply=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Редактор командной строки")
        self.geometry("560x520")
        self.grab_set()
        self.on_apply = on_apply
        self.prefs = preferences.load()
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Args input
        ctk.CTkLabel(self, text="Аргументы командной строки:").grid(
            row=0, column=0, padx=16, pady=(16, 4), sticky="w"
        )
        self.args_entry = ctk.CTkTextbox(self, height=80)
        self.args_entry.insert("1.0", self.prefs.get("cmd_args", ""))
        self.args_entry.grid(row=1, column=0, padx=16, sticky="ew")

        # Buttons row
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=16, pady=8, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(btn_frame, text="Применить", command=self._apply).grid(
            row=0, column=0, padx=(0, 4), sticky="ew"
        )
        ctk.CTkButton(btn_frame, text="Сохранить в историю", command=self._save_to_history).grid(
            row=0, column=1, padx=4, sticky="ew"
        )
        ctk.CTkButton(btn_frame, text="Очистить", fg_color="gray", command=self._clear).grid(
            row=0, column=2, padx=(4, 0), sticky="ew"
        )

        # History
        ctk.CTkLabel(self, text="История стратегий:").grid(
            row=3, column=0, padx=16, pady=(8, 4), sticky="w"
        )

        self.history_frame = ctk.CTkScrollableFrame(self, height=240)
        self.history_frame.grid(row=4, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self._refresh_history()

    def _refresh_history(self):
        for w in self.history_frame.winfo_children():
            w.destroy()

        history = preferences.load().get("history", [])
        for i, item in enumerate(history):
            name = item.get("name") or item.get("text", "")[:40]
            pinned = item.get("pinned", False)
            label = ("📌 " if pinned else "") + name

            row = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            row.grid(row=i, column=0, sticky="ew", pady=2)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(
                row, text=label, anchor="w",
                fg_color=("gray85", "gray25"),
                text_color=("black", "white"),
                command=lambda t=item["text"]: self._load_cmd(t)
            ).grid(row=0, column=0, sticky="ew")

            ctk.CTkButton(
                row, text="✕", width=32, fg_color="transparent",
                text_color=("gray40", "gray60"),
                command=lambda t=item["text"]: self._delete_cmd(t)
            ).grid(row=0, column=1, padx=(4, 0))

    def _load_cmd(self, text: str):
        self.args_entry.delete("1.0", "end")
        self.args_entry.insert("1.0", text)

    def _apply(self):
        args = self.args_entry.get("1.0", "end").strip()
        p = preferences.load()
        p["cmd_args"] = args
        preferences.save(p)
        if self.on_apply:
            self.on_apply()
        self.destroy()

    def _save_to_history(self):
        args = self.args_entry.get("1.0", "end").strip()
        if not args:
            return
        p = preferences.load()
        history = p.get("history", [])
        if not any(h["text"] == args for h in history):
            history.insert(0, {"text": args, "pinned": False, "name": None})
            if len(history) > 40:
                history = [h for h in history if h["pinned"]] + \
                          [h for h in history if not h["pinned"]][:40]
        p["history"] = history
        preferences.save(p)
        self._refresh_history()

    def _delete_cmd(self, text: str):
        p = preferences.load()
        p["history"] = [h for h in p.get("history", []) if h["text"] != text]
        preferences.save(p)
        self._refresh_history()

    def _clear(self):
        self.args_entry.delete("1.0", "end")
