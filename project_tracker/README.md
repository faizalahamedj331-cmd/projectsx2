# Student Project & Internship Tracking Platform

A complete Django-based full-stack web application for tracking student projects and internships with role-based access control.

## Project Overview

**Project Title:** Student Project & Internship Tracking Platform  
**Technology Stack:** Python, Django, SQLite, HTML5, CSS3  
**Architecture:** Three-Tier Architecture (Model-View-Template)  
**Database:** SQLite (Development)

## Features

### User Roles
- **Student**: Register, login, view profile, submit projects
- **Faculty**: Register, login, view profile, review student projects

### Key Functionality
✅ User Authentication & Authorization  
✅ Role-Based Access Control (Student & Faculty)  
✅ Student Registration & Profile Management  
✅ Faculty Registration & Profile Management  
✅ Login with Role-Based Redirection  
✅ Secure Logout  
✅ Dashboard Access Control  
✅ Django Admin Panel Integration  

### Future Enhancement
- Project submission and tracking
- Internship management
- Project review system
- Faculty-student mentorship tracking

## Project Structure

```
project_tracker/
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database (auto-generated)
│
├── project_tracker/                   # Main Django project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   ├── wsgi.py                        # WSGI application
│   └── asgi.py                        # ASGI application
│
├── core/                              # Core Django app
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                       # Django admin configuration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # Database models
│   ├── views.py                       # View functions
│   ├── urls.py                        # App URL patterns
│   └── tests.py                       # Unit tests
│
└── templates/                         # HTML templates
    ├── login.html                     # Login page
    ├── student_register.html          # Student registration
    ├── faculty_register.html          # Faculty registration
    ├── student_dashboard.html         # Student dashboard
    └── faculty_dashboard.html         # Faculty dashboard
```

## Database Models

### StudentProfile
```python
- user (OneToOneField → User)
- register_number (CharField, unique)
- department (CharField)
- year (IntegerField: 1-4)
- created_at, updated_at (timestamps)
```

### FacultyProfile
```python
- user (OneToOneField → User)
- employee_id (CharField, unique)
- department (CharField)
- designation (CharField: choices)
- created_at, updated_at (timestamps)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual Environment (recommended)

### Step 1: Create Virtual Environment (Optional but Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Apply Migrations
Initialize the database schema:
```bash
python manage.py migrate
```

### Step 4: Create Superuser (Admin Account)
Create an admin account to access Django admin panel:
```bash
python manage.py createsuperuser
```

Follow the prompts to enter username, email, and password.

### Step 5: Run Development Server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## URL Endpoints

| Endpoint | Purpose | Access |
|----------|---------|--------|
| `/register/student/` | Student registration | Public |
| `/register/faculty/` | Faculty registration | Public |
| `/login/` | User login | Public |
| `/logout/` | User logout | Authenticated |
| `/student/dashboard/` | Student dashboard | Students only |
| `/faculty/dashboard/` | Faculty dashboard | Faculty only |
| `/admin/` | Django admin panel | Superuser only |

## Usage Guide

### As a Student

1. **Register**
   - Go to `http://127.0.0.1:8000/register/student/`
   - Enter username, password, register number, department, and year
   - Submit to create account

2. **Login**
   - Go to `http://127.0.0.1:8000/login/`
   - Enter username and password
   - Automatically redirected to student dashboard

3. **Student Dashboard**
   - View your profile information
   - See your department, year, and register number
   - (Future) Submit projects and track internships

### As Faculty

1. **Register**
   - Go to `http://127.0.0.1:8000/register/faculty/`
   - Enter username, password, employee ID, department, and designation
   - Submit to create account

2. **Login**
   - Go to `http://127.0.0.1:8000/login/`
   - Enter username and password
   - Automatically redirected to faculty dashboard

3. **Faculty Dashboard**
   - View your profile information
   - See your department and designation
   - (Future) Review student projects

### Access Django Admin

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage users, groups, student profiles, and faculty profiles

## User Groups

The application uses Django's built-in Group system:

- **Group: Student** - Users with student access
- **Group: Faculty** - Users with faculty access

Each new student/faculty account is automatically assigned to the appropriate group.

## Security Features

✅ Password hashing using Django's authentication system  
✅ CSRF protection on all forms  
✅ Login required decorators on protected views  
✅ Group-based access control  
✅ User input validation  
✅ SQL injection prevention (via ORM)  

## Django Admin Features

Both StudentProfile and FacultyProfile models are registered in the Django admin with:

- List display with key information
- Search by username, register number, or employee ID
- Filtering by department and year/designation
- Read-only timestamp fields
- Organized fieldsets for better organization

## Testing

Run unit tests:
```bash
python manage.py test
```

Test cases included for:
- StudentProfile creation
- FacultyProfile creation
- User group assignments

## Code Quality

All code includes:
- Detailed comments explaining logic
- Meaningful variable and function names
- Proper error handling
- Clean, readable structure
- PEP 8 compliance

## Common Commands

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Clear database (creates new db)
python manage.py flush

# Open Django shell
python manage.py shell
```

## Troubleshooting

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```
Access at `http://127.0.0.1:8001/`

### Database Issues
```bash
# Delete db.sqlite3 and migrations
# Keep only __init__.py in migrations folder
python manage.py migrate
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Future Enhancements

1. **Project Management**
   - Project submission system
   - Project tracking dashboard
   - Grade/feedback system

2. **Internship Tracking**
   - Internship registration
   - Progress tracking
   - Company information database

3. **Communication**
   - Messaging system between students and faculty
   - Email notifications

4. **Reporting**
   - Project completion reports
   - Internship analytics
   - Skill development tracking

5. **Advanced Features**
   - File upload for projects
   - Real-time notifications
   - API integration
   - Mobile application

## Requirements for UG Final Year Project Review

✅ Clean and readable code  
✅ Well-commented logic explanation  
✅ No advanced/unnecessary features  
✅ Runs using `python manage.py runserver`  
✅ Complete project documentation  
✅ Database models with relationships  
✅ Role-based access control  
✅ Proper error handling  
✅ User-friendly interface  

## Technologies Used

- **Backend**: Django 4.2.8
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3
- **Python**: 3.8+

## Author & License

This project is created as a UG Final Year Project.

---

**Happy Coding! 🚀**

For any issues or questions, refer to the inline code comments or Django documentation at https://docs.djangoproject.com/
