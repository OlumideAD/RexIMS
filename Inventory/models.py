from django.db import models

# Create your models here.


#table Category
class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_default_category():
        # Ensure a default category exists
        category, created = Category.objects.get_or_create(name='Electronics')
        return category

class Inventory(models.Model):
    #Field Defination
    
    name = models.CharField(max_length=100, null=False, blank=True)
    cost_per_item = models.DecimalField(default='0.0', max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.IntegerField(default='0', null=False, blank=False)
    quantity_sold = models.IntegerField(default='0', null=False, blank=False)
    sales = models.DecimalField(default='0.0', max_digits=10, decimal_places=2, null=False, blank=False)

    stock_date = models.DateField(auto_now_add=True, auto_now=False) 
    #auto_now_add - when product is added thats the date will be stored and uneditable

    last_sales_date = models.DateField(auto_now=True, auto_now_add=False)
    #auto_now - when new sales is added then we the record will save the last sale date

    #newly added columns
    cost_sold_per_item = models.DecimalField(default='0.0', max_digits=19, decimal_places=2, null=False, blank=False)

    #foriegn key category that links to Category table
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
          # Override the save method
      # Override the save method
    def save(self, *args, **kwargs):
        if not self.category_id:  # Check if category is not set
            self.category = Category.get_default_category()
        super(Inventory, self).save(*args, **kwargs)


        
    reorder_level = models.IntegerField(default='0', blank=False, null=True)
    supplier = models.CharField(max_length=50, blank=True, null=True)
    sold_by = models.CharField(max_length=50, blank=True, null=True)
    sold_to = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)

    #newly added fields
    rating = models.DecimalField(default='0.0', max_digits=10, decimal_places=2, null=False, blank=False)
    review_body = models.CharField(max_length=500, blank=True, null=True)
    prediction = models.CharField(max_length=500, blank=True, null=True)

    # a lamda function to return the product name
    def __str__(self) -> str:
        return self.name
    

