import ttkbootstrap as ttk
from pos_sistem.modules.inventory.list_products import list_products
from ttkbootstrap.constants import *
from pos_sistem.ui.utils.binary_search_tree import ProductBST


class InventoryView(ttk.Frame):
    def __init__(self, master, show_view):
        super().__init__(master)
        self.show_view = show_view
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="📦 Inventario de Productos", font=("Segoe UI", 16)).pack(pady=10)

        #Buscador
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5)
        ttk.Label(search_frame, text="Buscar producto:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left")
        ttk.Button(search_frame, text="Buscar", command=self.search_product).pack(side="left", padx=5)

        columns = ("id", "name", "stock", "price")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20, bootstyle="info")

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("price", text="Precio Venta")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("stock", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="e")

        self.tree.pack(padx=10, pady=5, fill="both", expand=True)

        ttk.Button(self, text="🔄 Actualizar", bootstyle="primary", command=self.load_inventory).pack(pady=5)
        ttk.Button(self, text="⬅ Volver", bootstyle="secondary", command=lambda: self.show_view("main")).pack(pady=10)

        self.load_inventory()

    def load_inventory(self):
        from pos_sistem.modules.inventory.list_products import list_products

        self.tree.delete(*self.tree.get_children())
        self.products = list_products()  # Guardar todos

        self.bst = ProductBST()
        for p in self.products:
            self.bst.insert(p)

        self.display_products(self.products)

    def display_products(self, products):
        self.tree.delete(*self.tree.get_children())
        if not products:
            self.tree.insert("", "end", values=("Sin datos", "", "", ""))
            return
        for p in products:
            self.tree.insert("", "end", values=(p["id"], p["name"], p["stock"], f"${p['sale_price']:.2f}"))

    def search_product(self):
        query = self.search_entry.get()
        if query:
            filtered = self.bst.search_by_substring(query)
            self.display_products(filtered)
        else:
            self.display_products(self.products)
