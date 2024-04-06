from django.contrib import admin
from .models import *
from .form import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class StockCreateAdmin(ImportExportModelAdmin):
    list_display = ['category', 'name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold', 'cost_sold_per_item', 
                  'reorder_level', 'supplier', 'sold_by', 'sold_to', 'stock_date', 'last_sales_date', 'rating', 'prediction']
    form = AddInventoryFormAdmin
    list_filter = ['category']
    search_fields = ['name', 'sold_by', 'sold_to', 'supplier', 'reorder_level']


admin.site.register(Inventory, StockCreateAdmin)
admin.site.register(Category)
