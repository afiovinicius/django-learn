# Imports Django
from django.urls import path, re_path


# Imports App
from .views import (
    default,
    BooksList,
    CategoryList,
    DeleteBook,
    DeleteCategory,
    SendMail,
    UpdateBook,
    UpdateCategory,
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
)

urlpatterns = [
    path("", default, name="default"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/edit", UpdateCategory.as_view(), name="category-edit"),
    path(
        "categories/delete/<uuid:id>",
        DeleteCategory.as_view(),
        name="category-delete",
    ),
    path("books/", BooksList.as_view(), name="books-list"),
    path("books/edit", UpdateBook.as_view(), name="book-edit"),
    path(
        "books/delete/<uuid:id>",
        DeleteBook.as_view(),
        name="book-delete",
    ),
    path("send-mail/", SendMail.as_view(), name="send-mail"),
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("jwt/create/", CustomTokenObtainPairView.as_view()),
    path("jwt/refresh/", CustomTokenRefreshView.as_view()),
    path("jwt/verify/", CustomTokenVerifyView.as_view()),
    path("logout/", LogoutView.as_view()),
]
