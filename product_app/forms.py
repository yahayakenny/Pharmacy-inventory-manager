from django.forms import ModelForm
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['item_name', 'category_name', 'total_quantity']


class SalesForm(ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'


class IssueForm(ModelForm):
    class Meta:
        model = Product
        fields = ['issued_quantity']

class AddForm(ModelForm):
    class Meta:
        model = Product
        fields = ['received_quantity', 'received_by']