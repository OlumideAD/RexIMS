from django.test import TestCase
from Inventory.models import*
from django.utils import timezone
from decimal import Decimal

class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")

    def test_get_default_category(self):
        # This will test if the default category gets created or fetched
        default_category = Category.get_default_category()
        self.assertIsNotNone(default_category)
        self.assertEqual(default_category.name, "Electronics")
        # Verify it's a singleton behavior for default category
        same_default_category = Category.get_default_category()
        self.assertEqual(default_category.id, same_default_category.id)

class InventoryModelTest(TestCase):

    def setUp(self):
        # Create a default category for inventory items
        self.category = Category.objects.create(name="Electronics")
        # Create an inventory item
        self.inventory = Inventory.objects.create(
            name="Test Product",
            cost_per_item=Decimal('10.00'),
            quantity_in_stock=5,
            quantity_sold=2,
            sales=Decimal('20.00'),
            cost_sold_per_item=Decimal('10.00'),
            category=self.category,
            reorder_level=10,
            supplier="Test Supplier",
            sold_by="Test Seller",
            sold_to="Test Buyer",
            quantity=3,
            rating=Decimal('4.5'),
            review_body="Good product",
            prediction="Likely to sell",
        )

    def test_inventory_creation(self):
        self.assertEqual(self.inventory.name, "Test Product")
        self.assertEqual(self.inventory.cost_per_item, Decimal('10.00'))
        self.assertEqual(self.inventory.quantity_in_stock, 5)
        self.assertEqual(self.inventory.sales, Decimal('20.00'))
        self.assertEqual(self.inventory.category, self.category)

    def test_inventory_save_with_default_category(self):
        inventory_without_category = Inventory.objects.create(
            name="Another Product",
            cost_per_item=Decimal('15.00'),
            quantity_in_stock=10,
            quantity_sold=5,
            sales=Decimal('75.00'),
        )
        self.assertIsNotNone(inventory_without_category.category)
        self.assertEqual(inventory_without_category.category.name, "Electronics")

    def test_inventory_str_method(self):
        self.assertEqual(str(self.inventory), "Test Product")
