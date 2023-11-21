# Imports Django
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password

# Imports DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from learn.utils.supabase_utils import supabase_connect


# Imports App
from .models import UserCustom, Category, Books
from .serializers import UserSerializer, CategorySerializer, BooksSerializer

# Imports Utils
from learn.utils.send_mail_utils import smtplib_send_mail, resend_send_mail
from learn.utils.upload_files_utils import upload_file_to_supabase


# Imports Libs
from rest_framework_simplejwt.tokens import RefreshToken


class SignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        try:
            user = UserCustom.objects.get(
                username=request.data.get("username"))
            return Response(
                {"error": "Nome de usuário já existe."}, status=status.HTTP_400_BAD_REQUEST
            )
        except UserCustom.DoesNotExist:
            pass

        if serializer.is_valid():
            request.data['password'] = make_password(request.data['password'])

            avatar = None

            if "avatar" in request.data:
                file = request.data.get("avatar")
                try:
                    avatar = upload_file_to_supabase(
                        file, file.name, "avatars")
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )

            user = serializer.save()

            if "avatar" in request.data:
                user.avatar = avatar
                user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    def post(self, request):
        username_or_email = request.data.get("username_or_email", "")
        password = request.data.get("password", "")

        if "@" in username_or_email:
            user_query = {"email": username_or_email}
        else:
            user_query = {"username": username_or_email}

        try:
            user = UserCustom.objects.get(**user_query)
        except UserCustom.DoesNotExist:
            return Response(
                {"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)  # type: ignore

        serialized_user = UserSerializer(user).data
        response_data = {"user": serialized_user, "access_token": access_token}
        return Response(response_data, status=status.HTTP_200_OK)


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = UserCustom.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})


class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if not request.user.is_superuser:
            return Response(
                {"error": "Apenas superusuários podem excluir usuários."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            user = UserCustom.objects.get(id=id)
        except UserCustom.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user == request.user:
            return Response(
                {"error": "Você não pode excluir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.avatar:
            try:
                supabase = supabase_connect()
                file_name = user.avatar.split("/")[-1]
                supabase.storage.from_("avatars").remove(file_name)
            except Exception as e:
                return Response(
                    {"error": {str(e)}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})


class CategoryCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCategory(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        id = request.data.get("id", None)
        if id is None:
            return Response(
                {"error": "ID da categoria não fornecido no corpo JSON."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response(
                {"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response(
                {"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BooksList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response({"books": serializer.data})


class BookCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BooksSerializer(data=request.data)

        try:
            book = Books
        except Books.DoesNotExist:
            return Response(
                {"error": "Livro não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        if serializer.is_valid():
            url_file = None

            if "file" in request.data:
                file = request.data.get("file")
                try:
                    url_file = upload_file_to_supabase(
                        file, file.name, "cover-books")
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )

            book = serializer.save()

            if "file" in request.data:
                book.url_file = url_file
                book.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBook(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        id = request.data.get("id", None)

        if id is None:
            return Response(
                {"error": "ID do livro não fornecido no corpo JSON."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            book = Books.objects.get(id=id)
        except Books.DoesNotExist:
            return Response(
                {"error": "Livro não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        if "name" in request.data:
            book.name = request.data["name"]

        if "pagesRead" in request.data:
            book.pagesRead = request.data["pagesRead"]

        if "category" in request.data:
            try:
                category = request.data["category"]
                getCategory = Category.objects.get(id=category)
                book.category = getCategory
            except Category.DoesNotExist:
                return Response(
                    {"error": "Categoria especificada não encontrada."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if "file" in request.data:
            file = request.data.get("file")
            try:
                url_file = upload_file_to_supabase(
                    file, file.name, "cover-books")
                book.url_file = url_file
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        book.save()

        return Response(
            {
                "message": "Livro atualizado com sucesso.",
                "book": BooksSerializer(book).data,
            },
            status=status.HTTP_200_OK,
        )


class DeleteBook(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            book = Books.objects.get(id=id)
        except Books.DoesNotExist:
            return Response(
                {"error": "Livro não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        if book.url_file:
            try:
                supabase = supabase_connect()
                file_name = book.url_file.split("/")[-1]
                supabase.storage.from_(
                    "cover-books").remove(file_name)  # type: ignore
            except Exception as e:
                return Response(
                    {"error": {str(e)}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendMail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get("subject")
        fromuser = request.data.get("fromuser")
        tousers = request.data.get("tousers")
        send_method = request.data.get("send_method")
        for_mtk = request.data.get("for_mtk")

        if for_mtk:
            message = render_to_string(
                "email_mtk.html", context={"title": subject})
        else:
            message = request.data.get("message")

        try:
            if send_method is True:
                send_resend = resend_send_mail(subject, message, tousers)
                return Response({"message": send_resend})
            elif isinstance(tousers, list) and send_method is False:
                if not tousers:
                    return Response(
                        {
                            "error": "A lista de destinatários (tousers) não pode estar vazia."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                for recipient in tousers:
                    smtplib_send_mail(subject, message,
                                      fromuser, recipient, for_mtk)
                return JsonResponse({"message": "Email enviado com sucesso!"})
            else:
                return Response(
                    {"error": "O campo send_method deve ser True ou False."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            return Response(
                {"error": f"Erro de validação: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Não foi possível enviar o e-mail: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
