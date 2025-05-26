# StudyBuddy Developer Guide

## Project Architecture

### Django Apps Structure

StudyBuddy follows Django's modular app architecture with four main applications:

```
StudyBuddy/
├── ProjStudyBuddy/          # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── projLanding/            # Landing page and home
├── userAuth/               # Authentication system
├── userProfile/            # User profiles and subjects
├── userDashboard/          # Study groups and main functionality
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

#### App Responsibilities

**ProjStudyBuddy** (Main Project)
- Central configuration and settings
- Root URL routing
- WSGI/ASGI configuration
- Database configuration

**projLanding**
- Homepage and landing page
- Marketing content
- Initial user experience

**userAuth**
- User registration and login
- Password reset functionality
- Custom user model
- Authentication views and forms

**userProfile**
- User profile management
- Subject interest system
- Profile completion tracking
- Notification preferences

**userDashboard**
- Study group creation and management
- Group membership system
- Join request handling
- Group messaging
- Dashboard views and filtering

### Key Components

#### Custom User Model
- Extends Django's AbstractUser
- Email-based authentication
- Custom user manager
- Located in `userAuth.models.CustomUser`

#### Subject System
- Academic subject categorization
- Many-to-many relationship with users
- Used for group organization and filtering

#### Study Group System
- Core functionality for group management
- Membership tracking through intermediate model
- Join request approval workflow
- Message system integration

#### Permission System
- Django's built-in authentication
- Custom decorators for group access
- Host-specific permissions
- Member-only features

---

## Database Schema

### Entity Relationship Diagram

```
CustomUser (userAuth)
├── Profile (userProfile) [1:1]
├── StudyGroup (userDashboard) [1:Many as host]
├── GroupMembership (userDashboard) [1:Many]
├── GroupMessage (userDashboard) [1:Many]
└── GroupJoinRequest (userDashboard) [1:Many]

Subject (userProfile)
├── Profile (userProfile) [Many:Many]
└── StudyGroup (userDashboard) [1:Many]

StudyGroup (userDashboard)
├── GroupMembership (userDashboard) [1:Many]
├── GroupMessage (userDashboard) [1:Many]
└── GroupJoinRequest (userDashboard) [1:Many]
```

### Model Definitions

#### CustomUser (userAuth.models)
```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Inherits: username, first_name, last_name, is_active, etc.
```

**Key Features:**
- Email-based authentication
- Custom user manager
- Extends Django's AbstractUser
- Required fields: username, email

#### Profile (userProfile.models)
```python
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, blank=True)
    bio = models.TextField(blank=True)
    profile_completed = models.BooleanField(default=False)
    notify_on_join = models.BooleanField(default=True)
    notify_on_message = models.BooleanField(default=True)
    notify_on_new_group = models.BooleanField(default=False)
```

**Key Features:**
- Automatic creation via Django signals
- Subject interest tracking
- Notification preferences
- Profile completion status

#### Subject (userProfile.models)
```python
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
```

**Key Features:**
- Academic subject categorization
- Unique subject names
- Optional descriptions

#### StudyGroup (userDashboard.models)
```python
class StudyGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, through='GroupMembership')
    max_members = models.PositiveIntegerField(default=8)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    meeting_location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Key Features:**
- Host-member relationship
- Capacity management
- Meeting scheduling
- Timestamps for tracking

#### GroupMembership (userDashboard.models)
```python
class GroupMembership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

**Key Features:**
- Intermediate model for many-to-many relationship
- Join date tracking
- Active status management
- Unique constraint on user-group pairs

#### GroupMessage (userDashboard.models)
```python
class GroupMessage(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

**Key Features:**
- Group-specific messaging
- Chronological ordering
- User attribution
- Automatic timestamps

#### GroupJoinRequest (userDashboard.models)
```python
class GroupJoinRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
```

**Key Features:**
- Request approval workflow
- Status tracking
- Timestamp management
- Unique constraint prevents duplicate requests

### Database Relationships

#### One-to-One Relationships
- `CustomUser` ↔ `Profile`: Each user has exactly one profile

#### One-to-Many Relationships
- `CustomUser` → `StudyGroup`: User can host multiple groups
- `Subject` → `StudyGroup`: Subject can have multiple groups
- `StudyGroup` → `GroupMessage`: Group can have multiple messages
- `CustomUser` → `GroupMessage`: User can send multiple messages
- `StudyGroup` → `GroupJoinRequest`: Group can have multiple requests
- `CustomUser` → `GroupJoinRequest`: User can make multiple requests

#### Many-to-Many Relationships
- `CustomUser` ↔ `StudyGroup` (through `GroupMembership`): Users can join multiple groups
- `Profile` ↔ `Subject`: Users can be interested in multiple subjects

---

## URL Routing

### Root URL Configuration (ProjStudyBuddy/urls.py)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projLanding.urls')),
    path('auth/', include('userAuth.urls')),
    path('', include('userProfile.urls')),
    path('', include('userDashboard.urls')),
]
```

### App-Specific URL Patterns

#### projLanding URLs
```python
urlpatterns = [
    path('', views.home, name='home'),
]
```

#### userAuth URLs
```python
urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Password reset URLs
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
```

#### userProfile URLs
```python
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/setup/', profile_setup, name='profile_setup'),
]
```

#### userDashboard URLs
```python
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('create-group/', create_group, name='create_group'),
    path('group/<int:group_id>/', group_details, name='group_details'),
    path('join-group/<int:group_id>/', join_group, name='join_group'),
    path('leave-group/<int:group_id>/', leave_group, name='leave_group'),
    path('edit-group/<int:group_id>/', edit_group, name='edit_group'),
    path('approve-request/<int:request_id>/', approve_request, name='approve_request'),
    path('decline-request/<int:request_id>/', decline_request, name='decline_request'),
]
```

### URL Naming Conventions
- Use lowercase with hyphens for URL paths
- Use underscores for URL names
- Descriptive names that indicate functionality
- Consistent parameter naming (`<int:group_id>`)

---

## View Implementation

### View Patterns and Architecture

#### Function-Based Views
All views in StudyBuddy use function-based views for simplicity and clarity.

#### Authentication Decorators
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # View logic here
```

#### Common View Patterns

**List Views** (Dashboard)
```python
@login_required
def dashboard(request):
    # Get all objects
    study_groups = StudyGroup.objects.all().order_by('-created_at')
    
    # Apply filters
    subject_filter = request.GET.get('subject', '').strip()
    search_query = request.GET.get('search', '').strip()
    
    if subject_filter:
        study_groups = study_groups.filter(subject_id=int(subject_filter))
    
    if search_query:
        study_groups = study_groups.filter(title__icontains=search_query)
    
    # Context and render
    context = {'study_groups': study_groups}
    return render(request, 'template.html', context)
```

**Detail Views** (Group Details)
```python
@login_required
def group_details(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Check permissions
    is_member = group.members.filter(id=request.user.id).exists()
    is_host = group.host == request.user
    
    # Handle POST requests
    if request.method == 'POST' and (is_member or is_host):
        # Process form data
        pass
    
    context = {
        'group': group,
        'is_member': is_member,
        'is_host': is_host,
    }
    return render(request, 'template.html', context)
```

**Create Views** (Group Creation)
```python
@login_required
def create_group(request):
    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('group_title')
        # ... other fields
        
        try:
            # Create object
            study_group = StudyGroup.objects.create(
                title=title,
                host=request.user,
                # ... other fields
            )
            messages.success(request, 'Group created successfully!')
            return redirect('group_details', group_id=study_group.id)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # GET request - show form
    context = {'subjects': Subject.objects.all()}
    return render(request, 'template.html', context)
```

### Error Handling Patterns

#### Try-Catch Blocks
```python
try:
    group = StudyGroup.objects.get(id=group_id)
except StudyGroup.DoesNotExist:
    messages.error(request, "Study group not found.")
    return redirect('dashboard')
```

#### get_object_or_404
```python
group = get_object_or_404(StudyGroup, id=group_id)
```

#### Form Validation
```python
if form.is_valid():
    user = form.save()
    # Success logic
else:
    messages.error(request, 'Form validation failed.')
```

### Message Framework Usage
```python
from django.contrib import messages

# Success messages
messages.success(request, 'Operation completed successfully!')

# Error messages
messages.error(request, 'An error occurred.')

# Warning messages
messages.warning(request, 'This is a warning.')

# Info messages
messages.info(request, 'Information message.')
```

---

## Template Organization

### Template Structure
```
templates/
├── projLanding/
│   └── home.html
├── userAuth/
│   ├── login.html
│   ├── register.html
│   ├── password_reset.html
│   ├── password_reset_done.html
│   ├── password_reset_confirm.html
│   └── password_reset_complete.html
├── userProfile/
│   ├── profile.html
│   └── profile_setup.html
└── userDashboard/
    ├── dashboard.html
    ├── create_group.html
    ├── edit_group.html
    └── group_detail.html
```

### Materialize CSS Implementation

#### CDN Integration
```html
<!-- Materialize CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

<!-- Material Icons -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<!-- Materialize JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
```

#### Grid System Usage
```html
<div class="container">
  <div class="row">
    <div class="col s12 m6 l4">
      <!-- Content -->
    </div>
  </div>
</div>
```

#### Component Implementation

**Navigation Bar**
```html
<div class="navbar-fixed">
  <nav class="teal darken-1">
    <div class="nav-wrapper container">
      <a href="#" class="brand-logo">Study Buddy</a>
      <a href="#" data-target="mobile-nav" class="sidenav-trigger">
        <i class="material-icons">menu</i>
      </a>
      <ul class="right hide-on-med-and-down">
        <li><a href="#">Link</a></li>
      </ul>
    </div>
  </nav>
</div>
```

**Cards**
```html
<div class="card hoverable">
  <div class="card-content">
    <span class="card-title">Card Title</span>
    <p>Card content goes here.</p>
  </div>
  <div class="card-action">
    <a href="#" class="btn">Action</a>
  </div>
</div>
```

**Forms**
```html
<div class="input-field">
  <input id="input_id" type="text" name="field_name">
  <label for="input_id">Field Label</label>
</div>

<div class="input-field">
  <select name="select_field">
    <option value="" disabled selected>Choose option</option>
    <option value="1">Option 1</option>
  </select>
  <label>Select Label</label>
</div>
```

**Buttons**
```html
<a class="btn waves-effect waves-light" type="submit">
  <i class="material-icons left">send</i>
  Button Text
</a>
```

#### Custom CSS Styling

**Color Scheme**
```css
:root {
  --primary-color: #009688;
  --primary-dark: #00796B;
  --background-color: #f5f5f5;
}

.btn, .btn-large {
  background-color: var(--primary-color);
  border-radius: 4px;
}

.btn:hover, .btn-large:hover {
  background-color: var(--primary-dark);
}
```

**Typography**
```css
body {
  font-family: 'Poppins', sans-serif;
}

.page-title {
  font-weight: 600;
  color: var(--primary-color);
}
```

**Component Customizations**
```css
.group-card {
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}
```

#### JavaScript Initialization
```html
<script>
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Materialize components
  M.AutoInit();
  
  // Specific component initialization
  var elems = document.querySelectorAll('select');
  M.FormSelect.init(elems);
  
  var sidenavElems = document.querySelectorAll('.sidenav');
  M.Sidenav.init(sidenavElems);
});
</script>
```

### Template Inheritance

#### Base Template Pattern
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}StudyBuddy{% endblock %}</title>
  
  <!-- CSS includes -->
  {% block extra_css %}{% endblock %}
</head>
<body>
  {% include 'navbar.html' %}
  
  <main>
    {% block content %}{% endblock %}
  </main>
  
  {% include 'footer.html' %}
  
  <!-- JavaScript includes -->
  {% block extra_js %}{% endblock %}
</body>
</html>
```

#### Child Template Usage
```html
{% extends 'base.html' %}

{% block title %}Dashboard - StudyBuddy{% endblock %}

{% block content %}
<div class="container">
  <!-- Page content -->
</div>
{% endblock %}
```

---

## Authentication System

### Custom User Model Implementation

#### Model Definition
```python
# userAuth/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
```

#### Settings Configuration
```python
# settings.py
AUTH_USER_MODEL = 'userAuth.CustomUser'
```

### Authentication Views

#### Registration View
```python
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile_setup')
        else:
            messages.error(request, 'Registration failed.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'userAuth/register.html', {'form': form})
```

#### Login View
```python
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'userAuth/login.html', {'form': form})
```

#### Logout View
```python
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')
```

### Password Reset System

#### URL Configuration
```python
# Password reset URLs using Django's built-in views
path('password_reset/', 
     auth_views.PasswordResetView.as_view(
         template_name='userAuth/password_reset.html',
         email_template_name='userAuth/password_reset_email.html',
         subject_template_name='userAuth/password_reset_subject.txt'
     ), 
     name='password_reset'),
```

#### Email Configuration
```python
# settings.py
# Development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'

PASSWORD_RESET_TIMEOUT = 86400  # 1 day
```

### Permission System

#### Login Required Decorator
```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    # View logic for authenticated users only
    pass
```

#### Custom Permission Checks
```python
def group_details(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Check if user is member or host
    is_member = group.members.filter(id=request.user.id).exists()
    is_host = group.host == request.user
    
    # Permission-based logic
    if is_host:
        # Host-specific functionality
        pass
    elif is_member:
        # Member-specific functionality
        pass
    else:
        # Public view functionality
        pass
```

#### Template Permission Checks
```html
{% if user.is_authenticated %}
  <!-- Authenticated user content -->
  {% if is_host %}
    <!-- Host-specific content -->
  {% elif is_member %}
    <!-- Member-specific content -->
  {% endif %}
{% else %}
  <!-- Anonymous user content -->
{% endif %}
```

---

## Management Commands

### Database Cleanup Command

#### Command Structure
```python
# userDashboard/management/commands/cleanup_join_requests.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clean up duplicate or problematic join request records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleaned up without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        # Command logic here
```

#### Usage
```bash
# Dry run to see what would be cleaned
python manage.py cleanup_join_requests --dry-run

# Execute cleanup
python manage.py cleanup_join_requests
```

#### Functionality
- Removes redundant approved join requests
- Handles duplicate requests
- Maintains data integrity
- Provides detailed output

---

## Testing Approach

### Test Structure
```
tests/
├── test_models.py
├── test_views.py
├── test_forms.py
└── test_utils.py
```

### Model Testing Example
```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from userDashboard.models import StudyGroup, Subject

User = get_user_model()

class StudyGroupModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.subject = Subject.objects.create(name='Mathematics')

    def test_study_group_creation(self):
        group = StudyGroup.objects.create(
            title='Test Group',
            description='Test Description',
            subject=self.subject,
            host=self.user,
            meeting_date='2024-01-01',
            meeting_time='10:00:00'
        )
        self.assertEqual(group.title, 'Test Group')
        self.assertEqual(group.host, self.user)
```

### View Testing Example
```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/')

    def test_dashboard_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test userDashboard

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Deployment Configuration

### Production Settings

#### Environment Variables
```python
import os
from pathlib import Path

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

#### Static Files Configuration
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For production with CDN
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

#### Email Configuration
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

### Docker Configuration

#### Dockerfile
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ProjStudyBuddy.wsgi:application"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=studybuddy
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Deployment Checklist

1. **Security**
   - [ ] Set DEBUG=False
   - [ ] Configure SECRET_KEY
   - [ ] Set ALLOWED_HOSTS
   - [ ] Enable HTTPS
   - [ ] Configure CSRF_TRUSTED_ORIGINS

2. **Database**
   - [ ] Set up PostgreSQL
   - [ ] Run migrations
   - [ ] Create superuser
   - [ ] Set up database backups

3. **Static Files**
   - [ ] Configure static file serving
   - [ ] Run collectstatic
   - [ ] Set up CDN (optional)

4. **Email**
   - [ ] Configure SMTP settings
   - [ ] Test email functionality
   - [ ] Set up email monitoring

5. **Monitoring**
   - [ ] Set up logging
   - [ ] Configure error tracking
   - [ ] Set up performance monitoring

---

## Performance Considerations

### Database Optimization

#### Query Optimization
```python
# Use select_related for foreign keys
groups = StudyGroup.objects.select_related('subject', 'host').all()

# Use prefetch_related for many-to-many
groups = StudyGroup.objects.prefetch_related('members').all()

# Avoid N+1 queries
groups = StudyGroup.objects.select_related('subject').prefetch_related(
    'members', 'messages__user'
)
```

#### Database Indexing
```python
class StudyGroup(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['subject', 'created_at']),
            models.Index(fields=['meeting_date', 'meeting_time']),
        ]
```

### Caching Strategy

#### View-Level Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects': subjects})
```

#### Template Fragment Caching
```html
{% load cache %}
{% cache 500 subject_list %}
  <!-- Expensive template rendering -->
{% endcache %}
```

### Frontend Optimization

#### CSS/JS Minification
```python
# settings.py
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Use django-compressor for production
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
```

#### Image Optimization
- Use appropriate image formats (WebP, AVIF)
- Implement lazy loading
- Optimize image sizes

---

## Security Measures

### Django Security Features

#### CSRF Protection
```python
# Enabled by default in MIDDLEWARE
'django.middleware.csrf.CsrfViewMiddleware',

# In templates
{% csrf_token %}
```

#### SQL Injection Prevention
```python
# Use Django ORM (automatically escaped)
StudyGroup.objects.filter(title__icontains=search_query)

# For raw SQL (use parameterized queries)
cursor.execute("SELECT * FROM table WHERE id = %s", [user_id])
```

#### XSS Prevention
```html
<!-- Django templates auto-escape by default -->
{{ user_input }}  <!-- Automatically escaped -->

<!-- For trusted content -->
{{ trusted_content|safe }}
```

### Custom Security Measures

#### Input Validation
```python
def create_group(request):
    if request.method == 'POST':
        title = request.POST.get('group_title', '').strip()
        
        # Validate input
        if not title or len(title) > 100:
            messages.error(request, 'Invalid title')
            return redirect('create_group')
```

#### Permission Checks
```python
def edit_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Ensure only host can edit
    if group.host != request.user:
        messages.error(request, 'Permission denied')
        return redirect('dashboard')
```

#### Rate Limiting
```python
# Using django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # Login logic
    pass
```

### Security Headers

#### settings.py Configuration
```python
# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (for production)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## Code Style Guidelines

### Python Code Style

#### PEP 8 Compliance
- Line length: 79 characters
- Indentation: 4 spaces
- Import organization: standard, third-party, local

#### Django Conventions
```python
# Model naming
class StudyGroup(models.Model):  # PascalCase

# View naming
def group_details(request):  # snake_case

# URL naming
path('group-details/', views.group_details, name='group_details')
```

#### Documentation Standards
```python
def create_study_group(title, subject, host):
    """
    Create a new study group.
    
    Args:
        title (str): The group title
        subject (Subject): The academic subject
        host (User): The group host
    
    Returns:
        StudyGroup: The created study group instance
    
    Raises:
        ValidationError: If validation fails
    """
    pass
```

### HTML/CSS Style

#### HTML Structure
```html
<!-- Use semantic HTML -->
<main>
  <section class="hero">
    <h1>Page Title</h1>
  </section>
  
  <section class="content">
    <article>
      <!-- Content -->
    </article>
  </section>
</main>
```

#### CSS Organization
```css
/* Component-based organization */
/* Base styles */
body { }

/* Layout */
.container { }

/* Components */
.card { }
.btn { }

/* Utilities */
.text-center { }
.mb-2 { }
```

### JavaScript Style

#### ES6+ Features
```javascript
// Use const/let instead of var
const elements = document.querySelectorAll('.selector');

// Arrow functions
elements.forEach(element => {
    element.addEventListener('click', handleClick);
});

// Template literals
const message = `Hello, ${username}!`;
```

---

## Contributing Guidelines

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Make changes with tests**
4. **Run test suite**
   ```bash
   python manage.py test
   ```
5. **Submit pull request**

### Code Review Process

#### Pull Request Requirements
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered

#### Review Checklist
- [ ] Code functionality
- [ ] Test coverage
- [ ] Documentation quality
- [ ] Security considerations
- [ ] Performance implications

### Issue Reporting

#### Bug Reports
Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Screenshots (if applicable)

#### Feature Requests
Include:
- Use case description
- Proposed solution
- Alternative solutions
- Additional context

---

*Last updated: [Current Date]*
*Version: 1.0* 