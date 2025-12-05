# 🏪 TiendaPro Manager - Manual de Usuario

## 📋 Tabla de Contenidos
1. [Requisitos del Sistema](#requisitos)
2. [Instalación](#instalación)
3. [Primeros Pasos](#primeros-pasos)
4. [Funciones Principales](#funciones-principales)
5. [Soporte Técnico](#soporte-técnico)

## ⚙️ Requisitos del Sistema {#requisitos}

### Requisitos Mínimos:
- **Sistema Operativo:** Windows 10/11
- **Memoria RAM:** 4 GB
- **Espacio en disco:** 500 MB
- **MySQL:** Versión 5.7 o superior

### Software Requerido:
- ✅ MySQL Server (gratuito)
- ✅ TiendaPro Manager (este programa)

## 🚀 Instalación {#instalación}

### Paso 1: Instalar MySQL
1. Descarga MySQL desde: https://dev.mysql.com/downloads/mysql/
2. Ejecuta el instalador
3. Configura una contraseña para el usuario 'root'
4. Anota la contraseña, la necesitarás

### Paso 2: Crear Base de Datos
1. Abre MySQL Workbench o línea de comandos
2. Ejecuta: `CREATE DATABASE tienda_alimentos;`
3. Verifica que la base de datos se creó

### Paso 3: Ejecutar TiendaPro Manager
1. Ejecuta `TiendaProManager.exe`
2. El programa configurará automáticamente las tablas

## 👋 Primeros Pasos {#primeros-pasos}

### Login Inicial
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### Configuración Inicial
1. **Agregar Productos:** Ve a "Gestión de Productos"
2. **Crear Usuarios:** Ve a "Gestión de Usuarios" (solo admin)
3. **Probar Ventas:** Registra tu primera venta

## 💰 Funciones Principales {#funciones-principales}

### 1. Registrar Ventas
- Selecciona productos del combobox
- Ingresa cantidades
- Agrega al carrito
- Finaliza venta (actualiza stock automáticamente)

### 2. Gestión de Productos
- **Agregar:** Nombre, precio y stock inicial
- **Editar:** Modificar nombre y precio
- **Stock:** Reabastecer inventario
- **Eliminar:** Productos sin ventas registradas

### 3. Reportes de Ventas
- **Diario:** Ventas por fecha específica
- **Histórico:** Todas las ventas
- **Bajo Stock:** Productos con menos de 10 unidades

### 4. Gestión de Usuarios (Solo Administradores)
- **Crear usuarios** con roles (admin/vendedor)
- **Activar/desactivar** usuarios
- **Vendedores** solo ven ventas y reportes básicos

## 🛠️ Soporte Técnico {#soporte-técnico}

### Problemas Comunes:

**Error de Conexión a MySQL:**
- Verifica que MySQL esté ejecutándose
- Confirma la contraseña en db_operations.py
- Verifica que la base de datos 'tienda_alimentos' exista

**Usuario/Contraseña Incorrectos:**
- Usuario: `admin` - Contraseña: `admin123`
- Usuario: `vendedor` - Contraseña: `vendedor123`

**Producto No Encontrado:**
- Verifica que el producto esté registrado primero

### Contacto de Soporte:
- **Email:** [roldanjuan340@gmail.com]

---

**© 2024 TiendaPro Manager - Sistema Profesional de Gestión Comercial**