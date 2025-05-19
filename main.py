import sys
import os

# Asegura que los módulos se puedan importar correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pos_sistem.modules.inventory.add_product import add_product
from pos_sistem.modules.inventory.register_stock_entry import register_stock_entry
from pos_sistem.modules.inventory.list_products import list_products
from pos_sistem.modules.inventory.clean_duplicates import merge_duplicate_products
from pos_sistem.modules.sales.register_sale import register_sale

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
    register_sale(employee_id=1, items=items)


    # 📦 Listar productos para ver el resultado
    list_products()

    print("✅ Inventory operations completed.")

    

if __name__ == "__main__":
    main()
