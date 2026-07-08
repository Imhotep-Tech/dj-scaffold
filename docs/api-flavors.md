# 📡 API Framework Flavors

When scaffolding a project, you can choose how you want to build your APIs. `dj-scaffold` will pre-configure your selection automatically so you don't have to fiddle with settings.

### 1. DRF + Spectacular
**Django REST Framework (DRF)** is the industry standard for building robust APIs in Django.
- **What it installs**: `djangorestframework`, `drf-spectacular`, `djangorestframework-simplejwt`.
- **What it does**: 
  - Sets up DRF with JSON Web Token (JWT) authentication enabled by default.
  - Automatically wires `api/token/` and `api/token/refresh/` endpoints in your main `urls.py`.
  - Configures `drf-spectacular` to automatically generate an OpenAPI 3.0 schema and a gorgeous Swagger UI available at `/api/docs/`.
  - Generates the `example` app using DRF `APIView` and `Response`.

### 2. Django Ninja
**Django Ninja** is a fast, modern, Pydantic-based API framework for Django, highly inspired by FastAPI.
- **What it installs**: `django-ninja`.
- **What it does**: 
  - Creates a central `NinjaAPI` instance in your main `urls.py`.
  - Mounts the Ninja API instance to the `/api/` route.
  - Generates the `example` app using Ninja `@router` decorators and automatically registers the router to your main API instance.

### 3. Standard Django
If you prefer not to use a heavy API framework, this option gives you vanilla Django.
- **What it does**: 
  - Keeps your dependencies extremely light.
  - Generates the `example` app using standard Django `JsonResponse` and simple view functions.
