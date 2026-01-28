from django import forms
from django.core.exceptions import ValidationError
from .models import Project


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'domain', 'description', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AI, ML, Web Dev'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Project description...'}),
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
