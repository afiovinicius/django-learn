# Imports Django
from django.urls import path

# Imports Views
from .views import (
    BooksList,
    CategoryList,
    BookCreate,
    CategoryCreate,
    UpdateBook,
    UpdateCategory,
    DeleteBook,
    DeleteCategory,
    SendMail,
)


urlpatterns = [
    path("categories/", CategoryList.as_view(), name="categories-list"),
    path("books/", BooksList.as_view(), name="books-list"),
    path("book/add/", BookCreate.as_view(), name="book-create"),
    path("category/add/", CategoryCreate.as_view(), name="category-create"),
    path("book/edit/", UpdateBook.as_view(), name="book-edit"),
    path("category/edit/", UpdateCategory.as_view(), name="category-edit"),
    path(
        "book/delete/<uuid:id>",
        DeleteBook.as_view(),
        name="book-delete",
    ),
    path(
        "category/delete/<uuid:id>",
        DeleteCategory.as_view(),
        name="category-delete",
    ),
    path("send-mail/", SendMail.as_view(), name="send-mail"),
]
