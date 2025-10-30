from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('rentals/', views.RentalListView.as_view(), name='rental-list'),
    path('start-rental/', views.start_rental, name='start-rental'),
    path('extend-rental/<int:rental_id>/', views.extend_rental, name='extend-rental'),
]
