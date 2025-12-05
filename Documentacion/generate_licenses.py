from licensing import LicenseManager

def generar_licencias_ejemplo():
    manager = LicenseManager()
    
    # Generar licencias de ejemplo
    licencias = [
        ("cliente1@empresa.com", 365),
        ("cliente2@tienda.com", 365),
        ("demo@tiendapro.com", 30)  # Licencia demo
    ]
    
    for email, dias in licencias:
        licencia = manager.generate_license_key(email, dias)
        print(f"Email: {email}")
        print(f"Licencia: {licencia}")
        print(f"Días: {dias}")
        print("-" * 50)

if __name__ == "__main__":
    generar_licencias_ejemplo()