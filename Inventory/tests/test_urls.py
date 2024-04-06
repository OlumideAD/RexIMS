from django.test import *
from django.urls import reverse, resolve
from Inventory.views import *
from Inventory.models import *

class TestUrls(SimpleTestCase):

    #test the url to return the right link
    def test_Inventory_list_url_is_resolved(self):
        url = reverse('inventory_list')
        self.assertEqual(resolve(url).func, inventory_list)

    def test_Add_Inventory_url_is_resolved(self):
        url = reverse('add_inventory')
        self.assertEqual(resolve(url).func, add_product)
    
    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_product_view_url_is_resolved(self):
        url = reverse('product_view', args=['1'])
        self.assertEqual(resolve(url).func, product_view)



    
