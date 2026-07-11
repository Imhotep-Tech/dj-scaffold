# 🚀 dj-scaffold

[![CI Pipeline](https://github.com/Imhotep-Tech/dj-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/Imhotep-Tech/dj-scaffold/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/dj-scaffold-imhotep.svg)](https://pypi.org/project/dj-scaffold-imhotep/)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-scaffold-imhotep.svg)](https://pypi.org/project/dj-scaffold-imhotep/)

**dj-scaffold** is your ultimate CLI companion for rapidly scaffolding modern, production-ready Django applications. Inspired by tools like `create-next-app`, it gives you an interactive, zero-headache setup experience so you can start coding your business logic instantly.

## ✨ Why dj-scaffold?
- ⚡ **Interactive Setup**: Answer a few prompts and your project is ready.
- 🐳 **Docker-Ready**: Instantly containerized with zero setup required.
- 🛡️ **Secure & Configured**: CORS, CSP, and JWT auth out of the box.
- 🏗️ **Modern Architecture**: Enforces a scalable Service Layer pattern for your apps.

## 📦 Quick Start
Install the CLI globally or in your virtual environment:
```bash
pip install dj-scaffold-imhotep
```

### The Standard Workflow
1. **Create your project**:
   ```bash
   dj-scaffold create
   ```
   *(Answer the prompts to choose your database and API framework).*

2. **Start the server**:
   ```bash
   cd <your-project-name>
   docker compose up -d --build
   ```
   *(This automatically runs migrations and creates a superuser!)*

3. **Add a new app**:
   ```bash
   dj-scaffold startapp
   ```
   *(This wires a new app into your project using the Service Layer architecture).*

## 📚 Documentation
Dive deep into what `dj-scaffold` does under the hood. Check out our detailed documentation guides:

- ⌨️ [**CLI Commands Reference**](docs/cli-commands.md) – Full list of commands and interactive menus.
- 📖 [**Project Overview**](docs/overview.md) – Understand what gets generated and why.
- 🔑 [**Default Admin & Credentials**](docs/admin-credentials.md) – Learn how the auto-superuser works.
- 🗄️ [**Database Options**](docs/database-options.md) – Details on PostgreSQL, MySQL, and SQLite setups.
- 📡 [**API Framework Flavors**](docs/api-flavors.md) – Learn about DRF, Django Ninja, and Standard Django setups.
- 🏗️ [**Architecture Layouts**](docs/architecture-layout.md) – Deep dive into the Service Layer pattern vs Standard layout.

## 🛠️ Local Development & Testing

To set up the CLI tool for local development:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Imhotep-Tech/dj-scaffold.git
   cd dj-scaffold
   ```

2. **Install in editable mode with development dependencies**:
   ```bash
   pip install -e .[dev]
   ```

3. **Run the test suite**:
   ```bash
   pytest -v
   ```

---
*If you want to contribute to the project, please see our `CONTRIBUTING.md` file.*
