"""
api_urls.py  –  REST API URL configuration

Include this file in your project's main urls.py like so:

    # project/urls.py
    from django.urls import path, include

    urlpatterns = [
        ...
        path('api/', include('portal.api_urls')),   # adjust app name as needed
    ]

Available endpoints:
--------------------
CRUD (all support GET /list, POST /create, GET /detail, PATCH /partial_update):
    /api/employees/                         list + create
    /api/employees/{id}/                    retrieve, update, delete
    /api/employees/?department=IT           filter by department

    /api/courses/                           list + create
    /api/courses/{id}/                      retrieve, update, delete
    /api/courses/?category=Technical        filter by category

    /api/sessions/                          list + create
    /api/sessions/{id}/                     retrieve, update, delete
    /api/sessions/?instructor_name=Dr.+Lee  filter by instructor
    /api/sessions/?session_date_after=YYYY-MM-DD&session_date_before=YYYY-MM-DD

    /api/enrollments/                       list + create
    /api/enrollments/{id}/                  retrieve, partial update
    /api/enrollments/{id}/complete/         PATCH shortcut → sets status=COMPLETED
    /api/enrollments/?status=COMPLETED      filter by status

Analytics (all read-only GET):
    /api/analytics/course-popularity/              Course Popularity report
    /api/analytics/course-popularity/?category=X  filter by course category
    /api/analytics/department-participation/       Department Participation report
    /api/analytics/transcript/?employee_id=1       Employee Training Transcript
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    EmployeeViewSet,
    CourseViewSet,
    SessionViewSet,
    EnrollmentViewSet,
    CoursePopularityView,
    DepartmentParticipationView,
    EmployeeTranscriptView,
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    # CRUD endpoints
    path('', include(router.urls)),

    # Analytics endpoints
    path('analytics/course-popularity/', CoursePopularityView.as_view(), name='api-course-popularity'),
    path('analytics/department-participation/', DepartmentParticipationView.as_view(), name='api-department-participation'),
    path('analytics/transcript/', EmployeeTranscriptView.as_view(), name='api-transcript'),
]
