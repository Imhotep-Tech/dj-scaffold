import typer
import questionary
from rich.console import Console
from dj_scaffold.generators.project_generator import generate_project
from dj_scaffold.generators.app_generator import generate_app

app = typer.Typer(help="Modern Interactive Django Scaffolder")
console = Console()

@app.command()
def create(
    project_name: str = typer.Argument(None, help="Name of your Django project"),
    db: str = typer.Option(None, "--db", help="Database Engine (PostgreSQL, MySQL, SQLite)"),
    flavor: str = typer.Option(None, "--flavor", help="API Framework Flavor (Django Ninja, DRF + Spectacular, Standard Django)"),
):
    """
    Creates a new customized, Dockerized Django project.
    """
    if not project_name:
        project_name = questionary.text("Enter project name:").ask()
        if not project_name:
            console.print("[red]Error: Project name cannot be empty.[/red]")
            raise typer.Exit(1)

    if not db:
        db = questionary.select(
            "Select Database Engine:",
            choices=["PostgreSQL", "MySQL", "SQLite"]
        ).ask()
        if not db:
            raise typer.Exit(1)

    if not flavor:
        flavor = questionary.select(
            "Select API Framework Flavor:",
            choices=["Django Ninja", "DRF + Spectacular", "Standard Django"]
        ).ask()
        if not flavor:
            raise typer.Exit(1)

    db_clean = db.lower().replace(" + ", "_").replace(" ", "_")
    flavor_clean = flavor.lower().replace(" + ", "_").replace(" ", "_")

    generate_project(project_name, db_clean, flavor_clean)

@app.command()
def startapp(
    app_name: str = typer.Argument(None, help="Name of the Django app"),
    architecture: str = typer.Option(None, "--architecture", "-a", help="App Architecture Layout (Service Layer Pattern, Standard Django)"),
):
    """
    Creates a new Django application config.
    """
    if not app_name:
        app_name = questionary.text("Enter app name:").ask()
        if not app_name:
            console.print("[red]Error: App name cannot be empty.[/red]")
            raise typer.Exit(1)

    if not architecture:
        arch = questionary.select(
            "Select App Architecture Layout:",
            choices=["Service Layer Pattern", "Standard Django Layout"]
        ).ask()
        if not arch:
            raise typer.Exit(1)
        is_service = "Service" in arch
    else:
        is_service = "service" in architecture.lower()

    generate_app(app_name, is_service)

def main():
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user. Exiting...[/yellow]")
        raise typer.Exit(0)

if __name__ == "__main__":
    main()
