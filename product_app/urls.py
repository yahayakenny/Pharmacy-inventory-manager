from django.urls import  path
from product_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('receipt/', views.receipt, name = "receipt"),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('',auth_views.LoginView.as_view(template_name = 'products/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'products/logout.html'), name='logout'), 
    path('home/<int:product_id>/', views.product_detail, name='product_detail'),
    path('issue_item/<str:pk>/', views.issue_item, name='issue_item'),   
    path('add_to_stock/<str:pk>/', views.add_to_stock, name='add_to_stock'),
    path('all_sales/', views.all_sales, name = 'all_sales')

]
