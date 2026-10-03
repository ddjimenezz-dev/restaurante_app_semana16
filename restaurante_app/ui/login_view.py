# Vista de inicio de sesion
import tkinter as tk
from tkinter import ttk, messagebox

from ui import recursos


class LoginView(tk.Frame):
    def __init__(self, padre, servicio, al_ingresar):
        super().__init__(padre, bg=recursos.COLOR_FONDO)
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.logo = recursos.cargar_imagen("logo.png")
        self.crear_widgets()

    def crear_widgets(self):
        tarjeta = tk.Frame(self, bg="white", padx=40, pady=30, highlightbackground="#dddddd", highlightthickness=1)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        if self.logo:
            tk.Label(tarjeta, image=self.logo, bg="white").pack(pady=(0, 8))
        tk.Label(tarjeta, text="Restaurante App", font=recursos.FUENTE_TITULO, bg="white", fg=recursos.COLOR_PRIMARIO).pack()
        tk.Label(tarjeta, text="Inicie sesión para continuar", font=recursos.FUENTE, bg="white", fg=recursos.COLOR_GRIS).pack(pady=(0, 16))

        tk.Label(tarjeta, text="Usuario", bg="white", font=recursos.FUENTE, anchor="w").pack(fill="x")
        self.var_usuario = tk.StringVar()
        self.entrada_usuario = ttk.Entry(tarjeta, textvariable=self.var_usuario, width=30)
        self.entrada_usuario.pack(pady=(0, 10))

        tk.Label(tarjeta, text="Contraseña", bg="white", font=recursos.FUENTE, anchor="w").pack(fill="x")
        self.var_contrasena = tk.StringVar()
        self.entrada_contrasena = ttk.Entry(tarjeta, textvariable=self.var_contrasena, show="*", width=30)
        self.entrada_contrasena.pack(pady=(0, 16))

        crear = recursos.crear_boton(tarjeta, "Ingresar", self.iniciar_sesion, recursos.COLOR_PRIMARIO)
        crear.pack(fill="x")

        # Enter tambien permite iniciar sesion
        self.entrada_usuario.bind("<Return>", self.al_presionar_enter)
        self.entrada_contrasena.bind("<Return>", self.al_presionar_enter)
        self.entrada_usuario.focus()

    def al_presionar_enter(self, event):
        self.iniciar_sesion()

    def iniciar_sesion(self):
        try:
            self.servicio.iniciar_sesion(self.var_usuario.get(), self.var_contrasena.get())
        except ValueError as error:
            messagebox.showerror("Acceso denegado", str(error))
            self.var_contrasena.set("")
            return
        self.al_ingresar()
