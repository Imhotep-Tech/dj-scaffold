# 🗄️ Database Options

During the project creation menu, `dj-scaffold` asks you to select a Database Engine. Here is what each option does behind the scenes:

### 1. PostgreSQL
- Installs the `psycopg2-binary` driver via `requirements.txt`.
- Generates a `docker-compose.yml` file that spins up a `postgres:16-alpine` service.
- Configures `settings.py` to connect to the Docker container automatically via environment variables.
- Waits for the PostgreSQL port to be available before running migrations in Docker.

### 2. MySQL
- Installs the `mysqlclient` driver via `requirements.txt`.
- Generates a `docker-compose.yml` file that spins up a robust `mysql` service.
- Preconfigures the database connection in `settings.py` for MySQL standards.

### 3. SQLite
- The standard, lightweight default for Django.
- No extra database container is spun up.
- Generates a lightweight `docker-compose.yml` that only spins up the Django `web` service.
- The SQLite database is stored locally and mounted via volume, making it ideal for quick prototyping or small applications.
