"""
Option View
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from store.models import Option, Product
from store.serializers import (
    OptionSerializer,
    ProductSerializer
)

class ProductView(APIView):

    permission_classes = (AllowAny,)
    queryset = Option.objects.all()

    def get(self, request, pk=None):
        """ Get product detail """
        product_id = pk
        optioon_instance = Option.objects.filter(product_id=product_id)
        product_instance = Product.objects.get(id=product_id)
        option_serializer = OptionSerializer(optioon_instance, many=True)
        product_serializer = ProductSerializer(product_instance)

        result = product_serializer.data
        result['options'] = option_serializer.data

        return Response(result)