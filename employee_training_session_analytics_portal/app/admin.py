from django.contrib import admin
from .models import Employee, Course, Session, Enrollment


# -----------------------
# EMPLOYEE ADMIN
# -----------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'department')
    list_filter = ('department',)
    search_fields = ('full_name', 'email')


# -----------------------
# COURSE ADMIN
# -----------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration_minutes')
    list_filter = ('category',)
    search_fields = ('title',)


# -----------------------
# SESSION ADMIN
# -----------------------
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'session_date', 'instructor_name', 'mode')
    list_filter = ('mode', 'session_date', 'course')
    search_fields = ('instructor_name',)


# -----------------------
# ENROLLMENT ADMIN
# -----------------------
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'session', 'status')
    list_filter = ('status', 'session__course')
    search_fields = ('employee__full_name', 'session__course__title')