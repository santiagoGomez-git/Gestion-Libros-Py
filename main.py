from nicegui import ui
import repositorio
import interfaz

repositorio.inicializar_db()
interfaz.cargar_interfaz()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="CRUD Libros")