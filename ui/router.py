import ttkbootstrap as ttk
from pos_sistem.ui.main_view import MainView
from pos_sistem.ui.sales_view import SalesView
from pos_sistem.ui.inventory_view import InventoryView
from pos_sistem.ui.sales_register_view import SalesRegisterView
from pos_sistem.ui.register_product_view import RegisterProductView
from pos_sistem.ui.stats_view import StatsView 
from pos_sistem.ui.ai_assistant import AssistantAIView  


def launch_main_window():
    app = ttk.Window(title="POS System", themename="darkly", size=(900, 650))
    main_frame = ttk.Frame(app)
    main_frame.pack(fill="both", expand=True)

    def show_view(name):
        for widget in main_frame.winfo_children():
            widget.destroy()
        if name == "main":
            view = MainView(main_frame, show_view)
        elif name == "sales":
            view = SalesView(main_frame, show_view)
        elif name == "inventory":
            view = InventoryView(main_frame, show_view)
        elif name == "sales_register":
            view = SalesRegisterView(main_frame, show_view)
        elif name == "register_product":
            view = RegisterProductView(main_frame, show_view)
        elif name == "ai":
            view =AssistantAIView(main_frame, show_view)

        elif name == "stats":
            view = StatsView(main_frame, show_view)

        else:
            view = ttk.Label(main_frame, text="Vista no encontrada")
        view.pack(fill="both", expand=True)

    show_view("main")  # Vista por defecto

    app.mainloop()
