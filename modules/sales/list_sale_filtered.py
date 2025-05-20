from collections import defaultdict
from pos_sistem.database.connection import get_connection

def list_sales_filtered(start_date=None, end_date=None, employee_id=None, product_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            s.id AS sale_id, s.created_at, s.total,
            e.name AS employee_name,
            p.name AS product_name,
            sd.quantity, sd.unit_price
        FROM sales s
        JOIN employees e ON s.employee_id = e.id
        JOIN sale_details sd ON s.id = sd.sale_id
        JOIN products p ON sd.product_id = p.id
        WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND s.created_at >= %s"
        params.append(start_date)
    if end_date:
        query += " AND s.created_at <= %s"
        params.append(end_date)
    if employee_id:
        query += " AND s.employee_id = %s"
        params.append(employee_id)
    if product_id:
        query += " AND p.id = %s"
        params.append(product_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return []

    # Agrupar ventas por sale_id
    sales_dict = defaultdict(lambda: {
        "sale_id": None,
        "created_at": None,
        "employee_name": "",
        "total": 0,
        "products": []
    })

    for row in rows:
        sale = sales_dict[row["sale_id"]]
        sale["sale_id"] = row["sale_id"]
        sale["created_at"] = row["created_at"]
        sale["employee_name"] = row["employee_name"]
        sale["total"] = row["total"]
        sale["products"].append({
            "product_name": row["product_name"],
            "quantity": row["quantity"],
            "unit_price": row["unit_price"]
        })

    return list(sales_dict.values())