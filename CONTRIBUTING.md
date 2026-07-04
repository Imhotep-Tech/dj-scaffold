# Contributing to dj-scaffold

Thank you for your interest in contributing to `dj-scaffold`! We welcome all contributions, whether they are bug fixes, new features, templates, or documentation improvements.

This guide is designed to help new contributors get up and running quickly and learn how to add new features to the CLI tool.

---

## Development Setup

To set up your local development environment:

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/YourUsername/dj-scaffold.git
   cd dj-scaffold
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the Package in Editable Mode**:
   Install the package along with development and testing dependencies:
   ```bash
   pip install -e .[dev]
   ```

4. **Verify the Installation**:
   Ensure you can run the CLI tool locally:
   ```bash
   dj-scaffold --help
   ```

---

## Codebase Architecture

To easily add new features, it helps to understand the folder structure:

```text
dj-scaffold/
├── dj_scaffold/
│   ├── main.py              # CLI Entrypoint (Typer subcommands & questionary prompts)
│   ├── generators/
│   │   ├── project_generator.py   # Renders templates to generate new Django projects
│   │   └── app_generator.py       # Renders templates to generate new Django apps
│   └── templates/           # Raw Jinja2 files used during scaffolding
│       ├── core/            # Templates for whole projects (.env, settings, entrypoints, etc.)
│       └── service_app/     # Templates for Service Layer apps (apis.py, services.py, etc.)
├── tests/
│   └── test_main.py         # Unit tests checking command execution and input flows
└── pyproject.toml           # Project metadata, script mappings, and dependencies
```

---

## How to Add New Features

### 1. Adding configuration options to generated projects
If you want to configure how base Django projects are generated (e.g., adding a new database engine or setting default configuration variables):

1. **Update settings templates**: Modify `dj_scaffold/templates/core/settings.py.jinja` or `urls.py.jinja`. You can use Jinja statements based on the options, for example:
   ```django
   {% if db == "postgresql" %}
   # PostgreSQL configuration here
   {% endif %}
   ```
2. **Update the project generator**: Open `dj_scaffold/generators/project_generator.py` and modify `generate_project()`. If your feature needs new packages, append them to the `reqs` list so they get written to `requirements.txt`:
   ```python
   if some_feature_enabled:
       reqs.append("my-package>=1.0.0\n")
   ```

### 2. Adding a new CLI prompt or command option
If you want to add a prompt or option in the terminal wizard:

1. **Add the prompts**: Update `dj_scaffold/main.py`. Find the relevant subcommand (e.g., `create()` or `startapp()`) and prompt the user using `questionary`:
   ```python
   my_choice = _prompt_select(
       "Choose an option:",
       choices=["Option A", "Option B"]
   )
   ```
2. **Forward choices to the generator**: Pass the value selected by the user to the generator function (e.g., `generate_project(..., my_choice)`).

### 3. Adding files to scaffold templates
If your feature introduces new default files (like a custom README template or CI configurations):

1. Put the template file in `dj_scaffold/templates/core/yourfile.jinja`.
2. In `dj_scaffold/generators/project_generator.py`, read and compile this template using Jinja's Environment, then write it to the output directory:
   ```python
   with open("yourfile.md", "w") as f:
       f.write(env.get_template("yourfile.jinja").render(context))
   ```

---

## Running and Writing Tests

We write unit tests to ensure that command parsing and prompt selection logic work as expected.

### Running existing tests:
```bash
pytest -v
```

### Adding a new test:
Add test cases in `tests/test_main.py`. We use `pytest-mock` to mock out `subprocess.run` or prompt behaviors to prevent writing files to your hard drive during test runs:
```python
def test_my_new_feature_prompt(tmp_path, mocker):
    os.chdir(tmp_path)
    generate_project_mock = mocker.patch("dj_scaffold.main.generate_project")
    _mock_questionary_text(mocker, "project_name")
    
    # Mock sequence: Database selection, API flavor, and your new prompt selection
    _mock_questionary_select_sequence(mocker, ["SQLite", "Standard Django", "Option A"])

    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    # Assert your new value was passed to the generator logic
    generate_project_mock.assert_called_once_with("project_name", "sqlite", "standard_django", "option_a")
```

---

## Submitting Pull Requests

1. Create a descriptive branch name: `git checkout -b feat/add-my-feature` or `git checkout -b fix/correct-my-bug`.
2. Implement your changes following standard Python styling guidelines.
3. Ensure all tests pass: `pytest -v`.
4. Commit your changes with clear, structured messages:
   ```bash
   git commit -m "feat: Add support for [new feature name]"
   ```
5. Push to your fork and submit a Pull Request to the main branch!
