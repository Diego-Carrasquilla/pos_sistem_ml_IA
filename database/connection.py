import mysql.connector
from mysql.connector import Error

def get_connection():
    print("🟡 Intentando conectar a la base de datos...")
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='pos_system',
            connection_timeout=5
        )
        

        if connection.is_connected():
            print("✅ Conexión exitosa a MySQL.")
            return connection
        else:
            print("❌ La conexión no fue establecida.")
            return None

    except Error as e:
        print("❌ Error al conectar a MySQL:", e)
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("🔁 Cerrando conexión.")
        conn.close()
