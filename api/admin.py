from django.contrib import admin
from .models import (
    UserCustom,
    Category,
    Books,
)

admin.site.register(UserCustom)
admin.site.register(Category)
admin.site.register(Books)
