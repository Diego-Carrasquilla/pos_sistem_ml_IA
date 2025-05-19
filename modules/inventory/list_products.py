from database.connection import get_connection

def list_products():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, stock, sale_price FROM products")
            products = cursor.fetchall()
            for product in products:
                print(f"{product['id']} | {product['name']} | Stock: {product['stock']} | ${product['sale_price']}")
        except Exception as e:
            print("❌ Error listing products:", e)
        finally:
            cursor.close()
            conn.close()
