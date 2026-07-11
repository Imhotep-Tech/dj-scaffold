import os
import shutil
from pathlib import Path
from dj_scaffold.generators.project_generator import generate_project
from dj_scaffold.generators.app_generator import generate_app, wire_app

def test_generate_project_postgres_drf(tmp_path):
    # Set up directory
    os.chdir(tmp_path)
    
    # Run project generator
    generate_project("testproj", "postgresql", "drf_spectacular")
    
    # Assert core files exist
    assert Path("manage.py").exists()
    assert Path("testproj/settings.py").exists()
    assert Path("testproj/urls.py").exists()
    assert Path("Dockerfile").exists()
    assert Path(".env").exists()
    assert Path("requirements.txt").exists()
    assert Path("docker-compose.yml").exists()
    assert Path("entrypoint.sh").exists()
    
    # Check settings.py contents
    settings_content = Path("testproj/settings.py").read_text()
    assert "django.db.backends.postgresql" in settings_content
    assert "rest_framework" in settings_content
    assert "drf_spectacular" in settings_content
    
    # Check requirements.txt contents
    reqs_content = Path("requirements.txt").read_text()
    assert "psycopg2-binary" in reqs_content
    assert "djangorestframework-simplejwt" in reqs_content

def test_generate_project_sqlite_ninja(tmp_path):
    os.chdir(tmp_path)
    
    generate_project("testproj", "sqlite", "django_ninja")
    
    assert Path("manage.py").exists()
    settings_content = Path("testproj/settings.py").read_text()
    assert "django.db.backends.sqlite3" in settings_content
    
    reqs_content = Path("requirements.txt").read_text()
    assert "django-ninja" in reqs_content

def test_wire_app(tmp_path):
    os.chdir(tmp_path)
    
    # Write a mock manage.py that defines the DJANGO_SETTINGS_MODULE
    manage_py = Path("manage.py")
    manage_py.write_text("os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproj.settings')")
    
    # Write a mock settings.py
    project_dir = Path("testproj")
    project_dir.mkdir(parents=True, exist_ok=True)
    settings_py = project_dir / "settings.py"
    settings_py.write_text("INSTALLED_APPS = [\n    'django.contrib.admin',\n]")
    
    # Write a mock urls.py
    urls_py = project_dir / "urls.py"
    urls_py.write_text("urlpatterns = [\n    path('admin/', admin.site.urls),\n]")
    
    # Call wire_app
    wire_app("billing")
    
    # Verify settings.py was updated
    settings_content = settings_py.read_text()
    assert "'billing'" in settings_content
    assert "INSTALLED_APPS = [\n    'billing'," in settings_content
    
    # Verify urls.py was updated
    urls_content = urls_py.read_text()
    assert "path('billing/', include('billing.urls'))" in urls_content

def test_generate_app_service(tmp_path):
    os.chdir(tmp_path)
    
    # Set up dummy project structure
    manage_py = Path("manage.py")
    manage_py_content = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproj.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""
    manage_py.write_text(manage_py_content)
    
    project_dir = Path("testproj")
    project_dir.mkdir(parents=True, exist_ok=True)
    settings_py = project_dir / "settings.py"
    settings_py.write_text("INSTALLED_APPS = [\n]")
    urls_py = project_dir / "urls.py"
    urls_py.write_text("from django.urls import path, include\nurlpatterns = [\n    path('admin/', admin.site.urls),\n]")
    
    # Generate service app
    generate_app("billing", is_service=True)
    
    # Verify app files exist
    assert Path("billing").exists()
    assert Path("billing/apis.py").exists()
    assert Path("billing/selectors.py").exists()
    assert Path("billing/services.py").exists()
    assert Path("billing/urls.py").exists()
    assert Path("billing/apps.py").exists()
    
    # Verify autowiring
    assert "'billing'" in settings_py.read_text()
    assert "billing.urls" in urls_py.read_text()
