import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from datetime import datetime, timedelta
import db_operations as db
import licensing  # ✅ NUEVO: Sistema de licencias

# ✅ NUEVA FUNCIÓN: Verificación de licencia al inicio
def verificar_licencia_al_inicio():
    """Verifica la licencia al iniciar la aplicación"""
    status = licensing.license_manager.verify_license()
    
    if status['status'] == 'expired':
        # Mostrar ventana de activación obligatoria
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        messagebox.showerror(
            "Licencia Expirada", 
            "El período de prueba ha expirado.\n\n"
            "Por favor active una licencia para continuar usando TiendaPro Manager.\n\n"
            "Precios:\n"
            "• Personal (1 tienda): $29 USD\n"  
            "• Profesional (3 tiendas): $79 USD\n"
            "• Empresarial (Ilimitado): $149 USD\n\n"
            "Contacto: ventas@tiendapromanager.com"
        )
        
        # Mostrar ventana de activación
        licensing.license_manager.show_activation_window(root)
        
        # Verificar nuevamente después de la activación
        status = licensing.license_manager.verify_license()
        if status['status'] == 'expired':
            root.destroy()
            return False
            
        root.destroy()
    
    return True

# --- VENTANA DE LOGIN ---
class LoginWindow(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.usuario_autenticado = None
        
        self.title("🔐 Iniciar Sesión - TiendaPro Manager")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.crear_widgets_login()
        
    def crear_widgets_login(self):
        """Crea los widgets de la ventana de login."""
        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="🏪 TIENDAPRO MANAGER", 
            font=('Helvetica', 16, 'bold'),
            bootstyle="primary"
        )
        titulo.pack(pady=(0, 20))
        
        # Subtítulo
        subtitulo = ttk.Label(
            main_frame,
            text="Ingrese sus credenciales para continuar",
            font=('Helvetica', 10),
            bootstyle="secondary"
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame de formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill='x', pady=10)
        
        # Campo de usuario
        ttk.Label(form_frame, text="Usuario:", font=('Helvetica', 10)).grid(
            row=0, column=0, sticky='w', pady=8, padx=(0, 10)
        )
        self.entry_usuario = ttk.Entry(form_frame, width=20, font=('Helvetica', 10))
        self.entry_usuario.grid(row=0, column=1, sticky='ew', pady=8)
        self.entry_usuario.focus()
        
        # Campo de contraseña
        ttk.Label(form_frame, text="Contraseña:", font=('Helvetica', 10)).grid(
            row=1, column=0, sticky='w', pady=8, padx=(0, 10)
        )
        self.entry_password = ttk.Entry(form_frame, width=20, show='*', font=('Helvetica', 10))
        self.entry_password.grid(row=1, column=1, sticky='ew', pady=8)
        
        # Configurar columnas
        form_frame.columnconfigure(1, weight=1)
        
        # Botón de login
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=20)
        
        self.btn_login = ttk.Button(
            btn_frame,
            text="🔓 Iniciar Sesión",
            command=self.autenticar,
            bootstyle="success",
            width=15
        )
        self.btn_login.pack(pady=10)
        
        # Bind Enter key para login
        self.entry_password.bind('<Return>', lambda e: self.autenticar())
        
        # Credenciales por defecto (solo para desarrollo)
        cred_frame = ttk.Frame(main_frame)
        cred_frame.pack(fill='x', pady=10)
        
        ttk.Label(
            cred_frame, 
            text="💡 Demo: admin/admin123 | vendedor/vendedor123", 
            font=('Helvetica', 8),
            bootstyle="info"
        ).pack()
        
    def autenticar(self):
        """Autentica al usuario."""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
            
        self.btn_login.config(state='disabled', text="Autenticando...")
        self.update()
        
        # Verificar credenciales
        usuario_info = db.verificar_usuario(usuario, password)
        
        if usuario_info:
            self.usuario_autenticado = usuario_info
            self.destroy()  # Cierra la ventana de login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            self.btn_login.config(state='normal', text="🔓 Iniciar Sesión")
            self.entry_password.delete(0, 'end')
            self.entry_usuario.focus()

# --- APLICACIÓN PRINCIPAL ---
class TiendaProManager(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        
        # ✅ VERIFICAR LICENCIA PRIMERO
        if not verificar_licencia_al_inicio():
            self.destroy()  # Cerrar aplicación si no hay licencia válida
            return
        
        self.title("🏪 TiendaPro Manager - Sistema de Gestión Comercial")
        self.geometry("1200x800")
        
        # Variables de estado
        self.productos_venta = []
        self.producto_seleccionado_id = None
        self.usuario_autenticado = None
        
        # ✅ PRIMERO: Mostrar login
        self.mostrar_login()
        
    def mostrar_login(self):
        """Muestra la ventana de login."""
        login_window = LoginWindow(self)
        self.wait_window(login_window)  # Espera a que se cierre el login
        
        if login_window.usuario_autenticado:
            self.usuario_autenticado = login_window.usuario_autenticado
            self.inicializar_aplicacion()
        else:
            self.destroy()  # Cierra la aplicación si no se autentica
            
    def inicializar_aplicacion(self):
        """Inicializa la aplicación después del login exitoso."""
        # Actualizar título con información del usuario y licencia
        status_text = licensing.license_manager.get_license_status_message()
        titulo_usuario = f"🏪 TiendaPro Manager - {self.usuario_autenticado['nombre_completo']} ({self.usuario_autenticado['rol']}) | {status_text}"
        self.title(titulo_usuario)
        
        print(f"🎉 Usuario autenticado: {self.usuario_autenticado['nombre_completo']}")

        # Configuración de Pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Crear Pestañas (solo las permitidas según el rol)
        self.crear_pestañas_segun_rol()

        # Inicializar Componentes - SOLO LOS QUE CORRESPONDAN AL ROL
        self.setup_venta_tab()
        
        if hasattr(self, 'tab_reportes'):
            self.setup_reportes_tab()
            
        # Solo administradores tienen estas pestañas
        if self.usuario_autenticado['rol'] == 'administrador':
            if hasattr(self, 'tab_gestion'):
                self.setup_gestion_tab()
            if hasattr(self, 'tab_usuarios'):
                self.setup_usuarios_tab()

        # ✅ AGREGAR MENÚ DE LICENCIA
        self.crear_menu_licencia()

        # Inicializar datos - SOLO LOS NECESARIOS
        self.cargar_productos_combobox()
        
        # Solo cargar lista de productos si es administrador
        if self.usuario_autenticado['rol'] == 'administrador' and hasattr(self, 'tree_productos'):
            self.cargar_lista_productos()
        
    def crear_menu_licencia(self):
        """Crea el menú de licencia en la barra de título."""
        # Frame para información de licencia
        license_frame = ttk.Frame(self)
        license_frame.pack(side='top', fill='x', padx=10, pady=5)
        
        # Botón de información de licencia
        license_btn = ttk.Button(
            license_frame, 
            text="🔐 Licencia", 
            command=self.mostrar_info_licencia,
            bootstyle="info",
            width=12
        )
        license_btn.pack(side='right')
        
    def mostrar_info_licencia(self):
        """Muestra información de la licencia actual."""
        status = licensing.license_manager.verify_license()
        
        if status['status'] == 'licensed':
            messagebox.showinfo(
                "Información de Licencia",
                f"✅ LICENCIA ACTIVA\n\n"
                f"Email: {status['email']}\n"
                f"Días restantes: {status['days_remaining']}\n"
                f"Fecha de expiración: {status['expiry_date'].strftime('%d/%m/%Y')}\n\n"
                f"¡Gracias por usar TiendaPro Manager!"
            )
        elif status['status'] == 'trial':
            messagebox.showinfo(
                "Versión de Prueba",
                f"🆓 VERSIÓN DE PRUEBA\n\n"
                f"Días restantes: {status['days_remaining']}\n\n"
                f"Para adquirir una licencia completa:\n"
                f"• Personal (1 tienda): $29 USD\n"  
                f"• Profesional (3 tiendas): $79 USD\n"
                f"• Empresarial (Ilimitado): $149 USD\n\n"
                f"Contacto: ventas@tiendapromanager.com"
            )
            # Ofrecer activación
            if messagebox.askyesno("Activar Licencia", "¿Desea activar una licencia ahora?"):
                licensing.license_manager.show_activation_window(self)
                # Actualizar título
                status_text = licensing.license_manager.get_license_status_message()
                titulo_actual = self.title()
                nuevo_titulo = titulo_actual.split('|')[0] + f"| {status_text}"
                self.title(nuevo_titulo)
        
    def crear_pestañas_segun_rol(self):
        """Crea las pestañas según el rol del usuario."""
        rol = self.usuario_autenticado['rol']
        
        # Todos los roles tienen acceso a ventas
        self.tab_venta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_venta, text="💰 Registrar Venta")
        
        # Solo administradores tienen acceso completo
        if rol == 'administrador':
            self.tab_gestion = ttk.Frame(self.notebook)
            self.tab_reportes = ttk.Frame(self.notebook)
            self.tab_usuarios = ttk.Frame(self.notebook)
            
            self.notebook.add(self.tab_gestion, text="📦 Gestión de Productos")
            self.notebook.add(self.tab_reportes, text="📊 Reportes de Ventas")
            self.notebook.add(self.tab_usuarios, text="👥 Gestión de Usuarios")
        else:
            # Vendedores solo ven reportes básicos
            self.tab_reportes = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_reportes, text="📊 Reportes de Ventas")
            
    def on_tab_change(self, event):
        """Evento que se dispara al cambiar de pestaña."""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        print(f"🔄 Cambiando a pestaña: {selected_tab}")
        
        if selected_tab == "Gestión de Productos" and hasattr(self, 'tab_gestion'):
            self.cargar_productos_combobox()
            # Solo cargar lista si es administrador
            if self.usuario_autenticado['rol'] == 'administrador':
                self.cargar_lista_productos()
        
        elif selected_tab == "Registrar Venta":
            self.cargar_productos_combobox()

        elif selected_tab == "Reportes de Ventas" and hasattr(self, 'tab_reportes'):
            self.generar_reporte_gui(historico=True)
            
        elif selected_tab == "Gestión de Usuarios" and hasattr(self, 'tab_usuarios'):
            if self.usuario_autenticado['rol'] == 'administrador':
                self.cargar_lista_usuarios()

    # --- PESTAÑA DE VENTA ---
    def setup_venta_tab(self):
        """Configura los widgets de la pestaña de registro de ventas."""
        
        main_frame = ttk.Frame(self.tab_venta, padding=15)
        main_frame.pack(fill='both', expand=True)

        # Frame de Carrito
        carrito_frame = ttk.Labelframe(main_frame, text="🛒 Carrito de Venta", padding=10, bootstyle="primary")
        carrito_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Widgets de entrada
        input_frame = ttk.Frame(carrito_frame)
        input_frame.pack(fill='x', pady=10)

        ttk.Label(input_frame, text="Producto:").pack(side='left', padx=(0, 5))
        
        self.combo_productos_venta = ttk.Combobox(input_frame, state="readonly", width=30)
        self.combo_productos_venta.pack(side='left', padx=(0, 15), fill='x', expand=True)
        self.combo_productos_venta.bind("<<ComboboxSelected>>", self.actualizar_precio_display)

        ttk.Label(input_frame, text="Cantidad:").pack(side='left', padx=(0, 5))
        self.entry_cantidad_venta = ttk.Entry(input_frame, width=10)
        self.entry_cantidad_venta.pack(side='left', padx=(0, 15))
        self.entry_cantidad_venta.insert(0, "1")

        ttk.Label(input_frame, text="Precio U:").pack(side='left', padx=(0, 5))
        self.label_precio_unitario = ttk.Label(input_frame, text="0.00", bootstyle="info")
        self.label_precio_unitario.pack(side='left', padx=(0, 15))

        ttk.Button(input_frame, text="➕ Agregar al Carrito", command=self.agregar_a_carrito, bootstyle="success").pack(side='left')

        # Treeview para el Carrito
        self.tree_carrito = ttk.Treeview(carrito_frame, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings", height=10, bootstyle="primary")
        self.tree_carrito.heading("Producto", text="Producto")
        self.tree_carrito.heading("Cantidad", text="Cantidad")
        self.tree_carrito.heading("Precio", text="Precio U.")
        self.tree_carrito.heading("Subtotal", text="Subtotal")
        self.tree_carrito.column("Cantidad", width=70, anchor=CENTER)
        self.tree_carrito.column("Precio", width=100, anchor=E)
        self.tree_carrito.column("Subtotal", width=100, anchor=E)
        self.tree_carrito.pack(fill='both', expand=True, pady=10)

        # Botones del carrito
        ttk.Button(carrito_frame, text="🗑️ Quitar Seleccionado", command=self.quitar_de_carrito, bootstyle="danger").pack(fill='x', pady=(0, 10))

        # Resumen y Finalización
        resumen_frame = ttk.Frame(carrito_frame, relief='raised', padding=10, bootstyle="secondary")
        resumen_frame.pack(fill='x', pady=10)

        self.label_total = ttk.Label(resumen_frame, text="TOTAL: $0.00", font=('Helvetica', 16, 'bold'), bootstyle="warning")
        self.label_total.pack(side='left', padx=10)

        ttk.Button(resumen_frame, text="✅ Finalizar Venta", command=self.finalizar_venta_gui, bootstyle="success").pack(side='right', padx=10)
        ttk.Button(resumen_frame, text="Cerrar Carrito", command=self.cerrar_carrito, bootstyle="secondary").pack(side='right', padx=10)

        # Frame de Mensajes
        message_frame = ttk.Labelframe(main_frame, text="Estado de Stock", padding=10, bootstyle="info")
        message_frame.pack(side="right", fill="y", padx=10, pady=5)
        
        self.stock_message_text = tk.Text(message_frame, height=15, width=40, state='disabled', wrap='word', foreground='#333333', background='#F0F0F0')
        self.stock_message_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.display_low_stock()

    def actualizar_precio_display(self, event=None):
        """Muestra el precio unitario del producto seleccionado."""
        nombre_producto = self.combo_productos_venta.get()
        if nombre_producto:
            producto_id = db.get_product_id_by_name(nombre_producto)
            precio = db.get_product_price_by_id(producto_id)
            self.label_precio_unitario.config(text=f"{precio:,.2f}")
    
    def display_low_stock(self):
        """Muestra una advertencia de bajo stock."""
        df_low_stock = db.get_low_stock_products(threshold=10)
        
        self.stock_message_text.config(state='normal')
        self.stock_message_text.delete(1.0, END)
        
        if df_low_stock.empty:
            self.stock_message_text.insert(END, "✅ ¡Todos los productos tienen buen stock!\n\n(Umbral: 10 unidades)")
        else:
            self.stock_message_text.insert(END, "🚨 ALERTA DE BAJO STOCK 🚨\n\n", "alert")
            for index, row in df_low_stock.iterrows():
                self.stock_message_text.insert(END, f"- {row['NombreProducto']}: {row['Stock']} uds\n")
            self.stock_message_text.insert(END, "\n¡Hora de reabastecer!")
            
        self.stock_message_text.config(state='disabled')
        self.stock_message_text.tag_config("alert", foreground="red", font=('Helvetica', 10, 'bold'))

    def agregar_a_carrito(self):
        """Agrega un producto al carrito de venta."""
        nombre_producto = self.combo_productos_venta.get()
        cantidad_str = self.entry_cantidad_venta.get()

        if not nombre_producto:
            messagebox.showerror("Error de Venta", "Debe seleccionar un producto.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de Venta", "Cantidad inválida. Debe ser un número entero positivo.")
            return

        producto_id = db.get_product_id_by_name(nombre_producto)
        precio_unitario = float(db.get_product_price_by_id(producto_id))
        subtotal = cantidad * precio_unitario
        
        # Verificar stock
        stock_actual = db.get_product_stock(producto_id)
        if cantidad > stock_actual:
            messagebox.showwarning("Stock Insuficiente", f"Solo quedan {stock_actual} unidades de {nombre_producto}. No se puede agregar la cantidad solicitada.")
            return
            
        # Revisar si el producto ya está en el carrito
        producto_encontrado = False
        for item in self.productos_venta:
            if item['ProductoID'] == producto_id:
                item['Cantidad'] += cantidad
                item['Subtotal'] = float(item['Cantidad']) * float(item['PrecioUnitario'])
                producto_encontrado = True
                break

        if not producto_encontrado:
            self.productos_venta.append({
                "ProductoID": producto_id,
                "NombreProducto": nombre_producto,
                "Cantidad": cantidad,
                "PrecioUnitario": precio_unitario,
                "Subtotal": subtotal
            })

        self.actualizar_carrito_display()
        self.entry_cantidad_venta.delete(0, END)
        self.entry_cantidad_venta.insert(0, "1")

    def quitar_de_carrito(self):
        """Quita el producto seleccionado del carrito."""
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Selección Requerida", "Seleccione un producto del carrito para quitar.")
            return

        item_data = self.tree_carrito.item(seleccion, 'values')
        nombre_producto_a_quitar = item_data[0] 
        
        self.productos_venta = [item for item in self.productos_venta if item['NombreProducto'] != nombre_producto_a_quitar]
        self.actualizar_carrito_display()

    def cerrar_carrito(self):
        """Limpia el carrito sin finalizar la venta."""
        self.productos_venta = []
        self.actualizar_carrito_display()

    def actualizar_carrito_display(self):
        """Actualiza el Treeview del carrito y calcula el total."""
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)

        total_venta = 0.0
        
        for item in self.productos_venta:
            subtotal = float(item['Subtotal'])
            total_venta += subtotal
            
            self.tree_carrito.insert("", "end", 
                values=(
                    item['NombreProducto'], 
                    item['Cantidad'], 
                    f"${float(item['PrecioUnitario']):,.2f}",
                    f"${subtotal:,.2f}"
                )
            )

        self.label_total.config(text=f"TOTAL: ${total_venta:,.2f}")
        
    def finalizar_venta_gui(self):
        """Procesa la venta y registra las transacciones."""
        if not self.productos_venta:
            messagebox.showwarning("Carrito Vacío", "No hay productos en el carrito para vender.")
            return

        if not messagebox.askyesno("Confirmar Venta", f"¿Desea finalizar la venta por {self.label_total.cget('text').split(': ')[1]}?"):
            return

        exito_total = True
        
        for item in self.productos_venta:
            producto_id = item['ProductoID']
            cantidad = item['Cantidad']
            precio_unitario = float(item['PrecioUnitario'])
            ingreso_total = float(item['Subtotal'])
            
            if not db.record_sale(producto_id, cantidad, precio_unitario, ingreso_total):
                exito_total = False
                print(f"FALLO al registrar la venta para el producto ID: {producto_id}")

        if exito_total:
            messagebox.showinfo("Venta Exitosa", "La venta ha sido registrada exitosamente y el stock actualizado.")
            self.productos_venta = []
            self.actualizar_carrito_display()
            self.display_low_stock()
            # Solo actualizar lista de productos si es administrador
            if self.usuario_autenticado['rol'] == 'administrador' and hasattr(self, 'tree_productos'):
                self.cargar_lista_productos()
        else:
            messagebox.showerror("Error de Venta", "Ocurrió un error al registrar una o más partes de la venta. Se ha deshecho la transacción.")

    # --- PESTAÑA DE GESTIÓN DE PRODUCTOS ---
    def setup_gestion_tab(self):
        """Configura los widgets de la pestaña de gestión de productos."""
        if not hasattr(self, 'tab_gestion'):
            return
            
        main_frame = ttk.Frame(self.tab_gestion, padding=15)
        main_frame.pack(fill='both', expand=True)

        # Frame de Gestión
        gestion_frame = ttk.Labelframe(main_frame, text="➕ Agregar Nuevo Producto", padding=10, bootstyle="primary")
        gestion_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Entradas para Nombre, Precio y Stock Inicial
        input_frame = ttk.Frame(gestion_frame)
        input_frame.pack(fill='x', pady=5)

        ttk.Label(input_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_nombre = ttk.Entry(input_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Precio Unitario:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_precio = ttk.Entry(input_frame, width=15)
        self.entry_precio.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Stock Inicial:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_stock_inicial = ttk.Entry(input_frame, width=15)
        self.entry_stock_inicial.insert(0, "0")
        self.entry_stock_inicial.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Button(gestion_frame, text="➕ Registrar Producto", command=self.registrar_producto_gui, bootstyle="success").pack(pady=10)

        # Frame de Stock
        stock_frame = ttk.Labelframe(main_frame, text="📦 Añadir Stock (Reabastecer)", padding=10, bootstyle="info")
        stock_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        stock_input_frame = ttk.Frame(stock_frame)
        stock_input_frame.pack(fill='x', pady=5)

        ttk.Label(stock_input_frame, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.combo_productos_stock = ttk.Combobox(stock_input_frame, state="readonly", width=30)
        self.combo_productos_stock.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(stock_input_frame, text="Cantidad a Añadir:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_cantidad_stock = ttk.Entry(stock_input_frame, width=15)
        self.entry_cantidad_stock.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Button(stock_frame, text="🔄 Actualizar Stock", command=self.actualizar_stock_gui, bootstyle="warning").pack(pady=10)

        # Frame de Edición
        edit_frame = ttk.Labelframe(main_frame, text="✏️ Editar Producto Seleccionado", padding=10, bootstyle="secondary")
        edit_frame.pack(side="top", fill="x", padx=5, pady=5, anchor='n')

        edit_input_frame = ttk.Frame(edit_frame)
        edit_input_frame.pack(fill='x', pady=5)
        
        # Elementos de edición
        ttk.Label(edit_input_frame, text="Nombre Nuevo:").pack(side='left', padx=5)
        self.edit_nombre = ttk.Entry(edit_input_frame, width=25)
        self.edit_nombre.pack(side='left', padx=5)
        
        ttk.Label(edit_input_frame, text="Precio Nuevo:").pack(side='left', padx=5)
        self.edit_precio = ttk.Entry(edit_input_frame, width=15)
        self.edit_precio.pack(side='left', padx=5)
        
        ttk.Button(edit_frame, text="⚙️ Guardar Cambios", command=self.guardar_cambios_gui, bootstyle="success").pack(side='right', padx=10, pady=5)
        ttk.Button(edit_frame, text="❌ Eliminar Producto", command=self.eliminar_producto_gui, bootstyle="danger").pack(side='right', padx=10, pady=5)

        # Treeview de la lista de productos
        list_frame = ttk.Labelframe(main_frame, text="📋 Lista de Productos", padding=10, bootstyle="dark")
        list_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

        self.tree_productos = ttk.Treeview(list_frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=15, bootstyle="dark")
        self.tree_productos.heading("ID", text="ID")
        self.tree_productos.heading("Nombre", text="Nombre del Producto")
        self.tree_productos.heading("Precio", text="Precio Unitario")
        self.tree_productos.heading("Stock", text="Stock")
        
        self.tree_productos.column("ID", width=50, anchor=CENTER)
        self.tree_productos.column("Nombre", width=300)
        self.tree_productos.column("Precio", width=100, anchor=E)
        self.tree_productos.column("Stock", width=80, anchor=CENTER)
        
        self.tree_productos.pack(fill='both', expand=True)
        self.tree_productos.bind("<<TreeviewSelect>>", self.cargar_producto_seleccionado)

    # --- PESTAÑA DE REPORTES ---
    def setup_reportes_tab(self):
        """Configura los widgets de la pestaña de reportes."""
        if not hasattr(self, 'tab_reportes'):
            return
            
        top_frame = ttk.Frame(self.tab_reportes, padding=15)
        top_frame.pack(fill='x')

        # Control de Fecha y Filtro
        filter_frame = ttk.Labelframe(top_frame, text="📊 Filtro de Reportes de Venta", padding=10, bootstyle="info")
        filter_frame.pack(fill='x', pady=5)

        # ✅ SELECTOR DE FECHA SIMPLIFICADO (compatible con ttkbootstrap)
        ttk.Label(filter_frame, text="Fecha:").pack(side='left', padx=(0, 5))
        
        # Frame para el selector de fecha
        fecha_frame = ttk.Frame(filter_frame)
        fecha_frame.pack(side='left', padx=(0, 10))
        
        # Entrada de fecha con formato guiado
        self.entry_fecha_reporte = ttk.Entry(fecha_frame, width=12, font=('Consolas', 10))
        self.entry_fecha_reporte.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.entry_fecha_reporte.pack(side='left')
        
        # Botón para abrir selector simple de fecha
        ttk.Button(fecha_frame, text="📅", width=3, 
                   command=self.mostrar_selector_fecha, 
                   bootstyle="secondary").pack(side='left', padx=(5, 0))
        
        # Botones de reporte
        ttk.Button(filter_frame, text="📅 Generar Reporte Diario", command=self.generar_reporte_diario_gui, bootstyle="primary").pack(side='left', padx=10)
        ttk.Button(filter_frame, text="📊 Histórico (Todo)", command=lambda: self.generar_reporte_gui(historico=True), bootstyle="secondary").pack(side='left', padx=10)
        ttk.Button(filter_frame, text="🚨 Reporte Bajo Stock", command=self.generar_reporte_bajo_stock, bootstyle="warning").pack(side='right', padx=10)
        
        # Sección de Visualización
        self.report_area = ttk.Frame(self.tab_reportes, padding=15)
        self.report_area.pack(fill='both', expand=True)

        self.report_text = tk.Text(self.report_area, wrap='word', font=('Consolas', 10), state='disabled', padx=5, pady=5)
        self.report_text.pack(fill='both', expand=True)

    def mostrar_selector_fecha(self):
        """Muestra un diálogo simple para seleccionar fecha."""
        selector_fecha = tb.Toplevel(self)
        selector_fecha.title("Seleccionar Fecha")
        selector_fecha.geometry("300x200")
        selector_fecha.transient(self)
        selector_fecha.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(selector_fecha, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Seleccione una fecha:", font=('Helvetica', 12)).pack(pady=10)
        
        # Frame para controles de fecha
        controles_frame = ttk.Frame(main_frame)
        controles_frame.pack(pady=10)
        
        # Año
        ttk.Label(controles_frame, text="Año:").grid(row=0, column=0, padx=5, pady=5)
        año_actual = datetime.now().year
        self.spin_año = tk.Spinbox(controles_frame, from_=2020, to=2030, width=8, 
                                  font=('Consolas', 10), justify='center')
        self.spin_año.delete(0, 'end')
        self.spin_año.insert(0, str(año_actual))
        self.spin_año.grid(row=0, column=1, padx=5, pady=5)
        
        # Mes
        ttk.Label(controles_frame, text="Mes:").grid(row=1, column=0, padx=5, pady=5)
        meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.combo_mes = ttk.Combobox(controles_frame, values=meses, width=8, 
                                     state="readonly", font=('Consolas', 10))
        self.combo_mes.set(datetime.now().strftime('%m'))
        self.combo_mes.grid(row=1, column=1, padx=5, pady=5)
        
        # Día
        ttk.Label(controles_frame, text="Día:").grid(row=2, column=0, padx=5, pady=5)
        self.spin_dia = tk.Spinbox(controles_frame, from_=1, to=31, width=8, 
                                  font=('Consolas', 10), justify='center')
        self.spin_dia.delete(0, 'end')
        self.spin_dia.insert(0, datetime.now().strftime('%d'))
        self.spin_dia.grid(row=2, column=1, padx=5, pady=5)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(pady=10)
        
        ttk.Button(botones_frame, text="Hoy", 
                   command=lambda: self.establecer_fecha_hoy(selector_fecha),
                   bootstyle="secondary").pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Aceptar", 
                   command=lambda: self.aceptar_fecha(selector_fecha),
                   bootstyle="success").pack(side='left', padx=5)
        
        ttk.Button(botones_frame, text="Cancelar", 
                   command=selector_fecha.destroy,
                   bootstyle="danger").pack(side='left', padx=5)

    def establecer_fecha_hoy(self, ventana):
        """Establece la fecha actual en los controles."""
        hoy = datetime.now()
        self.spin_año.delete(0, 'end')
        self.spin_año.insert(0, str(hoy.year))
        self.combo_mes.set(hoy.strftime('%m'))
        self.spin_dia.delete(0, 'end')
        self.spin_dia.insert(0, hoy.strftime('%d'))

    def aceptar_fecha(self, ventana):
        """Acepta la fecha seleccionada y la establece en el campo."""
        try:
            año = int(self.spin_año.get())
            mes = int(self.combo_mes.get())
            dia = int(self.spin_dia.get())
            
            # Validar la fecha
            fecha = datetime(año, mes, dia)
            fecha_str = fecha.strftime('%Y-%m-%d')
            
            # Establecer en el campo de entrada
            self.entry_fecha_reporte.delete(0, 'end')
            self.entry_fecha_reporte.insert(0, fecha_str)
            
            ventana.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", "Fecha inválida. Por favor verifique los valores.")

    def generar_reporte_diario_gui(self):
        """Genera reporte usando la fecha seleccionada."""
        fecha_str = self.entry_fecha_reporte.get().strip()
        
        if not fecha_str:
            messagebox.showwarning("Fecha Requerida", "Por favor, seleccione una fecha.")
            return

        try:
            # Validar formato de fecha
            datetime.strptime(fecha_str, '%Y-%m-%d')
            print(f"📅 Generando reporte para fecha: {fecha_str}")
            self.generar_reporte_gui(date=fecha_str)
        except ValueError:
            messagebox.showerror("Formato Inválido", "El formato de fecha debe ser YYYY-MM-DD.")

    def generar_reporte_gui(self, date=None, historico=False):
        """Genera y muestra el reporte de ventas (diario o histórico)."""
        
        if historico:
            df = db.get_daily_sales_summary()
            titulo = "RESUMEN HISTÓRICO DE VENTAS (TODOS LOS TIEMPOS)"
        else:
            df = db.get_daily_sales_summary(date=date)
            titulo = f"RESUMEN DE VENTAS PARA LA FECHA: {date}"

        self.report_text.config(state='normal')
        self.report_text.delete(1.0, END)
        
        self.report_text.insert(END, titulo + "\n", "titulo")
        self.report_text.insert(END, "=" * len(titulo) + "\n\n")

        if df.empty:
            self.report_text.insert(END, "No se encontraron datos de ventas para este período.\n", "alerta")
        else:
            # Formatear el DataFrame para una mejor visualización en texto
            df['IngresosTotales'] = df['IngresosTotales'].apply(lambda x: f"${float(x):,.2f}")
            df['TotalUnidadesVendidas'] = df['TotalUnidadesVendidas'].astype(int)
            
            # Calcular el Total Global
            if historico:
                 conn = db.create_db_connection()
                 cursor = conn.cursor(dictionary=True)
                 cursor.execute("SELECT SUM(IngresoTotal) AS TotalGlobal FROM ventas")
                 total_global = cursor.fetchone()['TotalGlobal']
                 conn.close()
                 total_global_str = f"${float(total_global):,.2f}" if total_global is not None else "$0.00"
            else:
                 total_global = df['IngresosTotales'].str.replace('[$,]', '', regex=True).astype(float).sum()
                 total_global_str = f"${total_global:,.2f}"

            reporte_str = df.to_string(index=False)
            self.report_text.insert(END, reporte_str + "\n\n")
            self.report_text.insert(END, f"TOTAL DE INGRESOS GLOBALES: {total_global_str}\n", "total")
            
        self.report_text.config(state='disabled')
        self.report_text.tag_config("titulo", font=('Consolas', 12, 'bold'), foreground='#000080')
        self.report_text.tag_config("total", font=('Consolas', 12, 'bold'), foreground='#006400')
        self.report_text.tag_config("alerta", font=('Consolas', 10, 'italic'), foreground='red')

    def generar_reporte_bajo_stock(self):
        """Genera y muestra el reporte de productos con bajo stock."""
        df = db.get_low_stock_products(threshold=10)
        
        titulo = "🚨 REPORTE DE PRODUCTOS CON BAJO STOCK (<= 10 UNIDADES)"
        self.report_text.config(state='normal')
        self.report_text.delete(1.0, END)
        
        self.report_text.insert(END, titulo + "\n", "titulo")
        self.report_text.insert(END, "=" * len(titulo) + "\n\n")

        if df.empty:
            self.report_text.insert(END, "✅ ¡Todos los productos tienen stock por encima del umbral de 10!\n", "success")
        else:
            reporte_str = df.to_string(index=False)
            self.report_text.insert(END, reporte_str + "\n\n")

        self.report_text.config(state='disabled')
        self.report_text.tag_config("titulo", font=('Consolas', 12, 'bold'), foreground='red')
        self.report_text.tag_config("success", font=('Consolas', 10, 'bold'), foreground='green')

    # --- PESTAÑA DE GESTIÓN DE USUARIOS ---
    def setup_usuarios_tab(self):
        """Configura la pestaña de gestión de usuarios (solo admin)."""
        if not hasattr(self, 'tab_usuarios') or self.usuario_autenticado['rol'] != 'administrador':
            return
            
        main_frame = ttk.Frame(self.tab_usuarios, padding=15)
        main_frame.pack(fill='both', expand=True)
        
        # Frame para agregar usuario
        agregar_frame = ttk.Labelframe(main_frame, text="➕ Agregar Nuevo Usuario", padding=10, bootstyle="primary")
        agregar_frame.pack(fill='x', pady=(0, 10))
        
        form_frame = ttk.Frame(agregar_frame)
        form_frame.pack(fill='x', pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_nuevo_usuario = ttk.Entry(form_frame, width=20)
        self.entry_nuevo_usuario.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.entry_nueva_password = ttk.Entry(form_frame, width=20, show='*')
        self.entry_nueva_password.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nombre Completo:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_nombre_completo = ttk.Entry(form_frame, width=20)
        self.entry_nombre_completo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Rol:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.combo_rol = ttk.Combobox(form_frame, values=['vendedor', 'administrador'], state="readonly", width=15)
        self.combo_rol.set('vendedor')
        self.combo_rol.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(agregar_frame, text="➕ Crear Usuario", command=self.crear_usuario_gui, bootstyle="success").pack(pady=10)
        
        # Lista de usuarios
        lista_frame = ttk.Labelframe(main_frame, text="👥 Lista de Usuarios", padding=10, bootstyle="info")
        lista_frame.pack(fill='both', expand=True, pady=5)
        
        self.tree_usuarios = ttk.Treeview(lista_frame, columns=("ID", "Usuario", "Nombre", "Rol", "Estado"), show="headings", height=12)
        self.tree_usuarios.heading("ID", text="ID")
        self.tree_usuarios.heading("Usuario", text="Usuario")
        self.tree_usuarios.heading("Nombre", text="Nombre Completo")
        self.tree_usuarios.heading("Rol", text="Rol")
        self.tree_usuarios.heading("Estado", text="Estado")
        
        self.tree_usuarios.column("ID", width=50, anchor=CENTER)
        self.tree_usuarios.column("Usuario", width=100)
        self.tree_usuarios.column("Nombre", width=200)
        self.tree_usuarios.column("Rol", width=100, anchor=CENTER)
        self.tree_usuarios.column("Estado", width=80, anchor=CENTER)
        
        self.tree_usuarios.pack(fill='both', expand=True)
        
        # Botones de acción
        btn_frame = ttk.Frame(lista_frame)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="🔄 Actualizar Lista", command=self.cargar_lista_usuarios, bootstyle="primary").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✅ Activar", command=self.activar_usuario_gui, bootstyle="success").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="⛔ Desactivar", command=self.desactivar_usuario_gui, bootstyle="danger").pack(side='left', padx=5)
        
        # Cargar lista inicial
        self.cargar_lista_usuarios()

    def crear_usuario_gui(self):
        """Crea un nuevo usuario desde la interfaz."""
        usuario = self.entry_nuevo_usuario.get().strip()
        password = self.entry_nueva_password.get().strip()
        nombre_completo = self.entry_nombre_completo.get().strip()
        rol = self.combo_rol.get()
        
        if not all([usuario, password, nombre_completo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if db.crear_usuario(usuario, password, nombre_completo, rol):
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' creado correctamente")
            self.entry_nuevo_usuario.delete(0, 'end')
            self.entry_nueva_password.delete(0, 'end')
            self.entry_nombre_completo.delete(0, 'end')
            self.combo_rol.set('vendedor')
            self.cargar_lista_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario. ¿Ya existe?")

    def cargar_lista_usuarios(self):
        """Carga la lista de usuarios en el Treeview."""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
            
        usuarios = db.obtener_usuarios()
        for usuario in usuarios:
            estado = "✅ Activo" if usuario['Activo'] else "⛔ Inactivo"
            self.tree_usuarios.insert("", "end", values=(
                usuario['UsuarioID'],
                usuario['NombreUsuario'],
                usuario['NombreCompleto'],
                usuario['Rol'],
                estado
            ))

    def activar_usuario_gui(self):
        """Activa un usuario seleccionado."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Seleccione un usuario")
            return
            
        usuario_id = self.tree_usuarios.item(seleccion[0])['values'][0]
        if db.cambiar_estado_usuario(usuario_id, True):
            messagebox.showinfo("Éxito", "Usuario activado")
            self.cargar_lista_usuarios()

    def desactivar_usuario_gui(self):
        """Desactiva un usuario seleccionado."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Seleccione un usuario")
            return
            
        usuario_id = self.tree_usuarios.item(seleccion[0])['values'][0]
        # No permitir desactivarse a sí mismo
        if usuario_id == self.usuario_autenticado['usuario_id']:
            messagebox.showerror("Error", "No puede desactivar su propio usuario")
            return
            
        if db.cambiar_estado_usuario(usuario_id, False):
            messagebox.showinfo("Éxito", "Usuario desactivado")
            self.cargar_lista_usuarios()

    # --- FUNCIONES DE GESTIÓN ---
    def cargar_productos_combobox(self):
        """Carga la lista de nombres de productos en los Comboboxes."""
        print("🔄 Cargando productos en combobox...")
        nombres = db.get_all_product_names()
        
        self.combo_productos_venta['values'] = nombres
        if hasattr(self, 'combo_productos_stock'):
            self.combo_productos_stock['values'] = nombres
        
        if nombres:
            self.combo_productos_venta.set(nombres[0])
            if hasattr(self, 'combo_productos_stock'):
                self.combo_productos_stock.set(nombres[0])
            self.actualizar_precio_display()
            print(f"✅ Combobox actualizado con {len(nombres)} productos")
        else:
            self.combo_productos_venta.set("")
            if hasattr(self, 'combo_productos_stock'):
                self.combo_productos_stock.set("")
            self.label_precio_unitario.config(text="0.00")
            print("⚠️  No hay productos para cargar en combobox")

    def registrar_producto_gui(self):
        """Registra un nuevo producto en la BD."""
        print("🔄 EJECUTANDO registrar_producto_gui()")
        nombre = self.entry_nombre.get().strip()
        precio_str = self.entry_precio.get().strip()
        stock_str = self.entry_stock_inicial.get().strip()

        print(f"📝 Datos del producto: nombre='{nombre}', precio='{precio_str}', stock='{stock_str}'")

        if not nombre or not precio_str:
            messagebox.showerror("Error de Entrada", "Nombre y Precio Unitario son obligatorios.")
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            if precio <= 0 or stock < 0:
                 messagebox.showerror("Error de Valores", "El precio debe ser positivo y el stock no puede ser negativo.")
                 return
        except ValueError:
            messagebox.showerror("Error de Formato", "El Precio Unitario debe ser un número y el Stock Inicial un entero.")
            return

        if db.add_product(nombre, precio, stock):
            messagebox.showinfo("Éxito", f"Producto '{nombre}' registrado correctamente.")
            self.entry_nombre.delete(0, END)
            self.entry_precio.delete(0, END)
            self.entry_stock_inicial.delete(0, END)
            self.entry_stock_inicial.insert(0, "0")
            
            print("🔄 Actualizando interfaz...")
            self.cargar_lista_productos()
            self.cargar_productos_combobox()
            print("✅ Interfaz actualizada después de agregar producto")
        else:
            messagebox.showerror("Error de DB", "No se pudo registrar el producto. ¿Ya existe ese nombre?")

    def actualizar_stock_gui(self):
        """Actualiza el stock de un producto existente."""
        print("🔄 EJECUTANDO actualizar_stock_gui()")
        nombre_producto = self.combo_productos_stock.get()
        cantidad_str = self.entry_cantidad_stock.get().strip()
        
        print(f"📝 Actualizando stock: producto='{nombre_producto}', cantidad='{cantidad_str}'")
        
        if not nombre_producto or not cantidad_str:
            messagebox.showwarning("Campos Requeridos", "Debe seleccionar un producto e ingresar una cantidad.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                messagebox.showerror("Error de Cantidad", "La cantidad a añadir debe ser un número entero positivo.")
                return
        except ValueError:
            messagebox.showerror("Error de Formato", "La cantidad debe ser un número entero.")
            return
            
        producto_id = db.get_product_id_by_name(nombre_producto)
        if not producto_id:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
        
        if db.update_product_stock(producto_id, cantidad):
            messagebox.showinfo("Éxito", f"Stock de '{nombre_producto}' actualizado con {cantidad} unidades.")
            self.entry_cantidad_stock.delete(0, END)
            self.entry_cantidad_stock.insert(0, "1")
            
            print("🔄 Actualizando interfaz...")
            self.cargar_lista_productos()
            print("✅ Interfaz actualizada después de actualizar stock")
        else:
            messagebox.showerror("Error de DB", "No se pudo actualizar el stock.")

    def cargar_producto_seleccionado(self, event):
        """Carga los detalles del producto seleccionado en los campos de edición."""
        seleccion = self.tree_productos.focus()
        if seleccion:
            valores = self.tree_productos.item(seleccion, 'values')
            self.producto_seleccionado_id = valores[0]
            nombre_actual = valores[1]
            precio_actual = valores[2].replace('$', '').replace(',', '')

            self.edit_nombre.delete(0, END)
            self.edit_nombre.insert(0, nombre_actual)
            
            self.edit_precio.delete(0, END)
            self.edit_precio.insert(0, precio_actual)
            
            print(f"📝 Producto seleccionado: ID={self.producto_seleccionado_id}, Nombre='{nombre_actual}'")
        else:
            self.producto_seleccionado_id = None
            self.edit_nombre.delete(0, END)
            self.edit_precio.delete(0, END)

    def guardar_cambios_gui(self):
        """Guarda los cambios de nombre y precio del producto seleccionado."""
        print("🔄 EJECUTANDO guardar_cambios_gui()")
        if not self.producto_seleccionado_id:
            messagebox.showwarning("Selección Requerida", "Primero debe seleccionar un producto de la lista inferior.")
            return

        nombre_nuevo = self.edit_nombre.get().strip()
        precio_str = self.edit_precio.get().strip()

        print(f"📝 Editando producto ID {self.producto_seleccionado_id}: nombre='{nombre_nuevo}', precio='{precio_str}'")

        if not nombre_nuevo or not precio_str:
            messagebox.showerror("Error de Entrada", "Nombre y Precio Unitario son obligatorios.")
            return
            
        try:
            precio_nuevo = float(precio_str)
            if precio_nuevo <= 0:
                messagebox.showerror("Error de Valores", "El precio debe ser positivo.")
                return
        except ValueError:
            messagebox.showerror("Error de Formato", "El Precio Unitario debe ser un número.")
            return

        if db.update_product_details(self.producto_seleccionado_id, nombre_nuevo, precio_nuevo):
            messagebox.showinfo("Éxito", f"Producto ID {self.producto_seleccionado_id} actualizado.")
            print("🔄 Actualizando interfaz...")
            self.cargar_lista_productos()
            self.cargar_productos_combobox()
            print("✅ Interfaz actualizada después de editar producto")
        else:
            messagebox.showerror("Error de DB", "No se pudo actualizar el producto. ¿Nombre duplicado?")

    def eliminar_producto_gui(self):
        """Elimina el producto seleccionado."""
        print("🔄 EJECUTANDO eliminar_producto_gui()")
        if not self.producto_seleccionado_id:
            messagebox.showwarning("Selección Requerida", "Primero debe seleccionar un producto de la lista inferior.")
            return
            
        nombre_producto = self.edit_nombre.get()

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea ELIMINAR el producto '{nombre_producto}'? Esta acción es irreversible y afectará las ventas relacionadas."):
            if db.delete_product(self.producto_seleccionado_id):
                messagebox.showinfo("Éxito", f"Producto '{nombre_producto}' eliminado exitosamente.")
                self.producto_seleccionado_id = None
                self.edit_nombre.delete(0, END)
                self.edit_precio.delete(0, END)
                print("🔄 Actualizando interfaz...")
                self.cargar_lista_productos()
                self.cargar_productos_combobox()
                print("✅ Interfaz actualizada después de eliminar producto")
            else:
                messagebox.showerror("Error de DB", "No se pudo eliminar el producto. Podría haber registros de ventas asociados que lo impiden.")

    def cargar_lista_productos(self):
        """Carga la lista de todos los productos en el Treeview de gestión."""
        # ✅ VERIFICAR QUE EXISTA EL TREEVIEW (solo para administradores)
        if not hasattr(self, 'tree_productos') or self.usuario_autenticado['rol'] != 'administrador':
            return
            
        print("🔄 EJECUTANDO cargar_lista_productos()")
        
        # Limpiar Treeview
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        df = db.get_all_products_df()
        print(f"📊 Datos obtenidos de BD: {len(df)} productos")

        if df.empty:
            print("⚠️  No hay productos para mostrar")
            return

        # Insertar filas desde el DataFrame de Pandas
        for index, row in df.iterrows():
            # Formatear el precio para mostrar en el Treeview
            precio_formatted = f"${float(row['PrecioUnitario']):,.2f}"
            
            self.tree_productos.insert("", "end", 
                values=(
                    row['ProductoID'], 
                    row['NombreProducto'], 
                    precio_formatted, 
                    row['Stock']
                )
            )
    
        print(f"✅ Treeview actualizado con {len(df)} productos")
        print("📋 Productos en Treeview:", len(self.tree_productos.get_children()))

if __name__ == "__main__":
    app = TiendaProManager()
    app.mainloop()