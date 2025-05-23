import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Frame, ScrolledText
import threading
import requests
import os
from pos_sistem.modules.sales.sales_helper_ai import generate_prompt_for_question


API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-Title": "Prueba Asistente AI"
}

payload = {
    "model": "tngtech/deepseek-r1t-chimera:free",
    "messages": [
        {"role": "user", "content": "Hola, ¿quién eres?"}
    ]
}


class AssistantAIView(Frame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.show_view = show_view
        self.pack(fill="both", expand=True)
        self.init_ui()

    def init_ui(self):
        # Header
        header = ttk.Frame(self)
        header.pack(side="top", fill="x", pady=10, padx=10)

        title = ttk.Label(header, text="🤖 Asistente AI", font=("Helvetica", 18, "bold"))
        title.pack(side="left")

        back_button = ttk.Button(header, text="Volver al menú", command=lambda: self.show_view("main"), bootstyle="secondary")
        back_button.pack(side="right")

        # Chat display
        self.chat_display = ScrolledText(self, wrap="word", font=("Consolas", 10))
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.chat_display.configure(state="disabled")

        # Entrada del usuario
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        send_button = ttk.Button(input_frame, text="Enviar", command=self.send_message, bootstyle="primary")
        send_button.pack(side="right")

    def send_message(self):
        user_message = self.input_entry.get().strip()
        if not user_message:
            return
        self.display_message("Tú", user_message)
        self.input_entry.delete(0, tk.END)
        threading.Thread(target=self.get_response, args=(user_message,), daemon=True).start()

    def get_response(self, user_input):
        try:
            enriched_prompt = generate_prompt_for_question(user_input)

            payload = {
                "model": "tngtech/deepseek-r1t-chimera:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente útil para soporte interno del sistema POS. Usa la información de contexto provista para responder con precisión."
                    },
                    {
                        "role": "user",
                        "content": enriched_prompt
                    }
                ]
            }

            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
            ai_message = data["choices"][0]["message"]["content"]

        except Exception as e:
            ai_message = f"Error al obtener respuesta: {str(e)}"

        self.display_message("AI", ai_message)


    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}:\n{message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview_moveto(1.0)
