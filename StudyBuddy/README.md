# StudyBuddy - Collaborative Learning Platform

## Table of Contents

### For Users
1. [Installation and Setup](#installation-and-setup)
2. [User Account Management](#user-account-management)
3. [Feature Guides](#feature-guides)
4. [Navigation Guide](#navigation-guide)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)
7. [Support](#support)

### For Developers
1. [Project Architecture](#project-architecture)
2. [Database Schema](#database-schema)
3. [URL Routing](#url-routing)
4. [View Implementation](#view-implementation)
5. [Template Organization](#template-organization)
6. [Authentication System](#authentication-system)
7. [API Documentation](#api-documentation)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Performance](#performance)
11. [Security](#security)
12. [Code Style](#code-style)
13. [Contributing](#contributing)

---

## Application Overview

**StudyBuddy** is a web-based collaborative learning platform that connects students with similar academic interests. It enables users to create, join, and manage study groups organized by subject, schedule group sessions, and collaborate through real-time discussions.

### Purpose
StudyBuddy streamlines the process of finding study partners and provides tools for effective group study management, helping students achieve better academic outcomes through collaborative learning.

### Key Features

#### 🔐 User Authentication System
- Secure registration and login functionality with custom user model
- Comprehensive user profile creation and management
- Password reset capabilities with email notifications
- Profile completion tracking and setup wizard

#### 👥 Study Group Management
- Create study groups with detailed information (subject, schedule, location)
- Browse available study groups with advanced filtering by subject and search
- Robust membership request and approval system for group joining
- Group editing capabilities for hosts with capacity validation
- Enhanced join group system handling all edge cases including rejoining after leaving

#### 📊 Interactive Dashboards
- User-specific dashboard showing joined groups with membership status
- Group-specific dashboards with comprehensive member information
- Real-time status updates on group activities and pending requests
- Improved profile dashboard displaying user's study groups with detailed information

#### 💬 Real-time Group Discussions
- In-group messaging system with chronological ordering
- Message display with user attribution and timestamps
- Seamless message posting interface for members and hosts

#### 👤 User Profile System
- Subject interest selection with interactive chip interface
- Enhanced profile management with bio field and notification preferences
- User activity tracking and membership history
- Profile customization with study preferences

#### 🛠️ Administrative Tools
- Database cleanup commands for automated cleanup of redundant join requests
- Comprehensive admin interface for all models
- Data integrity validation and maintenance tools

### Tech Stack
- **Backend**: Django 5.2.1
- **Frontend**: HTML5, Materialize CSS 1.0.0
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication with custom user model
- **UI Framework**: Materialize CSS with Material Icons
- **Fonts**: Google Fonts (Poppins)

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudyBuddy
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000`
   - Admin interface: `http://127.0.0.1:8000/admin`

### Environment Configuration

#### Development Settings
The application is configured for development by default with:
- `DEBUG = True`
- SQLite database
- Console email backend
- Local static files serving

#### Production Considerations
For production deployment, update the following in `settings.py`:
- Set `DEBUG = False`
- Configure proper database (PostgreSQL recommended)
- Set up email backend (SMTP)
- Configure static files serving
- Update `ALLOWED_HOSTS`
- Set secure `SECRET_KEY`

---

## User Account Management

### Registration Process

1. **Navigate to Registration**
   - Click "Sign Up" on the homepage
   - Or visit `/auth/register/`

2. **Fill Registration Form**
   - Username (required, unique)
   - Email address (required, unique)
   - Password (with validation)
   - Password confirmation

3. **Automatic Profile Creation**
   - Profile is automatically created upon registration
   - User is redirected to profile setup page

### Login Process

1. **Access Login Page**
   - Click "Login" on homepage
   - Or visit `/auth/login/`

2. **Enter Credentials**
   - Username or email
   - Password

3. **Successful Login**
   - Redirected to dashboard
   - Session maintained across browser tabs

### Password Recovery

1. **Initiate Reset**
   - Click "Forgot Password?" on login page
   - Enter your email address

2. **Check Email**
   - Reset link sent to registered email
   - Link valid for 24 hours

3. **Set New Password**
   - Click link in email
   - Enter new password twice
   - Confirm reset

### Profile Setup

After registration, users are guided through profile completion:

1. **Subject Selection**
   - Choose academic subjects of interest
   - Multiple selections allowed
   - Affects group recommendations

2. **Bio Information**
   - Optional personal description
   - Study goals and preferences
   - Visible to other group members

3. **Notification Preferences**
   - Join request notifications
   - New message alerts
   - New group notifications

--- 