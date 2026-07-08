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

    # Scaffold example app
    try:
        from dj_scaffold.generators.app_generator import generate_app
        generate_app("example", is_service=True)
        
        # Populate with simple example code
        with open("example/models.py", "w") as f:
            f.write("from django.db import models\n\nclass ExampleItem(models.Model):\n    name = models.CharField(max_length=255)\n    description = models.TextField(blank=True)\n    created_at = models.DateTimeField(auto_now_add=True)\n\n    def __str__(self):\n        return self.name\n")
            
        with open("example/apis.py", "w") as f:
            if "drf" in flavor:
                f.write("from rest_framework.views import APIView\nfrom rest_framework.response import Response\nfrom .models import ExampleItem\n\nclass ExampleItemApi(APIView):\n    def get(self, request):\n        items = ExampleItem.objects.all().values('id', 'name', 'description')\n        return Response(list(items))\n")
            elif "ninja" in flavor:
                f.write("from ninja import Router\nfrom .models import ExampleItem\n\nrouter = Router()\n\n@router.get('/items/')\ndef example_list(request):\n    items = list(ExampleItem.objects.all().values('id', 'name', 'description'))\n    return items\n")
            else:
                f.write("from django.http import JsonResponse\nfrom .models import ExampleItem\n\ndef example_list(request):\n    items = list(ExampleItem.objects.all().values('id', 'name', 'description'))\n    return JsonResponse(items, safe=False)\n")
                
        with open("example/urls.py", "w") as f:
            if "drf" in flavor:
                f.write("from django.urls import path\nfrom . import apis\n\nurlpatterns = [\n    path('items/', apis.ExampleItemApi.as_view()),\n]\n")
            elif "ninja" in flavor:
                f.write("from django.urls import path\n\nurlpatterns = [\n    # For Django Ninja, register the router in your main urls.py instead:\n    # api.add_router('/example/', 'example.apis.router')\n]\n")
                urls_path = Path(name) / "urls.py"
                if urls_path.exists():
                    urls_content = urls_path.read_text()
                    urls_content = urls_content.replace("# Add router inclusions dynamically here", "# Add router inclusions dynamically here\napi.add_router('/example/', 'example.apis.router')")
                    urls_path.write_text(urls_content)
            else:
                f.write("from django.urls import path\nfrom . import apis\n\nurlpatterns = [\n    path('items/', apis.example_list),\n]\n")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not scaffold example app: {e}[/yellow]")

    console.print(Panel(
        f"[green]Successfully scaffolded {name}![/green]\n\n"
        f"Database: [bold]{db}[/bold]\n"
        f"API Style: [bold]{flavor}[/bold]\n\n"
        "To launch your workspace:\n"
        "1. [yellow]docker compose up -d --build[/yellow]\n"
        "2. [yellow]docker compose exec web python manage.py migrate[/yellow]",
        title="Scaffolding Complete"
    ))
