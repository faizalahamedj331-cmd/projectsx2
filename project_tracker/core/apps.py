from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Ensure required groups exist after migrations and automatically
        add superusers to the 'Admin' group when they are created.

        This uses Django signals so groups are created on app initialization
        (post-migrate) and superusers are assigned to the Admin group on
        user creation (post-save).
        """
        # Import here to avoid app loading issues at module import time
        from django.db.models.signals import post_migrate, post_save
        from django.contrib.auth.models import Group, User

        def create_user_groups(sender, **kwargs):
            # Create the default groups used by the application
            for group_name in ('Student', 'Faculty', 'Admin'):
                Group.objects.get_or_create(name=group_name)

        def assign_superuser_to_admin(sender, instance, created, **kwargs):
            # If a superuser is created, ensure they belong to the Admin group
            if instance and instance.is_superuser:
                admin_group, _ = Group.objects.get_or_create(name='Admin')
                if not instance.groups.filter(name='Admin').exists():
                    instance.groups.add(admin_group)

        post_migrate.connect(create_user_groups, sender=self)
        post_save.connect(assign_superuser_to_admin, sender=User)
