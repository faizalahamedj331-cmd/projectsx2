from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
import os
from django.core.files.base import ContentFile
from django.urls import reverse
from .models import StudentProfile, FacultyProfile, Project, ProjectReport, Internship
from .forms import ProjectSubmissionForm, ProjectReviewForm, InternshipForm, InternshipReviewForm
from .decorators import group_required
from django.db.models import Count

import io
from reportlab.pdfgen import canvas



# ========== REGISTRATION VIEWS ==========

def student_register(request):
    """
    Handle student registration.
    Create User and assign to 'Student' group, then create StudentProfile.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        register_number = request.POST.get('register_number')
        department = request.POST.get('department')
        year = request.POST.get('year')

        # Validate required fields
        if not all([username, password, register_number, department, year]):
            messages.error(request, "All fields are required!")
            return redirect('student_register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('student_register')

        # Check if register number already exists
        if StudentProfile.objects.filter(register_number=register_number).exists():
            messages.error(request, "Register number already exists!")
            return redirect('student_register')

        try:
            # Create User
            user = User.objects.create_user(username=username, password=password)

            # Get or create 'Student' group
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)

            # Create StudentProfile
            StudentProfile.objects.create(
                user=user,
                register_number=register_number,
                department=department,
                year=year
            )

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('student_register')

    return render(request, 'student_register.html')


def faculty_register(request):
    """
    Handle faculty registration.
    Create User and assign to 'Faculty' group, then create FacultyProfile.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')
        designation = request.POST.get('designation')

        # Validate required fields
        if not all([username, password, employee_id, department, designation]):
            messages.error(request, "All fields are required!")
            return redirect('faculty_register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('faculty_register')

        # Check if employee ID already exists
        if FacultyProfile.objects.filter(employee_id=employee_id).exists():
            messages.error(request, "Employee ID already exists!")
            return redirect('faculty_register')

        try:
            # Create User
            user = User.objects.create_user(username=username, password=password)

            # Get or create 'Faculty' group
            faculty_group, created = Group.objects.get_or_create(name='Faculty')
            user.groups.add(faculty_group)

            # Create FacultyProfile
            FacultyProfile.objects.create(
                user=user,
                employee_id=employee_id,
                department=department,
                designation=designation
            )

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('faculty_register')

    return render(request, 'faculty_register.html')


def admin_register(request):
    """
    Handle admin registration (one-time setup).
    Create User and assign to 'Admin' group. No profile needed.
    """
    # Check if any admin already exists
    if User.objects.filter(groups__name='Admin').exists():
        messages.error(request, "Admin user already exists! Registration is disabled.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate required fields
        if not all([name, email, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return redirect('admin_register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('admin_register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('admin_register')

        try:
            # Create User
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            user.is_staff = True  # Give admin access to Django admin
            user.is_superuser = True
            user.save()

            # Get or create 'Admin' group
            admin_group, created = Group.objects.get_or_create(name='Admin')
            user.groups.add(admin_group)

            messages.success(request, "Admin registration successful! Please login.")
            return redirect('admin_login')

        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('admin_register')

    return render(request, 'admin_register.html')


# ========== LOGIN & LOGOUT VIEWS ==========

def login_view(request):
    """
    Common login page for both students and faculty.
    Authenticates user and redirects based on their group membership.
    """
    if request.user.is_authenticated:
        # Re-fetch user from database to get latest group membership
        user = User.objects.get(pk=request.user.pk)
        
        # If user is already logged in, redirect to appropriate dashboard
        if user.groups.filter(name='Student').exists():
            return redirect('student_dashboard')
        elif user.groups.filter(name='Faculty').exists():
            return redirect('faculty_dashboard')
        elif user.groups.filter(name='Admin').exists():
            return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            
            # Re-fetch user from database to get latest group membership
            user = User.objects.get(pk=user.pk)

            # Redirect based on group membership
            if user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            elif user.groups.filter(name='Faculty').exists():
                return redirect('faculty_dashboard')
            elif user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Your account is not associated with any group. Please contact admin.")
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')


def admin_login(request):
    """
    Admin login page.
    Authenticates using email & password, checks if role == "Admin".
    """
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Admin').exists():
            return redirect('admin_dashboard')
        else:
            messages.error(request, "You are not authorized to access admin login!")
            return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None and user.groups.filter(name='Admin').exists():
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid email or password, or you are not an admin!")
            return redirect('admin_login')

    return render(request, 'admin/login.html')


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')


# ========== LANDING PAGE VIEW ==========

def landing_view(request):
    """
    Landing page with selection for Student, Faculty, Admin.
    """
    from django.contrib.auth.models import User
    admin_exists = User.objects.filter(groups__name='Admin').exists()
    context = {
        'admin_exists': admin_exists,
    }
    return render(request, 'landing.html', context)


# ========== DASHBOARD VIEWS ==========

@group_required('Student')
def student_dashboard(request):
    """
    Student dashboard - accessible only to users in 'Student' group.
    Display student profile information, projects, and internships.
    """
    # user is guaranteed to be authenticated and in Student group by decorator

    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found!")
        return redirect('login')

    # show student's projects and submission form
    projects = student_profile.projects.all()
    internships = student_profile.internships.all()
    
    # Handle project submission
    if request.method == 'POST':
        # Check which form was submitted
        if 'project_submit' in request.POST:
            form = ProjectSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                proj = form.save(commit=False)
                proj.student = student_profile
                # Assign faculty reviewer based on guide_faculty_id.
                try:
                    if proj.guide_faculty_id:
                        faculty = FacultyProfile.objects.get(employee_id=proj.guide_faculty_id)
                        proj.faculty_reviewer = faculty
                except FacultyProfile.DoesNotExist:
                    messages.error(request, f"No faculty found with Employee ID: {proj.guide_faculty_id}. Please check the ID.")
                    return redirect('student_dashboard')
                proj.save()
                messages.success(request, "Project submitted successfully!")
                return redirect('student_dashboard')
        elif 'internship_submit' in request.POST:
            internship_form = InternshipForm(request.POST, request.FILES)
            if internship_form.is_valid():
                internship = internship_form.save(commit=False)
                internship.student = student_profile
                internship.save()
                messages.success(request, "Internship submitted successfully!")
                return redirect('student_dashboard')
    else:
        form = ProjectSubmissionForm()
        internship_form = InternshipForm()

    context = {
        'student': student_profile,
        'user': request.user,
        'projects': projects,
        'internships': internships,
        'form': form,
        'internship_form': internship_form,
    }
    return render(request, 'student_dashboard.html', context)


@group_required('Faculty')
def faculty_dashboard(request):
    """
    Faculty dashboard - accessible only to users in 'Faculty' group.
    Display faculty profile information, project review, and internship review.
    """
    # user is guaranteed to be authenticated and in Faculty group by decorator

    try:
        faculty_profile = FacultyProfile.objects.get(user=request.user)
    except FacultyProfile.DoesNotExist:
        messages.error(request, "Faculty profile not found!")
        return redirect('login')

    # Get filter parameters
    project_status_filter = request.GET.get('project_status', '')
    internship_status_filter = request.GET.get('internship_status', '')

    # Show projects where the current faculty is assigned as the reviewer
    projects = Project.objects.filter(faculty_reviewer=faculty_profile).order_by('-submitted_at')
    
    # Apply project status filter
    if project_status_filter:
        projects = projects.filter(status=project_status_filter)

    # Show all internships for review (faculty can review any internship)
    internships = Internship.objects.all().order_by('-submitted_at')
    
    # Apply internship status filter
    if internship_status_filter:
        internships = internships.filter(status=internship_status_filter)

    # Handle project review
    if request.method == 'POST':
        if 'project_review' in request.POST:
            pid = request.POST.get('project_id')
            try:
                project = Project.objects.get(pk=pid)
            except Project.DoesNotExist:
                messages.error(request, 'Project not found')
                return redirect('faculty_dashboard')

            review_form = ProjectReviewForm(request.POST, instance=project)
            if review_form.is_valid():
                proj = review_form.save(commit=False)
                proj.faculty_reviewer = faculty_profile
                if proj.status != Project.STATUS_PENDING:
                    from django.utils import timezone
                    proj.reviewed_at = timezone.now()
                proj.save()
                messages.success(request, 'Project updated')
                return redirect('faculty_dashboard')
        
        # Handle internship review
        elif 'internship_review' in request.POST:
            iid = request.POST.get('internship_id')
            try:
                internship = Internship.objects.get(pk=iid)
            except Internship.DoesNotExist:
                messages.error(request, 'Internship not found')
                return redirect('faculty_dashboard')

            review_form = InternshipReviewForm(request.POST, instance=internship)
            if review_form.is_valid():
                intern = review_form.save(commit=False)
                if intern.status != Internship.STATUS_PENDING:
                    from django.utils import timezone
                    intern.reviewed_at = timezone.now()
                intern.save()
                messages.success(request, 'Internship updated')
                return redirect('faculty_dashboard')

    review_form = ProjectReviewForm()
    internship_review_form = InternshipReviewForm()
    context = {
        'faculty': faculty_profile,
        'user': request.user,
        'projects': projects,
        'internships': internships,
        'review_form': review_form,
        'internship_review_form': internship_review_form,
        'project_status_filter': project_status_filter,
        'internship_status_filter': internship_status_filter,
    }
    return render(request, 'faculty_dashboard.html', context)


@group_required('Faculty')
def generate_report(request, project_id):
    """
    Generate a simple PDF report for a project, save it to ProjectReport.
    """
    # user is guaranteed to be authenticated and in Faculty group by decorator

    try:
        faculty_profile = FacultyProfile.objects.get(user=request.user)
        project = Project.objects.get(pk=project_id)
    except (FacultyProfile.DoesNotExist, Project.DoesNotExist):
        messages.error(request, 'Invalid request')
        return redirect('faculty_dashboard')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 14)
    p.drawString(50, 800, f"Project Report: {project.title}")
    p.setFont('Helvetica', 11)
    p.drawString(50, 780, f"Student: {project.student.user.username} ({project.student.register_number})")
    p.drawString(50, 760, f"Domain: {project.domain}")
    p.drawString(50, 740, f"Status: {project.get_status_display()}")
    text = p.beginText(50, 720)
    text.textLines(f"Description:\n{project.description}\n\nFaculty Remarks:\n{project.faculty_remarks}")
    p.drawText(text)
    p.showPage()
    p.save()

    buffer.seek(0)
    content = buffer.read()
    filename = f"project_report_{project.id}.pdf"

    report = ProjectReport.objects.create(project=project, generated_by=faculty_profile)
    report.pdf_file.save(filename, ContentFile(content))
    report.save()

    # Return the generated PDF as a download response
    try:
        file_path = report.pdf_file.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    except Exception:
        # fallback to dashboard with message
        messages.warning(request, 'Report generated and saved, but could not be served for download.')

    return redirect('faculty_dashboard')


@group_required('Admin')
def admin_dashboard(request):
    """
    Admin dashboard - accessible only to users in 'Admin' group.
    Display overview statistics for users and projects.
    """
    # user is guaranteed to be authenticated and in Admin group by decorator

    # Get project statistics
    total_students = StudentProfile.objects.count()
    total_faculty = FacultyProfile.objects.count()
    total_projects = Project.objects.count()
    pending_projects = Project.objects.filter(status=Project.STATUS_PENDING).count()
    approved_projects = Project.objects.filter(status=Project.STATUS_APPROVED).count()
    rejected_projects = Project.objects.filter(status=Project.STATUS_REJECTED).count()

    # Get internship statistics
    total_internships = Internship.objects.count()
    pending_internships = Internship.objects.filter(status=Internship.STATUS_PENDING).count()
    approved_internships = Internship.objects.filter(status=Internship.STATUS_APPROVED).count()
    rejected_internships = Internship.objects.filter(status=Internship.STATUS_REJECTED).count()

    context = {
        'user': request.user,
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_projects': total_projects,
        'pending_projects': pending_projects,
        'approved_projects': approved_projects,
        'rejected_projects': rejected_projects,
        'total_internships': total_internships,
        'pending_internships': pending_internships,
        'approved_internships': approved_internships,
        'rejected_internships': rejected_internships,
    }
    return render(request, 'admin/dashboard.html', context)


@group_required('Admin')
def admin_students(request):
    """
    View all students - accessible only to users in 'Admin' group.
    Display table with Name, Email, Department, Year, Delete button.
    """
    students = StudentProfile.objects.select_related('user').all()
    context = {
        'user': request.user,
        'students': students,
    }
    return render(request, 'admin/students.html', context)


@group_required('Admin')
def admin_faculty(request):
    """
    View all faculty - accessible only to users in 'Admin' group.
    Display table with Name, Email, Department, Delete button.
    """
    faculty = FacultyProfile.objects.select_related('user').all()
    context = {
        'user': request.user,
        'faculty': faculty,
    }
    return render(request, 'admin/faculty.html', context)


@group_required('Admin')
def admin_projects(request):
    """
    View all projects - accessible only to users in 'Admin' group.
    Display table with Student Name, Title, Description, Status, Assigned Faculty, Delete button.
    """
    projects = Project.objects.select_related('student__user', 'faculty_reviewer__user').all()
    context = {
        'user': request.user,
        'projects': projects,
    }
    return render(request, 'admin/projects.html', context)


@group_required('Admin')
def delete_student(request, student_id):
    """
    Delete a student - accessible only to users in 'Admin' group.
    """
    try:
        student = StudentProfile.objects.get(pk=student_id)
        student.user.delete()  # This will cascade delete the profile
        messages.success(request, "Student deleted successfully!")
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student not found!")
    return redirect('admin_students')


@group_required('Admin')
def delete_faculty(request, faculty_id):
    """
    Delete a faculty - accessible only to users in 'Admin' group.
    """
    try:
        faculty = FacultyProfile.objects.get(pk=faculty_id)
        faculty.user.delete()  # This will cascade delete the profile
        messages.success(request, "Faculty deleted successfully!")
    except FacultyProfile.DoesNotExist:
        messages.error(request, "Faculty not found!")
    return redirect('admin_faculty')


@group_required('Admin')
def delete_project(request, project_id):
    """
    Delete a project - accessible only to users in 'Admin' group.
    """
    try:
        project = Project.objects.get(pk=project_id)
        project.delete()
        messages.success(request, "Project deleted successfully!")
    except Project.DoesNotExist:
        messages.error(request, "Project not found!")
    return redirect('admin_projects')
