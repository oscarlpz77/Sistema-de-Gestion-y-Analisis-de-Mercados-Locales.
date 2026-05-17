import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend import GestorDatos
import pandas as pd

gd = GestorDatos()

# Clear users and products
pd.DataFrame(columns=["nombre", "contacto", "rol", "password"]).to_csv(gd.archivo_usuarios, index=False)
pd.DataFrame(columns=["id_producto", "nombre", "categoria", "precio", "stock"]).to_csv(gd.archivo_productos, index=False)

# Add users
gd.registrar_usuario('admin', '12345678', 'Administrador', '1234')
gd.registrar_usuario('vende', '87654321', 'Vendedor', '1234')
gd.registrar_usuario('compra', '11111111', 'Comprador', '1234')

# Add products
gd.registrar_producto('Leche Entera', 'Lácteos', 1.50, 50)
gd.registrar_producto('Pan de Molde', 'Panadería', 2.00, 30)
gd.registrar_producto('Manzanas', 'Frutas', 0.50, 100)
gd.registrar_producto('Arroz', 'Abarrotes', 1.20, 5) # Low stock
gd.registrar_producto('Frijoles', 'Abarrotes', 1.80, 0) # Out of stock

print("Datos de prueba generados exitosamente.")
