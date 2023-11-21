# Imports DRF
from rest_framework import serializers

# Imports models
from .models import (
    UserCustom,
    Category,
    Books
)


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserCustom
        fields = ('id', 'avatar', 'name', 'username', 'email',
                  'phone', 'doc_register', 'password', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True}}

    def get_avatar(self, obj):
        avatar = obj.avatar
        return avatar

    def create(self, validated_data):
        user = UserCustom.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_category(self, value):
        if Category.objects.filter(category__iexact=value).exists():
            raise serializers.ValidationError(
                "Uma categoria com este nome já existe.")
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
