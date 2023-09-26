# Imports Django
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Route Default
    path("", include("app.urls")),
    # Route Django
    path("admin/", admin.site.urls),
    # Route API
    path("api/", include("app.urls")),
    path("api/", include("djoser.urls")),
    path("api/", include("djoser.urls.jwt")),
]
