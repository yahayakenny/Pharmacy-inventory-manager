from django.forms import ModelForm
from .models import *

class AddForm(ModelForm):
    class Meta:
        model = Product
        fields = ['received_quantity']

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ["quantity", "amount_received", "issued_to"]