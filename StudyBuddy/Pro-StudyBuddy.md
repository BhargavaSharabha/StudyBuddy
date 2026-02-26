# Project - StudyBuddy (Portfolio Web Application)

## Overview

**StudyBuddy** is a full-stack web application that connects students with similar academic interests by enabling them to create, join, and manage study groups. Users browse groups by subject, submit join requests that go through a host-approval workflow, and communicate within their groups through an integrated discussion system.

**GitHub:** https://github.com/BhargavaSharabha/StudyBuddy.git
**Type:** Portfolio Project
**Team Size:** 2–3 contributors
**License:** MIT
**Status:** Completed — production-ready deployment configuration included

---

## Problem Statement

Finding compatible study partners is fragmented and informal — students rely on class group chats, notice boards, or word of mouth. StudyBuddy addresses this by providing:

- A centralised platform for discovering subject-specific study groups
- A structured join-request and approval system so group hosts control membership quality
- Capacity management to keep groups productive (configurable member cap, default 8)
- An in-group discussion board to coordinate sessions without leaving the platform
- A user profile system with subject interests that gives context to every member

---

## Technical Implementation

### Application Architecture

The project is structured as a standard Django monolith with four focused apps:

| App | Responsibility |
|-----|---------------|
| `projLanding` | Public landing/home page |
| `userAuth` | Registration, login, logout, full password-reset flow |
| `userProfile` | User profile, subject interests, notification preferences |
| `userDashboard` | Study groups, memberships, discussions, join-request workflow |

Settings are split across three environment profiles:

- `settings/development.py` — SQLite, DEBUG=True, console email backend
- `settings/production.py` — PostgreSQL via `dj-database-url`, SMTP email, full security headers
- `settings/build.py` — Minimal in-memory SQLite used only during `docker build` to run `collectstatic` without needing real environment variables

### Database Design

Seven models across two apps, with clear separation of concerns:

**`userAuth` app**
- `CustomUser` — Extends `AbstractUser`; adds unique email constraint and a custom `CustomUserManager`

**`userProfile` app**
- `Subject` — Catalogue of academic subjects; used as a foreign key on study groups and a many-to-many on profiles
- `Profile` — One-to-one with `CustomUser`; stores bio, subject interests (M2M), profile completion flag, and three notification preference booleans. Auto-created via Django signal on user registration

**`userDashboard` app**
- `StudyGroup` — Core entity; fields: title, description, subject (FK), host (FK), max_members, meeting_date, meeting_time, meeting_location, slug (auto-generated from title via `slugify`), created_at, updated_at. Ordering by meeting date/time
- `GroupMembership` — Through table for the `StudyGroup ↔ User` many-to-many; records join date and active status. Unique constraint on `(user, group)`
- `GroupMessage` — Timestamped text messages attached to a group; ordered chronologically
- `GroupJoinRequest` — Approval workflow model; status choices: `pending / approved / declined`; tracks `requested_at` and `responded_at`; unique constraint on `(user, group)`

### Migration History (userDashboard)

| Migration | Date | Change |
|-----------|------|--------|
| `0001_initial` | 2025-05-22 | StudyGroup, GroupMembership, GroupMessage |
| `0002_groupjoinrequest` | 2025-05-24 | GroupJoinRequest approval model |
| `0003_studygroup_slug` | — | Slug field added to StudyGroup |
| `0004_auto_20250526_1512` | 2025-05-26 | Additional field refinements |

### Key Features

#### 1. Custom Authentication System
- `CustomUser` extends Django's `AbstractUser` with a mandatory, unique email field
- `CustomUserCreationForm` enforces email collection at registration
- Full password-reset flow using Django's built-in views with custom templates (reset email → token link → new password → confirmation)
- On registration, the user is redirected to a profile-setup wizard; subsequent logins go straight to the dashboard

#### 2. Subject-Based Group Discovery
- Dashboard lists all `StudyGroup` objects ordered by newest first
- Two simultaneous filters: dropdown filter by `subject_id` and free-text search on `title` (case-insensitive `icontains`)
- Filter state is preserved in GET parameters across page loads

#### 3. Structured Join-Request Workflow
- Non-members click **Join** → `GroupJoinRequest` created with `status='pending'`
- Host sees a pending-request badge on their groups in the dashboard
- Host navigates to group detail → reviews member profile → **Approve** or **Decline**
- Approving creates a `GroupMembership` record and updates the request to `approved`; declining marks it `declined` with a timestamp
- Edge cases handled: user already a member, group at capacity, re-joining after leaving (existing declined request is reset to `pending` rather than creating a duplicate, respecting the unique constraint)
- Admin interface supports bulk approve/decline actions

#### 4. Capacity Enforcement
- `StudyGroup.is_full` property compares `members.count()` against `max_members`
- Join requests are blocked server-side when the group is full
- When editing a group, hosts cannot lower `max_members` below the current active member count

#### 5. In-Group Discussion
- Any active member or host can post a `GroupMessage` from the group detail page
- Messages are displayed in chronological order with author attribution and timestamps
- Post triggers a POST → redirect pattern to prevent duplicate submissions on refresh

#### 6. SEO-Friendly Slug URLs
- Slugs are auto-generated from the group title on every save via `django.utils.text.slugify`
- Group detail URL: `/dashboard/group_details/<id>/<slug>`
- If a stale slug is used in the URL (e.g., after a title edit), the view redirects to the current slug automatically

#### 7. Custom Management Command
`python manage.py cleanup_join_requests`
- Finds and removes approved `GroupJoinRequest` records where the corresponding `GroupMembership` already exists (redundant after approval)
- Detects and resolves duplicate requests violating the unique constraint by keeping the most recent
- Supports `--dry-run` flag for safe preview before deletion

#### 8. Custom Template Tag
- `dashboard_extras.get_item` — allows Django templates to do dictionary lookups with dynamic keys, used to show per-group pending-request counts in the dashboard

#### 9. Signal-Driven Profile Creation
- `post_save` signal on `CustomUser` automatically creates a `Profile` instance for every new user
- A second signal keeps the profile in sync when the user record is saved
- Eliminates any risk of a user existing without a profile

### Security Implementation (Production)

| Setting | Value |
|---------|-------|
| `SECURE_HSTS_SECONDS` | 31 536 000 (1 year) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | True |
| `SECURE_HSTS_PRELOAD` | True |
| `SECURE_SSL_REDIRECT` | True (env-configurable) |
| `SESSION_COOKIE_SECURE` | True |
| `CSRF_COOKIE_SECURE` | True |
| `X_FRAME_OPTIONS` | DENY |
| `SECURE_BROWSER_XSS_FILTER` | True |
| `SECURE_CONTENT_TYPE_NOSNIFF` | True |
| `SECURE_REFERRER_POLICY` | strict-origin-when-cross-origin |
| `SECURE_PROXY_SSL_HEADER` | HTTP_X_FORWARDED_PROTO: https |

- All environment secrets managed via `python-decouple` (`.env` file, never committed)
- CSRF trusted origins configurable per environment
- Session backed by database; cookie lifetime 24 hours with `SAVE_EVERY_REQUEST=True`

### Deployment Infrastructure

**Docker — Multi-Stage Build**
- Stage 1 (`builder`): Python 3.11-slim + `build-essential` + `libpq-dev` to compile psycopg2
- Stage 2 (`production`): Minimal runtime image; copies only compiled site-packages from builder
- Non-root `django` user created inside the container
- `collectstatic` runs at build time using the `build` settings profile (no env vars needed)
- Health check: polls `/health/` endpoint every 30 seconds; 3 retries before marking unhealthy
- Gunicorn: 3 workers, 120-second timeout, bound to `0.0.0.0:8000`

**Docker Compose**
- `db` service: PostgreSQL 15-alpine; health-checked before web service starts
- `web` service: runs migrations then starts Gunicorn on container start
- Named volumes: `postgres_data`, `static_volume`, `media_volume`
- Isolated bridge network `studybuddy_network`
- Nginx reverse proxy configuration included (commented, ready to enable)

**Health Check Endpoint**
- `GET /health/` returns `{"status": "healthy"}` as JSON
- Used by Docker's built-in `HEALTHCHECK` instruction and compatible with load-balancer probes

---

## URL Routing Reference

| Method | URL Pattern | View | Auth Required |
|--------|-------------|------|---------------|
| GET | `/` | `home` | No |
| GET/POST | `/auth/login/` | `login_view` | No |
| GET/POST | `/auth/register/` | `register_view` | No |
| GET | `/auth/logout/` | `logout_view` | Yes |
| GET/POST | `/auth/password_reset/` | Django built-in | No |
| GET/POST | `/profile/profile` | `profile` | Yes |
| GET/POST | `/profile/profile_setup` | `profile_setup` | Yes |
| GET | `/dashboard/dashboard` | `dashboard` | Yes |
| GET/POST | `/dashboard/create_group` | `create_group` | Yes |
| GET/POST | `/dashboard/group_details/<id>/<slug>` | `group_details` | Yes |
| POST | `/dashboard/join_group/<id>` | `join_group` | Yes |
| POST | `/dashboard/leave_group/<id>` | `leave_group` | Yes |
| GET/POST | `/dashboard/edit_group/<id>` | `edit_group` | Yes (host only) |
| POST | `/dashboard/approve_request/<id>` | `approve_request` | Yes (host only) |
| POST | `/dashboard/decline_request/<id>` | `decline_request` | Yes (host only) |
| GET | `/health/` | `health_check` | No |
| GET/POST | `/admin/` | Django Admin | Staff only |

---

## Code Samples

### Auto Profile Creation via Signal
```python
# userProfile/models.py
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

### Slug Auto-Generation with Stale-URL Redirect
```python
# userDashboard/models.py — StudyGroup.save()
def save(self, *args, **kwargs):
    self.slug = slugify(self.title) if self.title else 'untitled'
    super().save(*args, **kwargs)

# userDashboard/views.py — group_details view
current_slug = slugify(group.title) if group.title else 'untitled'
if slug != current_slug:
    return redirect('group_details', group_id=group.id, slug=current_slug)
```

### Re-Join Edge Case Handling
```python
# userDashboard/views.py — join_group view
existing_request = GroupJoinRequest.objects.filter(
    user=request.user, group=group
).first()

if existing_request:
    existing_request.status = 'pending'
    existing_request.requested_at = timezone.now()
    existing_request.responded_at = None
    existing_request.save()
```

### Capacity Validation on Edit
```python
# userDashboard/views.py — edit_group view
if max_members < current_member_count:
    messages.error(request,
        f"Maximum members cannot be less than the current member count ({current_member_count}).")
```

### Management Command with Dry-Run Support
```bash
# Preview only — no changes made
python manage.py cleanup_join_requests --dry-run

# Apply cleanup
python manage.py cleanup_join_requests
```

---

## Technologies

| Category | Technology | Version |
|----------|-----------|---------|
| Language | Python | 3.11 |
| Web Framework | Django | 5.2.1 |
| WSGI Server | Gunicorn | 21.2.0 |
| Database (Dev) | SQLite | Bundled with Python |
| Database (Prod) | PostgreSQL | 15 (Alpine) |
| DB Adapter | psycopg2-binary | 2.9.9 |
| DB URL Parsing | dj-database-url | 2.1.0 |
| Configuration | python-decouple | 3.8 |
| Static Files | WhiteNoise | 6.6.0 |
| Frontend Framework | Materialize CSS | 1.0.0 |
| Icons | Google Material Icons | CDN |
| Fonts | Google Fonts (Poppins) | CDN |
| Containerisation | Docker | Multi-stage build |
| Orchestration | Docker Compose | — |
| Async ASGI | asgiref | 3.8.1 |
| SQL Parsing | sqlparse | 0.5.3 |
| Timezone Data | tzdata | 2025.2 |

---

## Project Structure

```
StudyBuddy/
├── ProjStudyBuddy/               # Django project config
│   ├── settings/
│   │   ├── base.py               # Shared settings
│   │   ├── development.py        # Dev overrides (SQLite, console email)
│   │   ├── production.py         # Prod overrides (PostgreSQL, SMTP, security headers)
│   │   └── build.py              # Build-time settings for Docker collectstatic
│   ├── urls.py                   # Root URL dispatcher + health check endpoint
│   └── wsgi.py
├── projLanding/                  # Public landing page app
├── userAuth/                     # Authentication app
│   ├── models.py                 # CustomUser, CustomUserManager
│   ├── forms.py                  # CustomUserCreationForm
│   ├── views.py                  # login, register, logout views
│   └── templates/userAuth/       # Login, register, password-reset templates (5 templates)
├── userProfile/                  # Profile management app
│   ├── models.py                 # Subject, Profile + auto-create signals
│   ├── views.py                  # profile, profile_setup views
│   └── templates/userProfile/
├── userDashboard/                # Core study group app
│   ├── models.py                 # StudyGroup, GroupMembership, GroupMessage, GroupJoinRequest
│   ├── views.py                  # 9 views covering full group lifecycle
│   ├── admin.py                  # Rich admin with inline members, bulk approve/decline
│   ├── templatetags/
│   │   └── dashboard_extras.py   # Custom get_item filter
│   ├── management/commands/
│   │   └── cleanup_join_requests.py
│   └── templates/userDashboard/
├── scripts/
│   ├── init-db.sql               # PostgreSQL init script (uuid-ossp, pg_trgm extensions)
│   └── migrate_data.py
├── Dockerfile                    # Multi-stage build (builder + production)
├── docker-compose.yml            # PostgreSQL + web services with health checks
├── requirements.txt              # 9 pinned dependencies
└── env.example                   # Environment variable template
```

---

## Skills Demonstrated

> *Assessment from a Full Stack Engineering and Career Development perspective*

### Backend Engineering
- Extending Django's authentication system (custom user model, custom manager, custom form)
- Relational data modelling: ForeignKey, ManyToManyField with through table, OneToOneField
- Signal-driven side effects (auto profile creation on user save)
- View-level authorisation guards (`login_required` decorator, host-only checks in view logic)
- POST → Redirect pattern to prevent duplicate form submissions on refresh
- Django ORM: `select_related`, `values_list(flat=True)`, `filter`, `annotate(Count)`, `update`
- Custom management commands with `--dry-run` support for safe database maintenance
- Custom template tags and filters
- Multi-environment Django settings architecture (dev / prod / build)
- Database migration management across iterative development

### DevOps & Deployment
- Multi-stage Docker builds to separate build-time dependencies from the runtime image
- Docker Compose orchestration with service health checks and dependency ordering
- Production security hardening (HSTS, SSL redirect, secure cookies, XSS/CSRF/clickjacking headers)
- Environment-based configuration via `python-decouple`
- WhiteNoise for zero-dependency static file serving in production
- Gunicorn WSGI configuration (workers, timeout)
- Health check endpoint designed for container orchestration

### Frontend
- Materialize CSS component system (cards, navbar, forms, chips, toast messages, modals)
- Responsive layout using the Materialize 12-column grid
- Google Material Icon integration
- JavaScript date/time picker integration with server-side parsing (12-hour → 24-hour conversion)

### Software Design Decisions
- Four-app separation of concerns with clear boundaries (landing / auth / profile / dashboard)
- Defensive programming: edge-case handling for re-join requests, capacity enforcement during group edits, stale-slug automatic redirects
- Django admin customisation with TabularInline members, readonly message history, and bulk approve/decline actions

---

## What This Project Shows to a Hiring Manager

| Skill Area | Evidence in Codebase |
|------------|---------------------|
| **Full-stack ownership** | End-to-end delivery from data models to Dockerfile and Docker Compose |
| **Real-world workflow patterns** | Host-approval join request system with pending/approved/declined state machine |
| **Security awareness** | Full production security header suite, non-root Docker user, env-var secret management |
| **Production mindset** | Separate dev/prod/build settings, multi-stage Docker build, health check endpoint, Gunicorn |
| **Database literacy** | Normalised schema with through table, unique constraints, cascading deletes, signal-driven auto-creation |
| **Code defensiveness** | Re-join edge case, capacity check on edit, stale-slug redirect, try/except around date parsing |
| **DevOps foundation** | Docker, Docker Compose, PostgreSQL, WhiteNoise, environment variable management |
| **Maintainability** | Custom management command with `--dry-run`, admin bulk actions, pinned dependency versions |

---

## Running Locally

```bash
# 1. Clone
git clone https://github.com/BhargavaSharabha/StudyBuddy.git
cd StudyBuddy

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate --settings=ProjStudyBuddy.settings.development

# 5. (Optional) Create admin user
python manage.py createsuperuser --settings=ProjStudyBuddy.settings.development

# 6. Run server
python manage.py runserver --settings=ProjStudyBuddy.settings.development
```

Access at `http://127.0.0.1:8000` · Admin at `http://127.0.0.1:8000/admin`

## Running with Docker

```bash
# 1. Copy and configure environment
cp env.example .env
# Edit .env with your values (SECRET_KEY, DATABASE_URL, email settings)

# 2. Build and start services
docker compose up --build

# Application: http://localhost:8888
# PostgreSQL:  localhost:5432
```

---

## Potential Improvements / Roadmap

- Real-time messaging via Django Channels / WebSockets (currently requires manual page refresh)
- Email notifications to users when their join request is approved or declined
- Group session scheduling with calendar export (iCal / Google Calendar link)
- Pagination on the dashboard for large group counts
- Profile avatar upload (Pillow is already available as an indirect dependency via the venv)
- Location-based group search in addition to subject filtering
- REST API layer (Django REST Framework) to support a future mobile client
- Redis cache for session storage and query result caching under load
