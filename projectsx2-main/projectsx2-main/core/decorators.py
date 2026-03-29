from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def group_required(group_name, login_url='login'):
    """Decorator to require user be authenticated and in a given group.

    Usage:
        @group_required('Faculty')
        def view(...):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect(login_url)
            if not user.groups.filter(name=group_name).exists():
                messages.error(request, "You do not have permission to access this page!")
                return redirect(login_url)
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
