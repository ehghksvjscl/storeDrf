"""
Cart View
"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from store.models import Cart
from store.serializers import CartCreateSerializer, CartSerializer


class CartView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()

    def post(self, request):
        """Add product to cart"""
        serializer = CartCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            cart = serializer.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Get cart"""
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
