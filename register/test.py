from django.contrib.auth import authenticate
from django.template import context
from django.test import TestCase
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps2023.settings')
django.setup()
from django.urls import reverse
from register.models import User


class RegisterViewTest(TestCase):
    def test_register_view(self):
        url = reverse('register:signup')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'currency_type': 'USD',
        }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('payapp:dashboard'))
        self.assertContains(response, 'Registration successful.')

        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.currency_type, 'USD')

    def test_invalid_register_view(self):
        url = reverse('register:signup')
        # Invalid data: password1 and password2 don't match
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword456',
            'currency_type': 'USD',
        }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email='testuser@example.com')
            print("user does not exist")


