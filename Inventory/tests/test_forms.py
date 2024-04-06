from django.test import TestCase
from Inventory.form import*
from Inventory.models import*

class AddInventoryFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.category = Category.objects.create(name="Electronics")

    def test_add_inventory_form_valid_data(self):
        form_data = {
            'category': self.category.id,
            'name': 'New Product',
            'cost_per_item': '100.00',
            'cost_sold_per_item': '150.00',
            'quantity_in_stock': 10,
            'supplier': 'Test Supplier',
            'reorder_level': 5,
        }
        form = AddInventoryForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Save the form and verify it creates an inventory item
        inventory_item = form.save()
        self.assertEqual(inventory_item.name, 'New Product')
        self.assertEqual(inventory_item.cost_per_item, 100.00)
        self.assertEqual(inventory_item.quantity_in_stock, 10)
        self.assertEqual(inventory_item.supplier, 'Test Supplier')

    def test_add_inventory_form_invalid_data(self):
        # Example of testing form with missing required fields
        form_data = {
            'cost_per_item': '100.00',  # Missing 'name', which is required
            'quantity_in_stock': 10,
        }
        form = AddInventoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_add_inventory_form_empty_data(self):
        form = AddInventoryForm(data={})
        self.assertFalse(form.is_valid())
        # Check that name is among the fields that have errors
        self.assertIn('name', form.errors)
