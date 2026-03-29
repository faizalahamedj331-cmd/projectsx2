import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

from core.forms import ProjectSubmissionForm
data = {
    'title': 'Test Project',
    'domain': 'Web Dev',
    'description': 'Test description that is long enough.',
    'guide_name': 'Test Guide',
    'guide_faculty_id': 'TEST123',
}
f = ProjectSubmissionForm(data)
print("Is valid:", f.is_valid())
print("Errors:", f.errors)
print("Cleaned data:", f.cleaned_data)

