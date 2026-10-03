# Punto de entrada de restaurante_app
import os
import tkinter as tk
from tkinter import ttk

from servicios.restaurante_servicio import RestauranteServicio
from ui import recursos
from ui.login_view import LoginView
from ui.main_view import MainView


class Aplicacion:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.servicio = RestauranteServicio(os.path.join(base, "datos"))
        self.raiz = tk.Tk()
        self.raiz.title("Restaurante App")
        self.raiz.geometry("1000x620")
        self.raiz.minsize(900, 560)
        self.raiz.configure(bg=recursos.COLOR_FONDO)
        self.icono = recursos.cargar_imagen("logo.png")
        if self.icono:
            self.raiz.iconphoto(True, self.icono)
        self.configurar_estilos()
        self.vista = None
        self.mostrar_login()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=26, font=recursos.FUENTE, background="white", fieldbackground="white")
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e8e8e8", relief="flat")
        estilo.map("Treeview", background=[("selected", recursos.COLOR_PRIMARIO)], foreground=[("selected", "white")])
        estilo.configure("TEntry", padding=4)
        estilo.configure("TCombobox", padding=4)

    def cambiar_vista(self, nueva):
        if self.vista is not None:
            self.vista.destroy()
        self.vista = nueva
        self.vista.pack(fill="both", expand=True)

    def mostrar_login(self):
        self.servicio.cerrar_sesion()
        self.cambiar_vista(LoginView(self.raiz, self.servicio, self.mostrar_principal))

    def mostrar_principal(self):
        self.cambiar_vista(MainView(self.raiz, self.servicio, self.mostrar_login))

    def ejecutar(self):
        self.raiz.mainloop()


if __name__ == "__main__":
    Aplicacion().ejecutar()
