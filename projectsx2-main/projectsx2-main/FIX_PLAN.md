c# Fix Plan: Registration Redirect Issue

## Issue Analysis
When a user registers as faculty or student, they see only the admin module instead of their respective dashboards.

After thorough analysis, the issue appears to be in the login_view function. After calling `login(request, user)`, the user object might not properly reflect the group membership because Django caches the user object. The `refresh_from_db()` method might not properly refresh the groups relationship.

## Fix Plan
1. Modify the login_view function to properly refresh the user object from the database after login
2. Instead of using `refresh_from_db()`, we should re-fetch the user from the database using `User.objects.get(pk=user.pk)` to ensure the groups relationship is properly loaded

## Files to Modify
- project_tracker/core/views.py
  - In login_view function, change `user.refresh_from_db()` to `user = User.objects.get(pk=user.pk)` to properly reload the user with groups

## Implementation Steps
1. Edit login_view function in views.py
2. Replace `user.refresh_from_db()` with `user = User.objects.get(pk=user.pk)`
