import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pos_sistem.modules.inventory.add_product import add_product  
from pos_sistem.ui.utils.custom_dialog import CustomDialog


class RegisterProductView(ttk.Frame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.show_view = show_view
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="🆕 Registrar Producto", font=("Segoe UI", 16)).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        # Nombre
        ttk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.name_entry = ttk.Entry(form, width=40)
        self.name_entry.grid(row=0, column=1)

        # Descripción
        ttk.Label(form, text="Descripción:").grid(row=1, column=0, sticky="e")
        self.description_entry = ttk.Entry(form, width=40)
        self.description_entry.grid(row=1, column=1)

        # Precio
        ttk.Label(form, text="Precio Venta:").grid(row=2, column=0, sticky="e")
        self.price_entry = ttk.Entry(form, width=40)
        self.price_entry.grid(row=2, column=1)

        # Stock
        ttk.Label(form, text="Stock Inicial:").grid(row=3, column=0, sticky="e")
        self.stock_entry = ttk.Entry(form, width=40)
        self.stock_entry.grid(row=3, column=1)

        # Botones
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="💾 Guardar", bootstyle="success", command=self.save_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅ Volver", bootstyle="secondary", command=lambda: self.show_view("inventory")).pack(side="left", padx=5)

    def save_product(self):
        name = self.name_entry.get().strip()
        desc = self.description_entry.get().strip()
        try:
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())
        except ValueError:
            CustomDialog(self, "Error", "Precio o stock no válidos", dialog_type="error")
            return

        if not name or price < 0 or stock < 0:
            CustomDialog(self, "Error", "Datos incompletos o inválidos", dialog_type="error")
            return

        product_id = add_product(name, desc, price, stock)
        if product_id:
            CustomDialog(self, "Éxito", f"Producto guardado con ID {product_id}", dialog_type="success")
            self.name_entry.delete(0, "end")
            self.description_entry.delete(0, "end")
            self.price_entry.delete(0, "end")
            self.stock_entry.delete(0, "end")
        else:
            CustomDialog(self, "Error", "No se pudo guardar el producto", dialog_type="error")

