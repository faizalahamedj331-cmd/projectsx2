from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Internship


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'domain', 'description', 'guide_name', 'guide_faculty_id', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AI, ML, Web Dev'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Project description...'}),
            'guide_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guide Faculty Name'}),
            'guide_faculty_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guide Faculty Employee ID'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 3:
            raise ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if desc and len(desc.strip()) < 10:
            raise ValidationError('Description must be at least 10 characters long.')
        return desc


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['status', 'faculty_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'faculty_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your remarks...'}),
        }


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['company_name', 'position', 'location', 'start_date', 'end_date', 
                  'description', 'stipend', 'supervisor_name', 'supervisor_email', 'attachment']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position/Role'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internship description...'}),
            'stipend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stipend (e.g., 10000/month)'}),
            'supervisor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supervisor Name'}),
            'supervisor_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Supervisor Email'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class InternshipReviewForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['status', 'faculty_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'faculty_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your remarks...'}),
        }
