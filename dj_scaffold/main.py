import typer
import questionary
from rich.console import Console
from dj_scaffold.generators.project_generator import generate_project
from dj_scaffold.generators.app_generator import generate_app

app = typer.Typer(help="Modern Interactive Django Scaffolder")
console = Console()


def _normalize_choice(value: str) -> str:
    return value.lower().replace(" + ", "_").replace(" ", "_")


def _prompt_text(message: str, error_message: str) -> str:
    value = questionary.text(message).ask()
    if not value:
        console.print(f"[red]{error_message}[/red]")
        raise typer.Exit(1)
    return value


def _prompt_select(message: str, choices: list[str]) -> str:
    value = questionary.select(message, choices=choices).ask()
    if not value:
        raise typer.Exit(1)
    return value


@app.callback(invoke_without_command=True)
def prompt_shell(ctx: typer.Context):
    if ctx.invoked_subcommand:
        return

    action = _prompt_select(
        "What would you like to create?",
        choices=["New Django project", "New Django app"],
    )

    if action == "New Django project":
        create()
        return

    if action == "New Django app":
        startapp()
        return

@app.command()
def create():
    """
    Creates a new customized, Dockerized Django project.
    """
    project_name = _prompt_text("Enter project name:", "Error: Project name cannot be empty.")
    db = _prompt_select(
        "Select Database Engine:",
        choices=["PostgreSQL", "MySQL", "SQLite"],
    )
    flavor = _prompt_select(
        "Select API Framework Flavor:",
        choices=["Django Ninja", "DRF + Spectacular", "Standard Django"],
    )

    db_clean = _normalize_choice(db)
    flavor_clean = _normalize_choice(flavor)

    generate_project(project_name, db_clean, flavor_clean)

@app.command()
def startapp():
    """
    Creates a new Django application config.
    """
    app_name = _prompt_text("Enter app name:", "Error: App name cannot be empty.")
    architecture = _prompt_select(
        "Select App Architecture Layout:",
        choices=["Service Layer Pattern", "Standard Django Layout"],
    )

    is_service = "service" in _normalize_choice(architecture)

    generate_app(app_name, is_service)

def main():
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user. Exiting...[/yellow]")
        raise typer.Exit(0)

if __name__ == "__main__":
    main()
