from database.connection import get_connection

def list_products():
    conn = get_connection()
    if conn is None:
        print("No database connection.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, stock, sale_price FROM products")
        products = cursor.fetchall()

        print("Inventory:")
        for p in products:
            print(f"ID: {p[0]} | {p[1]} | Stock: {p[2]} | Price: ${p[3]}")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
