"""
Order View
"""

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from store.models import Order
from store.serializers import OrderSerializer

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Order.objects.all()