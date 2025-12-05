import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'database': 'tienda_alimentos',
    'user': 'root',
    'password': 'abril2025'
}

def fix_users_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        print("🔧 REPARANDO TABLA DE USUARIOS...")
        
        # Verificar estructura actual
        cursor.execute("DESCRIBE usuarios")
        columnas = [col[0] for col in cursor.fetchall()]
        print(f"📋 Columnas actuales: {columnas}")
        
        # Agregar columna NombreCompleto si no existe
        if 'NombreCompleto' not in columnas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN NombreCompleto VARCHAR(100) NOT NULL AFTER PasswordHash")
            print("✅ Columna NombreCompleto agregada")
        
        # Actualizar los nombres de usuarios existentes
        cursor.execute("UPDATE usuarios SET NombreCompleto = 'Administrador Principal' WHERE NombreUsuario = 'admin'")
        cursor.execute("UPDATE usuarios SET NombreCompleto = 'Vendedor General' WHERE NombreUsuario = 'vendedor'")
        print("✅ Nombres actualizados")
        
        conn.commit()
        print("🎉 TABLA DE USUARIOS REPARADA")
        
        # Mostrar resultado
        cursor.execute("SELECT * FROM usuarios")
        for usuario in cursor.fetchall():
            print(f"👤 {usuario}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_users_table()