from nicegui import ui
import repositorio

def cargar_interfaz():
    ui.label('Gestión de Catálogo de Libros').classes('text-2xl font-bold mb-4')
    
    # ==========================================
    # 1. SECCIÓN: FORMULARIO DE CREACIÓN
    # ==========================================
    with ui.card().classes('w-full max-w-4xl mb-6'):
        ui.label('Agregar Nuevo Libro').classes('text-xl mb-2 font-semibold')
        
        with ui.row().classes('w-full gap-4'):
            input_titulo = ui.input(label='Título (Obligatorio)*').classes('flex-grow')
            input_autor = ui.input(label='Autor (Obligatorio)*').classes('flex-grow')
        
        with ui.row().classes('w-full gap-4'):
            input_genero = ui.input(label='Género').classes('flex-grow')
            input_precio = ui.number(label='Precio ($)', format='%.2f').classes('w-32')
            input_anio = ui.number(label='Año', format='%d').classes('w-32')
            input_editorial = ui.input(label='Editorial').classes('flex-grow')

        def guardar_libro():
            # Validación de campos obligatorios requerida por el TP
            if not input_titulo.value or not input_autor.value:
                ui.notify('Por favor, completá el Título y el Autor.', color='negative')
                return
            
            # Guardamos convirtiendo el año a entero como resolvimos antes
            repositorio.crear_libro(
                titulo=input_titulo.value,
                autor=input_autor.value,
                genero=input_genero.value or "",
                precio=float(input_precio.value or 0.0),
                anio_publicacion=int(input_anio.value or 0),
                editorial=input_editorial.value or ""
            )
            
            ui.notify('¡Libro guardado exitosamente!', color='positive')
            
            # Limpiamos los campos
            input_titulo.value = ''
            input_autor.value = ''
            input_genero.value = ''
            input_precio.value = None
            input_anio.value = None
            input_editorial.value = ''
            
            actualizar_tabla()

        ui.button('GUARDAR LIBRO', on_click=guardar_libro).classes('mt-4')

    # ==========================================
    # 2. SECCIÓN: VENTANA EMERGENTE (MODAL) PARA EDITAR
    # ==========================================
    # Usamos un dic para guardar el ID del libro que estamos diciendo en este momento
    estado_edicion = {'id': None}
    with ui.dialog() as dialogo_edicion, ui.card().classes('w-full max-w-2xl'):
        ui.label('Editar Libro').classes('text-xl font-bold mb-4')

        with ui.row().classes('w-full gap-4'):
            edit_titulo = ui.input(label='Titulo*').classes('flex-grow')
            edit_autor = ui.input(label='Autor*').classes('flex-grow')

        with ui.row().classes('w-full gap-4'):
            edit_genero = ui.input(label='Genero').classes('flex-grow')
            edit_precio = ui.number(label='Precio ($)', format='%.2f').classes('w-32')
            edit_anio = ui.number(label='Año', format='%d').classes('w-32')

        edit_editorial = ui.input(label='Editorial').classes('w-full')

        def confirmar_edicion():
            if not edit_titulo.value or not edit_autor.value:
                ui.notify('El Titulo y el Autor no pueden quedar vacios.', color='negative')
                return

            repositorio.actualizar_libro(
                id_libro=estado_edicion['id'],
                titulo=edit_titulo.value,
                autor=edit_autor.value,
                genero=edit_genero.value or "",
                precio=float(edit_precio.value or 0.0),
                anio_publicacion=int(edit_anio.value or 0),
                editorial=edit_editorial.value or ""
            )

            ui.notify('Libro actualizado correctamente!', color='positive')
            dialogo_edicion.close()
            actualizar_tabla()

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Cancelar', on_click=dialogo_edicion.close, color='gray')
            ui.button('Guardar Cambios', on_click=confirmar_edicion, color='blue')

    # ==========================================
    # 3. SECCIÓN: TABLA DE LECTURA Y ACCIONES
    # ==========================================

    columnas = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'titulo', 'label': 'Título', 'field': 'titulo'},
        {'name': 'autor', 'label': 'Autor', 'field': 'autor'},
        {'name': 'genero', 'label': 'Género', 'field': 'genero'},
        {'name': 'precio', 'label': 'Precio ($)', 'field': 'precio'},
        {'name': 'anio_publicacion', 'label': 'Año', 'field': 'anio_publicacion'},
        {'name': 'editorial', 'label': 'Editorial', 'field': 'editorial'},
        {'name': 'acciones', 'label': 'Acciones', 'field': 'acciones'}, # <- Columna del botón
    ]
    
    tabla = ui.table(columns=columnas, rows=[], row_key='id').classes('w-full max-w-4xl')

    # Inyectamos el diseño del botón Eliminar en la columna "acciones"
    tabla.add_slot('body-cell-acciones', '''
        <q-td :props="props">
            <q-btn label="Editar" color="blue" size="sm" dense @click="$parent.$emit('editar_libro', props.row)" />
            <q-btn label="Eliminar" color="red" size="sm" dense @click="$parent.$emit('borrar_libro', props.row)" />
        </q-td>
    ''')

    # Función que se dispara al apretar "Eliminar"
    def manejar_borrado(e):
        id_libro = e.args['id']
        repositorio.eliminar_libro(id_libro)
        ui.notify('Libro eliminado correctamente', color='info')
        actualizar_tabla() # Refresco automático de la vista

    def manejar_edicion(e):
        fila = e.args
        estado_edicion['id'] = int(fila['id'])

        edit_titulo.value = fila['titulo']
        edit_autor.value = fila['autor']
        edit_genero.value = fila['genero']
        edit_precio.value = float(fila['precio']) if fila['precio'] else None
        edit_anio.value = int(fila['anio_publicacion']) if fila['anio_publicacion'] else None
        edit_editorial.value = fila['editorial']

        dialogo_edicion.open()

    tabla.on('borrar_libro', manejar_borrado)
    tabla.on('editar_libro', manejar_edicion)

    # Función para cargar los datos de SQLite a la tabla
    def actualizar_tabla():
        libros_db = repositorio.obtener_libros()
        filas = []
        for libro in libros_db:
            filas.append({
                'id': str(libro[0]),
                'titulo': str(libro[1]),
                'autor': str(libro[2]),
                'genero': str(libro[3]) if libro[3] else "",
                'precio': str(libro[4]) if libro[4] else "",
                'anio_publicacion': str(libro[5]) if libro[5] else "",
                'editorial': str(libro[6]) if libro[6] else ""
            })
        
        # Usamos asignación directa para evitar el RecursionError
        tabla.rows = filas
        tabla.update()

    # Ejecutamos la carga inicial al abrir la página
    actualizar_tabla()