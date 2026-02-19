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
    print("Starting Internship Report Verification...")

    # 1. Setup Users (Reusing or creating if not exist)
    print("\n[1] Setting up users...")
    student_user, _ = User.objects.get_or_create(username='test_student_rep', defaults={'email': 'student_rep@test.com'})
    student_user.set_password('pass123')
    student_user.save()
    student_group, _ = Group.objects.get_or_create(name='Student')
    student_user.groups.add(student_group)
    student_profile, _ = StudentProfile.objects.get_or_create(user=student_user, defaults={'register_number': 'REG_REP', 'department': 'CSE', 'year': 4})
    
    faculty_user, _ = User.objects.get_or_create(username='test_faculty_rep', defaults={'email': 'faculty_rep@test.com'})
    faculty_user.set_password('pass123')
    faculty_user.save()
    faculty_group, _ = Group.objects.get_or_create(name='Faculty')
    faculty_user.groups.add(faculty_group)
    faculty_profile, _ = FacultyProfile.objects.get_or_create(user=faculty_user, defaults={'employee_id': 'EMP_REP', 'department': 'CSE'})

    # 2. Setup Internship
    print("\n[2] Creating internship...")
    internship, _ = Internship.objects.get_or_create(student=student_profile, company_name='Report Corp', defaults={
        'role': 'Reporter',
        'location': 'Remote',
        'duration': '1 Month',
        'faculty_status': Internship.FACULTY_STATUS_APPROVED,
        'faculty_remarks': 'Excellent work.'
    })
    
    # 3. Generate Report
    print("\n[3] Generating report as Faculty...")
    client = Client()
    client.login(username='test_faculty_rep', password='pass123')
    
    url = reverse('generate_internship_report', args=[internship.id])
    response = client.get(url)
    
    if response.status_code == 200:
        print("SUCCESS: Report generated.")
        if response['Content-Type'] == 'application/pdf':
             print("SUCCESS: Content-Type is PDF.")
        else:
             print(f"FAILURE: Content-Type is {response['Content-Type']}")
        
        # Check filename
        if f"internship_report_{internship.id}.pdf" in response['Content-Disposition']:
             print("SUCCESS: Filename matches.")
        else:
             print(f"FAILURE: Filename mismatch. Got: {response['Content-Disposition']}")

    else:
        print(f"FAILURE: Status code {response.status_code}")

    # 4. Clean up
    print("\n[4] Cleaning up...")
    internship.delete()
    print("Cleanup done.")
    print("\nVERIFICATION COMPLETE.")

if __name__ == '__main__':
    run_test()
