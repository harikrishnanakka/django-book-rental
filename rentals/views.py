from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
from .models import Book, Rental
from .serializers import (
    BookSerializer,
    RentalSerializer,
    StartRentalSerializer,
    ExtendRentalSerializer
)
from users.models import User
from django.utils import timezone


# ---------------------------
# Helper: Fetch from OpenLibrary
# ---------------------------
def fetch_book_from_openlibrary(title):
    """Search OpenLibrary for title and return dict with title, pages, authors, key."""
    params = {'title': title}
    resp = requests.get(settings.OPENLIBRARY_SEARCH_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    docs = data.get('docs', [])
    if not docs:
        return None

    best = None
    for d in docs:
        if 'number_of_pages' in d or 'number_of_pages_median' in d:
            best = d
            break
    if best is None:
        best = docs[0]

    title = best.get('title') or title
    authors = ', '.join(best.get('author_name', []))
    key = best.get('key')

    
    pages = best.get('number_of_pages') or best.get('number_of_pages_median') or 250
    try:
        pages = int(pages)
    except (ValueError, TypeError):
        pages = 250  # fallback default

    return {
        'title': title,
        'pages': pages,
        'authors': authors,
        'key': key,
    }



# ---------------------------
# API: Start a rental (Admin only)
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAdminUser])
def start_rental(request):
    """
    Admin-only: Start a rental for a student using a book title.
    Will call OpenLibrary.

    Request: {"title": "Book Name", "user_id": 2}
    """
    serializer = StartRentalSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    title = serializer.validated_data['title']
    user_id = serializer.validated_data['user_id']
    user = get_object_or_404(User, id=user_id)

    # Fetch book from OpenLibrary
    book_data = fetch_book_from_openlibrary(title)
    if not book_data:
        return Response({'detail': 'Book not found on OpenLibrary.'}, status=status.HTTP_404_NOT_FOUND)

    book, _ = Book.objects.get_or_create(
        openlibrary_key=book_data.get('key') or title,
        defaults={
            'title': book_data.get('title') or title,
            'pages': book_data.get('pages'),
            'authors': book_data.get('authors'),
        },
    )

    # Create rental (1 month free)
    rental = Rental.objects.create(user=user, book=book)
    return Response(RentalSerializer(rental).data, status=status.HTTP_201_CREATED)


# ---------------------------
# API: Extend rental
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extend_rental(request, rental_id):
    """
    Authenticated user can extend their rental.
    Request: {"months": 1}
    Charges = (pages / 100) * months
    """
    rental = get_object_or_404(Rental, id=rental_id)
    serializer = ExtendRentalSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    months = serializer.validated_data['months']
    book = rental.book
    charge = (book.pages or 0) / 100 * months
    rental.months_extended += months
    rental.total_charge += charge
    rental.save()

    return Response(
        {
            'message': f'Rental extended by {months} month(s).',
            'total_charge': rental.total_charge,
        },
        status=status.HTTP_200_OK,
    )



# ---------------------------
# API: List all rentals (Admin only)
# ---------------------------
class RentalListView(generics.ListAPIView):
    queryset = Rental.objects.all().select_related('book', 'user')
    serializer_class = RentalSerializer
    permission_classes = [IsAdminUser]


# ---------------------------
# API: List all books
# ---------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
