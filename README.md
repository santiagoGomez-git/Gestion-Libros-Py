# CRUD de Gestion de Libros

Este proyecto es una aplicacion web en Python para la gestion de un catalogo de libros. Fue desarrollado utilizando **NiceGUI** para la interfaz grafica y **SQLite** para la persistencia de datos.

## Estructura del proyecto
El codigo sigue una estricta separacion de responsabilidades en archivos independientes:
* `main.py`: Punto de entrada que inicializa la aplicacion.
* `interfaz.py` : Contiene toda la logica visual, formularios y tablas (Frontend)
* `repositorio.py` : Concentra las consultas SQL y conexion a la base de datos (Backend/Persistencia).

## Requisitos Previos
* Python 3 instalado en tu sistema.
* `uv` (o `pip`) para la gestion de entornos virtuales y dependencias.

## Instrucciones de Instalacion y Ejecucion

## 1. Clonar o descargar el repositorio

```bash
git clone <TU_ENLACE_DE_GITHUB_ACA>
cd Gestion_Libros
```
## 2. Crear y activar el entorno virtual

Crear el entorno:
```bash
uv venv
```
Activar el entorno (Windows):
```bash
.venv\Scripts\activate
```
Activar el entorno (Linux/macOS):
```bash
source .venv/bin/activate
```
## 3. Instalar las dependencias

Instalar las librerias especificadas en el archivo de requerimientos:
```bash
uv pip install -r requirements.txt
```
## 4. Ejecutar la aplicación

Para iniciar el servidor, ejecuta el siguiente comando en la terminal:
```bash
python main.py
```
La aplicación web se abrirá automáticamente en tu navegador predeterminado (por lo general en http://localhost:8080
