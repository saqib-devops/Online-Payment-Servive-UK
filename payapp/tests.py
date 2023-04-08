from django.test import TestCase, Client
from django.urls import reverse

from register.models import User
from .models import Transaction, TransactionRequest


class TransactionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='sender', email='sender@exarth.com', password='testpassword')
        self.user2 = User.objects.create_user(username='receiver', email='receiver@exarth.com', password='testpassword')
        self.transaction = Transaction.objects.create(sender=self.user1, receiver=self.user2, amount=50)

    def test_transaction_creation(self):
        transaction = Transaction.objects.get(id=self.transaction.id)
        self.assertEqual(transaction.sender, self.user1)
        self.assertEqual(transaction.receiver, self.user2)
        self.assertEqual(transaction.amount, 50)

    def test_transaction_str(self):
        transaction_str = str(self.transaction)
        self.assertEqual(transaction_str, f"Transferred 50 from {self.user1.get_full_name()} to {self.user2.get_full_name()}")


class TransactionRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='sender', email='sender@exarth.com', password='testpassword')
        self.user2 = User.objects.create_user(username='receiver', email='receiver@exarth.com', password='testpassword')
        self.transaction_request = TransactionRequest.objects.create(sender=self.user1, receiver=self.user2, amount=50, status='pending')

    def test_transaction_request_creation(self):
        transaction_request = TransactionRequest.objects.get(id=self.transaction_request.id)
        self.assertEqual(transaction_request.sender, self.user1)
        self.assertEqual(transaction_request.receiver, self.user2)
        self.assertEqual(transaction_request.amount, 50)
        self.assertEqual(transaction_request.status, 'pending')

    def test_transaction_request_str(self):
        transaction_request_str = str(self.transaction_request)
        self.assertEqual(transaction_request_str, f"Transferred 50 from {self.user1.get_full_name()} to {self.user2.get_full_name()}")


class TransactionListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        Transaction.objects.create(
            sender=self.user,
            recipient=self.user,
            amount=100,
            status=Transaction.SUCCESS
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/transaction/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('payapp:transactions'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('payapp:transactions'))
        self.assertTemplateUsed(response, 'payapp/transaction_list.html')

    def test_view_displays_correct_transactions(self):
        response = self.client.get(reverse('payapp:transactions'))
        transactions = response.context['object_list']
        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions.first().amount, 100)


class TransactionCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/transaction/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('payapp:transaction-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('payapp:transaction-create'))
        self.assertTemplateUsed(response, 'payapp/transaction_form.html')

    def test_form_submission_creates_transaction(self):
        data = {
            'recipient': self.user.id,
            'amount': 50
        }
        response = self.client.post(reverse('payapp:transaction-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.sender, self.user)
        self.assertEqual(transaction.recipient, self.user)
        self.assertEqual(transaction.amount, 50)
        self.assertEqual(transaction.status, Transaction.PENDING)