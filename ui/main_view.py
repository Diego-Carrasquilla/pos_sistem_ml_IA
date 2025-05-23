import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pos_sistem.modules.sales.daily_sales_inform import generate_daily_sales_pdf 
from pos_sistem.ui.utils.custom_dialog import CustomDialog

class MainView(ttk.Frame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.show_view = show_view
        self.create_widgets()


        ttk.Button(self, text="📄 Generar PDF Diario", bootstyle="light-outline", width=30,
                   command=self.handle_pdf).pack(pady=10)

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
        
        ttk.Button(self, text="📊 Ver Estadísticas", bootstyle="secondary", width=30,
                   command=lambda: self.show_view("stats")).pack(pady=10)
        
        ttk.Button(self, text="🤖 Asistente AI", bootstyle="", width=30,
                   command=lambda: self.show_view("ai")).pack(pady=10)
        
    def handle_pdf(self):
        try:
            generate_daily_sales_pdf()
            
        except Exception as e:
            CustomDialog("Error", f"No se pudo generar el PDF:\n{str(e)}")
        
        
        

