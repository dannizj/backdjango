# Django Blog API

REST API built with Python and Django for user management and articles, with JWT
authentication and a MySQL database.

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 6.1 |
| Authentication | JWT (PyJWT) |
| Serialization | Django REST Framework |
| Database | MySQL |

## Features

- User registration with server side validation and password hashing
- Login with JWT issuance and expiration
- Global JWT middleware protecting every route except login and register
- User profile lookup by id
- Article creation, paginated listing, detail, deletion and filtering by author
- Modular structure based on models, controllers, routes, validators and serializers

## Project structure

```
backdjango/
├── backdjango/            # project configuration
│   ├── settings.py        # apps, middleware, database
│   ├── urls.py            # root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── main/                  # application
│   ├── controllers/       # user.py, article.py
│   ├── routes/            # user/urls.py, article/urls.py
│   ├── migrations/
│   ├── models.py          # User, Article
│   ├── serializers.py     # UserSerializer, ArticleSerializer
│   ├── validator.py       # UserValidatorForm, ArticleValidatorForm
│   ├── helpers.py         # JWT generation
│   └── middlewares.py     # JWTAuthenticationMiddleware
├── manage.py
└── .gitignore
```

## Getting started

### Requirements

- Python 3.10 or newer (tested on 3.12)
- MySQL 8

### Installation

```bash
git clone <repository-url>
cd backdjango

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

pip install django pyjwt djangorestframework mysqlclient
```

### Database

Create the schema in MySQL:

```sql
CREATE DATABASE backdjango CHARACTER SET utf8mb4;
```

Set your credentials in `backdjango/settings.py`:

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

### Migrations and server

```bash
python manage.py migrate
python manage.py runserver
```

The API is served at `http://127.0.0.1:8000`.

## Authentication

`register` and `login` are public. Every other route requires the token returned
by the login endpoint:

```
Authorization: Bearer <token>
```

Tokens are signed with HS256 using the project `SECRET_KEY` and validated by
`main.middlewares.JWTAuthenticationMiddleware`. Requests with a missing, expired
or invalid token are rejected before reaching the view.

## Endpoints

### Users

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/user/register` | Create a new user | No |
| POST | `/api/user/login` | Authenticate and return the token | No |
| GET | `/api/user/profile/<id>` | User data by id | Yes |

### Articles

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/article/create` | Create an article | Yes |
| GET | `/api/article/articles/<page>` | Paginated listing, 5 per page | Yes |
| GET | `/api/article/article/<id>` | Article detail by id | Yes |
| DELETE | `/api/article/delete/<id>` | Delete an article by id | Yes |
| GET | `/api/article/articles-by-user/<userId>` | Articles written by a user | Yes |

The article author is taken from the token payload, not from the request body.

## Examples

### Register

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

### Create article

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

### Paginated listing

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

## Response format

Every endpoint answers JSON with a `status` field:

```json
{ "status": "success", "...": "..." }
{ "status": "error", "message": "..." }
```

## Notes

- `DEBUG = True` and `SECRET_KEY` live in `settings.py`. Move both to environment
  variables and set `DEBUG = False` before deploying.
- The JWT middleware currently applies to admin and static routes as well, add
  them to the excluded paths to reach `/admin/`.
- Error responses use HTTP 200 with `status: "error"`; mapped status codes are a
  pending improvement.
