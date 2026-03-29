from django.contrib import admin
from .models import StudentProfile, FacultyProfile, Project, ProjectReport


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """
    Django admin configuration for StudentProfile.
    Displays student information in a user-friendly format.
    """
    list_display = ('user', 'register_number', 'department', 'year', 'created_at')
    list_filter = ('department', 'year', 'created_at')
    search_fields = ('user__username', 'register_number', 'department')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Student Details', {
            'fields': ('register_number', 'department', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    """
    Django admin configuration for FacultyProfile.
    Displays faculty information in a user-friendly format.
    """
    list_display = ('user', 'employee_id', 'department', 'designation', 'created_at')
    list_filter = ('department', 'designation', 'created_at')
    search_fields = ('user__username', 'employee_id', 'department')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Faculty Details', {
            'fields': ('employee_id', 'department', 'designation')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'status', 'faculty_reviewer', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('title', 'student__register_number', 'student__user__username', 'domain')
    readonly_fields = ('submitted_at', 'reviewed_at', 'updated_at')


@admin.register(ProjectReport)
class ProjectReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'generated_by', 'generated_at')
    readonly_fields = ('generated_at',)
