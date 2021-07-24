from django.test import TestCase
from django.test.client import Client
from authapp.models import User
from django.core.management import call_command

from geekshop import settings


class TestUserManagement(TestCase):
    username = 'django2'
    email = 'django2@geekshop.local'
    password = 'geekbrains'
    status_code_success = 200
    status_code_redirect = 302

    new_user_data = {
        'username': 'samuel',
        'first_name': 'Сэмюэл',
        'last_name': 'Джексон',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'sumuel@geekshop.local',
        'age': '21'
    }

    def setUp(self):
        self.user = User.objects.create_superuser(username=self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)

        # response = self.client.get('/auth/login/')
        # self.assertEqual(response.status_code, self.status_code_success)
        # self.assertFalse(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.post('/auth/register/', data=self.new_user_data)
        # self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = User.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/{new_user.email}/{new_user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)