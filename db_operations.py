"""
TiendaPro Manager - Sistema de Gestión Comercial
Operaciones de Base de Datos y Autenticación
Versión 1.0
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import warnings
import hashlib

# Silenciar warnings
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

DB_CONFIG = {
    'host': 'localhost',
    'database': 'tienda_alimentos', 
    'user': 'root',
    'password': 'abril2025'
}

def create_db_connection():
    """Crea y devuelve un objeto de conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            conn.autocommit = False
            return conn
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

# --- FUNCIONES DE COMPATIBILIDAD ---
def obtener_conexion():
    return create_db_connection()

def obtener_todos_productos_detalles():
    query = "SELECT ProductoID, NombreProducto, PrecioUnitario, Stock FROM productos ORDER BY NombreProducto ASC"
    return execute_query(query, fetch=True)

def execute_query(query, params=None, fetch=False, commit=False):
    conn = create_db_connection()
    if conn is None:
        return None if fetch else False

    cursor = conn.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        if commit:
            conn.commit()
            print(f"✅ Consulta ejecutada y confirmada: {query[:50]}...")
    except Error as e:
        print(f"❌ Error en consulta: {e}")
        print(f"   Consulta: {query}")
        print(f"   Parámetros: {params}")
        if conn and conn.is_connected():
            conn.rollback()
        return None if fetch else False
    finally:
        cursor.close()
        conn.close()
    
    # ✅ Retornar el resultado correcto
    if fetch:
        return result
    else:
        return True

def setup_database():
    """SOLO crea las tablas si no existen."""
    conn = create_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        # Crear tabla productos si no existe
        create_productos_table = """
        CREATE TABLE IF NOT EXISTS productos (
            ProductoID INT AUTO_INCREMENT PRIMARY KEY,
            NombreProducto VARCHAR(255) NOT NULL UNIQUE,
            PrecioUnitario DECIMAL(10, 2) NOT NULL,
            Stock INT NOT NULL DEFAULT 0,
            FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_productos_table)

        # Crear tabla ventas si no existe
        create_ventas_table = """
        CREATE TABLE IF NOT EXISTS ventas (
            VentaID INT AUTO_INCREMENT PRIMARY KEY,
            ProductoID INT,
            Cantidad INT NOT NULL, 
            PrecioUnitario DECIMAL(10, 2) NOT NULL,
            IngresoTotal DECIMAL(10, 2) NOT NULL,
            FechaVenta DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ProductoID) REFERENCES productos(ProductoID)
        )
        """
        cursor.execute(create_ventas_table)

        # ✅ TABLA: Usuarios para el sistema de login
        create_usuarios_table = """
        CREATE TABLE IF NOT EXISTS usuarios (
            UsuarioID INT AUTO_INCREMENT PRIMARY KEY,
            NombreUsuario VARCHAR(50) NOT NULL UNIQUE,
            PasswordHash VARCHAR(255) NOT NULL,
            NombreCompleto VARCHAR(100) NOT NULL,
            Rol ENUM('administrador', 'vendedor') NOT NULL DEFAULT 'vendedor',
            Activo BOOLEAN DEFAULT TRUE,
            FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_usuarios_table)

        # ✅ INSERTAR USUARIOS POR DEFECTO
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            usuarios_por_defecto = [
                ('admin', 'admin123', 'Administrador Principal', 'administrador'),
                ('vendedor', 'vendedor123', 'Vendedor General', 'vendedor')
            ]
            
            for usuario, password, nombre, rol in usuarios_por_defecto:
                password_hash = hashlib.md5(password.encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO usuarios (NombreUsuario, PasswordHash, NombreCompleto, Rol) VALUES (%s, %s, %s, %s)",
                    (usuario, password_hash, nombre, rol)
                )
            print("✅ Usuarios por defecto creados para TiendaPro Manager")

        conn.commit()
        print("✅ Configuración de BD completada - TiendaPro Manager")
        
    except Error as e:
        print(f"❌ ERROR en setup_database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# --- FUNCIONES DE AUTENTICACIÓN ---
def hash_password(password):
    """Genera un hash MD5 de la contraseña."""
    return hashlib.md5(password.encode()).hexdigest()

def verificar_usuario(nombre_usuario, password):
    """Verifica las credenciales del usuario."""
    query = "SELECT UsuarioID, NombreUsuario, NombreCompleto, Rol, PasswordHash FROM usuarios WHERE NombreUsuario = %s AND Activo = TRUE"
    params = (nombre_usuario,)
    result = execute_query(query, params, fetch=True)
    
    if result:
        usuario = result[0]
        password_hash = hash_password(password)
        if usuario['PasswordHash'] == password_hash:
            print(f"✅ Usuario autenticado en TiendaPro Manager: {usuario['NombreCompleto']}")
            return {
                'usuario_id': usuario['UsuarioID'],
                'nombre_usuario': usuario['NombreUsuario'],
                'nombre_completo': usuario['NombreCompleto'],
                'rol': usuario['Rol']
            }
        else:
            print(f"❌ Contraseña incorrecta para: {nombre_usuario}")
    
    print(f"❌ Autenticación fallida en TiendaPro Manager para: {nombre_usuario}")
    return None

def crear_usuario(nombre_usuario, password, nombre_completo, rol='vendedor'):
    """Crea un nuevo usuario (solo administradores)."""
    check_query = "SELECT UsuarioID FROM usuarios WHERE NombreUsuario = %s"
    check_result = execute_query(check_query, (nombre_usuario,), fetch=True)
    
    if check_result:
        print(f"❌ El usuario '{nombre_usuario}' ya existe en TiendaPro Manager")
        return False
        
    password_hash = hash_password(password)
    
    query = "INSERT INTO usuarios (NombreUsuario, PasswordHash, NombreCompleto, Rol) VALUES (%s, %s, %s, %s)"
    params = (nombre_usuario, password_hash, nombre_completo, rol)
    success = execute_query(query, params, commit=True)
    if success:
        print(f"✅ Usuario '{nombre_usuario}' creado en TiendaPro Manager con rol: {rol}")
    else:
        print(f"❌ Error al crear usuario '{nombre_usuario}' en TiendaPro Manager")
    return success

def obtener_usuarios():
    """Obtiene lista de todos los usuarios."""
    query = "SELECT UsuarioID, NombreUsuario, NombreCompleto, Rol, Activo FROM usuarios ORDER BY NombreUsuario"
    return execute_query(query, fetch=True)

def cambiar_estado_usuario(usuario_id, activo):
    """Activa o desactiva un usuario."""
    query = "UPDATE usuarios SET Activo = %s WHERE UsuarioID = %s"
    params = (activo, usuario_id)
    success = execute_query(query, params, commit=True)
    if success:
        estado = "activado" if activo else "desactivado"
        print(f"✅ Usuario {usuario_id} {estado} en TiendaPro Manager")
    else:
        print(f"❌ Error al cambiar estado del usuario {usuario_id}")
    return success

def cambiar_password(usuario_id, nueva_password):
    """Cambia la contraseña de un usuario."""
    password_hash = hash_password(nueva_password)
    query = "UPDATE usuarios SET PasswordHash = %s WHERE UsuarioID = %s"
    params = (password_hash, usuario_id)
    success = execute_query(query, params, commit=True)
    if success:
        print(f"✅ Contraseña actualizada para usuario {usuario_id} en TiendaPro Manager")
    else:
        print(f"❌ Error al actualizar contraseña del usuario {usuario_id}")
    return success

# --- FUNCIONES DE PRODUCTOS ---
def get_all_products_df():
    query = "SELECT ProductoID, NombreProducto, PrecioUnitario, Stock FROM productos ORDER BY NombreProducto ASC"
    result = execute_query(query, fetch=True)
    if result:
        df = pd.DataFrame(result)
        print(f"✅ Obtenidos {len(df)} productos de la BD - TiendaPro Manager")
        return df
    print("❌ No se pudieron obtener productos")
    return pd.DataFrame()

def add_product(nombre, precio, stock_inicial):
    query = "INSERT INTO productos (NombreProducto, PrecioUnitario, Stock) VALUES (%s, %s, %s)"
    params = (nombre, precio, stock_inicial)
    success = execute_query(query, params, commit=True)
    if success:
        print(f"✅ Producto '{nombre}' AGREGADO a la BD - TiendaPro Manager")
    else:
        print(f"❌ ERROR al agregar producto '{nombre}'")
    return success

def update_product_stock(producto_id, cantidad_a_sumar):
    query = "UPDATE productos SET Stock = Stock + %s WHERE ProductoID = %s"
    params = (cantidad_a_sumar, producto_id)
    success = execute_query(query, params, commit=True)
    if success:
        print(f"✅ Stock del producto {producto_id} ACTUALIZADO en BD (+{cantidad_a_sumar})")
    else:
        print(f"❌ ERROR al actualizar stock del producto {producto_id}")
    return success

def update_product_details(producto_id, nombre_nuevo, precio_nuevo):
    query = "UPDATE productos SET NombreProducto = %s, PrecioUnitario = %s WHERE ProductoID = %s"
    params = (nombre_nuevo, precio_nuevo, producto_id)
    success = execute_query(query, params, commit=True)
    if success:
        print(f"✅ Producto {producto_id} ACTUALIZADO en BD: {nombre_nuevo}")
    else:
        print(f"❌ ERROR al actualizar producto {producto_id}")
    return success

def delete_product(producto_id):
    query = "DELETE FROM productos WHERE ProductoID = %s"
    params = (producto_id,)
    success = execute_query(query, params, commit=True)
    if success:
        print(f"✅ Producto {producto_id} ELIMINADO de BD - TiendaPro Manager")
    else:
        print(f"❌ ERROR al eliminar producto {producto_id}")
    return success

# --- FUNCIONES DE VENTAS ---
def record_sale(producto_id, cantidad, precio_unitario, ingreso_total):
    conn = create_db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        # 1. Registrar la venta
        sale_query = "INSERT INTO ventas (ProductoID, Cantidad, PrecioUnitario, IngresoTotal) VALUES (%s, %s, %s, %s)"
        sale_params = (producto_id, cantidad, precio_unitario, ingreso_total)
        cursor.execute(sale_query, sale_params)

        # 2. Actualizar el stock
        stock_query = "UPDATE productos SET Stock = Stock - %s WHERE ProductoID = %s"
        stock_params = (cantidad, producto_id)
        cursor.execute(stock_query, stock_params)

        conn.commit()
        print(f"✅ Venta REGISTRADA en TiendaPro Manager para producto {producto_id}, cantidad {cantidad}")
        return True
    except Error as e:
        print(f"❌ Error en transacción de venta: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_product_stock(producto_id):
    query = "SELECT Stock FROM productos WHERE ProductoID = %s"
    params = (producto_id,)
    result = execute_query(query, params, fetch=True)
    if result:
        stock = result[0]['Stock']
        print(f"✅ Stock del producto {producto_id}: {stock}")
        return stock
    print(f"❌ No se pudo obtener stock del producto {producto_id}")
    return 0

# --- FUNCIONES DE CONSULTA ---
def get_product_id_by_name(name):
    query = "SELECT ProductoID FROM productos WHERE NombreProducto = %s"
    params = (name,)
    result = execute_query(query, params, fetch=True)
    if result:
        producto_id = result[0]['ProductoID']
        print(f"✅ ID encontrado para '{name}': {producto_id}")
        return producto_id
    print(f"❌ No se encontró ID para '{name}'")
    return None

def get_product_price_by_id(product_id):
    query = "SELECT PrecioUnitario FROM productos WHERE ProductoID = %s"
    params = (product_id,)
    result = execute_query(query, params, fetch=True)
    if result:
        precio = float(result[0]['PrecioUnitario'])
        print(f"✅ Precio del producto {product_id}: {precio}")
        return precio
    print(f"❌ No se pudo obtener precio del producto {product_id}")
    return 0.0

def get_all_product_names():
    query = "SELECT NombreProducto FROM productos ORDER BY NombreProducto ASC"
    result = execute_query(query, fetch=True)
    if result:
        nombres = [item['NombreProducto'] for item in result]
        print(f"✅ Obtenidos {len(nombres)} nombres de productos - TiendaPro Manager")
        return nombres
    print("❌ No se pudieron obtener nombres de productos")
    return []

def get_product_by_id(product_id):
    query = "SELECT NombreProducto, PrecioUnitario, Stock FROM productos WHERE ProductoID = %s"
    params = (product_id,)
    result = execute_query(query, params, fetch=True)
    if result:
        return result[0]
    return None

# --- FUNCIONES DE REPORTES ---
def get_low_stock_products(threshold=10):
    query = "SELECT NombreProducto, Stock FROM productos WHERE Stock <= %s ORDER BY Stock ASC"
    params = (threshold,)
    result = execute_query(query, params, fetch=True)
    if result:
        df = pd.DataFrame(result)
        print(f"✅ Obtenidos {len(df)} productos con bajo stock - TiendaPro Manager")
        return df
    print("❌ No se pudieron obtener productos con bajo stock")
    return pd.DataFrame()

def get_top_selling_products(limit=5, date=None):
    if date:
        query = """
            SELECT P.NombreProducto, SUM(V.Cantidad) AS TotalUnidadesVendidas,
                   SUM(V.IngresoTotal) AS IngresosTotales
            FROM ventas V JOIN productos P ON V.ProductoID = P.ProductoID
            WHERE DATE(V.FechaVenta) = %s
            GROUP BY P.NombreProducto ORDER BY IngresosTotales DESC LIMIT %s
        """
        params = (date, limit)
    else:
        query = """
            SELECT P.NombreProducto, SUM(V.Cantidad) AS TotalUnidadesVendidas,
                   SUM(V.IngresoTotal) AS IngresosTotales
            FROM ventas V JOIN productos P ON V.ProductoID = P.ProductoID
            GROUP BY P.NombreProducto ORDER BY IngresosTotales DESC LIMIT %s
        """
        params = (limit,)
    
    result = execute_query(query, params, fetch=True)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()

def get_daily_sales_summary(date=None):
    if date:
        query = """
            SELECT P.NombreProducto, SUM(V.Cantidad) AS TotalUnidadesVendidas,
                   SUM(V.IngresoTotal) AS IngresosTotales
            FROM ventas V JOIN productos P ON V.ProductoID = P.ProductoID
            WHERE DATE(V.FechaVenta) = %s
            GROUP BY P.NombreProducto ORDER BY IngresosTotales DESC
        """
        params = (date,)
    else:
        query = """
            SELECT P.NombreProducto, SUM(V.Cantidad) AS TotalUnidadesVendidas,
                   SUM(V.IngresoTotal) AS IngresosTotales
            FROM ventas V JOIN productos P ON V.ProductoID = P.ProductoID
            GROUP BY P.NombreProducto ORDER BY IngresosTotales DESC
        """
        params = None
    
    result = execute_query(query, params, fetch=True)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()

def get_all_sales_df():
    query = """
    SELECT V.VentaID, P.NombreProducto, V.Cantidad, V.PrecioUnitario, 
           V.IngresoTotal, V.FechaVenta 
    FROM ventas V JOIN productos P ON V.ProductoID = P.ProductoID
    ORDER BY V.FechaVenta DESC
    """
    result = execute_query(query, fetch=True)
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()

# Inicializar la base de datos
setup_database()