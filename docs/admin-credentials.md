# 🔑 Default Admin & Credentials

One of the biggest pain points of starting a new Django project is running migrations and setting up a superuser. `dj-scaffold` automates this entirely!

### The Entrypoint Script
When you launch your project using Docker (`docker compose up -d --build`), the `entrypoint.sh` script automatically:
1. Waits for your database to be ready.
2. Applies all pending Django database migrations (`python manage.py migrate`).
3. Checks if a superuser exists, and if not, creates one using environment variables.

### Default Credentials
By default, the `.env` file generated in your project root contains these credentials:
```ini
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

You can log in to the Django Admin panel (`http://localhost:8000/admin/`) immediately using **`admin`** and **`adminpassword`**.

> **Important**: Always change these credentials in your `.env` file before deploying your application to production!
