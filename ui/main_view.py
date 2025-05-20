import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainView(ttk.Frame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.show_view = show_view
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="🏠 Menú Principal", font=("Segoe UI", 20)).pack(pady=30)

        ttk.Button(self, text="🔍 Ver Ventas", bootstyle="primary", width=30,
                   command=lambda: self.show_view("sales")).pack(pady=10)

        ttk.Button(self, text="📦 Ver Inventario", bootstyle="info", width=30,
                   command=lambda: self.show_view("inventory")).pack(pady=10)
        
        ttk.Button(self, text="🛒 Registrar Venta", bootstyle="success", width=30,
           command=lambda: self.show_view("sales_register")).pack(pady=10)
        
        ttk.Button(self, text="➕ Nuevo Producto", bootstyle="warning", width=30,
               command=lambda: self.show_view("register_product")).pack(pady=10)
        

