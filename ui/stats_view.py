import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

from pos_sistem.modules.ml.sales_prediction import (
    get_daily_sales,
    train_arima_model,
    predict_future_sales_arima
)

from pos_sistem.modules.ml.insight_detector import get_insights  # <--- nuevo módulo

class StatsView(Frame):
    def __init__(self, master, show_view): 
        super().__init__(master)
        self.show_view = show_view  
        self.pack(fill='both', expand=True)
        self.init_ui()

    def init_ui(self):
        # Header con botón de volver
        header = ttk.Frame(self)
        header.pack(side="top", fill="x", pady=10, padx=10)

        title = ttk.Label(header, text="📊 Estadísticas", font=("Helvetica", 18, "bold"))
        title.pack(side="left")

        back_button = ttk.Button(header, text="Volver al menú", command=lambda: self.show_view("main"), bootstyle="secondary")
        back_button.pack(side="right")

        # Notificaciones inteligentes
        insights = get_insights()
        if insights:
            notif_frame = ttk.LabelFrame(self, text="Notificaciones inteligentes", padding=10)
            notif_frame.pack(fill="x", padx=10, pady=(0, 10))
            for message in insights:
                label = ttk.Label(notif_frame, text=f"• {message}", foreground="red")
                label.pack(anchor="w")

        # Notebook para las pestañas de estadísticas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear pestañas
        self.prediction_tab = ttk.Frame(self.notebook)
        self.fast_movers_tab = ttk.Frame(self.notebook)
        self.employee_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.prediction_tab, text="Predicción de ventas")
        self.notebook.add(self.fast_movers_tab, text="Productos que se agotan")
        self.notebook.add(self.employee_tab, text="Empleados eficientes")

        # Ejecutar gráficos al cargar pestañas
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.current_tab = None

    def on_tab_change(self, event):
        tab = self.notebook.index(self.notebook.select())
        if tab == 0 and self.current_tab != 0:
            self.plot_predictions(self.prediction_tab)
        elif tab == 1 and self.current_tab != 1:
            self.show_fast_movers(self.fast_movers_tab)
        elif tab == 2 and self.current_tab != 2:
            self.plot_employee_efficiency(self.employee_tab)
        self.current_tab = tab

    def plot_predictions(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        df = get_daily_sales()
        model_fit = train_arima_model(df)
        future_df = predict_future_sales_arima(model_fit, df, days=7)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(df.index, df['total_sales'], label='Ventas reales', color='steelblue')
        ax.plot(future_df.index, future_df['predicted_sales'], label='Predicción', linestyle='--', color='darkorange')

        ax.set_title("Predicción de ventas futuras", fontsize=14, weight='bold')
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Total vendido")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_fast_movers(self, frame):
        from pos_sistem.modules.ml.fast_moving_predictor import train_model, predict_fast_products


        for widget in frame.winfo_children():
            widget.destroy()

        model = train_model()
        df = predict_fast_products(model)

        def get_urgency_color(stock, sales_per_day):
            if stock <= 1 and sales_per_day > 1:
                return "tomato"  # rojo claro
            elif stock <= 5 and sales_per_day > 1.5:
                return "gold"  # amarillo
            else:
                return "pale green"  # verde claro

        df["urgency_color"] = df.apply(lambda row: get_urgency_color(row["stock"], row["sales_per_day"]), axis=1)

        subtitle = ttk.Label(frame, text="Productos con riesgo de agotarse", font=("Helvetica", 14, "bold"))
        subtitle.pack(pady=(10, 5))

        content_frame = ttk.Frame(frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        table_frame = ttk.Frame(content_frame)
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        columns = ("ID", "Nombre", "Stock", "Vendidos", "Días activos", "Ventas/día", "Días sin vender")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
    
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        for i, row in df.iterrows():
            values = (
                row["id"], row.get("name", "Desconocido"), row["stock"], row["total_sold"], 
                row["active_days"], round(row["sales_per_day"], 2), row["days_since_last_sale"]
            )
            urgency_tag = f"urgency_{i}"
            tree.insert("", "end", values=values, tags=(urgency_tag,))
            tree.tag_configure(urgency_tag, background=row["urgency_color"])

        tree.pack(fill="both", expand=True)

        # Gráfico de barras 
        chart_frame = ttk.Frame(content_frame)
        chart_frame.pack(side="right", fill="both", expand=True)

        top_df = df.sort_values("sales_per_day", ascending=False).head(7)

        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(top_df["name"], top_df["sales_per_day"], color=sns.color_palette("flare", len(top_df)))

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f"{width:.2f}", va='center', fontsize=9)

        ax.set_title("Top 7 productos con mayor rotación", fontsize=12, weight='bold')
        ax.set_xlabel("Ventas por día")
        ax.invert_yaxis()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


    def plot_employee_efficiency(self, frame):
        from pos_sistem.modules.ml.employee_efficiency_predictor import get_employee_efficiency

        for widget in frame.winfo_children():
            widget.destroy()

        df = get_employee_efficiency()
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(9, 5))

        bars = ax.barh(df['employee_name'], df['efficiency_score'], color=sns.color_palette("flare", len(df)))

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, f"{width:.2f}", va='center', fontsize=9)

        ax.set_title('Top empleados más eficientes', fontsize=14, weight='bold')
        ax.set_xlabel('Puntaje de eficiencia')
        ax.invert_yaxis()
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
