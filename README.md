# dj-scaffold

[![CI Pipeline](https://github.com/Imhotep-Tech/dj-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/Imhotep-Tech/dj-scaffold/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/dj-scaffold-imhotep.svg)](https://pypi.org/project/dj-scaffold-imhotep/)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-scaffold-imhotep.svg)](https://pypi.org/project/dj-scaffold-imhotep/)
[![License](https://img.shields.io/github/license/Imhotep-Tech/dj-scaffold.svg)](https://github.com/Imhotep-Tech/dj-scaffold/blob/main/LICENSE)

A modern, interactive scaffolding CLI for Django projects, inspired by frontend tools like `create-next-app`. It helps developers set up containerized, production-ready Django applications and enforces a clean **Service Layer Architecture** for modular, testable django applications.

---

## Features

- ✨ **Interactive Prompts**: Quick setup via terminal menus using arrow keys.
- 🐳 **Dockerized by Default**: Generate production-ready `Dockerfile`, `.env` setups, and `docker-compose.yml` for PostgreSQL or MySQL.
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

#### Under the Hood:
1. Runs `django-admin startproject` to generate the default base.
2. Replaces core configurations with optimized Django settings (`settings.py`, `urls.py`) using Jinja templates.
3. Generates Docker configuration files (`Dockerfile`, `docker-compose.yml` configured for your database).
4. Generates `.env.example` and automatically copies it to `.env`.
5. Creates a `requirements.txt` preloaded with the correct packages based on your database and API style choices.

### 3. Creating a New App (Scaffolding layout)
To create a new app inside an existing project, run this command from the project root directory (where `manage.py` resides):
```bash
dj-scaffold startapp
```
You will be prompted for:
- **App Name**: Enter the name of the app.
- **Architecture Layout**: Choose between **Service Layer Pattern** (recommended) or **Standard Django Layout**.

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

## Local Development & Testing

We use `pytest` for unit testing the CLI scaffolding functionalities.

### Running Tests
To execute the tests locally:
```bash
pytest -v
```

### CI/CD Integration
Our GitHub Actions integration tests the package on Python versions `3.10`, `3.11`, and `3.12`. It builds, tests, and publishes the package to PyPI upon successful releases on the `main` branch.
