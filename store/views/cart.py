"""
Cart View
"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from store.models import Cart
from store.serializers import (
    CartCreateSerializer,
    ProductSerializer
)

class CartView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()

    def post(self, request):
        """ Add product to cart """
        serializer = CartCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)