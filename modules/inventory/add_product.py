from pos_sistem.database.connection import get_connection
from pos_sistem.modules.inventory.update_stock import update_stock

def add_product(name, description, price, initial_quantity=0):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)

            # Verificar si el producto ya existe por nombre
            cursor.execute("SELECT id FROM products WHERE name = %s", (name,))
            existing = cursor.fetchone()

            if existing:
                product_id = existing[0]
                print(f"⚠️ El producto '{name}' ya existe. Se actualizará el stock (+{initial_quantity}).")
                if initial_quantity > 0:
                    update_stock(product_id, initial_quantity)
                return product_id

            # Insertar nuevo producto
            cursor.execute("""
                INSERT INTO products (name, description, sale_price, stock)
                VALUES (%s, %s, %s, %s)
            """, (name, description, price, initial_quantity))
            conn.commit()
            product_id = cursor.lastrowid
            print(f"✅ Producto '{name}' agregado con ID {product_id} y stock inicial de {initial_quantity}.")
            return product_id
        except Exception as e:
            print("❌ Error al agregar producto:", e)
            return None
        finally:
            cursor.close()
            conn.close()
