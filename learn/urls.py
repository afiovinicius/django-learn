# Imports Django
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    # Route Default
    path("", TemplateView.as_view(template_name="index.html")),
    # Route Django
    path("admin/", admin.site.urls),
    # Route API
    path("api/", include("api.urls")),
]
