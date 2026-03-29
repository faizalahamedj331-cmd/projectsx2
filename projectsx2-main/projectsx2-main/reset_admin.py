import os
import django

# Load Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Remove existing admins
admin_users = User.objects.filter(groups__name='Admin')
print(f"Removing {admin_users.count()} existing admin users...")
admin_users.delete()
print("Existing admins removed.")

# Create new admin superuser
user, created = User.objects.get_or_create(
    username='admin@example.com',
    defaults={'email': 'admin@example.com', 'first_name': 'Admin'}
)
if created or not user.is_superuser:
    user.set_password('admin123456')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("New admin superuser created/updated.")

# Ensure Admin group
admin_group, _ = Group.objects.get_or_create(name='Admin')
user.groups.add(admin_group)

print("✅ Admin ready:")
print("Username: admin@example.com")
print("Password: admin123456")
print("Email: admin@example.com")
print("First name: Admin")
