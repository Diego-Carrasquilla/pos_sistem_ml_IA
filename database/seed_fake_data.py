import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

try:
    print("🟡 Conectando a la base de datos...")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pos_system"
    )
    print("✅ Conectado exitosamente.")
except mysql.connector.Error as err:
    print(f"❌ Error de conexión: {err}")
    exit(1)

cursor = connection.cursor()

try:
    # ─────────────────────────────
    # Empleados
    print("\n👤 Insertando empleados...")
    positions = ["cashier", "supervisor"]
    employee_ids = []
    for _ in range(10):
        name = fake.name()
        email = fake.unique.email()
        position = random.choice(positions)
        cursor.execute("""
            INSERT INTO employees (name, email, position)
            VALUES (%s, %s, %s)
        """, (name, email, position))
        employee_ids.append(cursor.lastrowid)
    connection.commit()

    # ─────────────────────────────
    # Productos
    print("📦 Insertando productos...")
    product_ids = []
    for _ in range(30):
        name = fake.unique.word().capitalize()
        description = fake.sentence()
        price = round(random.uniform(5, 100), 2)
        stock = random.randint(30, 100)
        cursor.execute("""
            INSERT INTO products (name, description, sale_price, stock)
            VALUES (%s, %s, %s, %s)
        """, (name, description, price, stock))
        product_ids.append(cursor.lastrowid)
    connection.commit()

    # ─────────────────────────────
    # Entradas de inventario
    print("📥 Insertando entradas de inventario...")
    for _ in range(40):
        product_id = random.choice(product_ids)
        quantity = random.randint(10, 50)
        cursor.execute("""
            INSERT INTO inventory_entries (product_id, quantity)
            VALUES (%s, %s)
        """, (product_id, quantity))
        # Aumentar stock manualmente también
        cursor.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (quantity, product_id))
    connection.commit()

    # ─────────────────────────────
    # Ventas con detalles
    print("💰 Insertando ventas realistas durante 30 días...")

    for _ in range(300):  # 300 ventas
        sale_date = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))

        employee_id = random.choice(employee_ids)
        total = 0

        cursor.execute("""
            INSERT INTO sales (employee_id, created_at, total)
            VALUES (%s, %s, %s)
        """, (employee_id, sale_date, 0))
        sale_id = cursor.lastrowid

        # Agregar entre 1 y 5 productos por venta
        products_in_sale = random.sample(product_ids, k=random.randint(1, 5))
        for product_id in products_in_sale:
            quantity = random.randint(1, 3)

            cursor.execute("SELECT sale_price, stock FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            if result is None:
                continue

            price, current_stock = result

            if current_stock >= quantity:
                line_total = price * quantity
                total += line_total

                # Insertar detalle de venta
                cursor.execute("""
                    INSERT INTO sale_details (sale_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                """, (sale_id, product_id, quantity, price))

                # Actualizar stock
                cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (quantity, product_id))

        # Actualizar el total real
        cursor.execute("UPDATE sales SET total = %s WHERE id = %s", (round(total, 2), sale_id))

    connection.commit()
    print("\n✅ Datos de prueba insertados con éxito.")

except mysql.connector.Error as err:
    print(f"❌ Error durante la operación: {err}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()
    print("\n🔒 Conexión cerrada.")
