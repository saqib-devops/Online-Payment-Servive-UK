from django.db.models import Q
from django.test import TestCase
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps2023.settings')
django.setup()
from django.urls import reverse
from register.models import User
from payapp.models import Transaction


class TransactionViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com', username='user1', password='password123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com', username='user2', password='password123'
        )

    def test_transaction_list_view(self):
        url = reverse('payapp:transactions')
        self.client.login(email='user1@example.com', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        tran = Transaction.objects.filter(Q(sender=self.user1)
                                          | Q(receiver=self.user2))
        self.assertTrue(response, tran)

    def test_transaction_create_view(self):
        url = reverse('payapp:transaction-create')
        response = self.client.get(url)

        transaction1 = Transaction.objects.create(
            sender=self.user1, receiver=self.user2, amount=100
        )
        transaction2 = Transaction.objects.create(
            sender=self.user2, receiver=self.user1, amount=170
        )
        self.assertTrue(response, transaction1)
        self.assertTrue(response, transaction2)
