# 📖 Project Overview

When you run `dj-scaffold create`, the CLI goes to work setting up a complete, production-ready Django environment for you. 

Here is what happens under the hood:
1. **Django Project Initialization**: It runs `django-admin startproject` to lay down the base files.
2. **Configuration Injection**: It overwrites the default `settings.py` and `urls.py` with enhanced versions that include middleware for security (CORS & CSP) and database configuration.
3. **Environment Files**: A `.env.example` is generated and copied to `.env` so you can securely store your secrets.
4. **Dockerization**: A `Dockerfile`, `docker-compose.yml`, and `entrypoint.sh` are created tailored to your database choice.
5. **Example App Generation**: Once the project is created, a sample `example` app is automatically generated and wired into your project settings and URLs. It provides a working template of a model and an API endpoint so you can start mimicking the setup right away!

### Middleware Auto-Configured
- **CORS**: (`django-cors-headers`) Configured to allow all origins in development.
- **CSP**: (`django-csp`) Sets strict, secure content-security policies by default.
