from pos_sistem.database.connection import get_connection
from pos_sistem.modules.inventory.update_stock import update_stock
from datetime import datetime

def register_sale(employee_id, items):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            total = 0
            for item in items:
                cursor.execute("SELECT sale_price, stock FROM products WHERE id = %s", (item['product_id'],))
                result = cursor.fetchone()

                if not result:
                    print(f"❌ Producto ID {item['product_id']} no existe.")
                    return
                if result['stock'] < item['quantity']:
                    print(f"❌ Stock insuficiente para producto ID {item['product_id']}.")
                    return
                total += result['sale_price'] * item['quantity']

            # Insertar en tabla sales
            cursor.execute("""
                INSERT INTO sales (employee_id, created_at, total)
                VALUES (%s, %s, %s)
            """, (employee_id, datetime.now(),total ))
            sale_id = cursor.lastrowid

            for item in items:
                # Obtener el precio actual
                cursor.execute("SELECT price FROM products WHERE id = %s", (item['product_id'],))
                price = cursor.fetchone()['price']

                # Insertar detalle de la venta
                cursor.execute("""
                    INSERT INTO sale_details (sale_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                """, (sale_id, item['product_id'], item['quantity'], price))

                # Actualizar stock
                update_stock(item['product_id'], -item['quantity'])

            conn.commit()
            print(f"✅ Venta registrada. Total: ${total:.2f}, realizada por empleado ID {employee_id}.")
        except Exception as e:
            print("❌ Error registrando venta:", e)
        finally:
            cursor.close()
            conn.close()
