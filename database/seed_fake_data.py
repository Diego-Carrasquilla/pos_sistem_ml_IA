import mysql.connector
from faker import Faker
import random

fake = Faker()

try:
    print("\U0001F7E1 Intentando conectar a la base de datos...")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pos_system"
    )
    print("\u2705 Conexión exitosa a MySQL.")
except mysql.connector.Error as err:
    print(f"\u274C Error al conectar a la base de datos: {err}")
    exit(1)

cursor = connection.cursor()

try:
    # Empleados
    print("\n▶️ Insertando empleados...")
    positions = ["cashier", "supervisor"]
    for _ in range(10):
        name = fake.name()
        email = fake.unique.email()
        position = random.choice(positions)
        cursor.execute("""
            INSERT INTO employees (name, email, position)
            VALUES (%s, %s, %s)
        """, (name, email, position))
    connection.commit()

    # Insertar productos ficticios
    product_ids = []
    for _ in range(30):
        name = fake.unique.word().capitalize()
        description = fake.sentence()
        price = round(random.uniform(5, 100), 2)
        stock = random.randint(10, 100)

        cursor.execute("""
        INSERT INTO products (name, description, sale_price, stock)
        VALUES (%s, %s, %s, %s)
    """, (name, description, price, stock))
    product_ids.append(cursor.lastrowid)  # Guardamos ID real insertado

    connection.commit()

    # Insertar entradas de inventario (solo usando product_ids existentes)
    for _ in range(40):
        product_id = random.choice(product_ids)
        quantity = random.randint(5, 30)
        cursor.execute("""
        INSERT INTO inventory_entries (product_id, quantity)
        VALUES (%s, %s)
    """, (product_id, quantity))

    connection.commit()


    # Ventas
    print("\n▶️ Insertando ventas...")
    for _ in range(10):
        employee_id = random.randint(1, 10)
        total = round(random.uniform(100, 2000), 2)
        cursor.execute("""
            INSERT INTO sales (employee_id, total)
            VALUES (%s, %s)
        """, (employee_id, total))

    # Detalles de venta
    print("\n▶️ Insertando detalles de venta...")
    for _ in range(30):
        sale_id = random.randint(1, 10)
        product_id = random.randint(1, 15)
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5, 500), 2)
        cursor.execute("""
            INSERT INTO sale_details (sale_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
        """, (sale_id, product_id, quantity, unit_price))

    connection.commit()
    print("\n✅ Migración de datos ficticios completada con éxito.")

except mysql.connector.Error as err:
    print(f"\n\u274C Error durante la migración: {err}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()
    print("\n👋 Conexión cerrada.")
