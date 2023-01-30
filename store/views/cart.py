"""
Cart View
"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

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
            return Response(CartSerializer(cart).data, status=201)

        return Response(serializer.errors, status=400)

    def get(self, request):
        """Get cart"""
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)
