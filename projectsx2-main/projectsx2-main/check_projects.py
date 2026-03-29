import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

from core.models import Project, StudentProfile

print("All students:")
for s in StudentProfile.objects.all():
    print(f"Student: {s.user.username} (ID: {s.id})")
    projects = Project.objects.filter(student=s)
    print(f"Projects count: {projects.count()}")
    for p in projects:
        print(f"  - {p.title} (status: {p.status}, submitted: {p.submitted_at})")
    print("---")

print("\nAll projects:")
for p in Project.objects.all():
    print(f"Project: {p.title} by student ID {p.student_id} ({p.student.user.username if p.student else 'No student'})")

