"""URL mappings for the store app"""

from django.urls import path


from store.views.order import OrderView, OrderDetailView
from store.views.product import ProductDetailView
from store.views.cart import CartView


app_name = "store"

urlpatterns = [
    path("orders/", OrderView.as_view(), name="order-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("carts/", CartView.as_view(), name="cart"),
]
