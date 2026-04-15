from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/delete/<int:id>/', views.employee_delete, name='employee_delete'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),

    # Sessions
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/add/', views.session_create, name='session_create'),

    # Enrollments
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/add/', views.enrollment_create, name='enrollment_create'),

    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/courses/', views.course_popularity, name='course_popularity'),
    path('analytics/departments/', views.department_participation, name='department_participation'),
    path('analytics/transcript/', views.employee_transcript, name='employee_transcript'),
]