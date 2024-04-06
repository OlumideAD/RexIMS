from django.urls import path
from .views import inventory_list, product_view, add_product, delete_inventory ,update_inventory, dashboard, sell_product, restock_product

urlpatterns = [
  path("", inventory_list, name="inventory_list"),
  path("product/<int:pk>", product_view, name="product_view"),
  path("add_inventory/", add_product, name="add_inventory"),
  path("sell_product/<int:pk>", sell_product, name="sell_product"),
  path("restock_product/<int:pk>", restock_product, name="restock_product"),
  path("delete/<int:pk>", delete_inventory, name="delete_inventory"),
  path("update/<int:pk>", update_inventory, name="update_inventory"),
  path("dashboard/", dashboard, name="dashboard")

]
