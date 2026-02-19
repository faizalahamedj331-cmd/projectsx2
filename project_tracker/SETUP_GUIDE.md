# Quick Start Guide - Setup Instructions

## 🚀 Quick Start (One-Click)

To run the entire application (Backend + Frontend):

```powershell
.\manage.bat runserver
```

This will:
1. Start the React Frontend in a separate window.
2. Start the Django Backend in the current window.

You can also use `.\manage.bat` to run other Django commands from the root, for example:
```powershell
.\manage.bat migrate
.\manage.bat createsuperuser
```

---

## Complete Setup in 5 Minutes

### 1️⃣ Install Python Dependencies
Open PowerShell/Command Prompt in the `project_tracker` folder and run:

```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize Database
```bash
python manage.py migrate
```

This creates the SQLite database and all required tables.

### 3️⃣ Create Admin Account
```bash
python manage.py createsuperuser
```

Enter your preferred credentials (e.g., username: `admin`, password: `admin123`)

### 4️⃣ Start Development Server
```bash
python manage.py runserver
```

You'll see output like:
```
Starting development server at http://127.0.0.1:8000/
```

### 5️⃣ Access the Application

**Main Application:**
- Login Page: http://127.0.0.1:8000/login/
- Student Register: http://127.0.0.1:8000/register/student/
- Faculty Register: http://127.0.0.1:8000/register/faculty/

**Admin Panel:**
- Admin: http://127.0.0.1:8000/admin/ (use superuser credentials)

---

## Test User Creation (Optional)

### Create Test Student

1. Go to `http://127.0.0.1:8000/register/student/`
2. Fill in the form:
   - Username: `student1`
   - Password: `Test@123`
   - Register Number: `CS001`
   - Department: `Computer Science`
   - Year: `3rd Year`
3. Click Register

### Create Test Faculty

1. Go to `http://127.0.0.1:8000/register/faculty/`
2. Fill in the form:
   - Username: `faculty1`
   - Password: `Test@123`
   - Employee ID: `FAC001`
   - Department: `Computer Science`
   - Designation: `Assistant Professor`
3. Click Register

### Test Login

1. Go to `http://127.0.0.1:8000/login/`
2. Login with created credentials
3. You should be redirected to appropriate dashboard

---

## Files Created

### Django Project Files
- ✅ `manage.py` - Django management script
- ✅ `requirements.txt` - Dependencies
- ✅ `db.sqlite3` - Database (auto-created)

### Configuration Files
- ✅ `project_tracker/settings.py`
- ✅ `project_tracker/urls.py`
- ✅ `project_tracker/wsgi.py`
- ✅ `project_tracker/asgi.py`
- ✅ `project_tracker/__init__.py`

### Core App Files
- ✅ `core/models.py` - Database models
- ✅ `core/views.py` - View logic
- ✅ `core/urls.py` - URL patterns
- ✅ `core/admin.py` - Admin configuration
- ✅ `core/apps.py` - App configuration
- ✅ `core/tests.py` - Unit tests

### Templates
- ✅ `templates/login.html`
- ✅ `templates/student_register.html`
- ✅ `templates/faculty_register.html`
- ✅ `templates/student_dashboard.html`
- ✅ `templates/faculty_dashboard.html`

---

## Project Features Implemented

### User Management
- ✅ Student Registration with profile
- ✅ Faculty Registration with profile
- ✅ Common Login Page
- ✅ Role-Based Redirection
- ✅ Secure Logout

### Access Control
- ✅ Login Required on Protected Pages
- ✅ Group-Based Access Control
- ✅ Student/Faculty Dashboard Separation
- ✅ Dashboard-Specific Data Display

### Admin Interface
- ✅ StudentProfile Management
- ✅ FacultyProfile Management
- ✅ Search & Filter Capabilities
- ✅ User Group Management

### Database
- ✅ SQLite Database
- ✅ StudentProfile Model
- ✅ FacultyProfile Model
- ✅ User Relationships
- ✅ Timestamps on Models

---

## Architecture Overview

```
Three-Tier Architecture

┌─────────────────────────┐
│   Presentation Layer    │
│  (HTML Templates/CSS)   │
│  - login.html           │
│  - *_register.html      │
│  - *_dashboard.html     │
└────────────┬────────────┘
             │ HTTP Requests
             ↓
┌─────────────────────────┐
│   Business Logic Layer  │
│  (Django Views)         │
│  - Registration Logic   │
│  - Authentication       │
│  - Access Control       │
└────────────┬────────────┘
             │ ORM Queries
             ↓
┌─────────────────────────┐
│   Data Access Layer     │
│  (Models/Database)      │
│  - User Model           │
│  - StudentProfile       │
│  - FacultyProfile       │
│  - SQLite Database      │
└─────────────────────────┘
```

---

## Common Issues & Solutions

### Issue: Port 8000 Already in Use
**Solution:**
```bash
python manage.py runserver 8001
```

### Issue: Module Not Found Error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database Errors
**Solution:**
```bash
python manage.py migrate
```

### Issue: CSRF Token Missing
**Solution:** Ensure form includes `{% csrf_token %}`
(Already included in all templates)

---

## Next Steps for Development

1. **Extend Models** - Add Project and Internship models
2. **Add Project Submission** - Create project submission views
3. **Implement File Upload** - Allow document uploads
4. **Add Search/Filter** - Search student projects by department
5. **Create API** - Build REST API endpoints
6. **Add Testing** - Expand unit test coverage
7. **Deploy** - Deploy to production server (Heroku, AWS, etc.)

---

## Useful Django Commands

```bash
# List all URLs
python manage.py show_urls

# Create backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json

# Run shell
python manage.py shell

# Check for issues
python manage.py check
```

---

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Python Documentation: https://docs.python.org/3/
- SQLite Documentation: https://www.sqlite.org/docs.html

---

**You're all set! Start the server and enjoy the application! 🎉**
