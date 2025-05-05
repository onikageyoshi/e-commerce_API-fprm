from django.urls import path
from .views import ProductListCreateView, OrderListCreateView, HomePageView



urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
]
