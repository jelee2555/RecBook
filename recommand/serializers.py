from .models import Book, Recommand, Like
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    Book.id = Book.book_id
    class Meta:
        model = Book
        fields = '__all__'


class RecommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommand
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'