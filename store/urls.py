"""URL mappings for the store app"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from store.views.order import OrderViewSet


router = DefaultRouter()
router.register('order', OrderViewSet)

app_name = 'order'

urlpatterns= [
    path('', include(router.urls))
]