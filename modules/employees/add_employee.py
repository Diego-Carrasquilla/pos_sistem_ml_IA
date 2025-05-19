from pos_sistem.database.connection import get_connection

def add_employee(name, email, position):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (name, email, position)
                VALUES (%s, %s, %s)
            """, (name, email, position))
            conn.commit()
            print(f"✅ Employee '{name}' registered.")
        except Exception as e:
            print("❌ Error adding employee:", e)
        finally:
            cursor.close()
            conn.close()
