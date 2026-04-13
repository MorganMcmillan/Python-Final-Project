# ─────────────────────────────────────────────────────────────────────────────
# ADD THESE SNIPPETS TO YOUR EXISTING settings.py
# ─────────────────────────────────────────────────────────────────────────────

# 1. Add to INSTALLED_APPS list:
INSTALLED_APPS_TO_ADD = [
    'rest_framework',
    'django_filters',
]

# Example – your INSTALLED_APPS should look like:
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     ...
#     'portal',           # your existing app
#     'rest_framework',   # ← add
#     'django_filters',   # ← add
# ]


# 2. Paste this block anywhere in settings.py (e.g. near the bottom):

REST_FRAMEWORK = {
    # Return JSON by default; the browsable HTML API is still available in browser
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # Use django-filter as the default filter backend
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    # Pagination (optional – remove if you want all results at once)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
