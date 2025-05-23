from pos_sistem.database.connection import get_connection

def detailed_sales_report(date=None, employee_id=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    s.id AS sale_id,
                    s.created_at,
                    s.total,
                    e.name AS employee_name,
                    p.name AS product_name,
                    d.quantity,
                    d.unit_price
                FROM sales s
                JOIN employees e ON s.employee_id = e.id
                JOIN sale_details d ON s.id = d.sale_id
                JOIN products p ON d.product_id = p.id
                WHERE 1=1
            """
            params = []

            if date:
                query += " AND DATE(s.created_at) = %s"
                params.append(date)
            if employee_id:
                query += " AND s.employee_id = %s"
                params.append(employee_id)

            query += " ORDER BY s.created_at DESC"

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

            if not rows:
                print("⚠️ No se encontraron ventas para los filtros indicados.")
                return

            current_sale = None
            for row in rows:
                if current_sale != row["sale_id"]:
                    if current_sale is not None:
                        print("————————————————————————————————————————")
                    current_sale = row["sale_id"]
                    print(f"\nVenta ID: {row['sale_id']} | Fecha: {row['created_at']}")
                    print(f"Empleado: {row['employee_name']}")
                print(f"- Producto: {row['product_name']} | Cantidad: {row['quantity']} | Precio unitario: ${row['unit_price']:.2f}")
            print("————————————————————————————————————————")

        except Exception as e:
            print("❌ Error generando reporte detallado:", e)
        finally:
            cursor.close()
            conn.close()

def get_today_sales_summary_text():
    conn = get_connection()
    summary = ""

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    s.id AS sale_id,
                    s.created_at,
                    s.total,
                    e.name AS employee_name,
                    p.name AS product_name,
                    d.quantity,
                    d.unit_price
                FROM sales s
                JOIN employees e ON s.employee_id = e.id
                JOIN sale_details d ON s.id = d.sale_id
                JOIN products p ON d.product_id = p.id
                WHERE DATE(s.created_at) = CURDATE()
                ORDER BY s.created_at DESC
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                return "Hoy no se han registrado ventas aún."

            current_sale = None
            for row in rows:
                if current_sale != row["sale_id"]:
                    if current_sale is not None:
                        summary += "---------------------------------------\n"
                    current_sale = row["sale_id"]
                    summary += f"\nVenta ID: {row['sale_id']} | Fecha: {row['created_at']}\n"
                    summary += f"Empleado: {row['employee_name']}\n"
                summary += f"- {row['product_name']}: {row['quantity']} x ${row['unit_price']:.2f}\n"

            summary += "---------------------------------------"
            return summary

        except Exception as e:
            return f"Error al generar el resumen de ventas: {e}"
        finally:
            cursor.close()
            conn.close()
    else:
        return "No se pudo conectar con la base de datos."