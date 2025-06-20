from pos_sistem.database.connection import get_connection


def update_stock(product_id, quantity):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products
                SET stock = stock + %s
                WHERE id = %s
            """, (quantity, product_id))
            conn.commit()
            print("🔁 Stock updated.")
        except Exception as e:
            print("❌ Error updating stock:", e)
        finally:
            cursor.close()
            conn.close()
