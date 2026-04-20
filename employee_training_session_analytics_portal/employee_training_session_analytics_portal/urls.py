from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # main site (your templates & pages)
    path('', include('training.urls')),

    # API routes
    path('api/', include('app.api_urls')),
]