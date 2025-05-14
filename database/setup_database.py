
from connection import get_connection

def crear_tablas():
    conn = get_connection()
    if conn is None:
        print("❌ No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()

    try:
        # Empleados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100) UNIQUE,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                precio_venta DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0,
                fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Entradas de inventario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entradas_inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                producto_id INT,
                cantidad INT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            );
        """)

        # Ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                empleado_id INT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                total DECIMAL(10,2),
                FOREIGN KEY (empleado_id) REFERENCES empleados(id)
            );
        """)

        # Detalle de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id INT AUTO_INCREMENT PRIMARY KEY,
                venta_id INT,
                producto_id INT,
                cantidad INT,
                precio_unitario DECIMAL(10,2),
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            );
        """)

        conn.commit()
        print("✅ Tablas creadas exitosamente.")
    
    except Exception as e:
        print("❌ Error al crear tablas:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_tablas()
