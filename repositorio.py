import sqlite3

DB_NAME = 'libros.db'

def conectar():
    """Establece y devuelve la conexion a la base de datos SQLite."""
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    """Crea la tabla 'libros' si no existe, respetando los campos del TP."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        genero TEXT,
        precio DECIMAL,
        anio_publicacion INTEGER,
        editorial TEXT
    )
''')
    conexion.commit()
    conexion.close()

def crear_libro(titulo:str, autor:str, genero:str, precio:float, anio_publicacion:int, editorial:str):
    """Inserta un nuevo registro en la base de datos"""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('''
        INSERT INTO libros (titulo, autor, genero, precio, anio_publicacion, editorial)
        VALUES (?,?,?,?,?,?)
    ''', (titulo, autor, genero, precio, anio_publicacion, editorial))

    conexion.commit()
    conexion.close()

def obtener_libros():
    """Lee y devuelve todos los libros de la base de datos"""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()

    conexion.close()
    return libros

def actualizar_libro(id_libro:int, titulo:str, autor:str, genero:str, precio:float, anio_publicacion:int, editorial:str):
    """Actualiza los datos de un libro existente usando su ID."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('''
        UPDATE libros
        SET titulo = ?, autor = ?, genero = ?, precio = ?, anio_publicacion = ?, editorial = ?
        WHERE id = ?
''', (titulo, autor, genero, precio, anio_publicacion, editorial, id_libro))

    conexion.commit()
    conexion.close()

def eliminar_libro(id_libro:int):
    """Elimina un libro de la base de datos usando un ID."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('DELETE FROM libros WHERE id = ?', (id_libro,))

    conexion.commit()
    conexion.close()