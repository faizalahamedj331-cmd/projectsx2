from django.urls import path
from . import views
from . import api

urlpatterns = [
    # Root — landing page
    path('', views.landing_view, name='home'),
    # Registration URLs
    path('register/student/', views.student_register, name='student_register'),
    path('register/faculty/', views.faculty_register, name='faculty_register'),
    path('register/admin/', views.admin_register, name='admin_register'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/faculty/', views.admin_faculty, name='admin_faculty'),
    path('admin/projects/', views.admin_projects, name='admin_projects'),
    path('admin/students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('admin/faculty/delete/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),
    path('admin/projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),

    path('project/<int:project_id>/generate_report/', views.generate_report, name='generate_report'),
    path('internship/<int:internship_id>/generate_report/', views.generate_internship_report, name='generate_internship_report'),
    
    # API URLs
    path('api/test/', api.test_api, name='test_api'),

    # Internship URLs
    path('internship/add/', views.internship_add, name='internship_add'),
    path('internship/edit/<int:internship_id>/', views.internship_edit, name='internship_edit'),
    path('internship/list/', views.internship_list, name='internship_list'),
    path('internship/approve/<int:internship_id>/', views.internship_approve, name='internship_approve'),
    path('internship/apply/<int:internship_id>/', views.internship_apply, name='internship_apply'),
]
