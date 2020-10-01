from django.shortcuts import render, redirect
from product_app.forms import *
from product_app.models import Product, Sale
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'products/index.html', {'products': products})

@login_required
def sales_form(request):
    form = SalesForm()
    if request.method == 'POST':
        form = SalesForm(request.POST or None) 
        if form.is_valid():
            form.save()
            return redirect('receipt') 
    return render(request, 'products/sales_form.html', {'form': form})

@login_required
def receipt(request): 
    sales = Sale.objects.all()
    total  = sum([items.amount_received for items in sales])
    change = sum([items.get_change() for items in sales])
    net = total - change
    return render(request, 'products/receipt.html', {'sales': sales, 'total': total, 'change': change, 'net': net})

@login_required
def update(request,customer_id):
    update = Sale.objects.get(id = customer_id)
    form = SalesForm(instance = update)
    if request.method == 'POST':
        form = SalesForm(request.POST, instance = update )
        if form.is_valid():
            form.save()
            return redirect('receipt')
    return render(request, 'products/sales_form.html', {'form': form})

@login_required
def delete(request, customer_id):
    customer_delete = Sale.objects.get(id = customer_id)
    customer_delete.delete()
    return redirect('receipt')

@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def issue_item(request, pk):
    issued_item = Product.objects.get(id = pk)
    form = IssueForm(request.POST or None, instance=issued_item)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.total_quantity -= instance.issued_quantity
        instance.save()
        return redirect('home')

    return render (request, 'products/add_item.html', {'form': form, 'issued_item': issued_item})
    
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