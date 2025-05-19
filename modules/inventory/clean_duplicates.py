from pos_sistem.database.connection import get_connection

def merge_duplicate_products():
    conn = get_connection()
    if not conn:
        print("❌ Error: no se pudo conectar a la base de datos.")
        return False

    try:
        cursor = conn.cursor(dictionary=True)

        # Paso 1: encontrar productos duplicados por nombre
        cursor.execute("""
            SELECT name
            FROM products
            GROUP BY name
            HAVING COUNT(*) > 1
        """)
        duplicate_names = cursor.fetchall()

        if not duplicate_names:
            print("✅ No hay productos duplicados.")
            return True

        for row in duplicate_names:
            name = row['name']

            # Obtener todos los productos con ese nombre
            cursor.execute("""
                SELECT id, stock
                FROM products
                WHERE name = %s
                ORDER BY id ASC
            """, (name,))
            products = cursor.fetchall()

            main_id = products[0]['id']
            total_stock = sum(p['stock'] for p in products)
            print(f"🔍 '{name}' → {len(products)} duplicados encontrados (ID principal: {main_id}).")

            # Paso 2: actualizar el stock del producto principal
            cursor.execute("""
                UPDATE products
                SET stock = %s
                WHERE id = %s
            """, (total_stock, main_id))

            # Paso 3: registrar entrada total en inventory_entries
            cursor.execute("""
                INSERT INTO inventory_entries (product_id, quantity)
                VALUES (%s, %s)
            """, (main_id, total_stock))

            # Paso 4: eliminar productos duplicados (excepto el principal)
            duplicate_ids = [p['id'] for p in products[1:]]
            format_ids = ','.join(['%s'] * len(duplicate_ids))
            cursor.execute(f"""
                DELETE FROM products
                WHERE id IN ({format_ids})
            """, tuple(duplicate_ids))

            print(f"✅ '{name}' unificado con stock total {total_stock}. Duplicados eliminados: {len(duplicate_ids)}.")

        conn.commit()
        return True

    except Exception as e:
        print("❌ Error al unificar duplicados:", e)
        return False
    finally:
        cursor.close()
        conn.close()
