# Hotel Paradise

## Sistema de Reservación de Hotel

Proyecto Integrador de Aprendizaje (PIA) de la materia
Fundamentos de Desarrollo Web.

Aplicación web desarrollada con Django para administrar
habitaciones, clientes y reservaciones de un hotel.

## Tecnologías utilizadas

- Python 3.13
- Django 6.1.3
- SQLite
- HTML
- Bootstrap 5
- Pillow

## Funcionalidades

- Inicio y cierre de sesión.
- Administración de habitaciones (CRUD).
- Administración de clientes (CRUD).
- Registro, edición y cancelación de reservaciones.
- Validación de fechas y disponibilidad.
- Prevención de reservaciones superpuestas.
- Búsquedas de habitaciones, clientes y reservaciones.
- Dashboard con estadísticas generales.
- Control de acceso mediante autenticación.

## Requisitos previos

- Python instalado.
- Git (opcional para descargar el proyecto).
- Conexión a Internet para cargar Bootstrap mediante CDN.

## Instalación en Windows

### 1. Descargar el proyecto

Descargar el repositorio desde GitHub y extraerlo.

Abrir PowerShell dentro de la carpeta que contiene manage.py.

### 2. Crear el entorno virtual

```powershell
py -m venv .venv
```

### 3. Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 5. Configurar variables de entorno

```powershell
$env:DJANGO_SECRET_KEY = "CAMBIAR-POR-UNA-CLAVE-PRIVADA"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
```

### 6. Preparar la base de datos

```powershell
python manage.py migrate
```

### 7. Iniciar el servidor

```powershell
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

## Pruebas automáticas

Para ejecutar las pruebas del módulo de reservaciones:

```powershell
python manage.py test reservaciones
```

## Base de datos

El proyecto utiliza SQLite.

El archivo db.sqlite3 no se incluye en GitHub.
Se genera automáticamente al ejecutar las migraciones.

## Acceso al sistema

Para utilizar Hotel Paradise es necesario iniciar sesión.

Después de ejecutar las migraciones, crear un usuario
de recepción con el siguiente comando:

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.get_or_create(username='recepcion')"
```

Después, establecer su contraseña:

```powershell
python manage.py changepassword recepcion
```

Django solicitará escribir y confirmar la contraseña.

Finalmente, ejecutar:

```powershell
python manage.py runserver
```

Abrir:

http://127.0.0.1:8000/usuarios/login/

Iniciar sesión con:

- Usuario: recepcion
- Contraseña: la establecida durante la configuración.

Esta cuenta es un usuario normal de Django y no necesita
permisos de superusuario para utilizar Hotel Paradise.

## Datos de demostración

Después de crear la base de datos y ejecutar las migraciones,
se pueden cargar datos ficticios con:

```powershell
python manage.py cargar_demo
```

Este comando crea habitaciones, clientes y reservaciones
de ejemplo para probar las funcionalidades de Hotel Paradise.

Se recomienda ejecutarlo en una base de datos nueva,
antes de registrar información manualmente.

## Proyecto académico

Universidad Autónoma de Nuevo León

Facultad de Contaduría Pública y Administración

Fundamentos de Desarrollo Web