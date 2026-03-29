# Complete Setup Guide - Student Project & Internship Tracker

## Prerequisites
1. Install Python 3.10+
2. Install MySQL Server, create DB `progresso`
3. VSCode with Python extension

## Step-by-Step Setup

### 1. Navigate to project
```
cd "c:/Users/FAIZAL AHAMED/OneDrive/Desktop/Final year project 2/projectsx2-main/projectsx2-main"
```

### 2. Virtual Environment
```
python -m venv .venv
.venv\\Scripts\\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
pip install mysqlclient reportlab django-cors-headers
```

### 4. MySQL Setup
```
mysql -u root -p123456
CREATE DATABASE progresso;
exit
```

### 5. Django Setup
```
python manage.py makemigrations
python manage.py migrate
python create_admin.py
python manage.py createsuperuser
```

### 6. Run Server
```
python manage.py runserver
```

### 7. Access
- Landing: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/django-admin/

**All navigations work after setup! Register Student/Faculty/Admin, login redirects to dashboard.**

## Troubleshooting
- Connection refused: Run `python manage.py runserver`
- DB error: Check MySQL running, DB exists
- ImportError: `pip install -r requirements.txt`

