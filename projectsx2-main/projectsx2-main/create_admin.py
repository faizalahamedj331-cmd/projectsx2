import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Handle multiple users with the same email by keeping one and deleting others
users_with_email = User.objects.filter(email='admin@example.com')
if users_with_email.exists():
    user = users_with_email.first()
    print(f"Admin user found by email, keeping user with id {user.id}.")
    # Delete duplicates
    users_with_email.exclude(id=user.id).delete()
    print("Deleted duplicate users.")
else:
    # If not found by email, check by username 'admin'
    try:
        user = User.objects.get(username='admin')
        print("Admin user found by username 'admin', updating username to email.")
user.username = 'admin@example.com'
user.save()
except User.DoesNotExist:

        user = User.objects.create_superuser('admin@example.com', 'admin@example.com', 'admin123')
        print("Admin user created successfully.")

# Get or create 'Admin' group and add the user to it
admin_group, created = Group.objects.get_or_create(name='Admin')
user.groups.add(admin_group)
user.save()
print("Admin user added to 'Admin' group.")

print("Username: admin@example.com")
print("Password: admin123")
