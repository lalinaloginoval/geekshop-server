from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command


class TestMainSmoke(TestCase):
    status_code_success = 200

    def setUp(self):
        cat_1 = ProductCategory.objects.create(name='cat 1')
        for i in range(100):
            Product.objects.create(category=cat_1, name=f'prod {i}')

        self.client = Client()

    def test_main_app_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_urls(self):
        response = self.client.get(f'/products/')
        self.assertEqual(response.status_code, self.status_code_success)