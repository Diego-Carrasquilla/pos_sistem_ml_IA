import sys
import os

# Asegura que los módulos se puedan importar correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pos_sistem.modules.inventory.add_product import add_product
from pos_sistem.modules.inventory.register_stock_entry import register_stock_entry
from pos_sistem.modules.inventory.list_products import list_products
from pos_sistem.modules.inventory.clean_duplicates import merge_duplicate_products
from pos_sistem.modules.sales.register_sale import register_sale
from pos_sistem.modules.sales.list_sales  import list_sales
from pos_sistem.modules.sales.list_sale_details import list_sale_details
from pos_sistem.modules.sales.list_sale_filtered import list_sales_filtered
from pos_sistem.modules.sales.sales_report import detailed_sales_report

def main():
    print("🛒 Starting POS inventory test...")

    # 🟡 Agregar un nuevo producto
    banana_id = add_product("Banana", "Fresh bananas", 0.25)

    # ✅ Registrar entrada de stock (si se insertó bien el producto)
    if banana_id:
        register_stock_entry(banana_id, 20)

    #print("Limpiando duplicados...")
    #merge_duplicate_products()
    items = [
    {"product_id": 1, "quantity": 5},
    {"product_id": 3, "quantity": 2}]
    register_sale(employee_id=2, items=items)


    #Listar productos para ver el resultado
    list_products()
    print("✅ Inventory operations completed.")
    print("sales list")
    list_sales()
    print("sales details")
    list_sale_details(4)
    print("sales filtered")
    # Todas las ventas
    list_sales_filtered()
    # Ventas por fecha
    # list_sales_filtered(start_date="2025-05-01", end_date="2025-05-19")
    # Ventas por empleado
    # list_sales_filtered(employee_id=2)
    # Ventas por producto
    # list_sales_filtered(product_id=3)
    # Combinado
    # list_sales_filtered(start_date="2025-05-01", end_date="2025-05-19", employee_id=1, product_id=3)
    detailed_sales_report(date="2025-05-19")




    

if __name__ == "__main__":
    main()
