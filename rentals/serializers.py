from rest_framework import serializers
from .models import Book, Rental


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'pages', 'openlibrary_key']


class RentalSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Rental
        fields = ['id', 'user', 'book', 'start_date', 'months_extended', 'total_charge', 'end_date']


class StartRentalSerializer(serializers.Serializer):
    title = serializers.CharField()
    user_id = serializers.IntegerField()


class ExtendRentalSerializer(serializers.Serializer):
    months = serializers.IntegerField(min_value=1)
