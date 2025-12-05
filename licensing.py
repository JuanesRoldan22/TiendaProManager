"""
TiendaPro Manager - Sistema de Gestión de Licencias
"""

import hashlib
import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox

class LicenseManager:
    def __init__(self):
        self.license_file = "license.json"
        self.trial_days = 15  # Período de prueba gratuito
        self.app_name = "TiendaPro Manager"
        
    def generate_license_key(self, email, days=365):
        """Genera una clave de licencia (para tu uso interno)"""
        seed = f"{email}|{days}|{self.app_name}|{datetime.datetime.now().strftime('%Y%m%d')}"
        license_hash = hashlib.sha256(seed.encode()).hexdigest()
        return f"TPM-{license_hash[:8]}-{license_hash[8:16]}-{license_hash[16:24]}-{license_hash[24:32]}".upper()
    
    def verify_license(self):
        """Verifica si hay una licencia válida"""
        # Verificar licencia activa
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    license_data = json.load(f)
                
                # Verificar expiración
                expiry_date = datetime.datetime.fromisoformat(license_data['expiry_date'])
                if datetime.datetime.now() < expiry_date:
                    return {
                        'status': 'licensed',
                        'email': license_data['email'],
                        'expiry_date': expiry_date,
                        'days_remaining': (expiry_date - datetime.datetime.now()).days
                    }
            except:
                pass
        
        # Verificar período de prueba
        return self.check_trial_period()
    
    def check_trial_period(self):
        """Verifica el período de prueba"""
        install_file = "install_date.txt"
        
        if not os.path.exists(install_file):
            # Primera ejecución - registrar fecha de instalación
            with open(install_file, 'w') as f:
                f.write(datetime.datetime.now().isoformat())
            return {'status': 'trial', 'days_remaining': self.trial_days}
        
        # Calcular días restantes de prueba
        with open(install_file, 'r') as f:
            install_date = datetime.datetime.fromisoformat(f.read().strip())
        
        days_used = (datetime.datetime.now() - install_date).days
        days_remaining = self.trial_days - days_used
        
        if days_remaining > 0:
            return {'status': 'trial', 'days_remaining': days_remaining}
        else:
            return {'status': 'expired'}
    
    def activate_license(self, license_key, email):
        """Activa una licencia"""
        # Validación básica (en producción, esto se conectaría a un servidor)
        if not license_key.startswith('TPM-') or len(license_key) != 23:
            return False, "Formato de licencia inválido"
        
        # Simulación de validación - EN PRODUCCIÓN CONECTAR A TU SERVIDOR
        try:
            # Aquí iría la validación real con tu servidor
            # Por ahora, simulamos una activación exitosa para licencias de prueba
            if "DEMO" in license_key:
                expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
            else:
                expiry_date = datetime.datetime.now() + datetime.timedelta(days=365)
            
            license_data = {
                'license_key': license_key,
                'email': email,
                'activation_date': datetime.datetime.now().isoformat(),
                'expiry_date': expiry_date.isoformat(),
                'app_version': '1.0'
            }
            
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=2)
            
            return True, "Licencia activada exitosamente"
            
        except Exception as e:
            return False, f"Error al activar licencia: {str(e)}"
    
    def get_license_status_message(self):
        """Retorna mensaje del estado de la licencia"""
        status = self.verify_license()
        
        if status['status'] == 'licensed':
            return f"✅ Licencia activa - Vence en {status['days_remaining']} días"
        elif status['status'] == 'trial':
            return f"🆓 Versión de prueba - {status['days_remaining']} días restantes"
        else:
            return "❌ Período de prueba expirado"
    
    def show_activation_window(self, parent):
        """Muestra ventana de activación de licencia"""
        activation_window = tk.Toplevel(parent)
        activation_window.title("🔐 Activar Licencia - TiendaPro Manager")
        activation_window.geometry("500x400")
        activation_window.resizable(False, False)
        activation_window.transient(parent)
        activation_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(activation_window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tk.Label(main_frame, text="🔐 ACTIVAR LICENCIA", 
                font=('Arial', 16, 'bold'), fg='#2E86AB').pack(pady=10)
        
        tk.Label(main_frame, text="TiendaPro Manager v1.0", 
                font=('Arial', 10), fg='#666').pack(pady=(0, 20))
        
        # Frame de formulario
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill='x', pady=10)
        
        # Email
        tk.Label(form_frame, text="Email:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=8)
        email_entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
        email_entry.grid(row=0, column=1, sticky='ew', pady=8, padx=(10, 0))
        
        # Clave de licencia
        tk.Label(form_frame, text="Clave de Licencia:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=8)
        license_entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
        license_entry.grid(row=1, column=1, sticky='ew', pady=8, padx=(10, 0))
        
        # Configurar expansión de columnas
        form_frame.columnconfigure(1, weight=1)
        
        # Estado actual
        status_frame = tk.Frame(main_frame, relief='groove', bd=1, padx=10, pady=10)
        status_frame.pack(fill='x', pady=20)
        
        status_text = self.get_license_status_message()
        status_label = tk.Label(status_frame, text=status_text, font=('Arial', 10, 'bold'))
        status_label.pack()
        
        # Botones
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        
        def activate_license():
            email = email_entry.get().strip()
            license_key = license_entry.get().strip()
            
            if not email or not license_key:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
            
            success, message = self.activate_license(license_key, email)
            
            if success:
                messagebox.showinfo("Éxito", message)
                status_label.config(text=self.get_license_status_message())
                activation_window.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Botón de activar
        activate_btn = tk.Button(button_frame, text="✅ Activar Licencia", 
                               command=activate_license, bg='#27AE60', fg='white',
                               font=('Arial', 10, 'bold'), padx=20)
        activate_btn.pack(pady=5)
        
        # Licencia de prueba
        def add_demo_license():
            email_entry.delete(0, tk.END)
            email_entry.insert(0, "demo@tiendapro.com")
            license_entry.delete(0, tk.END)
            license_entry.insert(0, "TPM-DEMO-1234-5678-90AB")
        
        demo_btn = tk.Button(button_frame, text="🆓 Licencia Demo (30 días)", 
                           command=add_demo_license, bg='#3498DB', fg='white',
                           font=('Arial', 9), padx=10)
        demo_btn.pack(pady=5)
        
        # Información de contacto
        contact_frame = tk.Frame(main_frame, relief='groove', bd=1, padx=10, pady=10)
        contact_frame.pack(fill='x', pady=10)
        
        tk.Label(contact_frame, text="📧 ¿Necesita una licencia?", 
                font=('Arial', 9, 'bold')).pack()
        tk.Label(contact_frame, text="Contacte: ventas@tiendapromanager.com", 
                font=('Arial', 9), fg='#2E86AB').pack()

# Instancia global del gestor de licencias
license_manager = LicenseManager()