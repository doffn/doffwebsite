# Dawit Neri — Engineering, AI & Software Portfolio

A responsive Django portfolio for Dawit Neri, combining aircraft powerplant/MRO experience, AI interests and backend/software projects.

## Included
- Responsive single-page portfolio with dark aerospace-inspired visual design.
- CSS-built 3D-inspired turbine hero with pointer parallax and reduced-motion support.
- Powerplant, AI, backend/software, project and contact sections.
- Django JSON APIs: `/api/health/`, `/api/projects/`, `/api/contact/`.
- Contact messages saved to Django database and manageable in `/admin/`.
- Optional email notification when SMTP environment variables are configured.
- Original CV PDF and favicon retained in `staticfiles/`.

## Requirements
- Python 3.12 recommended
- pip
- Django 5.2
- PostgreSQL for persistent production data

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and set a secure `DJANGO_SECRET_KEY`. Environment variables can also be set in your shell or hosting provider.

```bash
python manage.py makemigrations myApp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## API
- `GET /api/health/` — service health.
- `GET /api/projects/` — project data.
- `POST /api/contact/` — accepts JSON fields `name`, `email`, `subject`, `message` and honeypot `website`. The endpoint uses Django CSRF protection and validates the input.

## Admin
Open `/admin/` and sign in with the superuser created locally. Contact messages are listed in the Contact messages admin.

## Deploying
This repository retains the Vercel Django project shape and `vercel.json`. Configure these environment variables in the Vercel project:
- `DJANGO_SECRET_KEY`: strong random secret, never commit it.
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`: include your deployed hostname and `.vercel.app`.
- `CSRF_TRUSTED_ORIGINS`: include your exact HTTPS site origin, e.g. `https://your-domain.vercel.app`.
- `DATABASE_URL`: a managed PostgreSQL connection string.

**Important persistence note:** Vercel serverless filesystems are ephemeral. SQLite is for local development only; use managed PostgreSQL for contact messages in production. Run migrations against the production database as part of your deployment workflow. Configure SMTP variables if you want email notifications. Do not put database passwords or API secrets in frontend JavaScript.

## Accuracy / content
The portfolio text reflects the supplied professional details: GEnx-1B complete overhaul workflow and GE90 splitting/shipping operations. Review all wording and project links before publishing. Project descriptions are concise portfolio summaries; link to the exact repository or demo when one is available.

## Notes
The 3D turbine hero is a lightweight CSS 3D-inspired visual rather than a downloadable 3D engine CAD model. It avoids requiring a heavy WebGL bundle and works as a responsive decorative visualization.
