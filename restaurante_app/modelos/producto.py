# Modelo Producto del restaurante

CATEGORIAS = ["Platos fuertes", "Entradas", "Bebidas", "Postres"]


class Producto:
    def __init__(self, id_producto, nombre, categoria, precio, stock):
        self.__id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @property
    def id(self):
        return self.__id

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @staticmethod
    def desde_diccionario(datos):
        return Producto(
            datos["id"],
            datos["nombre"],
            datos["categoria"],
            datos["precio"],
            datos["stock"],
        )

    def __str__(self):
        return self.nombre + " - $" + format(self.precio, ".2f")
