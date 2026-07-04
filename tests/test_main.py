import os
from typer.testing import CliRunner
from dj_scaffold.main import app

runner = CliRunner()


def _mock_questionary_text(mocker, value):
    return mocker.patch(
        "dj_scaffold.main.questionary.text",
        return_value=mocker.Mock(ask=mocker.Mock(return_value=value)),
    )


def _mock_questionary_select(mocker, value):
    return mocker.patch(
        "dj_scaffold.main.questionary.select",
        return_value=mocker.Mock(ask=mocker.Mock(return_value=value)),
    )


def _mock_questionary_select_sequence(mocker, values):
    return mocker.patch(
        "dj_scaffold.main.questionary.select",
        side_effect=[mocker.Mock(ask=mocker.Mock(return_value=value)) for value in values],
    )

def test_project_generation_workflow(tmp_path, mocker):
    os.chdir(tmp_path)
    generate_project_mock = mocker.patch("dj_scaffold.main.generate_project")
    _mock_questionary_text(mocker, "sandbox_project")
    _mock_questionary_select_sequence(mocker, ["PostgreSQL", "Standard Django"])

    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    generate_project_mock.assert_called_once_with("sandbox_project", "postgresql", "standard_django")

def test_app_generation_workflow(tmp_path, mocker):
    os.chdir(tmp_path)
    generate_app_mock = mocker.patch("dj_scaffold.main.generate_app")
    _mock_questionary_text(mocker, "billing_service")
    _mock_questionary_select(mocker, "Service Layer Pattern")

    result = runner.invoke(app, ["startapp"])
    assert result.exit_code == 0
    generate_app_mock.assert_called_once_with("billing_service", True)

def test_startapp_without_manage_py(tmp_path):
    os.chdir(tmp_path)
    # No manage.py exists in tmp_path, should fail validation and return exit_code 1
    result = runner.invoke(app, ["startapp"], input="billing_service\nService Layer Pattern\n")
    assert result.exit_code == 1

def test_create_malformed_project_name(tmp_path, mocker):
    os.chdir(tmp_path)
    mocker.patch("dj_scaffold.generators.project_generator.subprocess.run", side_effect=Exception("boom"))
    result = runner.invoke(app, ["create"], input="valid_but_fails\nSQLite\nStandard Django\n")
    assert result.exit_code == 1

