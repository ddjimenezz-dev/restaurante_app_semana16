# Restaurante App – Semana 16: Manejo de eventos en Tkinter

Proyecto de Programación Orientada a Objetos (UEA). Esta semana se evoluciona `restaurante_app` (versión de la Semana 15) aplicando **manejo de eventos** en la gestión de usuarios.

## Evolución respecto a la semana anterior
- Se conserva la arquitectura modular: `datos`, `modelos`, `servicios`, `ui` y `main.py`.
- Se conservan el inicio de sesión, la navegación, Productos y Ventas.
- Se amplía la sección **Usuarios** con CRUD completo usando un formulario y una tabla `Treeview`.
- El modelo `Usuario` incorpora el atributo `rol`, que se guarda en `usuarios.json`.

## Estructura
```
restaurante_app/
├── datos/            productos.json, usuarios.json, ventas.json
├── modelos/          producto.py, usuario.py, venta.py
├── servicios/        archivo_servicio.py, restaurante_servicio.py
├── ui/               login_view.py, main_view.py, recursos.py
├── assets/           logo e íconos (PNG)
└── main.py
```

## Roles
| Rol | Acceso |
|---|---|
| Administrador | Productos, Ventas y gestión de Usuarios |
| Empleado | Productos y Ventas |
| Cliente | Productos y Ventas |

Solo el Administrador ve la opción **Usuarios**; además, `RestauranteServicio` valida el rol en cada operación. El administrador registra usuarios de tipo Empleado o Cliente.

Usuarios de prueba: `admin / admin123`, `empleado / emp123`, `cliente / cli123`.

## Gestión de usuarios
- **Registrar, Actualizar, Eliminar y Limpiar** desde el formulario.
- La tabla muestra ID, nombre, usuario y rol (nunca la contraseña).
- Al actualizar, si la contraseña queda vacía se conserva la anterior.
- Eliminar pide confirmación y no permite borrar la cuenta con la sesión activa.
- Validaciones (usuario único, longitud, rol válido) y persistencia están en `RestauranteServicio`; la interfaz no lee ni escribe JSON.

## Eventos implementados
| Evento | Dónde | Callback | Resultado |
|---|---|---|---|
| `<<TreeviewSelect>>` | Tabla de usuarios | `al_seleccionar_fila` | Busca el usuario por ID en el servicio y carga el formulario |
| `<Return>` | Campos del formulario | `al_presionar_enter` | Llama a `registrar_usuario()` (mismo método del botón) |
| `<Escape>` | Campos y tabla | `al_presionar_escape` | Llama a `limpiar_formulario()` y quita la selección |
| `<<ComboboxSelected>>` | Combobox de rol | `al_cambiar_rol` | Muestra la descripción del rol elegido |

## `bind()`, `command=` y callbacks
- `command=` se usa en los botones (Registrar, Actualizar, Eliminar, Limpiar): es la acción directa de un clic y el callback no recibe `event`.
- `bind()` asocia eventos de teclado o virtuales de ttk a un callback que recibe el objeto `event`.
- Los callbacks de eventos **reutilizan** los mismos métodos que los botones, sin duplicar lógica.
- Flujo: interacción → evento → `bind()` → callback → servicio → persistencia → respuesta visual.

## Persistencia
Los usuarios se guardan en `datos/usuarios.json` (con el campo `rol`) y se recuperan al reiniciar la aplicación.

## Cómo ejecutar
Requiere Python 3 con Tkinter.
```
cd restaurante_app
python main.py
```
