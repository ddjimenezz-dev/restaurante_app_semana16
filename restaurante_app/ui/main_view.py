# Vista principal: navegacion lateral y secciones Productos, Ventas y Usuarios
import tkinter as tk
from tkinter import ttk, messagebox

from modelos.producto import CATEGORIAS
from modelos.usuario import ROLES_GESTIONABLES, DESCRIPCION_ROLES
from ui import recursos


def crear_tabla(padre, columnas, alto=10):
    # columnas: lista de tuplas (identificador, titulo, ancho)
    contenedor = tk.Frame(padre, bg=recursos.COLOR_FONDO)
    ids = [c[0] for c in columnas]
    tabla = ttk.Treeview(contenedor, columns=ids, show="headings", selectmode="browse", height=alto)
    for identificador, titulo, ancho in columnas:
        tabla.heading(identificador, text=titulo)
        tabla.column(identificador, width=ancho, anchor="w")
    barra = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return contenedor, tabla


def crear_titulo(padre, texto):
    return tk.Label(padre, text=texto, font=recursos.FUENTE_TITULO, bg=recursos.COLOR_FONDO, fg=recursos.COLOR_TEXTO)


# =====================================================================
# Seccion de usuarios (Semana 16): manejo de eventos
# =====================================================================
class UsuariosView(tk.Frame):
    def __init__(self, padre, servicio):
        super().__init__(padre, bg=recursos.COLOR_FONDO)
        self.servicio = servicio
        self.id_seleccionado = None
        self.imagenes = {
            "registrar": recursos.cargar_imagen("icono_registrar.png"),
            "actualizar": recursos.cargar_imagen("icono_actualizar.png"),
            "eliminar": recursos.cargar_imagen("icono_eliminar.png"),
            "limpiar": recursos.cargar_imagen("icono_limpiar.png"),
        }
        self.crear_formulario()
        self.crear_tabla_usuarios()
        self.configurar_eventos()
        self.refrescar_tabla()
        self.limpiar_formulario()

    # ---------- Construccion de la interfaz ----------
    def crear_formulario(self):
        crear_titulo(self, "Gestión de usuarios").pack(anchor="w", pady=(0, 10))

        formulario = tk.Frame(self, bg="white", padx=16, pady=14, highlightbackground="#dddddd", highlightthickness=1)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        self.var_nombre = tk.StringVar()
        self.var_usuario = tk.StringVar()
        self.var_contrasena = tk.StringVar()
        self.var_rol = tk.StringVar()

        tk.Label(formulario, text="Nombre", bg="white", font=recursos.FUENTE).grid(row=0, column=0, sticky="w", pady=4)
        self.entrada_nombre = ttk.Entry(formulario, textvariable=self.var_nombre)
        self.entrada_nombre.grid(row=0, column=1, sticky="ew", padx=(8, 20), pady=4)

        tk.Label(formulario, text="Usuario", bg="white", font=recursos.FUENTE).grid(row=0, column=2, sticky="w", pady=4)
        self.entrada_usuario = ttk.Entry(formulario, textvariable=self.var_usuario)
        self.entrada_usuario.grid(row=0, column=3, sticky="ew", padx=8, pady=4)

        tk.Label(formulario, text="Contraseña", bg="white", font=recursos.FUENTE).grid(row=1, column=0, sticky="w", pady=4)
        self.entrada_contrasena = ttk.Entry(formulario, textvariable=self.var_contrasena, show="*")
        self.entrada_contrasena.grid(row=1, column=1, sticky="ew", padx=(8, 20), pady=4)

        tk.Label(formulario, text="Rol", bg="white", font=recursos.FUENTE).grid(row=1, column=2, sticky="w", pady=4)
        self.combo_rol = ttk.Combobox(formulario, textvariable=self.var_rol, values=ROLES_GESTIONABLES, state="readonly")
        self.combo_rol.grid(row=1, column=3, sticky="ew", padx=8, pady=4)

        self.etiqueta_rol = tk.Label(formulario, text="", bg="white", fg=recursos.COLOR_GRIS, font=("Segoe UI", 9, "italic"))
        self.etiqueta_rol.grid(row=2, column=2, columnspan=2, sticky="w", padx=8)
        self.etiqueta_modo = tk.Label(formulario, text="", bg="white", fg=recursos.COLOR_AZUL, font=("Segoe UI", 9, "bold"))
        self.etiqueta_modo.grid(row=2, column=0, columnspan=2, sticky="w")

        # Botones principales asociados con command=
        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=3, column=0, columnspan=4, sticky="w", pady=(12, 0))
        self.boton_registrar = recursos.crear_boton(botones, "Registrar", self.registrar_usuario, recursos.COLOR_VERDE, self.imagenes["registrar"])
        self.boton_actualizar = recursos.crear_boton(botones, "Actualizar", self.actualizar_usuario, recursos.COLOR_AZUL, self.imagenes["actualizar"])
        self.boton_eliminar = recursos.crear_boton(botones, "Eliminar", self.eliminar_usuario, recursos.COLOR_PRIMARIO, self.imagenes["eliminar"])
        self.boton_limpiar = recursos.crear_boton(botones, "Limpiar", self.limpiar_formulario, recursos.COLOR_NEUTRO, self.imagenes["limpiar"])
        for boton in (self.boton_registrar, self.boton_actualizar, self.boton_eliminar, self.boton_limpiar):
            boton.pack(side="left", padx=(0, 8))

        tk.Label(formulario, text="Enter registra  |  Esc limpia el formulario", bg="white", fg=recursos.COLOR_GRIS, font=("Segoe UI", 9)).grid(row=4, column=0, columnspan=4, sticky="w", pady=(8, 0))

    def crear_tabla_usuarios(self):
        columnas = [("id", "ID", 60), ("nombre", "Nombre", 300), ("usuario", "Usuario", 200), ("rol", "Rol", 160)]
        contenedor, self.tabla = crear_tabla(self, columnas, 8)
        contenedor.pack(fill="both", expand=True, pady=(14, 0))

    # ---------- Eventos con bind() ----------
    def configurar_eventos(self):
        # Seleccion de una fila del Treeview
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)
        # Cambio de opcion en el Combobox de rol
        self.combo_rol.bind("<<ComboboxSelected>>", self.al_cambiar_rol)
        # Enter confirma el registro desde los campos del formulario
        for campo in (self.entrada_nombre, self.entrada_usuario, self.entrada_contrasena, self.combo_rol):
            campo.bind("<Return>", self.al_presionar_enter)
        # Escape limpia el formulario desde cualquier campo o desde la tabla
        for campo in (self.entrada_nombre, self.entrada_usuario, self.entrada_contrasena, self.combo_rol, self.tabla):
            campo.bind("<Escape>", self.al_presionar_escape)

    # ---------- Callbacks de eventos ----------
    def al_seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if len(seleccion) == 0:
            return
        # El identificador de la fila (iid) se usa para consultar al servicio
        id_usuario = int(seleccion[0])
        usuario = self.servicio.buscar_usuario(id_usuario)
        if usuario is None:
            return
        self.id_seleccionado = usuario.id
        self.var_nombre.set(usuario.nombre)
        self.var_usuario.set(usuario.usuario)
        # La contraseña nunca se carga en el formulario
        self.var_contrasena.set("")
        self.var_rol.set(usuario.rol)
        self.mostrar_descripcion_rol()
        self.actualizar_estado_botones()

    def al_presionar_enter(self, event):
        # Reutiliza el mismo metodo del boton Registrar
        self.registrar_usuario()

    def al_presionar_escape(self, event):
        # Reutiliza el mismo metodo del boton Limpiar
        self.limpiar_formulario()

    def al_cambiar_rol(self, event):
        self.mostrar_descripcion_rol()

    # ---------- Acciones (command= y eventos) ----------
    def registrar_usuario(self):
        try:
            self.servicio.registrar_usuario(
                self.var_nombre.get(), self.var_usuario.get(), self.var_contrasena.get(), self.var_rol.get()
            )
        except (ValueError, PermissionError) as error:
            messagebox.showwarning("No se pudo registrar", str(error))
            return
        messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        self.refrescar_tabla()
        self.limpiar_formulario()

    def actualizar_usuario(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Usuarios", "Seleccione un usuario de la tabla.")
            return
        try:
            self.servicio.actualizar_usuario(
                self.id_seleccionado, self.var_nombre.get(), self.var_usuario.get(), self.var_contrasena.get(), self.var_rol.get()
            )
        except (ValueError, PermissionError) as error:
            messagebox.showwarning("No se pudo actualizar", str(error))
            return
        messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        self.refrescar_tabla()
        self.limpiar_formulario()

    def eliminar_usuario(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Usuarios", "Seleccione un usuario de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar al usuario '" + self.var_usuario.get() + "'?"):
            return
        try:
            self.servicio.eliminar_usuario(self.id_seleccionado)
        except (ValueError, PermissionError) as error:
            messagebox.showwarning("No se pudo eliminar", str(error))
            return
        self.refrescar_tabla()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.id_seleccionado = None
        self.var_nombre.set("")
        self.var_usuario.set("")
        self.var_contrasena.set("")
        self.var_rol.set("")
        self.etiqueta_rol.config(text="")
        # Quita la seleccion actual de la tabla
        self.tabla.selection_remove(self.tabla.selection())
        self.actualizar_estado_botones()
        self.entrada_nombre.focus()

    # ---------- Apoyo visual ----------
    def refrescar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for u in self.servicio.listar_usuarios():
            # La contraseña no se muestra en la tabla
            self.tabla.insert("", "end", iid=str(u.id), values=(u.id, u.nombre, u.usuario, u.rol))

    def mostrar_descripcion_rol(self):
        self.etiqueta_rol.config(text=DESCRIPCION_ROLES.get(self.var_rol.get(), ""))

    def actualizar_estado_botones(self):
        # Registrar solo en modo nuevo; Actualizar y Eliminar solo con una fila elegida
        if self.id_seleccionado is None:
            self.etiqueta_modo.config(text="Modo: nuevo usuario")
            self.boton_registrar.config(state="normal")
            self.boton_actualizar.config(state="disabled")
            self.boton_eliminar.config(state="disabled")
        else:
            self.etiqueta_modo.config(text="Modo: editando usuario #" + str(self.id_seleccionado) + " (contraseña vacía = sin cambios)")
            self.boton_registrar.config(state="disabled")
            self.boton_actualizar.config(state="normal")
            self.boton_eliminar.config(state="normal")


# =====================================================================
# Seccion de productos
# =====================================================================
class ProductosView(tk.Frame):
    def __init__(self, padre, servicio):
        super().__init__(padre, bg=recursos.COLOR_FONDO)
        self.servicio = servicio
        self.id_seleccionado = None
        self.imagenes = {
            "registrar": recursos.cargar_imagen("icono_registrar.png"),
            "actualizar": recursos.cargar_imagen("icono_actualizar.png"),
            "eliminar": recursos.cargar_imagen("icono_eliminar.png"),
            "limpiar": recursos.cargar_imagen("icono_limpiar.png"),
        }
        self.crear_widgets()
        self.refrescar_tabla()

    def crear_widgets(self):
        crear_titulo(self, "Productos").pack(anchor="w", pady=(0, 10))
        formulario = tk.Frame(self, bg="white", padx=16, pady=14, highlightbackground="#dddddd", highlightthickness=1)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        self.var_nombre = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()

        tk.Label(formulario, text="Nombre", bg="white", font=recursos.FUENTE).grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(formulario, textvariable=self.var_nombre).grid(row=0, column=1, sticky="ew", padx=(8, 20), pady=4)
        tk.Label(formulario, text="Categoría", bg="white", font=recursos.FUENTE).grid(row=0, column=2, sticky="w", pady=4)
        ttk.Combobox(formulario, textvariable=self.var_categoria, values=CATEGORIAS, state="readonly").grid(row=0, column=3, sticky="ew", padx=8, pady=4)
        tk.Label(formulario, text="Precio ($)", bg="white", font=recursos.FUENTE).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(formulario, textvariable=self.var_precio).grid(row=1, column=1, sticky="ew", padx=(8, 20), pady=4)
        tk.Label(formulario, text="Stock", bg="white", font=recursos.FUENTE).grid(row=1, column=2, sticky="w", pady=4)
        ttk.Entry(formulario, textvariable=self.var_stock).grid(row=1, column=3, sticky="ew", padx=8, pady=4)

        botones = tk.Frame(formulario, bg="white")
        botones.grid(row=2, column=0, columnspan=4, sticky="w", pady=(12, 0))
        recursos.crear_boton(botones, "Registrar", self.registrar_producto, recursos.COLOR_VERDE, self.imagenes["registrar"]).pack(side="left", padx=(0, 8))
        recursos.crear_boton(botones, "Actualizar", self.actualizar_producto, recursos.COLOR_AZUL, self.imagenes["actualizar"]).pack(side="left", padx=(0, 8))
        recursos.crear_boton(botones, "Eliminar", self.eliminar_producto, recursos.COLOR_PRIMARIO, self.imagenes["eliminar"]).pack(side="left", padx=(0, 8))
        recursos.crear_boton(botones, "Limpiar", self.limpiar_formulario, recursos.COLOR_NEUTRO, self.imagenes["limpiar"]).pack(side="left")

        columnas = [("id", "ID", 50), ("nombre", "Nombre", 260), ("categoria", "Categoría", 160), ("precio", "Precio", 90), ("stock", "Stock", 80)]
        contenedor, self.tabla = crear_tabla(self, columnas, 8)
        contenedor.pack(fill="both", expand=True, pady=(14, 0))
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)

    def al_seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if len(seleccion) == 0:
            return
        producto = self.servicio.buscar_producto(int(seleccion[0]))
        if producto is None:
            return
        self.id_seleccionado = producto.id
        self.var_nombre.set(producto.nombre)
        self.var_categoria.set(producto.categoria)
        self.var_precio.set(str(producto.precio))
        self.var_stock.set(str(producto.stock))

    def registrar_producto(self):
        try:
            self.servicio.registrar_producto(self.var_nombre.get(), self.var_categoria.get(), self.var_precio.get(), self.var_stock.get())
        except ValueError as error:
            messagebox.showwarning("No se pudo registrar", str(error))
            return
        self.refrescar_tabla()
        self.limpiar_formulario()

    def actualizar_producto(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Productos", "Seleccione un producto de la tabla.")
            return
        try:
            self.servicio.actualizar_producto(self.id_seleccionado, self.var_nombre.get(), self.var_categoria.get(), self.var_precio.get(), self.var_stock.get())
        except ValueError as error:
            messagebox.showwarning("No se pudo actualizar", str(error))
            return
        self.refrescar_tabla()
        self.limpiar_formulario()

    def eliminar_producto(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Productos", "Seleccione un producto de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar este producto?"):
            return
        try:
            self.servicio.eliminar_producto(self.id_seleccionado)
        except ValueError as error:
            messagebox.showwarning("No se pudo eliminar", str(error))
            return
        self.refrescar_tabla()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.id_seleccionado = None
        self.var_nombre.set("")
        self.var_categoria.set("")
        self.var_precio.set("")
        self.var_stock.set("")
        self.tabla.selection_remove(self.tabla.selection())

    def refrescar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for p in self.servicio.listar_productos():
            self.tabla.insert("", "end", iid=str(p.id), values=(p.id, p.nombre, p.categoria, "$" + format(p.precio, ".2f"), p.stock))


# =====================================================================
# Seccion de ventas
# =====================================================================
class VentasView(tk.Frame):
    def __init__(self, padre, servicio):
        super().__init__(padre, bg=recursos.COLOR_FONDO)
        self.servicio = servicio
        # carrito: lista de [id_producto, cantidad]
        self.carrito = []
        self.imagenes = {
            "registrar": recursos.cargar_imagen("icono_registrar.png"),
            "eliminar": recursos.cargar_imagen("icono_eliminar.png"),
            "ventas": recursos.cargar_imagen("icono_ventas.png"),
        }
        self.crear_widgets()
        self.refrescar_historial()

    def crear_widgets(self):
        crear_titulo(self, "Ventas").pack(anchor="w", pady=(0, 10))
        panel = tk.Frame(self, bg="white", padx=16, pady=14, highlightbackground="#dddddd", highlightthickness=1)
        panel.pack(fill="x")

        fila = tk.Frame(panel, bg="white")
        fila.pack(fill="x")
        tk.Label(fila, text="Producto", bg="white", font=recursos.FUENTE).pack(side="left")
        self.var_producto = tk.StringVar()
        self.combo_producto = ttk.Combobox(fila, textvariable=self.var_producto, state="readonly", width=34)
        self.combo_producto.pack(side="left", padx=8)
        tk.Label(fila, text="Cantidad", bg="white", font=recursos.FUENTE).pack(side="left")
        self.var_cantidad = tk.StringVar(value="1")
        ttk.Spinbox(fila, from_=1, to=99, textvariable=self.var_cantidad, width=5).pack(side="left", padx=8)
        recursos.crear_boton(fila, "Agregar", self.agregar_al_carrito, recursos.COLOR_VERDE, self.imagenes["registrar"]).pack(side="left", padx=(8, 0))
        self.actualizar_combo()

        columnas = [("producto", "Producto", 280), ("cantidad", "Cantidad", 80), ("precio", "Precio", 90), ("subtotal", "Subtotal", 100)]
        contenedor, self.tabla_carrito = crear_tabla(panel, columnas, 4)
        contenedor.pack(fill="x", pady=10)

        pie = tk.Frame(panel, bg="white")
        pie.pack(fill="x")
        recursos.crear_boton(pie, "Quitar", self.quitar_del_carrito, recursos.COLOR_NEUTRO, self.imagenes["eliminar"]).pack(side="left")
        recursos.crear_boton(pie, "Registrar venta", self.registrar_venta, recursos.COLOR_PRIMARIO, self.imagenes["ventas"]).pack(side="right")
        self.etiqueta_total = tk.Label(pie, text="Total: $0.00", bg="white", font=recursos.FUENTE_SUBTITULO)
        self.etiqueta_total.pack(side="right", padx=16)

        tk.Label(self, text="Historial de ventas", font=recursos.FUENTE_SUBTITULO, bg=recursos.COLOR_FONDO).pack(anchor="w", pady=(14, 4))
        columnas = [("id", "N°", 50), ("fecha", "Fecha", 150), ("usuario", "Usuario", 130), ("detalle", "Detalle", 320), ("total", "Total", 80)]
        contenedor, self.tabla_ventas = crear_tabla(self, columnas, 5)
        contenedor.pack(fill="both", expand=True)

    def actualizar_combo(self):
        self.mapa_productos = {}
        etiquetas = []
        for p in self.servicio.listar_productos():
            etiqueta = p.nombre + " ($" + format(p.precio, ".2f") + ") - stock " + str(p.stock)
            self.mapa_productos[etiqueta] = p.id
            etiquetas.append(etiqueta)
        self.combo_producto.config(values=etiquetas)
        self.var_producto.set("")

    def agregar_al_carrito(self):
        etiqueta = self.var_producto.get()
        if etiqueta not in self.mapa_productos:
            messagebox.showinfo("Ventas", "Seleccione un producto.")
            return
        try:
            cantidad = int(self.var_cantidad.get())
        except ValueError:
            messagebox.showwarning("Ventas", "La cantidad debe ser un número entero.")
            return
        if cantidad <= 0:
            messagebox.showwarning("Ventas", "La cantidad debe ser mayor que cero.")
            return
        id_producto = self.mapa_productos[etiqueta]
        producto = self.servicio.buscar_producto(id_producto)
        for item in self.carrito:
            if item[0] == id_producto:
                if item[1] + cantidad > producto.stock:
                    messagebox.showwarning("Ventas", "Stock insuficiente de " + producto.nombre + ".")
                    return
                item[1] += cantidad
                self.refrescar_carrito()
                return
        if cantidad > producto.stock:
            messagebox.showwarning("Ventas", "Stock insuficiente de " + producto.nombre + ".")
            return
        self.carrito.append([id_producto, cantidad])
        self.refrescar_carrito()

    def quitar_del_carrito(self):
        seleccion = self.tabla_carrito.selection()
        if len(seleccion) == 0:
            messagebox.showinfo("Ventas", "Seleccione una fila del carrito.")
            return
        indice = int(seleccion[0])
        del self.carrito[indice]
        self.refrescar_carrito()

    def refrescar_carrito(self):
        for fila in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(fila)
        total = 0
        for indice, item in enumerate(self.carrito):
            producto = self.servicio.buscar_producto(item[0])
            subtotal = producto.precio * item[1]
            total = total + subtotal
            self.tabla_carrito.insert("", "end", iid=str(indice), values=(producto.nombre, item[1], "$" + format(producto.precio, ".2f"), "$" + format(subtotal, ".2f")))
        self.etiqueta_total.config(text="Total: $" + format(total, ".2f"))

    def registrar_venta(self):
        items = [(item[0], item[1]) for item in self.carrito]
        try:
            venta = self.servicio.registrar_venta(items)
        except ValueError as error:
            messagebox.showwarning("No se pudo registrar", str(error))
            return
        messagebox.showinfo("Ventas", "Venta registrada. Total: $" + format(venta.total, ".2f"))
        self.carrito = []
        self.refrescar_carrito()
        self.actualizar_combo()
        self.refrescar_historial()

    def refrescar_historial(self):
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)
        for v in self.servicio.listar_ventas():
            partes = [str(d["cantidad"]) + "x " + d["producto"] for d in v.detalle]
            self.tabla_ventas.insert("", "end", values=(v.id, v.fecha, v.usuario, ", ".join(partes), "$" + format(v.total, ".2f")))


# =====================================================================
# Ventana principal con navegacion lateral
# =====================================================================
class MainView(tk.Frame):
    def __init__(self, padre, servicio, al_cerrar_sesion):
        super().__init__(padre, bg=recursos.COLOR_FONDO)
        self.servicio = servicio
        self.al_cerrar_sesion = al_cerrar_sesion
        self.vista_actual = None
        self.logo = recursos.cargar_imagen("logo.png")
        self.iconos = {
            "productos": recursos.cargar_imagen("icono_productos.png"),
            "ventas": recursos.cargar_imagen("icono_ventas.png"),
            "usuarios": recursos.cargar_imagen("icono_usuarios.png"),
            "salir": recursos.cargar_imagen("icono_salir.png"),
        }
        self.crear_menu()
        self.contenido = tk.Frame(self, bg=recursos.COLOR_FONDO, padx=24, pady=20)
        self.contenido.pack(side="left", fill="both", expand=True)
        self.mostrar_productos()

    def crear_menu(self):
        menu = tk.Frame(self, bg=recursos.COLOR_BARRA, width=210)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        if self.logo:
            tk.Label(menu, image=self.logo, bg=recursos.COLOR_BARRA).pack(pady=(20, 4))
        tk.Label(menu, text="Restaurante App", fg="white", bg=recursos.COLOR_BARRA, font=recursos.FUENTE_SUBTITULO).pack()
        usuario = self.servicio.usuario_actual
        tk.Label(menu, text=usuario.nombre, fg="#cccccc", bg=recursos.COLOR_BARRA, font=recursos.FUENTE).pack(pady=(10, 0))
        tk.Label(menu, text=usuario.rol, fg="#e6a39b", bg=recursos.COLOR_BARRA, font=("Segoe UI", 9, "italic")).pack(pady=(0, 20))

        self.agregar_opcion(menu, "Productos", "productos", self.mostrar_productos)
        self.agregar_opcion(menu, "Ventas", "ventas", self.mostrar_ventas)
        # Solo el Administrador ve la opcion de usuarios
        if self.servicio.es_administrador():
            self.agregar_opcion(menu, "Usuarios", "usuarios", self.mostrar_usuarios)

        boton_salir = tk.Button(
            menu, text=" Cerrar sesión", image=self.iconos["salir"], compound="left", command=self.al_cerrar_sesion,
            bg=recursos.COLOR_BARRA, fg="white", activebackground="#444444", activeforeground="white",
            relief="flat", bd=0, anchor="w", padx=20, pady=10, font=recursos.FUENTE, cursor="hand2",
        )
        boton_salir.pack(side="bottom", fill="x", pady=10)

    def agregar_opcion(self, menu, texto, icono, comando):
        boton = tk.Button(
            menu, text=" " + texto, image=self.iconos[icono], compound="left", command=comando,
            bg=recursos.COLOR_BARRA, fg="white", activebackground=recursos.COLOR_PRIMARIO, activeforeground="white",
            relief="flat", bd=0, anchor="w", padx=20, pady=10, font=recursos.FUENTE, cursor="hand2",
        )
        boton.pack(fill="x")

    def cambiar_seccion(self, clase_vista):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = clase_vista(self.contenido, self.servicio)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_productos(self):
        self.cambiar_seccion(ProductosView)

    def mostrar_ventas(self):
        self.cambiar_seccion(VentasView)

    def mostrar_usuarios(self):
        # Doble control de acceso: el servicio tambien valida el rol
        if not self.servicio.es_administrador():
            messagebox.showwarning("Acceso restringido", "Solo el Administrador puede gestionar usuarios.")
            return
        self.cambiar_seccion(UsuariosView)
