from django.db.models import Count, Q
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Employee, Course, Session, Enrollment
from .serializers import (
    EmployeeSerializer,
    CourseSerializer,
    SessionSerializer,
    EnrollmentSerializer,
    CoursePopularitySerializer,
    DepartmentParticipationSerializer,
    TranscriptEntrySerializer,
)


# ── CRUD ViewSets ─────────────────────────────────────────────────────────────

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Employee.

    Filtering:
        GET /api/employees/?department=IT
    Search:
        GET /api/employees/?search=john
    """
    queryset = Employee.objects.all().order_by('full_name')
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department']
    search_fields = ['full_name', 'email']


class CourseViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Course.

    Filtering:
        GET /api/courses/?category=Technical
    """
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']


class SessionViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Session.

    Filtering:
        GET /api/sessions/?instructor_name=Dr.+Lee
        GET /api/sessions/?session_date_after=2025-01-01&session_date_before=2025-12-31
        GET /api/sessions/?course=1
    """
    queryset = Session.objects.select_related('course').all().order_by('session_date')
    serializer_class = SessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'instructor_name', 'mode']
    search_fields = ['instructor_name', 'course__title']

    # Date-range filtering handled manually via query params
    def get_queryset(self):
        qs = super().get_queryset()
        date_after = self.request.query_params.get('session_date_after')
        date_before = self.request.query_params.get('session_date_before')
        if date_after:
            qs = qs.filter(session_date__gte=date_after)
        if date_before:
            qs = qs.filter(session_date__lte=date_before)
        return qs


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Enrollment (no DELETE per spec — only add/list/update).

    Filtering:
        GET /api/enrollments/?status=COMPLETED
        GET /api/enrollments/?employee=1
        GET /api/enrollments/?session=3

    Extra action:
        PATCH /api/enrollments/{id}/complete/  → sets status to COMPLETED
    """
    queryset = (
        Enrollment.objects
        .select_related('employee', 'session__course')
        .all()
        .order_by('id')
    )
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'employee', 'session']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']  # no PUT/DELETE

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete(self, request, pk=None):
        """Shortcut: mark an enrollment as COMPLETED."""
        enrollment = self.get_object()
        enrollment.status = 'COMPLETED'
        enrollment.save()
        return Response(EnrollmentSerializer(enrollment).data)


# ── Analytics Views ───────────────────────────────────────────────────────────

class CoursePopularityView(APIView):
    """
    GET /api/analytics/course-popularity/

    Returns each course with total enrollments and success rate
    (percentage of COMPLETED enrollments).

    Optional filter:
        ?category=Technical
    """
    def get(self, request):
        category = request.query_params.get('category')

        courses = Course.objects.all()
        if category:
            courses = courses.filter(category=category)

        data = []
        for course in courses:
            enrollments = Enrollment.objects.filter(session__course=course)
            total = enrollments.count()
            completed = enrollments.filter(status='COMPLETED').count()
            success_rate = round((completed / total * 100), 1) if total > 0 else 0.0

            data.append({
                'course_id': course.id,
                'course_title': course.title,
                'total_enrollments': total,
                'completed': completed,
                'success_rate': success_rate,
            })

        # Sort by most enrollments first
        data.sort(key=lambda x: x['total_enrollments'], reverse=True)
        serializer = CoursePopularitySerializer(data, many=True)
        return Response(serializer.data)


class DepartmentParticipationView(APIView):
    """
    GET /api/analytics/department-participation/

    Returns count of COMPLETED enrollments grouped by employee department.
    """
    def get(self, request):
        results = (
            Enrollment.objects
            .filter(status='COMPLETED')
            .values('employee__department')
            .annotate(completed_trainings=Count('id'))
            .order_by('-completed_trainings')
        )

        data = [
            {
                'department': row['employee__department'],
                'completed_trainings': row['completed_trainings'],
            }
            for row in results
        ]

        serializer = DepartmentParticipationSerializer(data, many=True)
        return Response(serializer.data)


class EmployeeTranscriptView(APIView):
    """
    GET /api/analytics/transcript/?employee_id=1

    Returns full training history for a single employee.
    Requires `employee_id` query parameter.
    """
    def get(self, request):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response(
                {'error': 'employee_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrollments = (
            Enrollment.objects
            .filter(employee=employee)
            .select_related('session__course')
            .order_by('session__session_date')
        )

        transcript = [
            {
                'session_date': e.session.session_date,
                'course_title': e.session.course.title,
                'status': e.status,
            }
            for e in enrollments
        ]

        return Response({
            'employee_id': employee.id,
            'employee_name': employee.full_name,
            'email': employee.email,
            'department': employee.department,
            'transcript': TranscriptEntrySerializer(transcript, many=True).data,
        })
