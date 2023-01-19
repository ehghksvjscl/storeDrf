"""URL mappings for the store app"""

from django.urls import path


from store.views.order import OrderView,OrderDetailView
from store.views.option import ProductView
from store.views.cart import CartView


app_name = 'store'

urlpatterns= [
    path('order/', OrderView.as_view(), name='order-create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('product/<int:pk>/', ProductView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
]