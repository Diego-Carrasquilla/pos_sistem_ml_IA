import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pos_sistem.modules.sales.list_sale_filtered import list_sales_filtered
from datetime import datetime
from ttkbootstrap.widgets import DateEntry


class SalesView(ttk.Frame):
    def __init__(self, master, show_view):  
        super().__init__(master)
        self.show_view = show_view          
        self.pack(fill="both", expand=True)
        self.create_widgets()
        

    def create_widgets(self):
        filter_frame = ttk.LabelFrame(self, text="🔍 Filtros de Búsqueda", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Fecha inicio
        ttk.Label(filter_frame, text="Fecha inicio:").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = DateEntry(filter_frame, firstweekday=0, bootstyle="info", dateformat="%Y-%m-%d", startdate=datetime.today())
        self.start_date.grid(row=0, column=1)

        # Fecha fin
        ttk.Label(filter_frame, text="Fecha fin:").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(filter_frame, firstweekday=0, bootstyle="info", dateformat="%Y-%m-%d")
        self.end_date.entry.delete(0, "end")
        self.end_date.grid(row=0, column=3)

        # ID Empleado
        ttk.Label(filter_frame, text="ID Empleado:").grid(row=1, column=0, padx=5, pady=5)
        self.employee_id = ttk.Entry(filter_frame)
        self.employee_id.grid(row=1, column=1)

        # ID Producto
        ttk.Label(filter_frame, text="ID Producto:").grid(row=1, column=2, padx=5, pady=5)
        self.product_id = ttk.Entry(filter_frame)
        self.product_id.grid(row=1, column=3)

        # Botones
        ttk.Button(filter_frame, text="🔎 Filtrar", bootstyle="primary", command=self.filter_sales).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(filter_frame, text="🧹 Limpiar", bootstyle="secondary", command=self.clear_filters).grid(row=2, column=1, padx=5, pady=10)

        # Tabla de resultados
        self.tree = ttk.Treeview(self, columns=("sale_id", "date", "employee", "total", "products"), show="headings", bootstyle="info", height=15)
        self.tree.heading("sale_id", text="ID Venta")
        self.tree.heading("date", text="Fecha")
        self.tree.heading("employee", text="Empleado")
        self.tree.heading("total", text="Total")
        self.tree.heading("products", text="Productos")

        self.tree.column("sale_id", width=80, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("employee", width=150, anchor="center")
        self.tree.column("total", width=100, anchor="center")
        self.tree.column("products", width=400)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Botón volver
        ttk.Button(self, text="⬅ Volver", bootstyle="secondary", command=lambda: self.show_view("main")).pack(pady=10)

    def clear_filters(self):
        self.start_date.set_date(datetime.today())
        self.end_date.set_date(datetime.today())
        self.employee_id.delete(0, "end")
        self.product_id.delete(0, "end")
        self.tree.delete(*self.tree.get_children())

    def filter_sales(self):
        start = self.start_date.entry.get() or None
        end = self.end_date.entry.get() or None
        emp = int(self.employee_id.get()) if self.employee_id.get().isdigit() else None
        prod = int(self.product_id.get()) if self.product_id.get().isdigit() else None

        ventas = list_sales_filtered(start_date=start, end_date=end, employee_id=emp, product_id=prod)

        self.tree.delete(*self.tree.get_children())

        if not ventas:
            self.tree.insert("", "end", values=("–", "–", "–", "–", "No hay ventas para los filtros dados"))
            return

        for venta in ventas:
            productos = ", ".join(f"{p['product_name']} (x{p['quantity']})" for p in venta["products"])
            self.tree.insert(
                "", "end",
                values=(
                    venta['sale_id'],
                    venta['created_at'],
                    venta['employee_name'],
                    f"${venta['total']:.2f}",
                    productos
                )
            )
