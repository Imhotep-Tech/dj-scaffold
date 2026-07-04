# dj-scaffold

[![CI Pipeline](https://github.com/Imhotep-Tech/dj-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/Imhotep-Tech/dj-scaffold/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/dj-scaffold-imhotep.svg)](https://pypi.org/project/dj-scaffold-imhotep/)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-scaffold-imhotep.svg)](https://pypi.org/project/dj-scaffold-imhotep/)
[![License](https://img.shields.io/github/license/Imhotep-Tech/dj-scaffold.svg)](https://github.com/Imhotep-Tech/dj-scaffold/blob/main/LICENSE)

A modern, interactive scaffolding CLI for Django projects, inspired by frontend tools like `create-next-app`. It helps developers set up containerized, production-ready Django applications and enforces a clean **Service Layer Architecture** for modular, testable django applications.

---

## Features

- ✨ **Interactive Prompts**: Quick setup via terminal menus using arrow keys.
- 🐳 **Dockerized & Auto-Provisioned**: Generate production-ready `Dockerfile`, `.env` setups, and `docker-compose.yml`. Executes database migrations and provisions a superuser automatically on startup.
- 🛡️ **Secure by Default**: Configures CORS (`django-cors-headers`) and Content Security Policy (`django-csp`) middleware out-of-the-box.
- 🔑 **Simple JWT Integration**: Auto-configures token-based authentication (`djangorestframework-simplejwt`) and endpoint routes if an API backend is selected.
- 🛠️ **API Flavors**: Choose from **Standard Django**, **Django REST Framework + Spectacular** (OpenAPI 3.0), or **Django Ninja**.
- 🏗️ **Service Layer Architecture**: Scaffolding for app structure segregating HTTP API route handlers (`apis.py`), Business Logic mutations (`services.py`), Database Queries (`selectors.py`), and Models (`models.py`).

---

## Installation

### From PyPI
You can install `dj-scaffold` directly from PyPI:

```bash
pip install dj-scaffold-imhotep
```

### For Local Development
To set up the CLI tool for local development:
1. Clone this repository:
   ```bash
   git clone https://github.com/Imhotep-Tech/dj-scaffold.git
   cd dj-scaffold
   ```
2. Install the package in editable mode with development dependencies:
   ```bash
   pip install -e .[dev]
   ```

---

## CLI Usage

Run `dj-scaffold` in your terminal with no flags to open the interactive wizard, or use the subcommands directly.

### 1. Interactive Menu
To open the interactive prompt wizard:
```bash
dj-scaffold
```
Use the arrow keys to move between choices and press **Enter** to confirm.

### 2. Creating a New Django Project
To initiate a new Django project:
```bash
dj-scaffold create
```
The CLI will guide you through:
- **Project Name**: Enter the name of your new Django project.
- **Database Engine**: Choose between **PostgreSQL**, **MySQL**, or **SQLite**.
- **API Framework Flavor**: Choose between **Django Ninja**, **DRF + Spectacular**, or **Standard Django**.

---

## Generated Project Configuration

When you scaffold a new project, `dj-scaffold` sets up the following environments:

### 1. Docker & Auto-Superuser Setup
The generated project uses a custom `entrypoint.sh` script to run migrations and create a superuser automatically when you run `docker compose up`. 

Configure the superuser credentials in your generated `.env` file:
```ini
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### 2. Security Middleware (CORS & CSP)
Every project has CORS and CSP configured by default in its generated `settings.py`:
- **CORS**: Powered by `django-cors-headers`, pre-configured with `CORS_ALLOW_ALL_ORIGINS = True` for easy API testing during development.
- **CSP**: Powered by `django-csp`, setting secure default script, style, and self-origin policies:
  ```python
  CSP_DEFAULT_SRC = ("'self'",)
  CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
  CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
  ```

### 3. API Authentication (Simple JWT)
If the **DRF + Spectacular** flavor is chosen, token-based authentication is preconfigured.
- **Settings**: Simple JWT config is added to `REST_FRAMEWORK` and settings:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework_simplejwt.authentication.JWTAuthentication',
      ],
      'DEFAULT_PERMISSION_CLASSES': [
          'rest_framework.permissions.IsAuthenticated',
      ],
  }
  ```
- **Endpoints**: The following routes are registered in your main `urls.py`:
  - `/api/token/` – Exchange username/password for access/refresh tokens.
  - `/api/token/refresh/` – Exchange a refresh token for a new access token.

---

## Scaffolding a New App (Service Layer Layout)

To create a new app inside an existing project, run this command from the project root directory (where `manage.py` resides):
```bash
dj-scaffold startapp
```
You will be prompted for:
- **App Name**: Enter the name of the app.
- **Architecture Layout**: Choose between **Service Layer Pattern** (recommended) or **Standard Django Layout**.

### Folder Structure for Service Layer Apps:
```text
your_app/
├── __init__.py
├── apps.py          # Django app configuration
├── models.py        # Database models & relationships
├── apis.py          # API ViewSets, Ninja Routers, or standard views
├── services.py      # Business logic mutators (Write actions)
├── selectors.py     # Pure database query helpers (Read actions)
└── urls.py          # App-specific URL patterns
```

---

## Architecture: Why the Service Layer Pattern?

Standard Django applications can easily lead to bloated model methods ("Fat Models") or complex views ("Fat Views"). The Service Layer Pattern enforces a strict separation of concerns:

```text
Request ──> APIs (apis.py) ──> Services (services.py) [Mutations] ──> Models (models.py)
              │
              └───────────────> Selectors (selectors.py) [Queries] ──> Models (models.py)
```

1. **APIs** (`apis.py`): Translates incoming HTTP requests, triggers services or selectors, handles request validation, and serializes responses. Keeps the HTTP layer lightweight.
2. **Services** (`services.py`): Contains your core business logic and database mutators (creating, updating, deleting database records). Wrapped in `@transaction.atomic` to ensure transactional integrity.
3. **Selectors** (`selectors.py`): Contains pure database query functions. They read and return QuerySets or dictionaries/objects and do not mutate state.
4. **Models** (`models.py`): Pure schema definitions, database relationships, and constraints. Contains minimal or zero business logic.

---

## Local Development & Testing

We use `pytest` for unit testing the CLI scaffolding functionalities.

### Running Tests
To execute the tests locally:
```bash
pytest -v
```

### CI/CD Integration
Our GitHub Actions integration tests the package on Python versions `3.10`, `3.11`, and `3.12`. It builds, tests, and publishes the package to PyPI upon successful releases on the `main` branch.
