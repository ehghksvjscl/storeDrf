"""
Option View
"""

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from store.models import Option, Product
from store.serializers import (
    OptionSerializer,
    ProductSerializer
)

class ProductViewSet(mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = OptionSerializer
    permission_classes = (AllowAny,)
    queryset = Option.objects.all()

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        optioon_instance = Option.objects.filter(product_id=product_id)
        product_instance = Product.objects.get(id=product_id)
        option_serializer = self.get_serializer(optioon_instance, many=True)
        product_serializer = ProductSerializer(product_instance)

        result = product_serializer.data
        result['options'] = option_serializer.data

        return Response(result)