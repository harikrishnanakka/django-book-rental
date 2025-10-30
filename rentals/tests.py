from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from rentals.models import Book, Rental

class RentalTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.force_authenticate(user=self.admin)

    def test_create_rental(self):
        response = self.client.post(reverse('start-rental'), {'title': 'Harry Potter', 'user_id': self.admin.id})
        self.assertEqual(response.status_code, 201)
