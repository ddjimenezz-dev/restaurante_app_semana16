# Utilidades visuales: colores, carga de imagenes desde assets/ y botones
import os
import tkinter as tk

RUTA_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

COLOR_PRIMARIO = "#c0392b"
COLOR_PRIMARIO_OSCURO = "#a93226"
COLOR_BARRA = "#2b2b2b"
COLOR_FONDO = "#f5f5f5"
COLOR_TEXTO = "#222222"
COLOR_GRIS = "#7f8c8d"
COLOR_VERDE = "#27ae60"
COLOR_AZUL = "#2980b9"
COLOR_NEUTRO = "#7f8c8d"

FUENTE = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 16, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 11, "bold")


def cargar_imagen(nombre):
    ruta = os.path.join(RUTA_ASSETS, nombre)
    if os.path.exists(ruta):
        return tk.PhotoImage(file=ruta)
    return None


def crear_boton(padre, texto, comando, color, imagen=None):
    # Boton plano con color; se asocia la accion mediante command=
    boton = tk.Button(
        padre,
        text=" " + texto,
        image=imagen,
        compound="left",
        command=comando,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        font=FUENTE,
        cursor="hand2",
    )
    return boton
