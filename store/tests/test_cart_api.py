"""
Test Cart API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from store.models import Product, Option

ORDER_URL = reverse("store:order-create")
CART_URL = reverse("store:cart")


def create_user(**parms):
    """Create and reutnr a user"""
    return get_user_model().objects.create_user(**parms)


class CartAPITests(TestCase):
    """Test Cart API"""

    def setUp(self):
        """Set up test environment"""
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="userpassword123")
        self.client.force_authenticate(self.user)

    def test_cart_has_option(self):
        """장바구니에는 옵션을 설정한 상품을 담을 수 있습니다."""

        call_command("mock_store")
        product = Product.objects.get(name="위처3")
        option = Option.objects.get(product=product, name="기본")

        payload = {"product": product.id, "option": option.id, "quantity": 1}

        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_cart_can_create_order(self):
        """장바구니에서는 다수의 상품을 한 번에 구매(주문서 생성)할 수 있습니다."""
        # given
        call_command("mock_store")
        last_option = Option.objects.all().last()
        first_option = Option.objects.all().first()

        payload1 = {
            "product": last_option.product.id,
            "option": last_option.id,
            "quantity": 10,
        }
        payload2 = {
            "product": first_option.product.id,
            "option": first_option.id,
            "quantity": 1,
        }
        res = self.client.post(CART_URL, payload1)
        res = self.client.post(CART_URL, payload2)

        # when
        res = self.client.get(CART_URL)
        payload = {
            "options": [
                {
                    "product": item["product"]["id"],
                    "name": item["option"]["name"],
                    "quantity": item["quantity"],
                }
                for item in res.data
            ]
        }

        # then
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_cart_can_not_create_order_when_option_is_sold_out(self):
        """장바구니에 담긴 상품 옵션 중 재고량이 0인 상품이 포함되어 있다면, 구매가 불가능합니다."""

        call_command("mock_store")
        last_option = Option.objects.all().last()

        payload = {
            "options": [
                {
                    "product": last_option.product.id,
                    "name": last_option.name,
                    "quantity": 10,
                }
            ]
        }
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_search_order_list(self):
        """유저는 바로 구매, 장바구니 구매와 상관없이 주문 내역 리스트를 조회할 수 있습니다."""
        call_command("mock_store")

        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
