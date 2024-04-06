
from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .form import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.shortcuts import render
from django.db.models import Sum
from django_pandas.io import read_frame
import plotly.express as px
import pandas as pd  # Import pandas
import json
import plotly

# Create your views here.



@login_required
def inventory_list(request):
    if request.method == 'POST':
        form = SearchInventoryForm(request.POST)
        if form.is_valid():
            query = Inventory.objects.all()
            
            # Filters
            category = form.cleaned_data.get('category')
            if category:
                query = query.filter(category__name__icontains=category)
            name = form.cleaned_data.get('name')
            if name:
                query = query.filter(name__icontains=name)
            sold_by = form.cleaned_data.get('sold_by')
            if sold_by:
                query = query.filter(sold_by__icontains=sold_by)
            sold_to = form.cleaned_data.get('sold_to')
            if sold_to:
                query = query.filter(sold_to__icontains=sold_to)
            supplier = form.cleaned_data.get('supplier')
            if supplier:
                query = query.filter(supplier__icontains=supplier)

            # Export to CSV
            if form.cleaned_data.get('export_to_CSV'):
                return export_to_csv(query)

            # Pagination setup remains similar, but now using the filtered `query`
        else:
            # Form not valid, fall back to default queryset
            query = Inventory.objects.all().order_by('-stock_date')
    else:
        form = SearchInventoryForm()
        query = Inventory.objects.all().order_by('-stock_date')

    # Set up pagination
    paginator = Paginator(query, 10)  # Show 10 inventories per page
    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    context = {
        "title": "Inventory List",
        "inventories": page,
        "form": form
    }
    return render(request, "inventory/inventory_list.html", context)

def export_to_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Product_Item_Lists.csv"'
    writer = csv.writer(response)
    writer.writerow(['CATEGORY', 'NAME', 'QTY IN STOCK', 'QTY SOLD', 'COST PER ITEM', 'SALES', 'SOLD_BY', 'SOLD_TO', 'SUPPLIER', 'STOCK DATE', 'LAST SALES DATE'])

    for product in queryset:
        writer.writerow([
            product.category, product.name, product.quantity_in_stock, product.quantity_sold,
            product.cost_per_item, product.sales, product.sold_by, product.sold_to,
            product.supplier, product.stock_date, product.last_sales_date
        ])
    return response


@login_required
def product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }

    return render(request, "inventory/product_view.html", context=context)


@login_required
def add_product(request):
    if request.method =="POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            #new_inventory.sales = float(add_form.data['cost_per_item']) * float(add_form.data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Item Successfully Added")
            return redirect("/inventory/")
    else:
        add_form = AddInventoryForm()
    return render(request, "inventory/inventory_add.html", {"form": add_form})

#compute the sales in stock
#compute quantity sold
#sell items from stock
#add cost per-item
@login_required
def sell_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        add_form = Sell_ProductForm(request.POST)  # No need for data= when initializing with POST data
        if add_form.is_valid():
            quantity_sold = int(add_form.cleaned_data['quantity'])  # Use cleaned_data for form data
            cost_sold_per_item = add_form.cleaned_data['cost_sold_per_item']
            sold_to = add_form.cleaned_data['sold_to']

            inventory.quantity_sold += quantity_sold
            inventory.quantity_in_stock -= quantity_sold
            inventory.cost_sold_per_item = cost_sold_per_item
            inventory.sold_to = sold_to
            inventory.sales += cost_sold_per_item * quantity_sold  # Assuming you want to add to existing sales
            inventory.save()

            messages.info(request, f"{quantity_sold} Items Sold Successfully")
            return redirect(f"/inventory/product/{pk}")
    else:
        add_form = Sell_ProductForm(instance=inventory)  # Use the same form name for consistency

    context = {"form": add_form}
    return render(request, "inventory/product_sales.html", context=context)


#compute the quantity in stock
#add Items to stock
#add cost per-item
@login_required
def restock_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method =="POST":
        add_form = Restock_ProductForm(data=request.POST)
        if add_form.is_valid():
            inventory.quantity = add_form.data['quantity']
            inventory.quantity_in_stock += int(add_form.data['quantity'])
            inventory.reorder_level = add_form.data['reorder_level']
            inventory.supplier = str(request.user)
            inventory.save()
            messages.info(request, str(inventory.quantity)+" Items Successfully added")
            return redirect(f"/inventory/product/{pk}")
    else:
        update_form = Restock_ProductForm(instance=inventory)
        context = {"form": update_form}
    return render(request, "inventory/product_restock.html", context=context)


#delete product from inventory 
@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.warning(request, "Item Successfully Deleted")
    return redirect("/inventory/")

#update product in inventory
@login_required
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method =="POST":
        add_form = UpdateInventoryForm(data=request.POST)
        if add_form.is_valid():
            inventory.name = add_form.data['name']
            inventory.reorder_level = add_form.data['reorder_level']
            inventory.save()
            messages.info(request, "Item Successfully Updated")
            return redirect(f"/inventory/product/{pk}")
    else:
        update_form = UpdateInventoryForm(instance=inventory)
        context = {"form": update_form}
    return render(request, "inventory/inventory_update.html", context=context)


@login_required
def dashboard(request):
    inventories = Inventory.objects.all()
    df = read_frame(inventories)

    # Ensure operations on dates are handled correctly
    df['last_sales_date'] = pd.to_datetime(df['last_sales_date'])
    df['stock_date'] = pd.to_datetime(df['stock_date'])

    # Sales graph
    sales_graph_df = df.groupby(by="last_sales_date", as_index=False).agg({'sales': 'sum'})
    sales_graph = px.line(sales_graph_df, x='last_sales_date', y='sales', title="Sales Trend")
    sales_graph_json = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

    # Best performing product
    best_performing_product_df = df.groupby('name', as_index=False).agg({'quantity_sold': 'sum'}).sort_values(by="quantity_sold", ascending=False)
    best_performing_product = px.bar(best_performing_product_df, x='quantity_sold', y='name', color='name', title="Best Performing Product")
    best_performing_product_json = json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)

    # # Most product in stock
    most_product_in_stock_df = df.groupby('name', as_index=False).agg({'quantity_in_stock': 'sum'}).sort_values(by="quantity_in_stock", ascending=False)
    most_product_in_stock_horizontal_bar = px.bar(most_product_in_stock_df, y='name', x='quantity_in_stock', color='name', orientation='h', title="Most Product In Stock")
    # If you need to convert the bar chart to JSON, like you did with the pie chart:
    most_product_in_stock_json = json.dumps(most_product_in_stock_horizontal_bar, cls=plotly.utils.PlotlyJSONEncoder)

    # Inventory levels over time
    inventory_levels_df = df.groupby(by='stock_date').agg({'quantity_in_stock': 'sum'}).reset_index()
    inventory_levels = px.line(inventory_levels_df, x='stock_date', y='quantity_in_stock', title='Inventory Levels Over Time')
    inventory_levels_json = json.dumps(inventory_levels, cls=plotly.utils.PlotlyJSONEncoder)

    # Sales over time by category
    sales_over_time_df = df.groupby(['last_sales_date', 'category']).agg({'sales': 'sum'}).reset_index()
    sales_over_time = px.area(sales_over_time_df, x='last_sales_date', y='sales', color='category', title='Sales Over Time by Category')
    sales_over_time_json = json.dumps(sales_over_time, cls=plotly.utils.PlotlyJSONEncoder)

    # Calculate total cost and net profit
    df['total_cost'] = df['cost_sold_per_item'] * df['quantity_sold']
    df['net_profit'] = df['sales'] - df['total_cost']

    # Sales and cost metrics over time
    metrics_over_time_df = df.groupby('last_sales_date').agg({'sales': 'sum', 'total_cost': 'sum', 'net_profit': 'sum'}).reset_index()
    metrics_over_time = px.line(metrics_over_time_df, x='last_sales_date', y=['sales', 'total_cost', 'net_profit'], title='Sales and Cost Metrics Over Time', markers=True)
    metrics_over_time.update_layout(yaxis_title='USD')
    metrics_over_time_json = json.dumps(metrics_over_time, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "sales_graph": sales_graph_json,
        "best_performing_product": best_performing_product_json,
        "most_product_in_stock": most_product_in_stock_json,
        "inventory_levels": inventory_levels_json,
        "sales_over_time": sales_over_time_json,
        "metrics_over_time": metrics_over_time_json,
        "inventories": inventories,
    }

    return render(request, "inventory/dashboard.html", context=context)