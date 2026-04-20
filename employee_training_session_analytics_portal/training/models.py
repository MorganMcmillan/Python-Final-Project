from django.db import models


class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('SALES', 'Sales'),
        ('FINANCE', 'Finance'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Technical'),
        ('SEC', 'Security'),
        ('SOFT', 'Soft Skills'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    duration_minutes = models.IntegerField()

    def __str__(self):
        return self.title


class Session(models.Model):
    MODE_CHOICES = [
        ('ONLINE', 'Online'),
        ('INPERSON', 'In-Person'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_date = models.DateField()
    instructor_name = models.CharField(max_length=200)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)

    def __str__(self):
        return f"{self.course.title} - {self.session_date}"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="enrollments")
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('employee', 'session')  # 🔥 REQUIRED BY PROJECT

    def __str__(self):
        return f"{self.employee.full_name} - {self.session}"