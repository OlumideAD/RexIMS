from django.test import TestCase, Client
from django.urls import reverse
from Inventory.models import *
from Inventory.views import *
from django.contrib.auth.models import User
from Inventory.form import *

class TestViews(TestCase):

    def setUp(self):
        # Create a user for testing protected views
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        # Create a sample inventory item for testing
        self.inventory = Inventory.objects.create(name="Test Item", quantity_in_stock=10, sales=0)

    def test_product_view(self):
        url = reverse('product_view', args=[self.inventory.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/product_view.html')


    def test_sell_product(self):
        url = reverse('sell_product', args=[self.inventory.pk])
        data = {'quantity': 5, 'cost_sold_per_item': 10, 'sold_to': 'Customer A'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Assuming redirection after selling
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.sales, 50)  # Assuming initial sales were 0

    def test_delete_inventory(self):
        url = reverse('delete_inventory', args=[self.inventory.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assuming redirection after deletion
        self.assertFalse(Inventory.objects.filter(pk=self.inventory.pk).exists())


