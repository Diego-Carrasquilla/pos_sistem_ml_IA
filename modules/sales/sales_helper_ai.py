from pos_sistem.database.connection import get_connection

def get_sales_as_texts(limit=300):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id AS sale_id, s.created_at, s.total, e.name AS employee_name,
                   p.name AS product_name, d.quantity, d.unit_price
            FROM sales s
            LEFT JOIN employees e ON s.employee_id = e.id
            JOIN sale_details d ON s.id = d.sale_id
            JOIN products p ON d.product_id = p.id
            ORDER BY s.created_at DESC
            LIMIT %s
        """, (limit,))

        rows = cursor.fetchall()
        sales_texts = {}

        for row in rows:
            sid = row["sale_id"]
            if sid not in sales_texts:
                sales_texts[sid] = {
                    "header": f"Venta #{sid} por {row['employee_name'] or 'Desconocido'} el {row['created_at']}: total ${row['total']:.2f}. Productos:",
                    "lines": []
                }
            sales_texts[sid]["lines"].append(
                f"- {row['quantity']}x {row['product_name']} a ${row['unit_price']:.2f}"
            )

        # Convertimos cada venta a un texto completo
        return [v["header"] + "\n" + "\n".join(v["lines"]) for v in sales_texts.values()]

    finally:
        cursor.close()
        conn.close()

def build_prompt(question, all_sales_context):
    context = "\n\n".join(all_sales_context)
    return f"""
Contexto:
{context}

Pregunta: {question}
Responde de forma clara, precisa y basada solamente en el contexto.
"""

def generate_prompt_for_question(question):
    all_sales = get_sales_as_texts()
    prompt = build_prompt(question, all_sales)
    return prompt
