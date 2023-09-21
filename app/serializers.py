# Imports DRF
from rest_framework import serializers

# Imports App
from .models import Category, Books


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_category(self, value):
        if Category.objects.filter(category__iexact=value).exists():
            raise serializers.ValidationError("Uma categoria com este nome já existe.")
        return value


class BooksSerializer(serializers.ModelSerializer):
    category_details = serializers.SerializerMethodField()
    url_file = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = "__all__"

    def get_url_file(self, obj):
        url_file = obj.url_file
        return url_file

    def get_category_details(self, obj):
        category = obj.category
        return {
            "id": category.id,
            "category": category.category,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
