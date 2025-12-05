# ❓ Preguntas Frecuentes - TiendaPro Manager

## 🔧 INSTALACIÓN Y CONFIGURACIÓN

### ❓ ¿Cómo instalo MySQL?
**✅ Respuesta:**
1. Ve a https://dev.mysql.com/downloads/mysql/
2. Descarga MySQL Community Server
3. Ejecuta el instalador y sigue los pasos
4. **Importante:** Anota la contraseña del usuario 'root'
5. El programa funciona con MySQL 5.7, 8.0, o versiones superiores

### ❓ ¿Qué hago si sale "Error de conexión a MySQL"?
**✅ Solución paso a paso:**
1. Verifica que el servicio MySQL esté ejecutándose
   - Presiona `Win + R`, escribe `services.msc`
   - Busca "MySQL" y asegúrate que esté "En ejecución"
2. Verifica la contraseña en el archivo `db_operations.py`
3. Confirma que la base de datos 'tienda_alimentos' existe

### ❓ ¿Puedo usar el programa sin instalar MySQL?
**✅ Respuesta:**
Actualmente requiere MySQL, pero estamos trabajando en una versión con base de datos incluida. Mientras tanto, MySQL es gratuito y fácil de instalar.

## 🔐 USUARIOS Y CONTRASEÑAS

### ❓ ¿Cuáles son los usuarios por defecto?
**✅ Credenciales iniciales:**
- **Administrador:** 
  - Usuario: `admin`
  - Contraseña: `admin123`
  - Acceso completo a todas las funciones

- **Vendedor:**
  - Usuario: `vendedor` 
  - Contraseña: `vendedor123`
  - Solo puede registrar ventas y ver reportes

### ❓ ¿Cómo cambio una contraseña?
**✅ Procedimiento:**
1. Inicia sesión como administrador
2. Ve a la pestaña "Gestión de Usuarios"
3. Selecciona el usuario y usa la función de cambiar contraseña

### ❓ ¿Qué hago si olvidé mi contraseña?
**✅ Solución:**
Contacta al administrador del sistema o reinstala la base de datos (esto borrará todos los datos).

## 💰 VENTAS Y PRODUCTOS

### ❓ ¿Por qué no puedo encontrar un producto al registrar una venta?
**✅ Causas posibles:**
- El producto no está registrado en "Gestión de Productos"
- El nombre está escrito diferente (es case-sensitive)
- El producto fue eliminado

**Solución:** Ve a "Gestión de Productos" y agrega el producto primero.

### ❓ ¿Por qué no me deja vender más de X unidades?
**✅ Razón:**
El sistema valida el stock disponible. Si intentas vender más unidades de las que hay en inventario, mostrará un error.

**Solución:** Reabastece el stock en "Gestión de Productos".

### ❓ ¿Cómo actualizo el precio de un producto?
**✅ Procedimiento:**
1. Ve a "Gestión de Productos"
2. Selecciona el producto en la lista inferior
3. Edita el precio en los campos superiores
4. Haz clic en "Guardar Cambios"

## 📊 REPORTES Y DATOS

### ❓ ¿Los reportes incluyen todas las fechas?
**✅ Opciones disponibles:**
- **Reporte Diario:** Solo ventas de una fecha específica
- **Reporte Histórico:** Todas las ventas registradas
- **Filtro por Fecha:** Usa el selector de fecha para filtrar

### ❓ ¿Cómo sé qué productos necesito reabastecer?
**✅ Alertas automáticas:**
- El sistema muestra alertas en la pestaña de ventas
- Ve a "Reportes de Ventas" → "Reporte Bajo Stock"
- Productos con menos de 10 unidades se marcan en rojo

### ❓ ¿Puedo exportar los reportes a Excel?
**✅ Actualmente:**
Los reportes se muestran en pantalla. Para exportar:
1. Copia los datos del reporte
2. Pégarlos en Excel
3. **Próxima versión:** Incluiremos exportación directa

## 🛠️ PROBLEMAS TÉCNICOS

### ❓ ¿El programa se cierra inesperadamente?
**✅ Soluciones:**
1. Verifica que MySQL esté ejecutándose
2. Ejecuta el programa como Administrador
3. Verifica que haya espacio en disco suficiente

### ❓ ¿Pierdo mis datos si reinstalo?
**✅ Los datos están seguros en MySQL:**
- Los datos se guardan en la base de datos MySQL
- Mientras no borres la base de datos, tu información está segura
- Recomendamos hacer backups periódicos

### ❓ ¿Cómo hago backup de mis datos?
**✅ Método recomendado:**
1. Abre MySQL Workbench
2. Ve a "Data Export"
3. Selecciona la base de datos 'tienda_alimentos'
4. Exporta como SQL file

## 💳 LICENCIAS Y PAGOS

### ❓ ¿El programa es gratuito?
**✅ Modelo de licencia:**
- **Prueba:** 15 días completos
- **Licencia Personal:** $29 USD (una tienda)
- **Licencia Profesional:** $79 USD (hasta 3 tiendas)
- **Licencia Empresarial:** $149 USD (tiendas ilimitadas)

### ❓ ¿Qué incluye cada licencia?
**✅ Comparativa:**
- **Todas incluyen:** Actualizaciones y soporte básico
- **Profesional y Empresarial:** Soporte prioritario y funciones avanzadas

### ❓ ¿Cómo activo mi licencia?
**✅ Proceso:**
1. Compra la licencia en nuestra tienda online
2. Recibirás un código de activación por email
3. Ingresa el código en la ventana de activación del programa

---

**¿No encontraste tu pregunta?** 
Contacta a nuestro soporte: [roldanjuan340@gmail.com] 📧