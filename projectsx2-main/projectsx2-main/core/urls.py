from django.urls import path
from . import views_fixed
from . import api

urlpatterns = [
    # Root — landing page
path('', views_fixed.landing_view, name='home'),
    # Registration URLs
path('register/student/', views_fixed.student_register, name='student_register'),
path('register/faculty/', views_fixed.faculty_register, name='faculty_register'),
path('register/admin/', views_fixed.admin_register, name='admin_register'),

    # Authentication URLs
path('login/', views_fixed.login_view, name='login'),
path('logout/', views_fixed.logout_view, name='logout'),

    # Dashboard URLs
path('student/dashboard/', views_fixed.student_dashboard, name='student_dashboard'),
path('faculty/dashboard/', views_fixed.faculty_dashboard, name='faculty_dashboard'),
path('admin/dashboard/', views_fixed.admin_dashboard, name='admin_dashboard'),

    # Admin URLs
path('admin/login/', views_fixed.admin_login, name='admin_login'),
path('admin/students/', views_fixed.admin_students, name='admin_students'),
path('admin/faculty/', views_fixed.admin_faculty, name='admin_faculty'),
path('admin/projects/', views_fixed.admin_projects, name='admin_projects'),
path('admin/students/delete/<int:student_id>/', views_fixed.delete_student, name='delete_student'),
path('admin/faculty/delete/<int:faculty_id>/', views_fixed.delete_faculty, name='delete_faculty'),
path('admin/projects/delete/<int:project_id>/', views_fixed.delete_project, name='delete_project'),

path('project/<int:project_id>/generate_report/', views_fixed.generate_report, name='generate_report'),
path('internship/<int:internship_id>/generate_report/', views_fixed.generate_internship_report, name='generate_internship_report'),
    
    # API URLs
path('api/test/', api.test_api, name='test_api'),

    # Internship URLs
path('internship/add/', views_fixed.internship_add, name='internship_add'),
path('internship/edit/<int:internship_id>/', views_fixed.internship_edit, name='internship_edit'),
path('internship/list/', views_fixed.internship_list, name='internship_list'),
path('internship/approve/<int:internship_id>/', views_fixed.internship_approve, name='internship_approve'),
path('internship/apply/<int:internship_id>/', views_fixed.internship_apply, name='internship_apply'),
]
