# dj-scaffold 🚀

A modern, interactive scaffolding CLI for Django projects, inspired by frontend tools like `create-next-app`. It helps developers set up containerized, production-ready Django applications and enforces a clean **Service Layer Architecture** for modular, testable django applications.

---

## Features

- ✨ **Interactive Prompts**: Quick setup via terminal menus using arrow keys.
- 🐳 **Dockerized by Default**: Generate production-ready `Dockerfile`, `.env` setups, and `docker-compose.yml` for PostgreSQL or MySQL.
- 🛠️ **API Flavors**: Choose from **Standard Django**, **Django REST Framework + Spectacular** (OpenAPI 3.0), or **Django Ninja**.
- 🏗️ **Service Layer Architecture**: Scaffolding for app structure segregating HTTP API route handlers (`apis.py`), Business Logic mutations (`services.py`), Database Queries (`selectors.py`), and Models (`models.py`).

---

## Installation

You can install the package locally in edit/development mode:

```bash
pip install -e .
```

---

## Usage

### 1. Creating a New Django Project

To create a new project:

```bash
dj-scaffold create [project_name]
```

If the project name is omitted, you will be prompted to enter one. The interactive shell will then guide you through selecting the database and API framework.

#### Commands run under the hood:
1. Standard `django-admin startproject` setup.
2. Custom settings/URLs rendering via Jinja templates to suit your database/flavor choices.
3. Creation of `.env.example`, `.gitignore`, `Dockerfile`, and `docker-compose.yml`.

### 2. Creating a New Service App

To create a new app:

```bash
dj-scaffold startapp [app_name]
```

If the app name is omitted, you will be prompted. You will then select whether you want a **Standard Django** app or a **Service Layer Pattern** app.

Under the Service Layer selection, the following file structure is created:
```text
your_app/
├── __init__.py
├── apps.py
├── models.py
├── apis.py
├── services.py
├── selectors.py
└── urls.py
```

---

## Architecture: Why the Service Layer Pattern?

Standard Django often leads to bloated model methods (Fat Models) or complex views (Fat Views). The Service Layer Pattern enforces separation of concerns:

1. **Selectors** (`selectors.py`): Contains pure database query functions. They return QuerySets or dictionaries/objects and do not mutate state.
2. **Services** (`services.py`): Contains business logic and mutators (creating, updating, deleting database records). Wrapped in `@transaction.atomic` to ensure transactional integrity.
3. **APIs** (`apis.py` / `views.py`): Translates requests, triggers services or selectors, and serializes responses. Keep them light.
4. **Models** (`models.py`): Pure schema definition and DB relationships, minimal or zero business logic.
