# Imports Django
from django.urls import path

# Imports Views
from .views import (
    BooksList,
    CategoryList,
    BookCreate,
    CategoryCreate,
    DeleteUser,
    SignIn,
    SignUp,
    UpdateBook,
    UpdateCategory,
    DeleteBook,
    DeleteCategory,
    SendMail,
    UserList,
)


urlpatterns = [
    path('auth/signup/', SignUp.as_view(), name='signup'),
    path('auth/signin/', SignIn.as_view(), name='signin'),
    path("users/", UserList.as_view(), name="user-list"),
    path("categories/", CategoryList.as_view(), name="categories-list"),
    path("books/", BooksList.as_view(), name="books-list"),
    path("book/add/", BookCreate.as_view(), name="book-create"),
    path("category/add/", CategoryCreate.as_view(), name="category-create"),
    path("book/edit/", UpdateBook.as_view(), name="book-edit"),
    path("category/edit/", UpdateCategory.as_view(), name="category-edit"),
    path('users/delete/<uuid:id>', DeleteUser.as_view(), name='delete_user'),
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
