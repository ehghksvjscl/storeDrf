"""
Option View
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from store.models import Option, Product
from store.serializers import OptionSerializer, ProductSerializer


class ProductListview(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        """Get product list"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):

    permission_classes = (AllowAny,)
    queryset = Option.objects.all()

    def get(self, request, pk=None):
        """Get product detail"""
        product_id = pk

        product_instance = get_object_or_404(Product, id=product_id)
        option_instance = product_instance.options.all()

        option_serializer = OptionSerializer(option_instance, many=True)
        product_serializer = ProductSerializer(product_instance)

        result = product_serializer.data
        result["options"] = option_serializer.data

        return Response(result, status=status.HTTP_200_OK)
