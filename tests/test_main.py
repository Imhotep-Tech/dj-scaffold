import os
from typer.testing import CliRunner
from dj_scaffold.main import app

runner = CliRunner()

def test_project_generation_workflow(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["create", "sandbox_project", "--db", "sqlite", "--flavor", "standard_django"])
    assert result.exit_code == 0
    assert (tmp_path / "sandbox_project").exists()
    assert (tmp_path / "sandbox_project" / "settings.py").exists()
    assert (tmp_path / "requirements.txt").exists()

def test_app_generation_workflow(tmp_path, mocker):
    os.chdir(tmp_path)
    mocker.patch("pathlib.Path.exists", return_value=True)
    mock_sub = mocker.patch("subprocess.run")

    result = runner.invoke(app, ["startapp", "billing_service", "--architecture", "service_layer_pattern"])
    assert result.exit_code == 0
    mock_sub.assert_called_once()

def test_startapp_without_manage_py(tmp_path):
    os.chdir(tmp_path)
    # No manage.py exists in tmp_path, should fail validation and return exit_code 1
    result = runner.invoke(app, ["startapp", "billing_service", "--architecture", "service_layer_pattern"])
    assert result.exit_code == 1

def test_create_malformed_project_name(tmp_path):
    os.chdir(tmp_path)
    # Invalid name (has spaces and special characters), django-admin fails and returns exit_code 1
    result = runner.invoke(app, ["create", "my project!", "--db", "sqlite", "--flavor", "standard_django"])
    assert result.exit_code == 1

