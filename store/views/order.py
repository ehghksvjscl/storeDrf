"""
Order View
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from store.models import Order
from store.serializers import (
    OrderSerializer,
    OrderCreateSerializer
)

class OrderViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer

        return self.serializer_class