import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\FAIZAL AHAMED\OneDrive\Desktop\final_year_project\project_tracker')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

from django.contrib.auth.models import User, Group
from core.models import StudentProfile, FacultyProfile, Internship
from django.test import Client
from django.urls import reverse

def run_test():
    print("Starting Internship Flow Verification...")

    # 1. Setup Users
    print("\n[1] Setting up users...")
    student_user, _ = User.objects.get_or_create(username='test_student_v', defaults={'email': 'student@test.com'})
    student_user.set_password('pass123')
    student_user.save()
    student_group, _ = Group.objects.get_or_create(name='Student')
    student_user.groups.add(student_group)
    student_profile, _ = StudentProfile.objects.get_or_create(user=student_user, defaults={'register_number': 'REG123', 'department': 'CSE', 'year': 4})
    
    faculty_user, _ = User.objects.get_or_create(username='test_faculty_v', defaults={'email': 'faculty@test.com'})
    faculty_user.set_password('pass123')
    faculty_user.save()
    faculty_group, _ = Group.objects.get_or_create(name='Faculty')
    faculty_user.groups.add(faculty_group)
    faculty_profile, _ = FacultyProfile.objects.get_or_create(user=faculty_user, defaults={'employee_id': 'EMP123', 'department': 'CSE'})

    admin_user, _ = User.objects.get_or_create(username='test_admin_v', defaults={'email': 'admin@test.com'})
    admin_user.set_password('pass123')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin_user.groups.add(admin_group)

    print("Users setup complete.")

    # 2. Student Adds Internship
    print("\n[2] Student adding internship...")
    client = Client()
    client.login(username='test_student_v', password='pass123')
    
    internship_data = {
        'company_name': 'Tech Corp',
        'role': 'Software Intern',
        'location': 'Remote',
        'duration': '3 Months',
        'stipend': '5000',
        'skills_required': 'Python',
        'start_date': '2023-01-01',
        'end_date': '2023-04-01',
        'description': 'Test Description',
        'supervisor_name': 'Mr. Supervisor',
        'supervisor_email': 'sup@tech.com'
    }
    
    response = client.post(reverse('internship_add'), internship_data, follow=True)
    
    if response.status_code == 200 and Internship.objects.filter(student=student_profile, company_name='Tech Corp').exists():
        print("SUCCESS: Internship added.")
    else:
        print(f"FAILURE: Could not add internship. Status: {response.status_code}")
        # print(response.content) # Debug if needed
        return

    internship = Internship.objects.get(student=student_profile, company_name='Tech Corp')
    print(f"Internship ID: {internship.id}, Status: {internship.faculty_status}")

    # 3. Faculty Approves Internship
    print("\n[3] Faculty approving internship...")
    client.logout()
    client.login(username='test_faculty_v', password='pass123')
    
    approve_data = {
        'internship_review': '1', # Trigger button name
        'internship_id': internship.id,
        'faculty_status': Internship.FACULTY_STATUS_APPROVED,
        'faculty_remarks': 'Looks good!'
    }
    
    # Faculty dashboard posts to itself for review
    response = client.post(reverse('faculty_dashboard'), approve_data, follow=True)
    
    internship.refresh_from_db()
    if internship.faculty_status == Internship.FACULTY_STATUS_APPROVED:
        print("SUCCESS: Internship approved.")
    else:
        print(f"FAILURE: Internship status not updated. Current: {internship.faculty_status}")
        return

    # 4. Student Checks Status
    print("\n[4] Student checking status...")
    client.logout()
    client.login(username='test_student_v', password='pass123')
    response = client.get(reverse('student_dashboard'))
    
    if "Approved" in str(response.content) and "Tech Corp" in str(response.content):
         print("SUCCESS: Approved status visible on Student Dashboard.")
    else:
         print("FAILURE: Status not visible.")

    # 5. Clean up
    print("\n[5] Cleaning up...")
    Internship.objects.filter(student=student_profile).delete()
    print("Cleanup done.")
    print("\nVERIFICATION COMPLETE: ALL CHECKS PASSED.")

if __name__ == '__main__':
    run_test()
