from django.db import models

# Create your models here.
class Employee(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    department = models.Choices(['IT', 'HR', 'SALES'])

class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='session')
    session_date = models.DateField()
    instructor_name = models.CharField(max_length=100)
    mode = models.Choices(['ONLINE', 'IN-PERSON'])

class Enrollment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='enrollment')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='enrollment')
    status = models.Choices(['ENROLLED', 'COMPLETED'])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'session'], name='unique_employee_per_session')
        ]