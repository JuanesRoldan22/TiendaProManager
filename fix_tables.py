"""
TiendaPro Manager - Utilidad de Reparación de Base de Datos
Corrige problemas de nombres de tablas y estructura
Versión 1.0
"""

import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'database': 'tienda_alimentos',
    'user': 'root',
    'password': 'abril2025'
}

def fix_tables():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        print("🔧 INICIANDO REPARACIÓN DE TABLAS - TiendaPro Manager...")
        
        # 1. Verificar qué tablas existen
        cursor.execute("SHOW TABLES")
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        print(f"📋 Tablas encontradas: {tablas}")
        
        # 2. Si existe Productos (mayúscula) y productos (minúscula)
        if 'Productos' in tablas and 'productos' in tablas:
            print("⚠️  Se encontraron ambas tablas (Productos y productos)")
            
            # Copiar datos de Productos a productos
            cursor.execute("INSERT IGNORE INTO productos SELECT * FROM Productos")
            print("✅ Datos copiados de Productos a productos")
            
            # Eliminar tabla Productos
            cursor.execute("DROP TABLE Productos")
            print("✅ Tabla Productos eliminada")
            
        elif 'Productos' in tablas:
            print("⚠️  Solo existe tabla Productos (mayúscula)")
            # Renombrar Productos a productos
            cursor.execute("RENAME TABLE Productos TO productos")
            print("✅ Tabla Productos renombrada a productos")
        
        # 3. Hacer lo mismo para ventas
        if 'Ventas' in tablas and 'ventas' in tablas:
            print("⚠️  Se encontraron ambas tablas (Ventas y ventas)")
            cursor.execute("INSERT IGNORE INTO ventas SELECT * FROM Ventas")
            cursor.execute("DROP TABLE Ventas")
            print("✅ Tabla Ventas unificada con ventas")
        elif 'Ventas' in tablas:
            print("⚠️  Solo existe tabla Ventas (mayúscula)")
            cursor.execute("RENAME TABLE Ventas TO ventas")
            print("✅ Tabla Ventas renombrada a ventas")
        
        conn.commit()
        print("🎉 REPARACIÓN COMPLETADA - TiendaPro Manager")
        
        # 4. Verificar resultado final
        cursor.execute("SHOW TABLES")
        tablas_finales = [tabla[0] for tabla in cursor.fetchall()]
        print(f"📋 Tablas finales: {tablas_finales}")
        
    except Exception as e:
        print(f"❌ Error en TiendaPro Manager: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_tables()