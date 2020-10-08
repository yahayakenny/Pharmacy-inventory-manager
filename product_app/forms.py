from django.forms import ModelForm
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['amount_received', 'issued_to', 'item_number', ]

class IssueForm(ModelForm):
    class Meta:
        model = Product
        fields = ['issued_quantity']

class AddForm(ModelForm):
    class Meta:
        model = Product
        fields = ['received_quantity']