# Servicio encargado de leer y escribir archivos JSON
import json
import os


class ArchivoServicio:
    def __init__(self, ruta_datos):
        self.ruta_datos = ruta_datos

    def leer(self, nombre_archivo):
        ruta = os.path.join(self.ruta_datos, nombre_archivo)
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            # Si el archivo esta dañado se devuelve una lista vacia
            return []

    def guardar(self, nombre_archivo, datos):
        os.makedirs(self.ruta_datos, exist_ok=True)
        ruta = os.path.join(self.ruta_datos, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
