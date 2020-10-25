import django_filters
from product_app.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['item_name']

class CategoryFilter(django_filters.FilterSet):
    class Meta: 
        model = Category
        fields = ['name']