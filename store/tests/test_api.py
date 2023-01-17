"""
Test Model
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.management import call_command

from rest_framework.test import APIClient
from rest_framework import status

from store.models import Product

ORDER_URL = reverse('store:order-list')

def create_user(**parms):
    """Create and reutnr a user"""
    return get_user_model().objects.create_user(**parms)


class OrderAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    # 옵션이 지정되지 않으면 주문서 생성이 불가합니다.
    def test_not_create_without_option(self):
        self.user = create_user(email='user@example.com', password='userpassword123')
        self.client.force_authenticate(self.user)

        payload = {
            "options": []
        }
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # 비회원들은 주문서를 생성할 수 없습니다.
    def test_not_create_order_without_login(self):
        payload = {
            "options": [
                {
                    "product": 1,
                    "name": "기본",
                    "quantity": 1
                }
            ]
        }
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # 유저가 주문하는 금액의 합계가 20,000원이 넘으면 배송비가 0원으로 변경됩니다.
    def test_shipping_fee_is_zero_when_total_price_is_over_20000(self):
        pass

    # 유저가 주문서를 생성 완료한 순간 옵션의 재고량에 반영이 되어야 합니다.
    def test_option_stock_is_changed_when_order_is_created(self):
        pass

    # 주문 내역에는 상품, 옵션, 구매 수량, 옵션별 총 주문 가격 정보들과  배송비가 표시되어야 합니다.
    def test_order_has_product_option_quantity_and_price_and_shipping_fee(self):
        pass

class ProductAPITests(TestCase):
    
    # 비회원들은 상품 정보를 조회할 수 있습니다.
    def test_anonymous_user_can_search_order(self):
        pass

class OptionAPITests(TestCase):
    # 유저가 주문서를 생성 완료한 순간 옵션의 재고량이 0이 되면 옵션의 판매 여부가 품절로 변경됩니다.
    def test_option_is_sold_out_when_stock_is_zero(self):
        pass

class CartAPITests(TestCase):

    #장바구니에는 옵션을 설정한 상품을 담을 수 있습니다.
    def test_cart_has_option(self):
        pass

    # 장바구니에서는 다수의 상품을 한 번에 구매(주문서 생성)할 수 있습니다.
    def test_cart_can_create_order(self):
        pass

    # 장바구니에 담긴 상품 옵션 중 재고량이 0인 상품이 포함되어 있다면, 구매가 불가능합니다.
    def test_cart_can_not_create_order_when_option_is_sold_out(self):
        pass

    # 장바구니에서는 담긴 상품을 선택하여 주문할 수 있습니다.
    def test_cart_can_create_order_with_selected_product(self):
        pass    

    # 유저는 바로 구매, 장바구니 구매와 상관없이 주문 내역 리스트를 조회할 수 있습니다.
    def test_user_can_search_order_list(self):
        pass
