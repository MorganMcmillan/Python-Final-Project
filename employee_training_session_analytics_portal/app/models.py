from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=10, choices=[
        ('IT', 'IT'), 
        ('HR', 'HR'), 
        ('SALES', 'Sales')
    ])

class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateField()
    instructor_name = models.CharField(max_length=100)
    mode = models.CharField(max_length=10, choices=[
        ('ONLINE', 'Online'), 
        ('IN-PERSON', 'In-Person')
    ])

class Enrollment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='enrollments')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=15, choices=[
        ('ENROLLED', 'Enrolled'), 
        ('COMPLETED', 'Completed')
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'session'], name='unique_employee_per_session')
        ]