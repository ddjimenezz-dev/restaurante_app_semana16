# Servicio principal: reglas de negocio, validaciones y persistencia
from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario, ROL_ADMINISTRADOR, ROL_EMPLEADO, ROL_CLIENTE, ROLES_GESTIONABLES
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, ruta_datos):
        self.archivos = ArchivoServicio(ruta_datos)
        self.productos = []
        self.usuarios = []
        self.ventas = []
        self.usuario_actual = None
        self.cargar_datos()

    # ---------- Carga y guardado ----------
    def cargar_datos(self):
        self.productos = [Producto.desde_diccionario(d) for d in self.archivos.leer("productos.json")]
        self.usuarios = [Usuario.desde_diccionario(d) for d in self.archivos.leer("usuarios.json")]
        self.ventas = [Venta.desde_diccionario(d) for d in self.archivos.leer("ventas.json")]

        # Datos iniciales si los archivos estan vacios
        if len(self.usuarios) == 0:
            self.usuarios = [
                Usuario(1, "Administrador General", "admin", "admin123", ROL_ADMINISTRADOR),
                Usuario(2, "Carlos Mesero", "empleado", "emp123", ROL_EMPLEADO),
                Usuario(3, "Laura Cliente", "cliente", "cli123", ROL_CLIENTE),
            ]
            self.guardar_usuarios()
        if len(self.productos) == 0:
            self.productos = [
                Producto(1, "Encebollado", "Platos fuertes", 3.50, 20),
                Producto(2, "Seco de pollo", "Platos fuertes", 4.50, 15),
                Producto(3, "Empanadas de viento", "Entradas", 1.25, 30),
                Producto(4, "Jugo de naranja", "Bebidas", 1.50, 25),
                Producto(5, "Tres leches", "Postres", 2.75, 10),
            ]
            self.guardar_productos()

    def guardar_productos(self):
        self.archivos.guardar("productos.json", [p.a_diccionario() for p in self.productos])

    def guardar_usuarios(self):
        self.archivos.guardar("usuarios.json", [u.a_diccionario() for u in self.usuarios])

    def guardar_ventas(self):
        self.archivos.guardar("ventas.json", [v.a_diccionario() for v in self.ventas])

    # ---------- Sesion ----------
    def iniciar_sesion(self, usuario, contrasena):
        usuario = usuario.strip()
        if usuario == "" or contrasena == "":
            raise ValueError("Ingrese usuario y contraseña.")
        for u in self.usuarios:
            if u.usuario == usuario and u.contrasena == contrasena:
                self.usuario_actual = u
                return u
        raise ValueError("Usuario o contraseña incorrectos.")

    def cerrar_sesion(self):
        self.usuario_actual = None

    def es_administrador(self):
        return self.usuario_actual is not None and self.usuario_actual.es_administrador()

    def _exigir_administrador(self):
        if not self.es_administrador():
            raise PermissionError("Solo el Administrador puede gestionar usuarios.")

    def _siguiente_id(self, lista):
        if len(lista) == 0:
            return 1
        return max(elemento.id for elemento in lista) + 1

    # ---------- Usuarios ----------
    def listar_usuarios(self):
        self._exigir_administrador()
        return list(self.usuarios)

    def buscar_usuario(self, id_usuario):
        for u in self.usuarios:
            if u.id == id_usuario:
                return u
        return None

    def _validar_datos_usuario(self, nombre, usuario, rol, id_ignorar=None):
        if nombre.strip() == "":
            raise ValueError("El nombre es obligatorio.")
        if len(usuario) < 3 or " " in usuario:
            raise ValueError("El usuario debe tener al menos 3 caracteres y no llevar espacios.")
        for u in self.usuarios:
            if u.usuario.lower() == usuario.lower() and u.id != id_ignorar:
                raise ValueError("Ya existe un usuario con ese nombre de usuario.")

    def registrar_usuario(self, nombre, usuario, contrasena, rol):
        self._exigir_administrador()
        nombre = nombre.strip()
        usuario = usuario.strip()
        self._validar_datos_usuario(nombre, usuario, rol)
        if len(contrasena) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")
        if rol not in ROLES_GESTIONABLES:
            raise ValueError("Seleccione un rol válido (Empleado o Cliente).")
        nuevo = Usuario(self._siguiente_id(self.usuarios), nombre, usuario, contrasena, rol)
        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        self._exigir_administrador()
        existente = self.buscar_usuario(id_usuario)
        if existente is None:
            raise ValueError("Seleccione un usuario de la tabla.")
        nombre = nombre.strip()
        usuario = usuario.strip()
        self._validar_datos_usuario(nombre, usuario, rol, id_usuario)
        # La cuenta administradora conserva su rol
        if existente.es_administrador():
            rol = ROL_ADMINISTRADOR
        elif rol not in ROLES_GESTIONABLES:
            raise ValueError("Seleccione un rol válido (Empleado o Cliente).")
        # Si la contraseña queda vacia se conserva la anterior
        if contrasena != "":
            if len(contrasena) < 4:
                raise ValueError("La contraseña debe tener al menos 4 caracteres.")
            existente.cambiar_contrasena(contrasena)
        existente.nombre = nombre
        existente.usuario = usuario
        existente.rol = rol
        self.guardar_usuarios()
        return existente

    def eliminar_usuario(self, id_usuario):
        self._exigir_administrador()
        existente = self.buscar_usuario(id_usuario)
        if existente is None:
            raise ValueError("Seleccione un usuario de la tabla.")
        if self.usuario_actual is not None and existente.id == self.usuario_actual.id:
            raise ValueError("No puede eliminar la cuenta con la que inició sesión.")
        self.usuarios.remove(existente)
        self.guardar_usuarios()

    # ---------- Productos ----------
    def listar_productos(self):
        return list(self.productos)

    def buscar_producto(self, id_producto):
        for p in self.productos:
            if p.id == id_producto:
                return p
        return None

    def _validar_producto(self, nombre, precio, stock):
        if nombre.strip() == "":
            raise ValueError("El nombre del producto es obligatorio.")
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            raise ValueError("Precio y stock deben ser numéricos.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        return precio, stock

    def registrar_producto(self, nombre, categoria, precio, stock):
        precio, stock = self._validar_producto(nombre, precio, stock)
        nuevo = Producto(self._siguiente_id(self.productos), nombre.strip(), categoria, precio, stock)
        self.productos.append(nuevo)
        self.guardar_productos()
        return nuevo

    def actualizar_producto(self, id_producto, nombre, categoria, precio, stock):
        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("Seleccione un producto de la tabla.")
        precio, stock = self._validar_producto(nombre, precio, stock)
        producto.nombre = nombre.strip()
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        self.guardar_productos()

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("Seleccione un producto de la tabla.")
        self.productos.remove(producto)
        self.guardar_productos()

    # ---------- Ventas ----------
    def listar_ventas(self):
        if self.es_administrador():
            return list(self.ventas)
        # Los demas roles solo ven sus propias ventas
        return [v for v in self.ventas if v.usuario == self.usuario_actual.usuario]

    def registrar_venta(self, items):
        # items: lista de tuplas (id_producto, cantidad)
        if len(items) == 0:
            raise ValueError("Agregue al menos un producto a la venta.")
        detalle = []
        total = 0
        for id_producto, cantidad in items:
            producto = self.buscar_producto(id_producto)
            if producto is None:
                raise ValueError("Un producto de la venta ya no existe.")
            if cantidad > producto.stock:
                raise ValueError("Stock insuficiente de " + producto.nombre + ".")
            detalle.append({"producto": producto.nombre, "cantidad": cantidad, "precio": producto.precio})
            total = total + producto.precio * cantidad
        # Se descuenta el stock solo si todo es valido
        for id_producto, cantidad in items:
            self.buscar_producto(id_producto).stock -= cantidad
        venta = Venta(
            self._siguiente_id(self.ventas),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            self.usuario_actual.usuario,
            detalle,
            round(total, 2),
        )
        self.ventas.append(venta)
        self.guardar_productos()
        self.guardar_ventas()
        return venta
