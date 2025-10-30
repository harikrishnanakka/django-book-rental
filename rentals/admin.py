from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Rental

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'pages')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'start_date', 'months_extended', 'total_charge')
