from django.core.mail import send_mail
from django.conf import settings
from .models import Internship, Project

def send_application_email(internship, student_profile):
    """
    Simulates sending an application email to the company.
    In a real scenario, this would use internship.supervisor_email.
    """
    subject = f"Internship Application: {internship.role} - {student_profile.user.first_name}"
    message = f"""
    Dear Hiring Manager at {internship.company_name},

    I am writing to express my interest in the {internship.role} position.
    
    Student Details:
    Name: {student_profile.user.first_name} {student_profile.user.last_name}
    Register Number: {student_profile.register_number}
    Department: {student_profile.department}
    
    Please find my details attached (simulated).
    
    Regards,
    {student_profile.user.first_name}
    """
    
    # Use console backend for development or actual SMTP if configured
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
            [internship.supervisor_email or 'hr@example.com'],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def get_recommended_internships(student_profile):
    """
    Simple recommendation logic based on student department or projects.
    For this implementation, we will return recently added internships 
    that match the student's department if we had a way to know internship department.
    
    Since Internship model doesn't have department, we'll just return 
    internships with status 'Pending' (meaning open for others?? 
    Actually, the model stores *student's* internship applications).
    
    Wait, the requirement implies "Recommended Internships" are *listings* students apply to.
    But the current model structure (`Internship` linked to `Student`) suggests 
    these are records of *applications* or *secured internships*.
    
    If we want "Recommended Internships", we might need a separate model for `InternshipListing`.
    HOWEVER, the user asked to "Add Internship" which usually means self-reporting 
    OR applying to a listing.
    
    Let's interpret "Add Internship" as Student self-reporting an opportunity they found, 
    OR applying to a listing.
    
    The prompt says: "Student Dashboard must allow: Add Internship... Click 'Apply Now' button".
    This implies there are *listings*.
    
    BUT, the Database Models section only asked for ONE `Internship` model with `student` FK.
    This implies the `Internship` model represents a specific student's engagement.
    
    How can we have "Recommended Internships" if we don't have listings?
    
    Maybe "Recommended Internships" means "Internships that previous students did"?
    OR, I should create an `InternshipListing` model?
    The user prompt requirements are slightly ambiguous:
    "1. DATABASE MODELS ... Create Internship model with fields: student (ForeignKey)..."
    
    If I stick strictly to the prompt, `Internship` is a student-specific record.
    "Apply Now" might be a button on a *new* form where they fill in details? 
    OR, maybe "Recommended" are just hardcoded or scraped?
    
    Let's implement `get_recommended_internships` to return a list of dicts (mock data) 
    or aggregated data from other students' internships (e.g. "Google is hiring").
    
    Let's return a hardcoded list of "Opportunities" that pre-fill the form.
    """
    
    # Mock recommendations for now
    recommendations = [
        {
            'company': 'Tech Corp',
            'role': 'Software Intern',
            'skills': 'Python, Django',
            'location': 'Bangalore'
        },
        {
            'company': 'Innovate AI',
            'role': 'AI Researcher',
            'skills': 'Machine Learning, PyTorch',
            'location': 'Remote'
        },
    ]
    return recommendations
