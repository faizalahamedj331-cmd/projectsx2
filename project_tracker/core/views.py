from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
import os
from django.core.files.base import ContentFile
from django.urls import reverse
from .models import StudentProfile, FacultyProfile, Project, ProjectReport
from .forms import ProjectSubmissionForm, ProjectReviewForm
from .decorators import group_required

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


# ========== LOGIN & LOGOUT VIEWS ==========

def login_view(request):
    """
    Common login page for both students and faculty.
    Authenticates user and redirects based on their group membership.
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to appropriate dashboard
        if request.user.groups.filter(name='Student').exists():
            return redirect('student_dashboard')
        elif request.user.groups.filter(name='Faculty').exists():
            return redirect('faculty_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")

            # Redirect based on group membership
            if user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            elif user.groups.filter(name='Faculty').exists():
                return redirect('faculty_dashboard')
            else:
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')


# ========== DASHBOARD VIEWS ==========

@group_required('Student')
def student_dashboard(request):
    """
    Student dashboard - accessible only to users in 'Student' group.
    Display student profile information and project placeholder.
    """
    # user is guaranteed to be authenticated and in Student group by decorator

    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found!")
        return redirect('login')

    # show student's projects and submission form
    projects = student_profile.projects.all()
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.student = student_profile
            proj.save()
            return redirect('student_dashboard')
    else:
        form = ProjectSubmissionForm()

    context = {
        'student': student_profile,
        'user': request.user,
        'projects': projects,
        'form': form,
    }
    return render(request, 'student_dashboard.html', context)


@group_required('Faculty')
def faculty_dashboard(request):
    """
    Faculty dashboard - accessible only to users in 'Faculty' group.
    Display faculty profile information and project review placeholder.
    """
    # user is guaranteed to be authenticated and in Faculty group by decorator

    try:
        faculty_profile = FacultyProfile.objects.get(user=request.user)
    except FacultyProfile.DoesNotExist:
        messages.error(request, "Faculty profile not found!")
        return redirect('login')

    # show projects pending review
    projects = Project.objects.all().order_by('-submitted_at')

    # optional review handling
    if request.method == 'POST':
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

    review_form = ProjectReviewForm()
    context = {
        'faculty': faculty_profile,
        'user': request.user,
        'projects': projects,
        'review_form': review_form,
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
