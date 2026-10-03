# Modelo Usuario del restaurante

ROL_ADMINISTRADOR = "Administrador"
ROL_EMPLEADO = "Empleado"
ROL_CLIENTE = "Cliente"

# Roles que el administrador puede asignar desde el formulario
ROLES_GESTIONABLES = [ROL_EMPLEADO, ROL_CLIENTE]

DESCRIPCION_ROLES = {
    ROL_ADMINISTRADOR: "Gestiona usuarios, productos y ventas.",
    ROL_EMPLEADO: "Atiende el local: gestiona productos y registra ventas.",
    ROL_CLIENTE: "Consulta productos y realiza compras.",
}


class Usuario:
    def __init__(self, id_usuario, nombre, usuario, contrasena, rol):
        self.__id = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.__contrasena = contrasena
        self.rol = rol

    # Propiedades de solo lectura
    @property
    def id(self):
        return self.__id

    @property
    def contrasena(self):
        return self.__contrasena

    def cambiar_contrasena(self, nueva):
        self.__contrasena = nueva

    def es_administrador(self):
        return self.rol == ROL_ADMINISTRADOR

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.__contrasena,
            "rol": self.rol,
        }

    @staticmethod
    def desde_diccionario(datos):
        return Usuario(
            datos["id"],
            datos["nombre"],
            datos["usuario"],
            datos["contrasena"],
            datos.get("rol", ROL_CLIENTE),
        )

    def __str__(self):
        return self.nombre + " (" + self.rol + ")"
