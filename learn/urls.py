# Imports Django
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    # Rota Django
    path("admin/", admin.site.urls),
    # Rota API
    path("api/", include("app.urls")),
    path("api/", include("djoser.urls")),
    path("api/", include("djoser.urls.jwt")),
]
