from pos_sistem.database.connection import get_connection

def delete_employee(employee_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            conn.commit()
            print(f"Employee ID {employee_id} deleted.")
        except Exception as e:
            print("❌ Error deleting employee:", e)
        finally:
            cursor.close()
            conn.close()
