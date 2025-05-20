import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Toplevel

class CustomDialog(Toplevel):
    def __init__(self, master, title, message, dialog_type="info"):
        super().__init__(master)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.style = ttk.Style()
        self.icon_map = {
            "info": "🛈",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=self.icon_map.get(dialog_type, "ℹ️"), font=("Segoe UI", 28)).pack()
        ttk.Label(frame, text=message, font=("Segoe UI", 12), wraplength=350).pack(pady=10)

        ttk.Button(frame, text="Aceptar", bootstyle="primary", command=self.destroy).pack(pady=10)
