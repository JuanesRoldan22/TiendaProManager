"""
TiendaPro Manager - Sistema de Gestión Comercial
Módulo de línea de comandos para registro de ventas
Versión 1.0
"""

import mysql.connector
from datetime import datetime
import time
import sys

# =================================================================
# CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS
# =================================================================

DB_CONFIG = {
    'user': 'root',
    'password': 'abril2025',
    'host': '127.0.0.1',
    'database': 'tienda_alimentos'
}

# =================================================================
# UTILIDADES Y CONEXIÓN
# =================================================================

def mostrar_mensaje(mensaje, es_error=False):
    """Muestra un mensaje en la consola con formato."""
    if es_error:
        print("\n\n#####################################################")
        print(f"!!! ERROR: {mensaje} !!!")
        print("#####################################################\n")
    else:
        print(f"--- {mensaje} ---")

def obtener_conexion():
    """Intenta establecer y retornar la conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        mostrar_mensaje(f"Fallo al conectar a MySQL: {err}", es_error=True)
        return None
    
# =================================================================
# INTERFACES DE USUARIO
# =================================================================

def obtener_datos_venta():
    """Pide al usuario los datos para registrar una venta."""
    try:
        nombre = input("▶️ Nombre del Producto: ").strip()
        cantidad = int(input("▶️ Cantidad vendida: "))
        if cantidad <= 0:
            mostrar_mensaje("La cantidad debe ser mayor que cero.", es_error=True)
            return None, None
        return nombre, cantidad
    except ValueError:
        mostrar_mensaje("Error: La cantidad debe ser un número entero válido.", es_error=True)
        return None, None

def obtener_datos_producto():
    """Pide al usuario los datos para registrar un nuevo producto."""
    try:
        nombre = input("▶️ Nombre del Nuevo Producto: ").strip()
        precio = float(input("▶️ Precio Unitario (ej: 3500.00): "))
        if precio <= 0:
            mostrar_mensaje("El precio debe ser positivo.", es_error=True)
            return None, None
        return nombre, precio
    except ValueError:
        mostrar_mensaje("Error: El precio debe ser un número válido.", es_error=True)
        return None, None

# =================================================================
# GESTIÓN DE PRODUCTOS
# =================================================================

def registrar_nuevo_producto(nombre, precio):
    """Registra un nuevo producto en la tabla Productos."""
    conn = obtener_conexion()
    if conn is None: return
    cursor = conn.cursor()
    
    try:
        # Verificar si el producto ya existe
        query_check = "SELECT ProductoID FROM Productos WHERE NombreProducto = %s"
        cursor.execute(query_check, (nombre,))
        if cursor.fetchone():
            mostrar_mensaje(f"ADVERTENCIA: El producto '{nombre}' ya existe.", es_error=False)
            return

        # Comando SQL para insertar el nuevo producto
        query_insert = "INSERT INTO Productos (NombreProducto, PrecioUnitario) VALUES (%s, %s)"
        cursor.execute(query_insert, (nombre, precio))
        conn.commit()
        
        mostrar_mensaje(f"Nuevo producto registrado con éxito:")
        print(f"  Nombre: {nombre} | Precio: {precio:.2f}")
        
    except mysql.connector.Error as err:
        conn.rollback() 
        mostrar_mensaje(f"Error al registrar el producto: {err}", es_error=True)
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# =================================================================
# REGISTRO DE VENTA
# =================================================================

def registrar_venta(nombre_producto, cantidad):
    """Registra una venta, buscando el ProductoID y el precio unitario."""
    conn = obtener_conexion()
    if conn is None: return
    cursor = conn.cursor()
    
    try:
        # Buscar el ID del producto y su precio unitario
        query_producto = "SELECT ProductoID, PrecioUnitario FROM Productos WHERE NombreProducto = %s"
        cursor.execute(query_producto, (nombre_producto,))
        producto_data = cursor.fetchone()
        
        if not producto_data:
            mostrar_mensaje(f"Producto '{nombre_producto}' no encontrado en la base de datos. ¡Añádelo primero!", es_error=True)
            return

        producto_id, precio_unitario = producto_data
        total_linea = precio_unitario * cantidad
        fecha_venta = datetime.now().strftime('%Y-%m-%d') 
        hora_venta = datetime.now().strftime('%H:%M:%S')
        
        # Comando SQL para insertar el registro de la venta
        query_insert = """
        INSERT INTO Ventas 
        (ProductoID, FechaVenta, HoraVenta, Cantidad, TotalLinea) 
        VALUES (%s, %s, %s, %s, %s)
        """
        datos_venta = (producto_id, fecha_venta, hora_venta, cantidad, total_linea)
        
        cursor.execute(query_insert, datos_venta)
        conn.commit()
        
        mostrar_mensaje(f"Venta registrada con éxito:")
        print(f"  Producto: {nombre_producto} | Total: {total_linea:.2f} | Fecha: {fecha_venta}")
        
    except mysql.connector.Error as err:
        conn.rollback() 
        mostrar_mensaje(f"Error al registrar la venta: {err}", es_error=True)
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# =================================================================
# REPORTE DE VENTAS
# =================================================================

def generar_reporte_ventas(fecha_filtro=None):
    """Genera y muestra el reporte consolidado, opcionalmente filtrado por una fecha."""
    conn = obtener_conexion()
    if conn is None: return
    cursor = conn.cursor()
    
    # 1. Base de la consulta (JOIN, SUM, GROUP BY)
    query_reporte = """
    SELECT
        P.NombreProducto,
        SUM(V.Cantidad) AS TotalUnidadesVendidas,
        SUM(V.TotalLinea) AS IngresosTotales
    FROM
        Ventas AS V
    JOIN 
        Productos AS P ON V.ProductoID = P.ProductoID
    """
    
    # 2. Construcción dinámica del filtro WHERE
    parametros = []
    filtro_titulo = " (HISTÓRICO)"
    if fecha_filtro:
        query_reporte += " WHERE V.FechaVenta = %s "
        parametros.append(fecha_filtro)
        filtro_titulo = f" (FILTRADO POR: {fecha_filtro})"

    # 3. Finalización de la consulta
    query_reporte += " GROUP BY P.NombreProducto ORDER BY IngresosTotales DESC;"
    
    try:
        print("\n" + "="*70)
        print(f"📊 REPORTE DE VENTAS CONSOLIDADO - TiendaPro Manager {filtro_titulo}")
        print("="*70)
        
        cursor.execute(query_reporte, parametros if parametros else None)
        
        print(f"{'Producto':<30} | {'Unidades Vendidas':>10} | {'Ingresos Totales':>20}")
        print("-" * 70)

        encontrado = False
        for (nombre, unidades, ingresos) in cursor:
            # Formateo de los resultados
            print(f"{nombre:<30} | {unidades:^17.0f} | ${ingresos:19.2f}")
            encontrado = True

        if not encontrado:
             print(f"{'No se encontraron resultados para este filtro.':^70}")

        print("="*70)

    except mysql.connector.Error as err:
        mostrar_mensaje(f"Error al generar el reporte: {err}", es_error=True)
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# =================================================================
# MENÚ PRINCIPAL (CONTROL DE FLUJO DE LA APLICACIÓN)
# =================================================================

def menu_principal():
    """Muestra el menú principal y gestiona las opciones del usuario."""
    while True:
        print("\n\n" + "="*40)
        print("       TIENDAPRO MANAGER - SISTEMA CLI")
        print("="*40)
        print("1. 💰 Registrar Nueva Venta")
        print("2. 🔍 Generar Reporte de Ventas")
        print("3. ➕ Añadir Nuevo Producto")
        print("4. 🚪 Salir")
        print("-" * 40)
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == '1':
            print("\n--- REGISTRAR VENTA ---")
            nombre, cantidad = obtener_datos_venta()
            if nombre and cantidad:
                registrar_venta(nombre, cantidad)
                
        elif opcion == '2':
            print("\n--- GENERAR REPORTE ---")
            filtro = input("¿Desea filtrar por fecha? (YYYY-MM-DD o dejar vacío para histórico): ").strip()
            generar_reporte_ventas(filtro if filtro else None)
            
        elif opcion == '3':
            print("\n--- AÑADIR PRODUCTO ---")
            nombre, precio = obtener_datos_producto()
            if nombre and precio:
                registrar_nuevo_producto(nombre, precio)
                
        elif opcion == '4':
            mostrar_mensaje("Saliendo del TiendaPro Manager. ¡Hasta pronto!")
            sys.exit()
            
        else:
            mostrar_mensaje("Opción no válida. Por favor, intente de nuevo.", es_error=True)

# =================================================================
# INICIO DEL PROGRAMA
# =================================================================
if __name__ == "__main__":
    print("🏪 TiendaPro Manager - Versión de Línea de Comandos")
    print("Sistema de Gestión Comercial para Pequeños Negocios\n")
    
    # Verifica la conexión antes de iniciar el menú
    if obtener_conexion():
        menu_principal()
    else:
        mostrar_mensaje("No se pudo conectar a la base de datos. Verifique DB_CONFIG.", es_error=True)