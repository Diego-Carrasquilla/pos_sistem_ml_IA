from pos_sistem.database.connection import get_connection

def list_sales():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    s.id AS sale_id,
                    s.created_at,
                    s.total,
                    e.name AS employee_name,
                    e.position
                FROM sales s
                JOIN employees e ON s.employee_id = e.id
                ORDER BY s.created_at DESC
            """)
            results = cursor.fetchall()

            if results:
                print("\nListado de ventas:")
                for sale in results:
                    print(f"Venta #{sale['sale_id']} | Fecha: {sale['created_at']} | Total: ${sale['total']:.2f} | Empleado: {sale['employee_name']} ({sale['position']})")
            else:
                print("No hay ventas registradas.")
        except Exception as e:
            print("❌Error al listar las ventas:", e)
        finally:
            cursor.close()
            conn.close()
