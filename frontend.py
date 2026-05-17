import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend import GestorDatos

# Configuraciones de colores (manteniendo tu diseño original)
COLOR_FONDO = "#0f0a1f"
COLOR_FRAME = "#1e1b3a"
COLOR_BOTON = "#8b5cf6"
COLOR_HOVER = "#7c3aed"
COLOR_TEXTO = "#ede9fe"
COLOR_SECUNDARIO = "#c4b5fd"

class AplicacionVentas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Ventas y Mercados")
        self.geometry("900x600")
        self.config(bg=COLOR_FONDO)
        
        # Inicializar Backend
        self.backend = GestorDatos()
        self.rol_actual = None  # Almacenará el rol del usuario actual
        self.usuario_actual = None  # Almacenará el nombre del usuario actual
        
        # Contenedor principal que albergará todos los frames
        self.container = ctk.CTkFrame(self, fg_color=COLOR_FONDO)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Diccionario para almacenar las pantallas
        self.frames = {}
        
        # Inicializar pantallas
        for F in (PantallaInicio, PantallaGestionUsuarios, PantallaPanel, PantallaProductos, PantallaRegistrarProducto, PantallaRegistrarVenta, PantallaEstadisticas, PantallaMisCompras):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Poner todos los frames en la misma celda
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Mostrar pantalla de inicio por defecto
        self.mostrar_frame("PantallaInicio")

    def mostrar_frame(self, page_name):
        """Muestra un frame por su nombre y actualiza datos si es necesario"""
        frame = self.frames[page_name]
        
        # Llamar función de actualización si existe (ej. para cargar productos nuevos)
        if hasattr(frame, 'actualizar_datos'):
            frame.actualizar_datos()
            
        frame.tkraise()

# ==========================================
# PANTALLAS
# ==========================================

class PantallaInicio(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        frame_login = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=25, width=400, height=350)
        frame_login.pack_propagate(False)
        frame_login.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        label_titulo = ctk.CTkLabel(frame_login, text="Bienvenido a VentasApp", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        label_titulo.pack(pady=30)
        
        # Entradas
        self.entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Nombre de usuario", width=250, height=40, corner_radius=10)
        self.entry_usuario.pack(pady=10, padx=40)
        
        self.entry_contrasena = ctk.CTkEntry(frame_login, placeholder_text="Contraseña", width=250, height=40, corner_radius=10, show="*")
        self.entry_contrasena.pack(pady=10, padx=40)
        
        # Botones
        boton_ingresar = ctk.CTkButton(frame_login, text="Acceder", width=200, height=40, corner_radius=10,
                                       fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=self.verificar_login)
        boton_ingresar.pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_contrasena.get()
        
        if not usuario or not password:
            messagebox.showwarning("Error", "Por favor completa todos los campos")
            return
            
        exito, rol = self.controller.backend.autenticar_usuario(usuario, password)
        if exito:
            messagebox.showinfo("Éxito", f"Bienvenido {usuario} ({rol})")
            self.entry_usuario.delete(0, 'end')
            self.entry_contrasena.delete(0, 'end')
            self.controller.rol_actual = rol
            self.controller.usuario_actual = usuario
            self.controller.mostrar_frame("PantallaPanel")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


class PantallaGestionUsuarios(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        label_titulo = ctk.CTkLabel(self, text="GESTIÓN DE USUARIOS", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        label_titulo.pack(pady=10)
        
        # Frame tabla
        frame_tabla = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', COLOR_BOTON)])
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Contacto", "Rol", "Password", "Fecha"), show="headings", height=8, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Contacto", text="Contacto")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Password", text="Contraseña")
        self.tree.heading("Fecha", text="Fecha Creación")
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar)
        self.tree.bind("<Button-1>", self.al_hacer_clic_tabla)
        
        # Frame Detalles
        frame_detalles = ctk.CTkFrame(self, fg_color=COLOR_FRAME, height=150)
        frame_detalles.pack(fill="x", padx=20, pady=10)
        
        # Entradas
        self.entry_nombre = ctk.CTkEntry(frame_detalles, placeholder_text="Nombre", width=150)
        self.entry_nombre.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_contacto = ctk.CTkEntry(frame_detalles, placeholder_text="Contacto", width=150)
        self.entry_contacto.grid(row=0, column=1, padx=10, pady=10)
        
        self.combo_tipo = ctk.CTkComboBox(frame_detalles, values=["Vendedor", "Comprador", "Administrador"], width=150)
        self.combo_tipo.grid(row=0, column=2, padx=10, pady=10)
        
        self.entry_password = ctk.CTkEntry(frame_detalles, placeholder_text="Contraseña", width=150)
        self.entry_password.grid(row=0, column=3, padx=10, pady=10)
        
        # Botones de Acción
        self.btn_guardar_nuevo = ctk.CTkButton(frame_detalles, text="Registrar Nuevo", fg_color=COLOR_BOTON, command=self.registrar)
        self.btn_guardar_nuevo.grid(row=1, column=0, padx=10, pady=10)
        
        self.btn_guardar_cambios = ctk.CTkButton(frame_detalles, text="Guardar Cambios", fg_color="#3b82f6", command=self.guardar_edicion)
        self.btn_guardar_cambios.grid(row=1, column=1, padx=10, pady=10)
        
        self.btn_elim_seleccionados = ctk.CTkButton(frame_detalles, text="Eliminar Seleccionados", fg_color="#eab308", text_color="black", command=self.eliminar_seleccionados)
        self.btn_elim_seleccionados.grid(row=1, column=2, padx=10, pady=10)
        
        self.btn_elim_todos = ctk.CTkButton(frame_detalles, text="Eliminar Todos", fg_color="#ef4444", command=self.eliminar_todos)
        self.btn_elim_todos.grid(row=1, column=3, padx=10, pady=10)
        
        # Volver
        btn_volver = ctk.CTkButton(self, text="Volver al Panel", fg_color="transparent", border_width=2, border_color=COLOR_BOTON, 
                                   command=lambda: controller.mostrar_frame("PantallaPanel"))
        btn_volver.pack(pady=5)

    def al_hacer_clic_tabla(self, event):
        item = self.tree.identify_row(event.y)
        if not item: # Clic en espacio vacío
            self.tree.selection_remove(self.tree.selection())
            self.limpiar_campos()

    def al_seleccionar(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])['values']
            self.limpiar_campos()
            self.entry_nombre.insert(0, item[0])
            self.entry_nombre.configure(state="disabled") # No cambiamos el nombre
            self.entry_contacto.insert(0, item[1])
            self.entry_contacto.configure(state="disabled")
            self.combo_tipo.set(item[2])
            self.entry_password.insert(0, str(item[3]))
            
    def limpiar_campos(self):
        self.entry_nombre.configure(state="normal")
        self.entry_nombre.delete(0, 'end')
        self.entry_contacto.configure(state="normal")
        self.entry_contacto.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.combo_tipo.set("Vendedor")
        
    def actualizar_datos(self):
        self.limpiar_campos()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        df = self.controller.backend.cargar_usuarios()
        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=(row['nombre'], row['contacto'], row['rol'], row['password'], row.get('fecha_creacion', '')))
            
    def registrar(self):
        self.entry_nombre.configure(state="normal")
        self.entry_contacto.configure(state="normal")
        nombre = self.entry_nombre.get()
        contacto = self.entry_contacto.get()
        tipo = self.combo_tipo.get()
        password = self.entry_password.get()
        
        if not all([nombre, contacto, tipo, password]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
            
        exito, msj = self.controller.backend.registrar_usuario(nombre, contacto, tipo, password)
        if exito:
            messagebox.showinfo("Exito", msj)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", msj)

    def guardar_edicion(self):
        if self.entry_nombre.cget("state") != "disabled":
            messagebox.showwarning("Aviso", "Selecciona un usuario de la tabla para editarlo.")
            return
            
        nombre = self.entry_nombre.get()
        nuevo_rol = self.combo_tipo.get()
        nueva_pass = self.entry_password.get()
        
        exito, msj = self.controller.backend.actualizar_usuario(nombre, nuevo_rol, nueva_pass)
        if exito:
            messagebox.showinfo("Exito", msj)
            self.actualizar_datos()

    def eliminar_seleccionados(self):
        seleccion = self.tree.selection()
        if not seleccion: return
        nombres = [self.tree.item(item)['values'][0] for item in seleccion]
        
        if self.controller.usuario_actual in nombres:
            messagebox.showwarning("Cuidado", "No puedes eliminar tu propio usuario actual.")
            nombres.remove(self.controller.usuario_actual)
            
        if not nombres: return
            
        if messagebox.askyesno("Confirmar", f"¿Eliminar {len(nombres)} usuarios?"):
            self.controller.backend.eliminar_usuarios(nombres)
            self.actualizar_datos()

    def eliminar_todos(self):
        if messagebox.askyesno("Confirmar", "¿Eliminar a todos los usuarios (excepto a ti mismo)?"):
            exito, msg = self.controller.backend.eliminar_todos_usuarios(excluidos=[self.controller.usuario_actual])
            self.actualizar_datos()
            messagebox.showinfo("Exito", msg)


class PantallaPanel(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        frame_panel = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=25, width=450, height=500)
        frame_panel.pack_propagate(False)
        frame_panel.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        label_titulo = ctk.CTkLabel(frame_panel, text="PANEL PRINCIPAL", font=("Arial", 30, "bold"), text_color=COLOR_TEXTO)
        label_titulo.pack(pady=40)
        
        self.btn_productos = ctk.CTkButton(frame_panel, text="Ver Productos", width=250, height=50, font=("Arial", 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaProductos"))
        
        self.btn_venta = ctk.CTkButton(frame_panel, text="Registrar Venta", width=250, height=50, font=("Arial", 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaRegistrarVenta"))
        
        self.btn_datos = ctk.CTkButton(frame_panel, text="Consultar Estadísticas", width=250, height=50, font=("Arial", 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaEstadisticas"))
        
        self.btn_registrar = ctk.CTkButton(frame_panel, text="Gestionar Usuarios", width=250, height=50, font=("Arial", 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaGestionUsuarios"))
        
        self.btn_mis_compras = ctk.CTkButton(frame_panel, text="Mis Compras", width=250, height=50, font=("Arial", 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaMisCompras"))
        
        self.btn_salir = ctk.CTkButton(frame_panel, text="Cerrar Sesión", width=150, height=40, 
                                    fg_color="red", hover_color="darkred", command=self.cerrar_sesion)

    def cerrar_sesion(self):
        self.controller.rol_actual = None
        self.controller.mostrar_frame("PantallaInicio")

    def actualizar_datos(self):
        rol = self.controller.rol_actual
        
        # Ocultar todos los botones primero
        self.btn_productos.pack_forget()
        self.btn_venta.pack_forget()
        self.btn_datos.pack_forget()
        self.btn_registrar.pack_forget()
        self.btn_mis_compras.pack_forget()
        self.btn_salir.pack_forget()
        
        # Mostrar botones dependiendo del rol
        self.btn_productos.pack(pady=15) # Todos pueden ver productos
        
        if rol == "Administrador":
            self.btn_venta.configure(text="Registrar Venta")
            self.btn_venta.pack(pady=15)
            self.btn_datos.pack(pady=10)
            self.btn_registrar.pack(pady=10)
        elif rol == "Vendedor":
            self.btn_venta.configure(text="Registrar Venta")
            self.btn_venta.pack(pady=15)
        elif rol == "Comprador":
            self.btn_venta.configure(text="Comprar Producto")
            self.btn_venta.pack(pady=15)
            self.btn_mis_compras.pack(pady=10)
            
        self.btn_salir.pack(pady=15)


class PantallaProductos(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        label_titulo = ctk.CTkLabel(self, text="PRODUCTOS", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        label_titulo.pack(pady=20)
        
        # Frame para el Buscador
        frame_buscador = ctk.CTkFrame(self, fg_color="transparent")
        frame_buscador.pack(fill="x", padx=40, pady=(10, 0))
        
        self.entry_buscar = ctk.CTkEntry(frame_buscador, placeholder_text="Buscar producto por nombre...", width=300)
        self.entry_buscar.pack(side="left")
        self.entry_buscar.bind("<KeyRelease>", self.buscar_producto)

        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Usar Treeview de tk para la tabla (CustomTkinter no tiene tabla nativa aún)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', COLOR_BOTON)])
        
        scrollbar_y = ttk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Categoria", "Precio", "Stock"), show="headings", yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Categoria", text="Categoría")
        self.tree.heading("Precio", text="Precio ($)")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.tree.tag_configure('low_stock', background='#9a3412') # Color naranja oscuro para bajo stock
        
        self.tree.bind("<Button-1>", self.al_hacer_clic_tabla)
        
        frame_botones_inferior = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones_inferior.pack(pady=20)
        
        self.btn_nuevo_prod = ctk.CTkButton(frame_botones_inferior, text="Agregar Nuevo Producto", width=200, height=40,
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaRegistrarProducto"))
        
        self.btn_editar = ctk.CTkButton(frame_botones_inferior, text="Editar Seleccionado", width=200, height=40,
                                    fg_color="#3b82f6", hover_color="#2563eb", text_color="white", command=self.editar_producto)

        self.btn_eliminar = ctk.CTkButton(frame_botones_inferior, text="Eliminar Seleccionados", width=200, height=40,
                                    fg_color="#eab308", hover_color="#ca8a04", text_color="black", command=self.eliminar_seleccionados)
                                    
        self.btn_eliminar_todos = ctk.CTkButton(frame_botones_inferior, text="Eliminar Todos", width=200, height=40,
                                    fg_color="#ef4444", hover_color="#dc2626", text_color="white", command=self.eliminar_todos)
        
        self.btn_volver = ctk.CTkButton(frame_botones_inferior, text="Volver al Panel", width=200, height=40,
                                    fg_color="transparent", border_width=2, border_color=COLOR_BOTON, hover_color=COLOR_FRAME, command=lambda: controller.mostrar_frame("PantallaPanel"))

    def eliminar_seleccionados(self):
        seleccionados = self.tree.selection()
        if not seleccionados:
            messagebox.showwarning("Advertencia", "Selecciona al menos un producto para eliminar.")
            return
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar {len(seleccionados)} producto(s)?"):
            ids_a_eliminar = [self.tree.item(item, "values")[0] for item in seleccionados]
            exito, msg = self.controller.backend.eliminar_productos(ids_a_eliminar)
            if exito:
                self.actualizar_datos()
                messagebox.showinfo("Éxito", msg)

    def eliminar_todos(self):
        if messagebox.askyesno("¡Cuidado!", "¿Estás TOTALMENTE seguro de querer eliminar TODOS los productos?"):
            exito, msg = self.controller.backend.eliminar_todos_productos()
            if exito:
                self.actualizar_datos()
                messagebox.showinfo("Éxito", msg)

    def al_hacer_clic_tabla(self, event):
        item = self.tree.identify_row(event.y)
        if not item: # Clic en espacio vacío
            self.tree.selection_remove(self.tree.selection())

    def editar_producto(self):
        seleccionados = self.tree.selection()
        if not seleccionados or len(seleccionados) > 1:
            messagebox.showwarning("Advertencia", "Selecciona exactamente UN producto para editar.")
            return
        
        valores = self.tree.item(seleccionados[0], "values")
        id_p, nom, cat, pre, stk = valores
        
        # Pasarle los datos a PantallaRegistrarProducto
        pantalla_rp = self.controller.frames["PantallaRegistrarProducto"]
        pantalla_rp.cargar_producto_para_edicion(id_p, nom, cat, pre, stk)
        self.controller.mostrar_frame("PantallaRegistrarProducto")

    def buscar_producto(self, event):
        texto_busqueda = self.entry_buscar.get()
        self.cargar_tabla_productos(texto_busqueda)

    def actualizar_datos(self):
        self.entry_buscar.delete(0, 'end')
        
        # Mostrar/Ocultar botones según el rol
        self.btn_nuevo_prod.pack_forget()
        self.btn_editar.pack_forget()
        self.btn_eliminar.pack_forget()
        self.btn_eliminar_todos.pack_forget()
        self.btn_volver.pack_forget()
        
        rol = self.controller.rol_actual
        if rol in ["Administrador", "Vendedor"]:
            self.btn_nuevo_prod.pack(side="left", padx=5)
            self.btn_editar.pack(side="left", padx=5)
            self.btn_eliminar.pack(side="left", padx=5)
            self.btn_eliminar_todos.pack(side="left", padx=5)
            
        self.btn_volver.pack(side="left", padx=5)

        self.cargar_tabla_productos()

    def cargar_tabla_productos(self, filtro_nombre=""):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Llenar tabla
        df = self.controller.backend.cargar_productos()
        if not df.empty:
            if filtro_nombre:
                df = df[df['nombre'].str.contains(filtro_nombre, case=False, na=False)]
            for index, row in df.iterrows():
                id_p = row.get('id_producto', '')
                nom = row.get('nombre', '')
                cat = row.get('categoria', '')
                pre = row.get('precio', 0)
                stk = row.get('stock', 0)
                
                tags = ()
                if stk <= 5:
                    tags = ('low_stock',)
                self.tree.insert("", tk.END, values=(id_p, nom, cat, pre, stk), tags=tags)

class PantallaRegistrarProducto(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        self.id_producto_editando = None
        
        frame_rp = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=25, width=450, height=500)
        frame_rp.pack_propagate(False)
        frame_rp.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        self.label_titulo = ctk.CTkLabel(frame_rp, text="Registrar Producto", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        self.label_titulo.pack(pady=20)
        
        self.entry_nombre = ctk.CTkEntry(frame_rp, placeholder_text="Nombre del Producto", width=300, height=40, corner_radius=10)
        self.entry_nombre.pack(pady=10)
        
        self.entry_categoria = ctk.CTkEntry(frame_rp, placeholder_text="Categoría (Ej. Lácteos)", width=300, height=40, corner_radius=10)
        self.entry_categoria.pack(pady=10)
        
        self.entry_precio = ctk.CTkEntry(frame_rp, placeholder_text="Precio", width=300, height=40, corner_radius=10)
        self.entry_precio.pack(pady=10)
        
        self.entry_stock = ctk.CTkEntry(frame_rp, placeholder_text="Stock Inicial", width=300, height=40, corner_radius=10)
        self.entry_stock.pack(pady=10)
        
        boton_guardar = ctk.CTkButton(frame_rp, text="Guardar Producto", width=250, height=40, corner_radius=10,
                                       fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=self.registrar)
        boton_guardar.pack(pady=20)
        
        boton_volver = ctk.CTkButton(frame_rp, text="Volver a Productos", width=250, height=30, corner_radius=10,
                                       fg_color="transparent", text_color=COLOR_SECUNDARIO, hover_color=COLOR_FRAME, 
                                       command=lambda: [controller.mostrar_frame("PantallaProductos"), self.limpiar_campos()])
        boton_volver.pack(pady=5)

    def cargar_producto_para_edicion(self, id_p, nom, cat, pre, stk):
        self.limpiar_campos()
        self.id_producto_editando = id_p
        self.label_titulo.configure(text=f"Editar Producto {id_p}")
        self.entry_nombre.insert(0, nom)
        self.entry_categoria.insert(0, cat)
        self.entry_precio.insert(0, pre)
        self.entry_stock.insert(0, stk)

    def registrar(self):
        nombre = self.entry_nombre.get()
        categoria = self.entry_categoria.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        
        if not all([nombre, categoria, precio, stock]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
            
        if self.id_producto_editando:
            exito, msj = self.controller.backend.actualizar_producto(self.id_producto_editando, nombre, categoria, precio, stock)
        else:
            exito, msj = self.controller.backend.registrar_producto(nombre, categoria, precio, stock)
            
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.limpiar_campos()
            # Refrescar la tabla de productos
            self.controller.frames["PantallaProductos"].actualizar_datos()
            self.controller.mostrar_frame("PantallaProductos")
        else:
            messagebox.showerror("Error", msj)
            
    def limpiar_campos(self):
        self.id_producto_editando = None
        self.label_titulo.configure(text="Registrar Producto")
        self.entry_nombre.delete(0, 'end')
        self.entry_categoria.delete(0, 'end')
        self.entry_precio.delete(0, 'end')
        self.entry_stock.delete(0, 'end')

class PantallaRegistrarVenta(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        frame_v = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=25, width=450, height=500)
        frame_v.pack_propagate(False)
        frame_v.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        self.label_titulo = ctk.CTkLabel(frame_v, text="REGISTRAR VENTA", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        self.label_titulo.pack(pady=30)
        
        self.label_prod = ctk.CTkLabel(frame_v, text="Seleccionar Producto:", text_color=COLOR_SECUNDARIO)
        self.label_prod.pack(pady=(10,0))
        self.combo_productos = ctk.CTkComboBox(frame_v, width=300, height=40)
        self.combo_productos.pack(pady=(0, 20))
        
        self.label_cant = ctk.CTkLabel(frame_v, text="Cantidad:", text_color=COLOR_SECUNDARIO)
        self.label_cant.pack(pady=(10,0))
        self.entry_cantidad = ctk.CTkEntry(frame_v, placeholder_text="Ej: 2", width=300, height=40)
        self.entry_cantidad.pack(pady=(0, 20))
        
        self.boton_guardar = ctk.CTkButton(frame_v, text="Guardar Venta", width=200, height=40, corner_radius=10,
                                       fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=self.guardar_venta)
        self.boton_guardar.pack(pady=20)
        
        btn_volver = ctk.CTkButton(frame_v, text="Volver al Panel", width=150, height=30,
                                    fg_color="transparent", hover_color=COLOR_FONDO, command=lambda: controller.mostrar_frame("PantallaPanel"))
        btn_volver.pack(pady=10)

    def actualizar_datos(self):
        # Adaptar interfaz según rol
        if self.controller.rol_actual == "Comprador":
            self.label_titulo.configure(text="COMPRAR PRODUCTO")
            self.boton_guardar.configure(text="Confirmar Compra")
        else:
            self.label_titulo.configure(text="REGISTRAR VENTA")
            self.boton_guardar.configure(text="Guardar Venta")
            
        # Actualizar lista de productos en el combobox
        lista_prod = self.controller.backend.obtener_lista_productos()
        if lista_prod:
            self.combo_productos.configure(values=lista_prod)
            self.combo_productos.set(lista_prod[0])
        else:
            self.combo_productos.configure(values=["No hay productos"])
            self.combo_productos.set("No hay productos")

    def guardar_venta(self):
        producto = self.combo_productos.get()
        cantidad = self.entry_cantidad.get()
        
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showwarning("Error", "Ingrese una cantidad válida mayor a 0")
            return
            
        usuario = self.controller.usuario_actual
        exito, msj = self.controller.backend.registrar_venta(producto, cantidad, usuario)
        if exito:
            titulo_msg = "Compra Exitosa" if self.controller.rol_actual == "Comprador" else "Venta Registrada"
            messagebox.showinfo(titulo_msg, msj)
            self.entry_cantidad.delete(0, 'end')
        else:
            messagebox.showerror("Error", msj)


class PantallaEstadisticas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        label_titulo = ctk.CTkLabel(self, text="NUESTRAS ESTADÍSTICAS", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        label_titulo.pack(pady=10)
        
        # Frame para las gráficas
        self.frame_graficas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_graficas.pack(fill="both", expand=True, padx=20, pady=10)
        
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=10)
        
        btn_exportar = ctk.CTkButton(frame_botones, text="Exportar Reporte", width=200, height=40,
                                     fg_color="#10b981", hover_color="#059669", command=self.exportar_reporte)
        btn_exportar.pack(side="left", padx=10)
        
        btn_volver = ctk.CTkButton(frame_botones, text="Volver al Panel", width=150, height=40,
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=lambda: controller.mostrar_frame("PantallaPanel"))
        btn_volver.pack(side="left", padx=10)

    def exportar_reporte(self):
        import os
        from datetime import datetime
        descargas_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(descargas_path):
            os.makedirs(descargas_path)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(descargas_path, f"reporte_estadisticas_{timestamp}.xlsx")
        
        exito, msj = self.controller.backend.exportar_reporte(filepath)
        if exito:
            messagebox.showinfo("Éxito", f"Reporte descargado automáticamente en:\n{filepath}")
        else:
            messagebox.showerror("Error", msj)

    def actualizar_datos(self):
        # Limpiar gráficas anteriores
        for widget in self.frame_graficas.winfo_children():
            widget.destroy()
            
        df_prod, df_dia = self.controller.backend.obtener_datos_estadisticas()
        
        if df_prod is None or df_prod.empty:
            lbl_error = ctk.CTkLabel(self.frame_graficas, text="No hay suficientes datos para mostrar estadísticas.", text_color=COLOR_TEXTO)
            lbl_error.pack(pady=50)
            return

        # Configurar Matplotlib para fondo oscuro
        plt.style.use('dark_background')
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor(COLOR_FRAME)
        
        # Gráfica 1: Ventas por Producto (Barras)
        ax1 = fig.add_subplot(121)
        ax1.set_facecolor(COLOR_FRAME)
        ax1.bar(df_prod['producto'], df_prod['cantidad'], color=COLOR_SECUNDARIO)
        ax1.set_title("Cantidades Vendidas por Producto")
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfica 2: Ventas por Día (Línea o Pastel, haremos Pastel de Ingresos por Producto)
        df_prod_ingresos = self.controller.backend.cargar_ventas().groupby('producto')['total'].sum().reset_index()
        ax2 = fig.add_subplot(122)
        ax2.set_facecolor(COLOR_FRAME)
        ax2.pie(df_prod_ingresos['total'], labels=df_prod_ingresos['producto'], autopct='%1.1f%%', colors=[COLOR_BOTON, COLOR_SECUNDARIO, '#6d28d9', '#a78bfa'])
        ax2.set_title("Ingresos Totales por Producto")
        
        fig.tight_layout()
        
        # Integrar gráfica a Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

class PantallaMisCompras(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.controller = controller
        
        label_titulo = ctk.CTkLabel(self, text="MIS COMPRAS", font=("Arial", 25, "bold"), text_color=COLOR_TEXTO)
        label_titulo.pack(pady=20)
        
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=10)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', COLOR_BOTON)])
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Producto", "Cantidad", "Total", "Fecha"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="ID Venta")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Total", text="Total Pagado ($)")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind("<Button-1>", self.al_hacer_clic_tabla)
        
        btn_volver = ctk.CTkButton(self, text="Volver al Panel", width=200, height=40,
                                    fg_color="transparent", border_width=2, border_color=COLOR_BOTON, hover_color=COLOR_FRAME, 
                                    command=lambda: controller.mostrar_frame("PantallaPanel"))
        btn_volver.pack(pady=20)

    def al_hacer_clic_tabla(self, event):
        item = self.tree.identify_row(event.y)
        if not item: # Clic en espacio vacío
            self.tree.selection_remove(self.tree.selection())

    def actualizar_datos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        usuario = self.controller.usuario_actual
        if not usuario:
            return
            
        df = self.controller.backend.obtener_compras_usuario(usuario)
        if not df.empty:
            for index, row in df.iterrows():
                id_v = row.get('id_venta', '')
                prod = row.get('producto', '')
                cant = row.get('cantidad', 0)
                tot = row.get('total', 0)
                fec = row.get('fecha', '')
                self.tree.insert("", tk.END, values=(id_v, prod, cant, tot, fec))

if __name__ == "__main__":
    app = AplicacionVentas()
    app.mainloop()