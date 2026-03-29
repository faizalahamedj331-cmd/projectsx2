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
from .forms import ProjectSubmissionForm, ProjectReviewForm, InternshipForm, InternshipReviewForm, StudentRegistrationForm, FacultyRegistrationForm, AdminRegistrationForm
from .decorators import group_required
from django.db.models import Count

import io
try:
    from reportlab.pdfgen import canvas
except ImportError:
    canvas = None


from .utils import send_application_email, get_recommended_internships

# ========== REGISTRATION VIEWS ==========

def student_register(request):
    """
    Handle student registration using StudentRegistrationForm.
    """
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create User
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username=username, password=password)

                # Get or create 'Student' group
                student_group, created = Group.objects.get_or_create(name='Student')
                user.groups.add(student_group)

                # Create StudentProfile
                profile = form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Registration successful! Please login.")
                return redirect('login')

            except Exception as e:
                messages.error(request, f"Error during registration: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'student_register.html', {'form': form})


def faculty_register(request):
    """
    Handle faculty registration using FacultyRegistrationForm.
    """
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create User
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username=username, password=password)

                # Get or create 'Faculty' group
                faculty_group, created = Group.objects.get_or_create(name='Faculty')
                user.groups.add(faculty_group)

                # Create FacultyProfile
                profile = form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Registration successful! Please login.")
                return redirect('login')

            except Exception as e:
                messages.error(request, f"Error during registration: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FacultyRegistrationForm()

    return render(request, 'faculty_register.html', {'form': form})


def admin_register(request):
    """
    Handle admin registration (one-time setup) using AdminRegistrationForm.
    """
    # Check if any admin already exists
    if User.objects.filter(groups__name='Admin').exists():
        messages.error(request, "Admin user already exists! Registration is disabled.")
        return redirect('home')

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create User
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                name = form.cleaned_data['name']
                
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
        else:
             messages.error(request, "Please correct the errors below.")
    else:
        form = AdminRegistrationForm()

    return render(request, 'admin_register.html', {'form': form})


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
        student_profile = StudentProfile.objects.create(
            user=request.user,
            register_number=f'STUD{request.user.id:04d}',
            department='Computer Science',
            year=3,
        )
        messages.info(request, 'Default profile created. Update your details.')


# show student's projects and submission form
    projects = student_profile.projects.all()
    internships = student_profile.internships.all()
    
    form = ProjectSubmissionForm()
    internship_form = InternshipForm()
    
    # Handle project submission
    if request.method == 'POST':
        # Check which form was submitted
        if 'project_submit' in request.POST:
            form = ProjectSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                proj = form.save(commit=False)
                proj.student = student_profile
                # Assign faculty reviewer based on guide_faculty_id (optional)
                if proj.guide_faculty_id:
                    try:
                        faculty = FacultyProfile.objects.get(employee_id=proj.guide_faculty_id)
                        proj.faculty_reviewer = faculty
                    except FacultyProfile.DoesNotExist:
                        messages.warning(request, f"Faculty ID '{proj.guide_faculty_id}' not found. Project saved without assigned reviewer.")
                        proj.faculty_reviewer = None
                proj.save()
                messages.success(request, "Project submitted successfully!")
                return redirect('student_dashboard')
            # If invalid, form has errors, use it in context
        elif 'internship_submit' in request.POST:
            internship_form = InternshipForm(request.POST, request.FILES)
            if internship_form.is_valid():
                internship = internship_form.save(commit=False)
                internship.student = student_profile
                internship.save()
                messages.success(request, "Internship submitted successfully!")
                return redirect('student_dashboard')
            # If invalid, internship_form has errors

    context = {
        'student': student_profile,
        'user': request.user,
        'projects': projects,
        'internships': internships,
        'form': form,
        'internship_form': internship_form,
        'recommended_internships': get_recommended_internships(student_profile),
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
        faculty_profile = FacultyProfile.objects.create(
            user=request.user,
            employee_id=f'F{request.user.id:04d}',
            department='Computer Science',
            designation='Assistant Professor',
        )
        messages.info(request, 'Default profile created. Update your details.')


    # Get filter parameters
    project_status_filter = request.GET.get('project_status', '')
    internship_status_filter = request.GET.get('internship_status', '')

    # Show projects where the current faculty is assigned as the reviewer
    projects = Project.objects.filter(faculty_reviewer=faculty_profile).order_by('-submitted_at')
    
    # Apply project status filter
    if project_status_filter:
        projects = projects.filter(status=project_status_filter)

    # Show all internships for review (faculty can review any internship)
    internships = Internship.objects.all().order_by('-applied_date')
    
    # Apply internship status filter
    if internship_status_filter:
        internships = internships.filter(faculty_status=internship_status_filter)

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
                # No reviewed_at field in new model? I removed it in replacement? 
                # Let's check model again. I think I kept updated_at.
                # If I removed reviewed_at, I should remove this line.
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

    if canvas is None:
        messages.error(request, 'PDF generation requires reportlab: pip install reportlab')
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


@group_required('Faculty')
def generate_internship_report(request, internship_id):
    """
    Generate a simple PDF report for an internship.
    """
    try:
        faculty_profile = FacultyProfile.objects.get(user=request.user)
        internship = Internship.objects.get(pk=internship_id)
    except (FacultyProfile.DoesNotExist, Internship.DoesNotExist):
        messages.error(request, 'Invalid request')
        return redirect('faculty_dashboard')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 14)
    p.drawString(50, 800, f"Internship Report: {internship.company_name}")
    p.setFont('Helvetica', 11)
    p.drawString(50, 780, f"Student: {internship.student.user.username} ({internship.student.register_number})")
    p.drawString(50, 760, f"Role: {internship.role}")
    p.drawString(50, 740, f"Duration: {internship.duration}")
    p.drawString(50, 720, f"Faculty Status: {internship.get_faculty_status_display()}")
    
    y = 700
    p.drawString(50, y, "Description:")
    text = p.beginText(50, y - 15)
    text.textLines(f"{internship.description}\n\nFaculty Remarks:\n{internship.faculty_remarks}")
    p.drawText(text)
    
    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"internship_report_{internship.id}.pdf"
    
    return FileResponse(buffer, as_attachment=True, filename=filename)


@group_required('Admin')
def admin_dashboard(request):
    """
    Admin dashboard - accessible only to users in 'Admin' group.
    Display overview statistics for users and projects.
    """
    # user is guaranteed to be authenticated in Admin group by decorator

    # Get project statistics
    total_students = StudentProfile.objects.count()
    total_faculty = FacultyProfile.objects.count()
    total_projects = Project.objects.count()
    pending_projects = Project.objects.filter(status=Project.STATUS_PENDING).count()
    approved_projects = Project.objects.filter(status=Project.STATUS_APPROVED).count()
    rejected_projects = Project.objects.filter(status=Project.STATUS_REJECTED).count()

    # Get internship statistics
    total_internships = Internship.objects.count()
    pending_internships = Internship.objects.filter(faculty_status=Internship.FACULTY_STATUS_PENDING).count()
    approved_internships = Internship.objects.filter(faculty_status=Internship.FACULTY_STATUS_APPROVED).count()
    rejected_internships = Internship.objects.filter(faculty_status=Internship.FACULTY_STATUS_REJECTED).count()

    # --- Analytics Data ---
    from django.db.models.functions import TruncDate
    from django.utils import timezone
    import datetime

    # 1. Internship Status Distribution
    status_counts = Internship.objects.values('faculty_status').annotate(count=Count('id'))
    status_labels = [item['faculty_status'] for item in status_counts]
    status_values = [item['count'] for item in status_counts]

    # 2. Top 5 Companies
    top_companies_data = Internship.objects.values('company_name').annotate(count=Count('id')).order_by('-count')[:5]
    company_labels = [item['company_name'] for item in top_companies_data]
    company_values = [item['count'] for item in top_companies_data]

    # 3. Application Trend (Last 30 days)
    last_30_days = timezone.now() - datetime.timedelta(days=30)
    trend_data = Internship.objects.filter(applied_date__gte=last_30_days)\
        .annotate(date=TruncDate('applied_date'))\
        .values('date')\
        .annotate(count=Count('id'))\
        .order_by('date')
    
    trend_labels = [item['date'].strftime('%Y-%m-%d') for item in trend_data]
    trend_values = [item['count'] for item in trend_data]

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
        
        # Analytics
        'status_labels': status_labels,
        'status_values': status_values,
        'company_labels': company_labels,
        'company_values': company_values,
        'trend_labels': trend_labels,
        'trend_values': trend_values,
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


# ========== INTERNSHIP VIEWS ==========

@group_required('Student')
def internship_add(request):
    """
    View for students to add/submit an internship.
    """
    if request.method == 'POST':
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.student = StudentProfile.objects.get(user=request.user)
            internship.save()
            messages.success(request, "Internship added successfully!")
            return redirect('student_dashboard')
    else:
        form = InternshipForm()
    
    return render(request, 'internship_form.html', {'form': form, 'title': 'Add Internship'})


@group_required('Student')
def internship_edit(request, internship_id):
    """
    View for students to edit an existing internship (only if not approved).
    """
    internship = Internship.objects.get(pk=internship_id)
    if internship.student.user != request.user:
        messages.error(request, "Access denied!")
        return redirect('student_dashboard')
        
    if internship.faculty_status == Internship.FACULTY_STATUS_APPROVED:
        messages.error(request, "Cannot edit approved internship!")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = InternshipForm(request.POST, request.FILES, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, "Internship updated successfully!")
            return redirect('student_dashboard')
    else:
        form = InternshipForm(instance=internship)
    
    return render(request, 'internship_form.html', {'form': form, 'title': 'Edit Internship'})


@group_required('Student')
def internship_apply(request, internship_id):
    """
    Simulate applying to an internship via email.
    Note: This expects 'internship_id' to be passed, but if we are applying to 
    'Recommended Internships' which aren't in DB yet, we might need a different approach.
    
    However, assuming the flow is: 
    1. Student sees recommendation.
    2. Student clicks 'Apply' -> This might just pre-fill a form OR 
       if the recommendation was an actual Internship object (which it isn't currently), 
       we would update it.
       
    Let's assume this view is for 'Apply Now' on an EXISTING Internship object 
    (e.g. one they added but haven't 'applied' to company yet? 
     Or maybe the 'Recommended' list initiates this?)
    
    If 'Recommended' list items are just dicts, we can't link to `internship_apply/<id>`.
    
    Let's handle the case where student clicks 'Apply' on their OWN internship record 
    to trigger the email.
    """
    try:
        internship = Internship.objects.get(pk=internship_id)
        if internship.student.user != request.user:
            messages.error(request, "Access denied!")
            return redirect('student_dashboard')
            
        student_profile = StudentProfile.objects.get(user=request.user)
        
        if send_application_email(internship, student_profile):
            internship.application_status = Internship.APP_STATUS_APPLIED
            internship.save()
            messages.success(request, f"Application email sent to {internship.company_name}!")
        else:
            messages.error(request, "Failed to send application email.")
            
    except Internship.DoesNotExist:
        messages.error(request, "Internship not found!")
        
    return redirect('student_dashboard')


@group_required('Faculty')
def internship_approve(request, internship_id):
    """
    View for faculty to approve/reject internship.
    """
    try:
        internship = Internship.objects.get(pk=internship_id)
    except Internship.DoesNotExist:
        messages.error(request, "Internship not found!")
        return redirect('faculty_dashboard')

    if request.method == 'POST':
        form = InternshipReviewForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, "Internship status updated!")
            return redirect('faculty_dashboard')
    else:
        form = InternshipReviewForm(instance=internship)
        
    return render(request, 'internship_review.html', {'form': form, 'internship': internship})


def internship_list(request):
    """
    List view (placeholder/utility).
    """
    return redirect('student_dashboard')
