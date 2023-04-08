from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='test1@test.com', username='testuser1', password='password')
        self.user2 = User.objects.create(email='test2@test.com', username='testuser2', password='password')

    def test_user_str_method(self):
        self.assertEqual(str(self.user1), self.user1.username)

    def test_user_email_field(self):
        self.assertEqual(self.user1.email, 'test1@test.com')
        self.assertEqual(self.user2.email, 'test2@test.com')

    def test_user_total_amount_field(self):
        self.assertEqual(self.user1.total_amount, 1000)
        self.assertEqual(self.user2.total_amount, 1000)

    def test_user_sent_amount_field(self):
        self.assertEqual(self.user1.sent_amount, 0)
        self.assertEqual(self.user2.sent_amount, 0)

    def test_user_currency_type_field(self):
        self.assertEqual(self.user1.currency_type, 'USD')
        self.assertEqual(self.user2.currency_type, 'USD')

    def test_user_required_fields(self):
        self.assertEqual(User.REQUIRED_FIELDS, ['username',])

    def test_user_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_user_creation(self):
        user = User.objects.create_user(email='test3@test.com', username='testuser3', password='password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test3@test.com')
        self.assertEqual(user.username, 'testuser3')
        self.assertEqual(user.currency_type, 'USD')
        self.assertEqual(user.total_amount, 1000)
        self.assertEqual(user.sent_amount, 0)


class LoginTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # Login successfully
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'))

        # Login with incorrect password
        self.credentials['password'] = 'wrong_password'
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "Please enter a correct username and password")

    def test_logout(self):
        # Logout successfully
        self.client.login(**self.credentials)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_signup(self):
        # Signup successfully
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'new_secret',
            'password2': 'new_secret',
        }
        response = self.client.post(reverse('signup'), data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'))

        # Signup with existing username
        data['username'] = 'testuser'
        response = self.client.post(reverse('signup'), data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "A user with that username already exists.")
