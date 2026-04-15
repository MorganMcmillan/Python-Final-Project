from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from .models import Employee, Course, Session, Enrollment


# =========================
# HOME
# =========================
def home(request):
    return render(request, 'home.html', {
        'total_employees': Employee.objects.count(),
        'total_courses': Course.objects.count(),
        'total_sessions': Session.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
    })


# =========================
# EMPLOYEES
# =========================
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})


def employee_create(request):
    if request.method == "POST":
        Employee.objects.create(
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            department=request.POST['department']
        )
        return redirect('employee_list')

    return render(request, 'employee_form.html')


def employee_delete(request, id):
    Employee.objects.get(id=id).delete()
    return redirect('employee_list')


# =========================
# COURSES
# =========================
def course_list(request):
    return render(request, 'courses/course_list.html', {
        'courses': Course.objects.all()
    })


def course_create(request):
    if request.method == "POST":
        Course.objects.create(
            title=request.POST['title'],
            category=request.POST['category'],
            duration_minutes=request.POST['duration_minutes']
        )
        return redirect('course_list')

    return render(request, 'course_form.html')


# =========================
# SESSIONS
# =========================
def session_list(request):
    return render(request, 'sessions/session_list.html', {
        'sessions': Session.objects.all()
    })


def session_create(request):
    if request.method == "POST":
        Session.objects.create(
            course_id=request.POST['course'],
            session_date=request.POST['session_date'],
            instructor_name=request.POST['instructor_name'],
            mode=request.POST['mode']
        )
        return redirect('session_list')

    return render(request, 'session_form.html', {
        'courses': Course.objects.all()
    })


# =========================
# ENROLLMENTS
# =========================
def enrollment_list(request):
    return render(request, 'enrollments/enrollment_list.html', {
        'enrollments': Enrollment.objects.select_related('employee', 'session')
    })


def enrollment_create(request):
    if request.method == "POST":
        Enrollment.objects.create(
            employee_id=request.POST['employee'],
            session_id=request.POST['session'],
            status=request.POST['status']
        )
        return redirect('enrollment_list')

    return render(request, 'enrollment_form.html', {
        'employees': Employee.objects.all(),
        'sessions': Session.objects.all()
    })


# =========================
# ANALYTICS
# =========================
def analytics_dashboard(request):
    return render(request, 'analytics/analytics_dashboard.html')


def course_popularity(request):
    data = []
    for c in Course.objects.all():
        total = Enrollment.objects.filter(session__course=c).count()
        completed = Enrollment.objects.filter(session__course=c, status='COMPLETED').count()

        rate = (completed / total * 100) if total else 0

        data.append({
            'title': c.title,
            'total': total,
            'success_rate': round(rate, 2)
        })

    return render(request, 'analytics/analytics_course_popularity.html', {
        'data': data
    })


def department_participation(request):
    data = Employee.objects.values('department').annotate(
        completed=Count('enrollments', filter=Q(enrollments__status='COMPLETED'))
    )

    return render(request, 'analytics/analytics_department.html', {
        'data': data
    })


def employee_transcript(request):
    employees = Employee.objects.all()
    selected_employee = None
    records = []

    emp_id = request.GET.get('employee')

    if emp_id:
        selected_employee = Employee.objects.get(id=emp_id)
        records = Enrollment.objects.filter(employee=selected_employee)

    return render(request, 'analytics/analytics_transcript.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'records': records
    })