from django.db import models
from django.contrib.auth.models import User

# StudentProfile Model
class StudentProfile(models.Model):
    """
    Model to store student-specific information.
    Links to Django's built-in User model using OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    register_number = models.CharField(max_length=20, unique=True, help_text="Student registration number")
    department = models.CharField(max_length=100, help_text="Department name (e.g., CSE, ECE, ME)")
    year = models.IntegerField(
        choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')],
        help_text="Academic year"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Student Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.register_number}"


# FacultyProfile Model
class FacultyProfile(models.Model):
    """
    Model to store faculty-specific information.
    Links to Django's built-in User model using OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=20, unique=True, help_text="Faculty employee ID")
    department = models.CharField(max_length=100, help_text="Department name (e.g., CSE, ECE, ME)")
    designation = models.CharField(
        max_length=100,
        choices=[
            ('Assistant Professor', 'Assistant Professor'),
            ('Associate Professor', 'Associate Professor'),
            ('Professor', 'Professor'),
            ('Lecturer', 'Lecturer'),
        ],
        help_text="Faculty designation/position"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Faculty Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"


# Project Model
class Project(models.Model):
    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    faculty_reviewer = models.ForeignKey(FacultyProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_projects')
    faculty_remarks = models.TextField(blank=True)
    attachment = models.FileField(upload_to='project_attachments/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.title} ({self.student.register_number})"


# ProjectReport Model
class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    generated_by = models.ForeignKey(FacultyProfile, on_delete=models.SET_NULL, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='project_reports/', null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        by = self.generated_by.user.username if self.generated_by else 'N/A'
        return f"Report for {self.project.title} by {by}"
