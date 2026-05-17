import pandas as pd
import os
import hashlib
from datetime import datetime

class GestorDatos:
    def __init__(self):
        # Directorio actual
        self.directorio = os.path.dirname(os.path.abspath(__file__))
        self.archivo_usuarios = os.path.join(self.directorio, "usuarios.csv")
        self.archivo_productos = os.path.join(self.directorio, "productos.csv")
        self.archivo_ventas = os.path.join(self.directorio, "ventas.csv")

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ==========================
    # GESTIÓN DE USUARIOS
    # ==========================
    def cargar_usuarios(self):
        if os.path.exists(self.archivo_usuarios):
            return pd.read_csv(self.archivo_usuarios)
        else:
            return pd.DataFrame(columns=["nombre", "contacto", "rol", "password"])

    def guardar_usuarios(self, df):
        df.to_csv(self.archivo_usuarios, index=False)

    def registrar_usuario(self, nombre, contacto, rol, password):
        df = self.cargar_usuarios()
        # Verificar si el usuario ya existe
        if nombre in df['nombre'].values:
            return False, "El usuario ya existe"
        
        password_hash = self._hash_password(password)
        
        nuevo_registro = pd.DataFrame([{
            "nombre": nombre, 
            "contacto": contacto, 
            "rol": rol, 
            "password": password_hash
        }])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        self.guardar_usuarios(df)
        return True, "Registro exitoso"

    def autenticar_usuario(self, nombre, password):
        df = self.cargar_usuarios()
        password_hash = self._hash_password(password)
        if not df.empty and 'nombre' in df.columns and 'password' in df.columns:
            usuario = df[(df['nombre'] == nombre) & (df['password'] == password_hash)]
            if not usuario.empty:
                return True, usuario.iloc[0]['rol']
        return False, None

    def actualizar_usuario(self, nombre, nuevo_rol, nueva_pass=None):
        df = self.cargar_usuarios()
        if nombre not in df['nombre'].values:
            return False, "Usuario no encontrado"
        
        idx = df.index[df['nombre'] == nombre].tolist()[0]
        df.at[idx, 'rol'] = nuevo_rol
        if nueva_pass and nueva_pass != '***':
            df.at[idx, 'password'] = self._hash_password(nueva_pass)
        self.guardar_usuarios(df)
        return True, "Usuario actualizado correctamente"

    def eliminar_usuarios(self, nombres):
        df = self.cargar_usuarios()
        df = df[~df['nombre'].isin(nombres)]
        self.guardar_usuarios(df)
        return True, "Usuarios eliminados correctamente"

    def eliminar_todos_usuarios(self, excluidos=[]):
        df = self.cargar_usuarios()
        if excluidos is None:
            excluidos = []
        df = df[df['nombre'].isin(excluidos)]
        self.guardar_usuarios(df)
        return True, "Todos los usuarios han sido eliminados"

    # ==========================
    # GESTIÓN DE PRODUCTOS
    # ==========================
    def cargar_productos(self):
        if os.path.exists(self.archivo_productos):
            return pd.read_csv(self.archivo_productos)
        else:
            return pd.DataFrame(columns=["id_producto", "nombre", "categoria", "precio", "stock"])

    def guardar_productos(self, df):
        df.to_csv(self.archivo_productos, index=False)

    def registrar_producto(self, nombre, categoria, precio, stock):
        df = self.cargar_productos()
        if nombre in df['nombre'].values:
            return False, "El producto ya existe"
        
        # Generar ID de producto
        if df.empty:
            nuevo_id = "P_1"
        else:
            if 'id_producto' in df.columns:
                try:
                    ultimo_id = df.iloc[-1]['id_producto']
                    n = int(ultimo_id.split("_")[1])
                    nuevo_id = f"P_{n + 1}"
                except:
                    nuevo_id = f"P_{len(df) + 1}"
            else:
                nuevo_id = f"P_{len(df) + 1}"
                
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return False, "Precio o stock inválidos"
            
        nuevo_registro = pd.DataFrame([{
            "id_producto": nuevo_id,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "stock": stock
        }])
        
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        self.guardar_productos(df)
        return True, "Producto registrado con éxito"

    def obtener_lista_productos(self):
        df = self.cargar_productos()
        if not df.empty:
            return df['nombre'].tolist()
        return []

    def actualizar_producto(self, id_producto, nombre, categoria, precio, stock):
        df = self.cargar_productos()
        if id_producto not in df['id_producto'].values:
            return False, "Producto no encontrado"
        
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return False, "Precio o stock inválidos"

        # Comprobar que el nuevo nombre no exista ya (salvo que sea el mismo id)
        if nombre in df[df['id_producto'] != id_producto]['nombre'].values:
            return False, "El nombre del producto ya está en uso"

        idx = df.index[df['id_producto'] == id_producto].tolist()[0]
        df.at[idx, 'nombre'] = nombre
        df.at[idx, 'categoria'] = categoria
        df.at[idx, 'precio'] = precio
        df.at[idx, 'stock'] = stock
        
        self.guardar_productos(df)
        return True, "Producto actualizado con éxito"

    def eliminar_productos(self, ids_a_eliminar):
        df = self.cargar_productos()
        df = df[~df['id_producto'].isin(ids_a_eliminar)]
        self.guardar_productos(df)
        return True, "Productos eliminados correctamente"

    def eliminar_todos_productos(self):
        df = self.cargar_productos()
        df = pd.DataFrame(columns=df.columns)
        self.guardar_productos(df)
        return True, "Todos los productos han sido eliminados"

    # ==========================
    # GESTIÓN DE VENTAS
    # ==========================
    def cargar_ventas(self):
        if os.path.exists(self.archivo_ventas):
            df = pd.read_csv(self.archivo_ventas)
            if "usuario" not in df.columns:
                df["usuario"] = "Desconocido"
            return df
        else:
            return pd.DataFrame(columns=["id_venta", "producto", "cantidad", "total", "fecha", "usuario"])

    def guardar_ventas(self, df):
        df.to_csv(self.archivo_ventas, index=False)

    def registrar_venta(self, nombre_producto, cantidad, usuario="Desconocido"):
        df_prod = self.cargar_productos()
        df_ventas = self.cargar_ventas()

        if df_prod.empty:
            return False, "No hay productos registrados"

        # Buscar el producto
        producto_filtro = df_prod['nombre'] == nombre_producto
        if not producto_filtro.any():
            return False, "Producto no encontrado"
        
        idx = df_prod.index[producto_filtro].tolist()[0]
        stock_actual = float(df_prod.at[idx, 'stock'])
        precio = float(df_prod.at[idx, 'precio'])
        cantidad = float(cantidad)

        if stock_actual < cantidad:
            return False, "Stock insuficiente"

        # Actualizar stock
        nuevo_stock = stock_actual - cantidad
        if nuevo_stock <= 0:
            df_prod = df_prod.drop(idx)  # Eliminar producto si se acaba el stock
        else:
            df_prod.at[idx, 'stock'] = nuevo_stock
            
        self.guardar_productos(df_prod)

        # Registrar venta
        total = precio * cantidad
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generar ID de venta
        if df_ventas.empty:
            nuevo_id = "V_1"
        else:
            if 'id_venta' in df_ventas.columns:
                # Extraer número del último ID, asumiendo formato V_X
                try:
                    ultimo_id = df_ventas.iloc[-1]['id_venta']
                    n = int(ultimo_id.split("_")[1])
                    nuevo_id = f"V_{n + 1}"
                except:
                    nuevo_id = f"V_{len(df_ventas) + 1}"
            else:
                nuevo_id = f"V_{len(df_ventas) + 1}"

        nueva_venta = pd.DataFrame([{
            "id_venta": nuevo_id,
            "producto": nombre_producto,
            "cantidad": cantidad,
            "total": total,
            "fecha": fecha_actual,
            "usuario": usuario
        }])
        
        df_ventas = pd.concat([df_ventas, nueva_venta], ignore_index=True)
        self.guardar_ventas(df_ventas)
        
        return True, "Operación registrada con éxito"

    def obtener_compras_usuario(self, usuario):
        df_ventas = self.cargar_ventas()
        if df_ventas.empty or 'usuario' not in df_ventas.columns:
            return pd.DataFrame()
        return df_ventas[df_ventas['usuario'] == usuario]

    # ==========================
    # ESTADÍSTICAS
    # ==========================
    def obtener_datos_estadisticas(self):
        df_ventas = self.cargar_ventas()
        if df_ventas.empty or 'producto' not in df_ventas.columns:
            return None, None
            
        # Agrupar por producto y sumar cantidad
        ventas_por_producto = df_ventas.groupby('producto')['cantidad'].sum().reset_index()
        
        # Agrupar por fecha (solo día) y sumar total
        df_ventas['dia'] = pd.to_datetime(df_ventas['fecha']).dt.date
        ventas_por_dia = df_ventas.groupby('dia')['total'].sum().reset_index()
        
        return ventas_por_producto, ventas_por_dia

    def exportar_reporte(self, filepath):
        df_ventas = self.cargar_ventas()
        df_productos = self.cargar_productos()
        df_usuarios = self.cargar_usuarios()
        
        # Eliminar las contraseñas antes de exportar por seguridad
        if not df_usuarios.empty and 'password' in df_usuarios.columns:
            df_usuarios = df_usuarios.drop(columns=['password'])
        
        if df_ventas.empty and df_productos.empty and df_usuarios.empty:
            return False, "No hay datos para exportar"
            
        try:
            if filepath.endswith('.xlsx'):
                import pandas as pd
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    if not df_ventas.empty:
                        df_ventas.to_excel(writer, sheet_name='Ventas', index=False)
                    if not df_productos.empty:
                        df_productos.to_excel(writer, sheet_name='Productos', index=False)
                    if not df_usuarios.empty:
                        df_usuarios.to_excel(writer, sheet_name='Usuarios', index=False)
                        
                    # Estadísticas visuales (gráfico de ventas)
                    if not df_ventas.empty and 'producto' in df_ventas.columns:
                        # 1. Ventas por producto (BarChart)
                        ventas_por_producto = df_ventas.groupby('producto')['cantidad'].sum().reset_index()
                        ventas_por_producto.to_excel(writer, sheet_name='Estadisticas', index=False)
                        
                        # 2. Ventas por Día (LineChart)
                        df_ventas['dia'] = pd.to_datetime(df_ventas['fecha']).dt.date
                        ventas_por_dia = df_ventas.groupby('dia')['total'].sum().reset_index()
                        # Escribir a partir de la columna E (índice 4)
                        ventas_por_dia.to_excel(writer, sheet_name='Estadisticas', index=False, startcol=4)
                        
                        # Generar gráficos usando openpyxl
                        workbook  = writer.book
                        worksheet = writer.sheets['Estadisticas']
                        
                        from openpyxl.chart import BarChart, LineChart, Reference
                        
                        # --- Gráfico de Barras ---
                        chart_bar = BarChart()
                        chart_bar.type = "col"
                        chart_bar.style = 10
                        chart_bar.title = "Cantidades Vendidas por Producto"
                        chart_bar.y_axis.title = "Cantidad"
                        chart_bar.x_axis.title = "Producto"
                        
                        # Los datos están en las columnas A (1) y B (2)
                        max_row_prod = len(ventas_por_producto) + 1
                        data_bar = Reference(worksheet, min_col=2, min_row=1, max_row=max_row_prod, max_col=2)
                        cats_bar = Reference(worksheet, min_col=1, min_row=2, max_row=max_row_prod)
                        chart_bar.add_data(data_bar, titles_from_data=True)
                        chart_bar.set_categories(cats_bar)
                        chart_bar.width = 15
                        chart_bar.height = 10
                        worksheet.add_chart(chart_bar, "A15")
                        
                        # --- Gráfico de Líneas ---
                        chart_line = LineChart()
                        chart_line.title = "Ingresos por Día"
                        chart_line.style = 13
                        chart_line.y_axis.title = "Ingresos ($)"
                        chart_line.x_axis.title = "Día"
                        
                        # Los datos están en las columnas E (5) y F (6)
                        max_row_dia = len(ventas_por_dia) + 1
                        data_line = Reference(worksheet, min_col=6, min_row=1, max_row=max_row_dia, max_col=6)
                        cats_line = Reference(worksheet, min_col=5, min_row=2, max_row=max_row_dia)
                        chart_line.add_data(data_line, titles_from_data=True)
                        chart_line.set_categories(cats_line)
                        chart_line.width = 15
                        chart_line.height = 10
                        worksheet.add_chart(chart_line, "J15")
                        
            else:
                if not df_ventas.empty:
                    df_ventas.to_csv(filepath, index=False)
                else:
                    df_productos.to_csv(filepath, index=False)
            return True, "Reporte exportado correctamente"
        except Exception as e:
            return False, f"Error al exportar: {e}"
