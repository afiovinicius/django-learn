# Imports Django
from django.http import JsonResponse
from django.core.exceptions import ValidationError

# Imports DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Imports App
from .models import Books, Category
from .serializers import CategorySerializer, BooksSerializer

# Imports Utils
from learn.utils.send_mail_utils import smtplib_send_mail, resend_send_mail
from learn.utils.upload_coverbook_utils import upload_file_to_supabase


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
                    url_file = upload_file_to_supabase(file, file.name)
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
                url_file = upload_file_to_supabase(file, file.name)
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

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendMail(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get("subject")
        message = request.data.get("message")
        fromuser = request.data.get("fromuser")
        tousers = request.data.get("tousers")
        send_method = request.data.get("send_method")

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
                    smtplib_send_mail(subject, message, fromuser, recipient)
                return JsonResponse({"message": "Emails enviados com sucesso!"})
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
