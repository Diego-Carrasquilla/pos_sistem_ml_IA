from pos_sistem.database.connection import get_connection
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def get_daily_sales_summary():
    conn = get_connection()
    today = datetime.now().date()
    summary = f"Reporte de ventas del día {today}:\n\n"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id, s.created_at, s.total, e.name AS employee_name
            FROM sales s
            LEFT JOIN employees e ON s.employee_id = e.id
            WHERE DATE(s.created_at) = CURDATE()
            ORDER BY s.created_at
        """)
        rows = cursor.fetchall()

        if not rows:
            summary += "No se realizaron ventas hoy."
        else:
            for row in rows:
                summary += f"- Venta #{row['id']} por {row['employee_name'] or 'Desconocido'} a las {row['created_at'].strftime('%H:%M')} por ${row['total']:.2f}\n"
            total_dia = sum(r["total"] for r in rows)
            summary += f"\nTotal vendido: ${total_dia:.2f}"

        return summary

    finally:
        cursor.close()
        conn.close()


def generate_daily_sales_pdf():
    today = datetime.now().strftime("%Y-%m-%d")
    report_text = get_daily_sales_summary()
    file_path = f"daily_sales_{today}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    y = height - 40

    for line in report_text.split("\n"):
        c.drawString(40, y, line)
        y -= 15
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    os.startfile(file_path) 

