from pos_sistem.database.connection import get_connection
from pos_sistem.modules.inventory.update_stock import update_stock  

def register_stock_entry(product_id, quantity):
    if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity <= 0:
        print("❌ Invalid input: product_id and quantity must be positive integers.")
        return False

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Verificamos que exista el producto
            cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
            if cursor.fetchone() is None:
                print("❌ Product not found.")
                return False

            # Registramos entrada en inventory_entries
            cursor.execute("""
                INSERT INTO inventory_entries (product_id, quantity)
                VALUES (%s, %s)
            """, (product_id, quantity))
            conn.commit() 

            
            update_stock(product_id, quantity)

            print(f"✅ Stock entry registered and updated for product ID {product_id} (+{quantity}).")
            return True
        except Exception as e:
            print("❌ Error registering stock entry:", e)
            return False
        finally:
            cursor.close()
            conn.close()
