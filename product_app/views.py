from django.shortcuts import render, redirect
from product_app.forms import *
from product_app.models import Product
from django.contrib.auth.decorators import login_required
from product_app.filters import ProductFilter, CategoryFilter


# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset = products)
    products = product_filters.qs

    # categories = Category.objects.all()
    # category_filters = CategoryFilter(request.GET, queryset = categories)
    # categories = category_filters.qs

    return render(request, 'products/index.html', {
        'products': products, 'product_filters': product_filters,
    })


@login_required
def receipt(request): 
    sales = Sale.objects.all().order_by('-id')
    total  = sum([items.amount_received for items in sales])
    change = sum([items.get_change() for items in sales])
    net = total - change
    return render(request, 
    'products/receipt.html', 
    {'sales': sales,
    'total': total, 
    'change': change, 
    'net': net, 
    })


def all_sales(request):
    sales = Sale.objects.all()
    total  = sum([items.amount_received for items in sales])
    change = sum([items.get_change() for items in sales])
    net = total - change
    return render(request, 'products/all_sales.html',
     {
     'sales': sales, 
     'total': total,
     'change': change, 
     'net': net,
      })


@login_required
def update(request,product_id):
    update = Product.objects.get(id = product_id)
    form = SaleForm()
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            print(f"Here is the form {form}" )
            return redirect('receipt')
    return render(request, 'products/add_item.html', {'form': form})


@login_required
def delete(request, customer_id):
    customer_delete = Product.objects.get(id = customer_id)
    customer_delete.delete()
    return redirect('all_sales')


@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def receipt_detail(request, receipt_id):
    receipt = Sale.objects.get(id = receipt_id)
    return render(request, 'products/receipt_detail.html', {'receipt': receipt})


@login_required
def issue_item(request, pk):
    issued_item = Product.objects.get(id = pk)
    sales_form = SaleForm(request.POST)

    if request.method == 'POST':     
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.item = issued_item
            new_sale.unit_price = issued_item.unit_price   
            new_sale.save()
            return redirect('receipt') 

    return render (request, 'products/add_item.html',
     {
    'sales_form': sales_form,
    })
    

@login_required
def add_item(request, pk):
    issued_item = Product.objects.get(id = pk)
    form = IssueForm(request.POST or None, instance=issued_item)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.total_quantity += instance.issued_quantity
        instance.save()
        return redirect('home')

    return render (request, 'products/add_item.html', {'form': form, 'issued_item': issued_item})