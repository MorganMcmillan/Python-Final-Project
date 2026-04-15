from django.contrib import admin
from .models import Employee, Course, Session, Enrollment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'department')
    search_fields = ('full_name', 'email')
    list_filter = ('department',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'duration_minutes')
    search_fields = ('title',)
    list_filter = ('category',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'session_date', 'instructor_name', 'mode')
    list_filter = ('course', 'session_date', 'mode')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'session', 'status')
    list_filter = ('status', 'session')