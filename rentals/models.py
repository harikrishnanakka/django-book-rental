from django.db import models
from django.utils import timezone
from users.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    openlibrary_key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateTimeField(default=timezone.now)
    months_extended = models.PositiveIntegerField(default=0)
    total_charge = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    @property
    def end_date(self):
        """First month free + any extended months."""
        return self.start_date + timezone.timedelta(days=30 * (1 + self.months_extended))
