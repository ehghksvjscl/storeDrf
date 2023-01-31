"""
Test Order API
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


def order_detail_url(order_id):
    """Create and return a order detail URL."""
    return reverse("store:order-detail", args=[order_id])


class PublicOrderAPITests(TestCase):
    """Public Order API Tests"""

    def setUp(self):
        """Set up test environment"""
        self.client = APIClient()

    def test_not_create_order_without_login(self):
        """비회원들은 주문서를 생성할 수 없습니다."""

        payload = {"options": [{"product": 1, "name": "기본", "quantity": 1}]}
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderAPITests(TestCase):
    """Private Order API Tests"""

    def setUp(self):
        """Set up test environment"""

        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="userpassword123")
        self.client.force_authenticate(self.user)

    def test_not_create_without_option(self):
        """옵션이 지정되지 않으면 주문서 생성이 불가합니다."""
        payload = {"options": []}
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shipping_fee_is_zero_when_total_price_is_over_20000(self):
        """유저가 주문하는 금액의 합계가 20,000원이 넘으면 배송비가 0원으로 변경됩니다."""

        call_command("mock_store")
        product = Product.objects.get(name="위처3")
        payload = {
            "options": [
                {"product": product.id, "name": "기본", "quantity": 10},
                {"product": product.id, "name": "DLC 하츠 오브 스톤", "quantity": 10},
            ]
        }
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.data["shipping_fee"], 0)

        return payload

    def test_option_stock_is_changed_when_order_is_created(self):
        """유저가 주문서를 생성 완료한 순간 옵션의 재고량에 반영이 되어야 합니다."""

        res = self.test_shipping_fee_is_zero_when_total_price_is_over_20000()
        options = Option.objects.filter(
            name__in=[option["name"] for option in res["options"]],
        )

        for option in options:
            self.assertEqual(option.stock, 0)

    def test_order_has_product_option_quantity_and_price_and_shipping_fee(self):
        """주문 내역에는 상품, 옵션, 구매 수량, 옵션별 총 주문 가격 정보들과  배송비가 표시되어야 합니다."""

        call_command("mock_store")
        product = Product.objects.get(name="위처3")
        payload = {
            "options": [
                {"product": product.id, "name": "기본", "quantity": 10},
                {"product": product.id, "name": "DLC 하츠 오브 스톤", "quantity": 10},
            ]
        }
        res = self.client.post(ORDER_URL, payload, format="json")

        url = order_detail_url(res.data["id"])
        res = self.client.get(url)

        self.assertEqual(len(res.data["purchases"]), 2)
        self.assertIn("quantity", res.data)
        self.assertIn("total_price", res.data)
        self.assertIn("shipping_fee", res.data)

        for purchase in res.data["purchases"]:
            self.assertIn("product", purchase)
            self.assertIn("quantity", purchase)
            self.assertIn("total_price", purchase)
            self.assertIn("option", purchase)

    def test_option_is_sold_out_when_stock_is_zero(self):
        """유저가 주문서를 생성 완료한 순간 옵션의 재고량이 0이 되면 옵션의 판매 여부가 품절로 변경됩니다."""
        
        res = self.test_shipping_fee_is_zero_when_total_price_is_over_20000()

        for option in res["options"]:
            option = Option.objects.get(name=option["name"], product=option["product"])
            self.assertTrue(option.is_sold_out, True)
