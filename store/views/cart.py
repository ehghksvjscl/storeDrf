"""
Cart View
"""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from store.serializers import CartCreateSerializer, CartSerializer

from store.queries.cart import get_all_cart, get_cart_list


class CartView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = get_all_cart()

    def post(self, request):
        """장바구니에 상품 추가 API

        - request
        {
            "option_id": 1,
            "quantity": 1
        }

        - response
        {
            "id": 1,
            "user": 1,
            "option": 1,
            "quantity": 1,
            "created_at": "2021-05-01T00:00:00Z"
        }

        - error
        {
            400 : Option {...} is not available
            400 : Option {...} is already in cart
        }

        """
        serializer = CartCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            cart = serializer.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Get cart"""
        cart = get_cart_list(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
