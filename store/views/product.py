"""
Product View
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


from store.models import Option
from store.serializers import OptionSerializer, ProductSerializer
from store.queries.product import get_all_product, get_product_or_404


class ProductListview(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        """Get product list"""
        products = get_all_product()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):

    permission_classes = (AllowAny,)
    queryset = Option.objects.all()

    def get(self, request, pk=None):
        """Get product detail"""
        product_id = pk

        product_instance = get_product_or_404(id=product_id)
        option_instance = product_instance.options.all()

        option_serializer = OptionSerializer(option_instance, many=True)
        product_serializer = ProductSerializer(product_instance)

        result = product_serializer.data
        result["options"] = option_serializer.data

        return Response(result, status=status.HTTP_200_OK)
