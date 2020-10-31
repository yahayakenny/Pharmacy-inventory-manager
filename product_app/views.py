from django.shortcuts import render, redirect
from product_app.forms import AddForm, SaleForm
from product_app.models import Product,Sale
from django.contrib.auth.decorators import login_required
from product_app.filters import ProductFilter


# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset = products)
    products = product_filters.qs

    return render(request, 'products/index.html', {
        'products': products, 'product_filters': product_filters,
    })


@login_required
def receipt(request): 
    sales = Sale.objects.all().order_by('-id')
    return render(request, 
    'products/receipt.html', 
    {'sales': sales,
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
            #To keep track of the stock remaining after sales
            issued_quantity = int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save()

            print(issued_item.item_name)
            print(request.POST['quantity'])
            print(issued_item.total_quantity)

            return redirect('receipt') 

    return render (request, 'products/issue_item.html',
     {
    'sales_form': sales_form,
    })
    

@login_required
def add_to_stock(request, pk):
    issued_item = Product.objects.get(id = pk)
    form = AddForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST['received_quantity'])
            issued_item.total_quantity += added_quantity
            issued_item.save()

            #To add to the remaining stock quantity is reducing
            print(added_quantity)
            print (issued_item.total_quantity)
            return redirect('home')

    return render (request, 'products/add_to_stock.html', {'form': form})