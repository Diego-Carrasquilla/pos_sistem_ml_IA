from pos_sistem.database.connection import get_connection

def list_sale_details(sale_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Primero, obtener la venta y el empleado
            cursor.execute("""
                SELECT s.id, s.created_at, s.total, e.name AS employee_name, e.position
                FROM sales s
                JOIN employees e ON s.employee_id = e.id
                WHERE s.id = %s
            """, (sale_id,))
            sale = cursor.fetchone()

            if not sale:
                print(f"❌ Venta con ID {sale_id} no encontrada.")
                return

            print(f"\n Detalles de la Venta #{sale['id']}")
            print(f" Fecha: {sale['created_at']}")
            print(f"Empleado: {sale['employee_name']} ({sale['position']})")
            print(f"Total: ${sale['total']:.2f}\n")

            # Ahora, obtener los detalles
            cursor.execute("""
                SELECT 
                    p.name AS product_name,
                    d.quantity,
                    d.unit_price,
                    d.quantity * d.unit_price AS subtotal
                FROM sale_details d
                JOIN products p ON d.product_id = p.id
                WHERE d.sale_id = %s
            """, (sale_id,))
            details = cursor.fetchall()

            if not details:
                print("Esta venta no tiene productos registrados.")
                return

            for item in details:
                print(f"Producto: {item['product_name']} | Cantidad: {item['quantity']} | "
                      f"Unitario: ${item['unit_price']:.2f} | Subtotal: ${item['subtotal']:.2f}")

        except Exception as e:
            print("❌ Error al obtener detalles de la venta:", e)
        finally:
            cursor.close()
            conn.close()
