from pos_sistem.database.connection import get_connection

def list_employees():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, email, position, created_at
                FROM employees
                ORDER BY created_at DESC
            """)
            employees = cursor.fetchall()

            if not employees:
                print("⚠️ No employees found.")
                return

            print("Employee List:")
            for emp in employees:
                print(f"ID: {emp[0]} | Name: {emp[1]} | Email: {emp[2]} | Position: {emp[3]} | Created: {emp[4]}")
        except Exception as e:
            print("❌ Error listing employees:", e)
        finally:
            cursor.close()
            conn.close()
