from django.urls import path
from . import views

urlpatterns = [
    # Root — redirect to login page
    path('', views.login_view, name='home'),
    # Registration URLs
    path('register/student/', views.student_register, name='student_register'),
    path('register/faculty/', views.faculty_register, name='faculty_register'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('project/<int:project_id>/generate_report/', views.generate_report, name='generate_report'),
]
