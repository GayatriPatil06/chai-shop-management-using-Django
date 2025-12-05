# Chai Aur Django

A Django application for managing and reviewing different chai varieties, stores, and certificates.

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd chaiaurDjango
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
# Chai Aur Django

Chai Aur Django is a development/testing Django project for browsing, reviewing, and rating different chai (tea) varieties, stores, and related certificates. It includes admin management, image uploads, user reviews, favorites, and basic rating aggregation.

Topics/tags: django, django-app, chai, reviews, tailwind, python

---

**Recommended GitHub repository settings (you can set these when creating the repo):**
- **Visibility:** Public (so others can discover and contribute) — or choose Private if you prefer to keep the source private.
- **Who can see:** Everyone (for Public) / Only you and invited collaborators (for Private).
- **Who can commit:** Only you and collaborators you invite. Use branch protection rules for `main` if you want enforced reviews.

---

## Quickstart (development)

Follow these steps in a Windows `cmd.exe` shell.

1. Clone the repository and enter the folder:

```bat
git clone <repository-url>
cd chaiaurDjango
```

2. Create and activate a Python virtual environment (Windows):

```bat
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bat
pip install -r requirements.txt
```

4. Copy the example environment file and edit values:

```bat
copy .env.example .env
```

Edit `.env` and set `SECRET_KEY`, `DEBUG`, and database settings as needed.

5. Run migrations and create a superuser:

```bat
python manage.py migrate
python manage.py createsuperuser
```

6. Run the development server:

```bat
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. Admin site: `http://127.0.0.1:8000/admin/`.

---

## Project layout (high level)
- `chai/` — Django app: models, views, forms, templates
- `chaiaurDjango/` — Django project settings (wsgi/asgi, urls, settings)
- `templates/` — global templates (404/500/layout)
- `static/` and `static_src/` — CSS and assets
- `media/` — uploaded images (recommended to add to `.gitignore`)

---

## Key features implemented
- Browsing and searching chai varieties
- Chai detail pages with reviews and average rating
- Favorites (user-specific)
- Store pages for finding chai sellers
- Image upload with server-side compression (Pillow)
- Admin registrations for models
- Logging and simple rotating file handler

---

## Preparing for GitHub

Suggested repository settings to select when creating the repo on GitHub:
- **Initialize this repository with a README:** No (we are providing one locally). If the GitHub UI forces an initial commit, you can still `git pull --rebase` before pushing.
- **Add .gitignore:** No (we will add one locally). Use the `.gitignore` provided in this repo.
- **Add a license:** Choose **MIT License** if you want permissive reuse. A `LICENSE` file is included.

To create the repository locally and push to GitHub (replace `<OWNER>` and `<REPO>`):

```bat
git init
git add .
git commit -m "Initial commit: Chai Aur Django"
# Option A: Create remote manually on GitHub and then add the remote
git remote add origin https://github.com/<OWNER>/<REPO>.git
git branch -M main
git push -u origin main

# Option B: Use GitHub CLI (if installed):
# gh repo create <OWNER>/<REPO> --public --source=. --remote=origin --push
```

If GitHub reports a README exists remotely, run:

```bat
git pull --rebase origin main
git push origin main
```

---

## Development notes & next steps
- For production, set `DEBUG=False`, rotate the `SECRET_KEY`, configure `ALLOWED_HOSTS`, and use PostgreSQL or another managed DB.
- Consider adding automated tests (unit and integration) and GitHub Actions for CI.
- Use branch protection and PR reviews for the `main` branch.

---

## Contribution
Contributions are welcome. Open an issue to propose changes or a pull request with a clear description of your changes.

---

## License
This project is distributed under the MIT License. See `LICENSE`.

---

If you want, I can initialize the git repository and push these files to a new GitHub repo for you — tell me the desired `visibility` (Public/Private) and the repository `name` and `owner` (your GitHub username or org), and whether you want me to run the `git` commands here.
