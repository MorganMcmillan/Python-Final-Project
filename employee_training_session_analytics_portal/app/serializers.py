from rest_framework import serializers
from .models import Employee, Course, Session, Enrollment


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'email', 'department']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'category', 'duration_minutes']


class SessionSerializer(serializers.ModelSerializer):
    # Read: show course title; Write: accept course id
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'course', 'course_title', 'session_date', 'instructor_name', 'mode']


class EnrollmentSerializer(serializers.ModelSerializer):
    # Nested read-only display fields
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    course_title = serializers.CharField(source='session.course.title', read_only=True)
    session_date = serializers.DateField(source='session.session_date', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'employee', 'employee_name', 'employee_email',
            'session', 'course_title', 'session_date',
            'status',
        ]

    def validate(self, data):
        """Enforce the unique-together constraint: one employee per session."""
        employee = data.get('employee')
        session = data.get('session')

        # On create (no instance yet) check for duplicates
        if self.instance is None:
            if Enrollment.objects.filter(employee=employee, session=session).exists():
                raise serializers.ValidationError(
                    "This employee is already enrolled in this session."
                )
        return data


# ── Analytics serializers (read-only, no model) ──────────────────────────────

class CoursePopularitySerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_title = serializers.CharField()
    total_enrollments = serializers.IntegerField()
    completed = serializers.IntegerField()
    success_rate = serializers.FloatField()


class DepartmentParticipationSerializer(serializers.Serializer):
    department = serializers.CharField()
    completed_trainings = serializers.IntegerField()


class TranscriptEntrySerializer(serializers.Serializer):
    session_date = serializers.DateField()
    course_title = serializers.CharField()
    status = serializers.CharField()
