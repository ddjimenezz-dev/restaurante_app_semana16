# Modelo Venta del restaurante


class Venta:
    def __init__(self, id_venta, fecha, usuario, detalle, total):
        self.__id = id_venta
        self.fecha = fecha
        self.usuario = usuario
        # detalle: lista de diccionarios con producto, cantidad y precio
        self.detalle = detalle
        self.total = total

    @property
    def id(self):
        return self.__id

    def a_diccionario(self):
        return {
            "id": self.__id,
            "fecha": self.fecha,
            "usuario": self.usuario,
            "detalle": self.detalle,
            "total": self.total,
        }

    @staticmethod
    def desde_diccionario(datos):
        return Venta(
            datos["id"],
            datos["fecha"],
            datos["usuario"],
            datos["detalle"],
            datos["total"],
        )
