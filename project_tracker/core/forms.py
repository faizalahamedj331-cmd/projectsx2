from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Project, Internship, StudentProfile, FacultyProfile


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


class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = StudentProfile
        fields = ['register_number', 'department', 'year']
        widgets = {
            'register_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Register Number'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'year': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_register_number(self):
        reg_no = self.cleaned_data.get('register_number')
        if StudentProfile.objects.filter(register_number=reg_no).exists():
            raise ValidationError("Register number already exists")
        return reg_no


class FacultyRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = FacultyProfile
        fields = ['employee_id', 'department', 'designation']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_employee_id(self):
        emp_id = self.cleaned_data.get('employee_id')
        if FacultyProfile.objects.filter(employee_id=emp_id).exists():
            raise ValidationError("Employee ID already exists")
        return emp_id


class AdminRegistrationForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
