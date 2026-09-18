# Healthcare Backend API

A Django REST Framework backend for managing patients, doctors, and their
relationships, secured with JWT authentication.

## Tech Stack

- Django 5.2 + Django REST Framework
- PostgreSQL (tested against [Neon](https://neon.tech))
- JWT auth via `djangorestframework-simplejwt`
- Environment-based configuration via `python-decouple` + `dj-database-url`

## Project Structure

```
config/         # project settings, root URLs, custom exception handler
accounts/       # custom User model, register/login
patients/       # Patient model + CRUD, scoped to the creating user
doctors/        # Doctor model + CRUD, shared read / owner-only write
mappings/       # Patient <-> Doctor assignment
```

## Setup

1. **Clone and enter the project, create a virtualenv:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the project root (see `.env.example`):
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
   ACCESS_TOKEN_LIFETIME_MIN=60
   REFRESH_TOKEN_LIFETIME_DAYS=7
   ```
   `DATABASE_URL` works with any PostgreSQL instance — a hosted one
   (Neon, Supabase, RDS, etc.) or a local install.

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the server:**
   ```bash
   python manage.py runserver
   ```
   API is now available at `http://127.0.0.1:8000/api/`.

5. *(Optional)* Create an admin user to browse data at `/admin/`:
   ```bash
   python manage.py createsuperuser
   ```

## Authentication

All endpoints except register/login require a JWT access token:

```
Authorization: Bearer <access_token>
```

Access tokens expire after `ACCESS_TOKEN_LIFETIME_MIN` minutes (default 60).

## API Reference

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | No | Register with `name`, `email`, `password` |
| POST | `/api/auth/login/` | No | Log in with `email`, `password`; returns `access` + `refresh` tokens |

### Patients
*Private per user — a user only ever sees, edits, or deletes patients they created.*

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List patients created by the authenticated user |
| GET | `/api/patients/<id>/` | Retrieve a patient (own records only) |
| PUT | `/api/patients/<id>/` | Update a patient (own records only) |
| DELETE | `/api/patients/<id>/` | Delete a patient (own records only) |

Fields: `name, age, gender, address, phone_number, medical_history`

### Doctors
*Shared resource — any authenticated user can read; only the creator can update/delete.*

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor (creator only) |
| DELETE | `/api/doctors/<id>/` | Delete a doctor (creator only) |

Fields: `name, specialization, email, phone_number, years_of_experience`

### Patient-Doctor Mappings
*Scoped to mappings the authenticated user created; a mapping can only be created for a patient the user owns.*

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor (`doctor`) to a patient (`patient`) |
| GET | `/api/mappings/` | List all mappings created by the authenticated user |
| GET | `/api/mappings/<patient_id>/` | List doctors assigned to a specific patient |
| DELETE | `/api/mappings/<id>/` | Remove a mapping by its own id |

