# ⌨️ CLI Commands Reference

`dj-scaffold` is designed to be interactive, but it also provides direct subcommands if you know exactly what you want to do.

## 1. The Interactive Wizard
```bash
dj-scaffold
```
If you run `dj-scaffold` with no arguments, it will launch the interactive terminal wizard. 
- You can use your **Up / Down arrow keys** to navigate the menus.
- Press **Enter** to select an option.
- It will automatically detect if you are inside an existing Django project and prompt you to create a new app, or if you are in a clean directory, it will prompt you to create a new project.

## 2. Create a New Project
```bash
dj-scaffold create
```
Use this command in an empty directory (or your projects folder) to scaffold a brand new Django project.
You will be asked to provide:
1. **Project Name**: The name of your root Django folder.
2. **Database Engine**: See [Database Options](database-options.md).
3. **API Flavor**: See [API Framework Flavors](api-flavors.md).

After running this, you can immediately `cd` into your project and run `docker compose up -d --build` to start it!

## 3. Create a New App
```bash
dj-scaffold startapp
```
**Important**: You must run this command from the root of your newly created Django project (the folder containing `manage.py`).

Use this command to add a new app to your project. You will be asked for:
1. **App Name**: The name of your new app (e.g., `users`, `blog`, `payments`).
2. **Architecture Layout**: See [Architecture Layouts](architecture-layout.md).

This command goes beyond Django's default `startapp`. It will automatically:
- Generate your chosen folder structure.
- Add the app to your `INSTALLED_APPS` in `settings.py`.
- Wire the app's `urls.py` into your main project's `urls.py`.
