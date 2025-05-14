from database.connection import get_connection

def add_product(name, description, price):
    conn = get_connection()
    if conn is None:
        print("No database connection.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, description, sale_price)
            VALUES (%s, %s, %s)
        """, (name, description, price))
        conn.commit()
        print("Product added successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
