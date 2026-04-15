from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Employee, Course, Session, Enrollment


# -------------------------
# HOME DASHBOARD
# -------------------------
def home(request):
    context = {
        'total_employees': Employee.objects.count(),
        'total_courses': Course.objects.count(),
        'total_sessions': Session.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
    }
    return render(request, 'home.html', context)


# =========================
# EMPLOYEES
# =========================
def employee_list(request):
    dept = request.GET.get('department')

    employees = Employee.objects.all()
    if dept:
        employees = employees.filter(department=dept)

    return render(request, 'employees_list.html', {'employees': employees})


def employee_create(request):
    if request.method == "POST":
        Employee.objects.create(
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            department=request.POST['department']
        )
        return redirect('employee_list')
    return render(request, 'employee_form.html')


def employee_update(request, id):
    emp = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        emp.full_name = request.POST['full_name']
        emp.email = request.POST['email']
        emp.department = request.POST['department']
        emp.save()
        return redirect('employee_list')

    return render(request, 'employee_form.html', {'employee': emp})


def employee_delete(request, id):
    emp = get_object_or_404(Employee, id=id)
    emp.delete()
    return redirect('employee_list')


# =========================
# COURSES
# =========================
def course_list(request):
    category = request.GET.get('category')

    courses = Course.objects.all()
    if category:
        courses = courses.filter(category=category)

    return render(request, 'courses_list.html', {'courses': courses})


def course_create(request):
    if request.method == "POST":
        Course.objects.create(
            title=request.POST['title'],
            category=request.POST['category'],
            duration_minutes=request.POST['duration_minutes']
        )
        return redirect('course_list')
    return render(request, 'course_form.html')


def course_update(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.title = request.POST['title']
        course.category = request.POST['category']
        course.duration_minutes = request.POST['duration_minutes']
        course.save()
        return redirect('course_list')

    return render(request, 'course_form.html', {'course': course})


def course_delete(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course_list')


# =========================
# SESSIONS
# =========================
def session_list(request):
    sessions = Session.objects.all()

    instructor = request.GET.get('instructor')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if instructor:
        sessions = sessions.filter(instructor_name__icontains=instructor)

    if start_date and end_date:
        sessions = sessions.filter(session_date__range=[start_date, end_date])

    return render(request, 'sessions_list.html', {'sessions': sessions})


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


def session_update(request, id):
    session = get_object_or_404(Session, id=id)

    if request.method == "POST":
        session.course_id = request.POST['course']
        session.session_date = request.POST['session_date']
        session.instructor_name = request.POST['instructor_name']
        session.mode = request.POST['mode']
        session.save()
        return redirect('session_list')

    return render(request, 'session_form.html', {
        'session': session,
        'courses': Course.objects.all()
    })


def session_delete(request, id):
    session = get_object_or_404(Session, id=id)
    session.delete()
    return redirect('session_list')


# =========================
# ENROLLMENTS
# =========================
def enrollment_list(request):
    status = request.GET.get('status')

    enrollments = Enrollment.objects.select_related('employee', 'session', 'session__course')

    if status:
        enrollments = enrollments.filter(status=status)

    return render(request, 'enrollments_list.html', {'enrollments': enrollments})


def enrollment_create(request):
    if request.method == "POST":
        employee_id = request.POST['employee']
        session_id = request.POST['session']
        status = request.POST['status']

        # prevent duplicate (extra safety even with DB constraint)
        exists = Enrollment.objects.filter(employee_id=employee_id, session_id=session_id).exists()
        if exists:
            return redirect('enrollment_list')

        Enrollment.objects.create(
            employee_id=employee_id,
            session_id=session_id,
            status=status
        )
        return redirect('enrollment_list')

    return render(request, 'enrollment_form.html', {
        'employees': Employee.objects.all(),
        'sessions': Session.objects.all()
    })


def enrollment_update(request, id):
    enrollment = get_object_or_404(Enrollment, id=id)

    if request.method == "POST":
        enrollment.status = request.POST['status']
        enrollment.save()
        return redirect('enrollment_list')

    return render(request, 'enrollment_form.html', {
        'enrollment': enrollment
    })


# =========================
# ANALYTICS DASHBOARD
# =========================
def analytics_dashboard(request):
    return render(request, 'analytics_dashboard.html')


# -------------------------
# 1. COURSE POPULARITY
# -------------------------
def course_popularity(request):
    data = []

    courses = Course.objects.all()

    for c in courses:
        total = Enrollment.objects.filter(session__course=c).count()
        completed = Enrollment.objects.filter(
            session__course=c,
            status='COMPLETED'
        ).count()

        success_rate = (completed / total * 100) if total > 0 else 0

        data.append({
            'title': c.title,
            'total': total,
            'success_rate': round(success_rate, 2)
        })

    return render(request, 'analytics_course_popularity.html', {'data': data})


# -------------------------
# 2. DEPARTMENT PARTICIPATION
# -------------------------
def department_participation(request):
    data = Employee.objects.values('department').annotate(
        completed=Count('enrollments', filter=Q(enrollments__status='COMPLETED'))
    )

    return render(request, 'analytics_department.html', {'data': data})


# -------------------------
# 3. EMPLOYEE TRANSCRIPT
# -------------------------
def employee_transcript(request):
    employees = Employee.objects.all()
    selected_employee = None
    records = []

    emp_id = request.GET.get('employee')

    if emp_id:
        selected_employee = Employee.objects.get(id=emp_id)
        records = Enrollment.objects.filter(employee=selected_employee)

    return render(request, 'analytics_transcript.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'records': records
    })