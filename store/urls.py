"""URL mappings for the store app"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from store.views.order import OrderViewSet
from store.views.option import ProductViewSet


router = DefaultRouter()
router.register('order', OrderViewSet)
router.register('product', ProductViewSet)

app_name = 'store'

urlpatterns= [
    path('', include(router.urls))
]