# REST API – Employee Training Analytics Portal

This folder contains the Django REST Framework layer added on top of the existing
Django portal. It exposes all functional requirements as JSON endpoints.

---

## Installation

Install the two extra packages:

```bash
pip install djangorestframework django-filter
```

---

## Integration Steps

### 1. Copy files into your app

Copy these three files into the `portal` app directory (same folder as `models.py`):

| File | Purpose |
|------|---------|
| `serializers.py` | Converts model instances ↔ JSON |
| `api_views.py` | All ViewSets and analytics views |
| `api_urls.py` | URL routing for all `/api/` endpoints |

### 2. Update `settings.py`

Add to `INSTALLED_APPS`:
```python
'rest_framework',
'django_filters',
```

Paste the `REST_FRAMEWORK` dict from `settings_additions.py` into your settings file.

### 3. Update `urls.py` (project-level)

```python
# project/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),        # existing HTML views
    path('api/', include('portal.api_urls')), # ← add this line
]
```

---

## Endpoint Reference

### Employees
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/employees/` | List all employees |
| GET | `/api/employees/?department=IT` | Filter by department |
| POST | `/api/employees/` | Create employee |
| GET | `/api/employees/{id}/` | Get one employee |
| PATCH | `/api/employees/{id}/` | Update employee |
| DELETE | `/api/employees/{id}/` | Delete employee |

### Courses
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/courses/` | List all courses |
| GET | `/api/courses/?category=Technical` | Filter by category |
| POST | `/api/courses/` | Create course |
| PATCH | `/api/courses/{id}/` | Update course |
| DELETE | `/api/courses/{id}/` | Delete course |

### Sessions
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/sessions/` | List all sessions |
| GET | `/api/sessions/?instructor_name=Dr.+Lee` | Filter by instructor |
| GET | `/api/sessions/?session_date_after=2025-01-01&session_date_before=2025-12-31` | Date range filter |
| POST | `/api/sessions/` | Schedule a session |
| PATCH | `/api/sessions/{id}/` | Update session |
| DELETE | `/api/sessions/{id}/` | Delete session |

### Enrollments
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/enrollments/` | List all enrollments |
| GET | `/api/enrollments/?status=COMPLETED` | Filter by status |
| POST | `/api/enrollments/` | Enroll employee in session |
| PATCH | `/api/enrollments/{id}/` | Update enrollment status |
| PATCH | `/api/enrollments/{id}/complete/` | Quick-complete shortcut |

> Note: DELETE is intentionally disabled on enrollments (per project spec: add/list/update only).

### Analytics
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/analytics/course-popularity/` | Enrollment counts + success rate per course |
| GET | `/api/analytics/course-popularity/?category=Technical` | Filter by course category |
| GET | `/api/analytics/department-participation/` | Completed trainings per department |
| GET | `/api/analytics/transcript/?employee_id=1` | Full training history for one employee |

---

## Example Responses

### `GET /api/analytics/course-popularity/`
```json
[
  {
    "course_id": 1,
    "course_title": "Python Basics",
    "total_enrollments": 42,
    "completed": 34,
    "success_rate": 81.0
  }
]
```

### `GET /api/analytics/transcript/?employee_id=1`
```json
{
  "employee_id": 1,
  "employee_name": "John Smith",
  "email": "john@company.com",
  "department": "IT",
  "transcript": [
    {"session_date": "2025-03-10", "course_title": "Python Basics", "status": "COMPLETED"},
    {"session_date": "2025-03-15", "course_title": "Security 101", "status": "ENROLLED"}
  ]
}
```

### `POST /api/enrollments/` — duplicate rejected
```json
{
  "non_field_errors": ["This employee is already enrolled in this session."]
}
```
