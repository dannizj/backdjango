# Django Blog API

API REST construida con Python y Django para la gestión de usuarios y artículos,
con autenticación JWT y base de datos MySQL.

## Stack

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.12 |
| Framework | Django 6.1 |
| Autenticación | JWT (PyJWT) |
| Serialización | Django REST Framework |
| Base de datos | MySQL |

## Funcionalidades

- Registro de usuarios con validación en servidor y contraseña cifrada
- Login con emisión y caducidad del token JWT
- Middleware global de JWT que protege todas las rutas salvo login y registro
- Consulta del perfil de usuario por id
- Creación, listado paginado, detalle, borrado y filtrado por autor de artículos
- Estructura modular basada en modelos, controladores, rutas, validadores y serializers

## Estructura del proyecto

```
backdjango/
├── backdjango/            # configuración del proyecto
│   ├── settings.py        # apps, middleware, base de datos
│   ├── urls.py            # configuración de rutas raíz
│   ├── asgi.py
│   └── wsgi.py
├── main/                  # aplicación
│   ├── controllers/       # user.py, article.py
│   ├── routes/            # user/urls.py, article/urls.py
│   ├── migrations/
│   ├── models.py          # User, Article
│   ├── serializers.py     # UserSerializer, ArticleSerializer
│   ├── validator.py       # UserValidatorForm, ArticleValidatorForm
│   ├── helpers.py         # generación de JWT
│   └── middlewares.py     # JWTAuthenticationMiddleware
├── manage.py
└── .gitignore
```

## Puesta en marcha

### Requisitos

- Python 3.10 o superior (probado en 3.12)
- MySQL 8

### Instalación

```bash
git clone <repository-url>
cd backdjango

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

pip install django pyjwt djangorestframework mysqlclient
```

### Base de datos

Crea el esquema en MySQL:

```sql
CREATE DATABASE backdjango CHARACTER SET utf8mb4;
```

Configura tus credenciales en `backdjango/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backdjango',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

### Migraciones y servidor

```bash
python manage.py migrate
python manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000`.

## Autenticación

`register` y `login` son públicas. El resto de rutas requieren el token que
devuelve el login:

```
Authorization: Bearer <token>
```

Los tokens se firman con HS256 usando el `SECRET_KEY` del proyecto y los valida
`main.middlewares.JWTAuthenticationMiddleware`. Las peticiones sin token, con
token caducado o con firma inválida se rechazan antes de llegar a la vista.

## Endpoints

### Usuarios

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/user/register` | Crea un usuario | No |
| POST | `/api/user/login` | Autentica y devuelve el token | No |
| GET | `/api/user/profile/<id>` | Datos del usuario por id | Sí |

### Artículos

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/article/create` | Crea un artículo | Sí |
| GET | `/api/article/articles/<page>` | Listado paginado, 5 por página | Sí |
| GET | `/api/article/article/<id>` | Detalle del artículo por id | Sí |
| DELETE | `/api/article/delete/<id>` | Borra un artículo por id | Sí |
| GET | `/api/article/articles-by-user/<userId>` | Artículos de un autor | Sí |

El autor del artículo se toma del payload del token, no del cuerpo de la petición.

## Ejemplos

### Registro

```http
POST /api/user/register
Content-Type: application/json
```

```json
{
  "name": "Dani",
  "surname": "ZJ",
  "nick": "dannizj",
  "email": "dani@test.com",
  "bio": "backend developer",
  "password": "Test1234"
}
```

```json
{
  "status": "success",
  "message": "Validacion completada",
  "user": {
    "id": 1,
    "name": "Dani",
    "surname": "ZJ",
    "nick": "dannizj",
    "email": "dani@test.com",
    "bio": "backend developer",
    "created_at": "2026-11-17"
  }
}
```

### Login

```http
POST /api/user/login
Content-Type: application/json
```

```json
{
  "email": "dani@test.com",
  "password": "Test1234"
}
```

```json
{
  "status": "success",
  "accion": "Login",
  "data": {
    "status": "success",
    "user": { "id": 1, "nick": "dannizj" },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### Crear artículo

```http
POST /api/article/create
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{
  "title": "First article",
  "content": "Content of the first article"
}
```

### Listado paginado

```http
GET /api/article/articles/1
Authorization: Bearer <token>
```

```json
{
  "status": "success",
  "articles": [],
  "itemsPerPage": 5,
  "pages": 1,
  "totalArticles": 0
}
```

## Formato de respuesta

Todos los endpoints devuelven JSON con un campo `status`:

```json
{ "status": "success", "...": "..." }
{ "status": "error", "message": "..." }
```

## Notas

- `DEBUG = True` y `SECRET_KEY` están en `settings.py`. Pásalos a variables de
  entorno y pon `DEBUG = False` antes de desplegar.
- El middleware JWT también se aplica a `/admin/` y `/static/`; añádelos a las
  rutas excluidas para poder entrar al admin.
- Los errores se devuelven con HTTP 200 y `status: "error"`; mapear los códigos
  de estado reales queda pendiente.
