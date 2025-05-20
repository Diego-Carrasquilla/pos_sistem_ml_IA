import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.constants import *
from pos_sistem.modules.sales.register_sale import register_sale
from pos_sistem.modules.inventory.list_products import list_products
from pos_sistem.ui.utils.custom_dialog import CustomDialog

class SalesRegisterView(ttk.Frame):
    def __init__(self, master, show_view, employee_id=2):
        super().__init__(master)
        self.show_view = show_view
        self.employee_id = employee_id
        self.items = []
        self.products = list_products()
        self.create_widgets()
        self.suggestion_box = tk.Listbox(self, height=5)
        self.suggestion_box.pack_forget()
        self.suggestion_box.bind("<<ListboxSelect>>", self.select_suggestion)

    def create_widgets(self):
        ttk.Label(self, text="🛒 Registro de Venta", font=("Segoe UI", 16)).pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="ID o Nombre Producto").grid(row=0, column=0, padx=5, pady=5)
        self.entry_product = ttk.Entry(form_frame)
        self.entry_product.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="Cantidad").grid(row=0, column=2, padx=5)
        self.entry_quantity = ttk.Entry(form_frame, width=5)
        self.entry_quantity.grid(row=0, column=3, padx=5)

        ttk.Button(form_frame, text="➕ Agregar", bootstyle="success", command=self.add_item).grid(row=0, column=4, padx=5)

        # suggestion box
        self.entry_product.bind("<KeyRelease>", self.update_suggestions)
        self.entry_product.bind("<FocusOut>", lambda e: self.after(100, self.suggestion_box.place_forget))


        columns = ("id", "name", "quantity", "unit_price", "subtotal")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10, bootstyle="info")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center", stretch=True)
        self.tree.pack(padx=10, pady=5, fill="x")

        self.label_total = ttk.Label(self, text="💰 Total: $0.00", font=("Segoe UI", 14))
        self.label_total.pack(pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✅ Confirmar Venta", bootstyle="primary", command=self.confirm_sale).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="❌ Cancelar", bootstyle="danger", command=self.clear_sale).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="⬅ Volver", bootstyle="secondary", command=lambda: self.show_view("main")).grid(row=0, column=2, padx=10)

    def add_item(self):
        name_or_id = self.entry_product.get().strip()
        quantity = self.entry_quantity.get().strip()

        if not name_or_id or not quantity.isdigit():
            CustomDialog(self, "Datos inválidos", "Ingresa un ID/nombre válido y cantidad numérica.", dialog_type="warning")
            return

        quantity = int(quantity)
        found = None
        for p in self.products:
            if name_or_id.lower() == str(p['id']).lower() or name_or_id.lower() in p['name'].lower():
                found = p
                break

        if not found:
            CustomDialog(self, "No encontrado", f"No se encontró el producto '{name_or_id}'.", dialog_type="error")
            return
        if found["stock"] < quantity:
            CustomDialog(self, "Stock insuficiente", f"Solo hay {found['stock']} unidades disponibles.", dialog_type="warning")
            return

        subtotal = found['sale_price'] * quantity
        self.items.append({
            "product_id": found['id'],
            "name": found['name'],
            "quantity": quantity,
            "unit_price": found['sale_price'],
            "subtotal": subtotal
        })

        self.tree.insert("", "end", values=(found['id'], found['name'], quantity, f"${found['sale_price']:.2f}", f"${subtotal:.2f}"))
        self.update_total()
        self.entry_product.delete(0, "end")
        self.entry_quantity.delete(0, "end")

    def update_total(self):
        total = sum(item["subtotal"] for item in self.items)
        self.label_total.config(text=f"💰 Total: ${total:.2f}")

    def confirm_sale(self):
        if not self.items:
            CustomDialog(self, "Vacío", "No has agregado productos.", dialog_type="warning")
            return

        try:
            register_sale(self.employee_id, self.items)
            CustomDialog(self, "Venta Exitosa", "La venta fue registrada correctamente.", dialog_type="success")
            self.clear_sale()
        except Exception as e:
            CustomDialog(self, "Error", f"Ocurrió un error: {e}", dialog_type="error")

    def clear_sale(self):
        self.items = []
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.label_total.config(text="💰 Total: $0.00")

    def update_suggestions(self, event):
        typed = self.entry_product.get().lower()
        matches = [p["name"] for p in self.products if typed in p["name"].lower()]

        if matches and typed:
            self.suggestion_box.delete(0, tk.END)
            for match in matches:
                self.suggestion_box.insert(tk.END, match)
            self.suggestion_box.place(x=self.entry_product.winfo_rootx() - self.winfo_rootx(),
                                      y=self.entry_product.winfo_rooty() - self.winfo_rooty() + 25,
                                      width=self.entry_product.winfo_width())
            self.suggestion_box.lift()
        else:
            self.suggestion_box.place_forget()

    def select_suggestion(self, event):
        if not self.suggestion_box.curselection():
            return
        selected = self.suggestion_box.get(self.suggestion_box.curselection())
        self.entry_product.delete(0, tk.END)
        self.entry_product.insert(0, selected)
        self.suggestion_box.place_forget()


