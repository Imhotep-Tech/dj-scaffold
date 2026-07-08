import os
import shutil
import subprocess
import typer
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel

console = Console()

def generate_project(name: str, db: str, flavor: str):
    console.print(f"[cyan]Initializing base Django project '{name}' via django-admin...[/cyan]")
    try:
        subprocess.run(["django-admin", "startproject", name, "."], check=True)
    except Exception as e:
        console.print(f"[red]Failed to run django-admin. Ensure Django is installed. Error: {e}[/red]")
        raise typer.Exit(1)

    # Evacuate default files to overwrite with templates
    config_dir = Path(name)
    if (config_dir / "settings.py").exists():
        os.remove(config_dir / "settings.py")
    if (config_dir / "urls.py").exists():
        os.remove(config_dir / "urls.py")

    template_base = Path(__file__).parent.parent / "templates" / "core"
    env = Environment(loader=FileSystemLoader(str(template_base)))

    context = {"project_name": name, "db": db, "flavor": flavor}

    # Write core configurations
    with open(config_dir / "settings.py", "w") as f:
        f.write(env.get_template("settings.py.jinja").render(context))
        
    with open(config_dir / "urls.py", "w") as f:
        f.write(env.get_template("urls.py.jinja").render(context))

    with open(".env.example", "w") as f:
        f.write(env.get_template(".env.example.jinja").render(context))
    shutil.copy(".env.example", ".env")

    with open(".gitignore", "w") as f:
        f.write(env.get_template(".gitignore.jinja").render(context))

    with open("Dockerfile", "w") as f:
        f.write(env.get_template("Dockerfile.jinja").render(context))

    with open("entrypoint.sh", "w") as f:
        f.write(env.get_template("entrypoint.sh.jinja").render(context))

    # Construct clean requirements dynamic manifest
    reqs = [
        "django>=4.2.0\n",
        "python-dotenv>=1.0.0\n",
        "django-cors-headers>=4.4.0\n",
        "django-csp>=4.0\n",
    ]
    if "postgres" in db:
        reqs.append("psycopg2-binary>=2.9.0\n")
        shutil.copy(template_base / "docker-compose.postgres.yml.jinja", "docker-compose.yml")
    elif "mysql" in db:
        reqs.append("mysqlclient>=2.2.0\n")
        shutil.copy(template_base / "docker-compose.mysql.yml.jinja", "docker-compose.yml")
    else:
        shutil.copy(template_base / "docker-compose.sqlite.yml.jinja", "docker-compose.yml")

    if "ninja" in flavor:
        reqs.append("django-ninja>=1.1.0\n")
    elif "drf" in flavor:
        reqs.append("djangorestframework>=3.14.0\n")
        reqs.append("drf-spectacular>=0.26.0\n")
        reqs.append("djangorestframework-simplejwt>=5.5.1\n")

    with open("requirements.txt", "w") as f:
        f.writelines(reqs)

    console.print(Panel(
        f"[green]Successfully scaffolded {name}![/green]\n\n"
        f"Database: [bold]{db}[/bold]\n"
        f"API Style: [bold]{flavor}[/bold]\n\n"
        "To launch your workspace:\n"
        "1. [yellow]docker compose up -d --build[/yellow]\n"
        "2. [yellow]docker compose exec web python manage.py migrate[/yellow]",
        title="Scaffolding Complete"
    ))
