from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError

class AddInventoryFormAdmin(ModelForm):
    name = forms.CharField(required=True, max_length=50)

    class Meta:
        model = Inventory
        fields = ['category','name', 'cost_per_item', 'cost_sold_per_item', 'quantity_in_stock', 'supplier', 'reorder_level', 'sold_to', 'sold_by']


class AddInventoryForm(ModelForm):
    name = forms.CharField(required=True, max_length=50)

    class Meta:
        model = Inventory
        fields = ['category','name', 'cost_per_item', 'cost_sold_per_item', 'quantity_in_stock', 'supplier', 'reorder_level']


class UpdateInventoryForm(ModelForm):
    name = forms.CharField(required=True, max_length=50)
    
    class Meta:
        model = Inventory
        fields = ['category','name', 'cost_per_item', 'cost_sold_per_item', 'quantity_in_stock', 'supplier', 'reorder_level']



class Sell_ProductForm(ModelForm):

    class Meta:
        model = Inventory
        fields = ['cost_sold_per_item', 'quantity', 'sold_to', 'sold_by']

class Restock_ProductForm(ModelForm):

    class Meta:
        model = Inventory
        fields = ['cost_per_item', 'quantity', 'reorder_level', 'supplier']
 

class SearchInventoryForm(ModelForm):
    

    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Inventory
        fields = ['category', 'name', 'sold_by', 'sold_to', 'supplier' ]


