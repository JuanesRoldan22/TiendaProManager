🏪 TiendaPro Manager: Sistema de Gestión Comercial y Punto de Venta (POS)

TiendaPro Manager es una solución de escritorio integral desarrollada en Python para la gestión eficiente de inventario, ventas y usuarios, diseñada específicamente para pequeños y medianos comercios (minimarkets, tiendas de abarrotes, etc.).

🎯 Objetivo del Proyecto

El proyecto tiene como objetivo principal automatizar los procesos de venta y contabilidad de stock, minimizando el error humano y ofreciendo reportes precisos para facilitar la toma de decisiones empresariales.

✨ Funcionalidades Destacadas

Punto de Venta (POS) Rápido: Interfaz intuitiva para el registro de ventas, cálculo automático de totales y gestión de carrito.

Control de Inventario en Tiempo Real: Gestión completa de productos (CRUD) y reabastecimiento de stock.

Seguridad Basada en Roles: Módulo de autenticación con roles diferenciados: Administrador (acceso total) y Vendedor (acceso limitado a ventas y reportes básicos).

Reportes y Analíticas: Generación de informes históricos, reportes diarios y alertas de bajo stock para evitar quiebres en la cadena de suministro.

Integridad de Datos: Uso estricto de tipos de datos DECIMAL en la base de datos para garantizar la precisión financiera en precios y transacciones.

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Lenguaje de Programación** | Python 3.11+ | Lógica de negocio y desarrollo de la interfaz gráfica. |
| **Base de Datos** | MySQL Server | Persistencia de datos, transacciones y almacenamiento de inventario. |
| **Generación de Reportes** | Pandas | Utilizado para procesar datos de MySQL y generar informes analíticos. |
| **Distribución** | PyInstaller| Empaquetado de la aplicación en un ejecutable (.exe) para Windows. |


⚙️ Instalación y Configuración

Para ejecutar este proyecto en tu entorno de desarrollo, sigue estos pasos:

1. Requisitos

Python 3.11 o superior.

MySQL Server (Versión 5.7+).

2. Configuración de la Base de Datos

Asegúrate de que MySQL Server esté corriendo.

Accede a MySQL (Workbench o consola) y crea la base de datos:

CREATE DATABASE tienda_alimentos;


El programa se conecta por defecto a esta base de datos. Si deseas cambiar las credenciales de conexión (usuario/contraseña de MySQL), edita la variable DB_CONFIG dentro del archivo db_operations.py.

3. Instalación de Dependencias

Crea y activa tu entorno virtual:

python -m venv venv
.\venv\Scripts\activate


Instala las librerías necesarias (asumiendo que están listadas en un requirements.txt):

pip install -r requirements.txt 
# (Si no tienes requirements.txt, usa: pip install mysql-connector-python pandas)


4. Ejecución

Ejecuta la aplicación principal:

python main_app.py 
# (o el nombre de tu archivo principal)


🔑 Credenciales Iniciales

El sistema se inicializa con el siguiente usuario de administrador por defecto:

| Rol | Usuario | Contraseña |
| :--- | :--- | :--- |
| **Administrador** | admin | admin123 |

🤝 Contribuciones

Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Haz un "Fork" del repositorio.

2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).

3. Haz tus cambios y prueba rigurosamente.

4. Realiza un "Pull Request".

Desarrollado por: JuanesRoldan22
