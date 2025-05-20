from pos_sistem.database.connection import get_connection

def list_products():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, stock, sale_price FROM products")
            products = cursor.fetchall()
            return products
        except Exception as e:
            print("❌ Error listing products:", e)
            return []
        finally:
            cursor.close()
            conn.close()
    return []