"""
Test Model
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from store.models import Product, Option
from store.views.option import ProductView

ORDER_URL = reverse('store:order-create')
CART_URL = reverse('store:cart')

def create_user(**parms):
    """Create and reutnr a user"""
    return get_user_model().objects.create_user(**parms)

def order_detail_url(order_id):
    """Create and return a order detail URL."""
    return reverse('store:order-detail', args=[order_id])

def product_detail_url(product_id):
    """Create and return a product detail URL."""
    return reverse('store:product-detail', args=[product_id])

class PublicOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()  

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


class PrivateOrderAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='userpassword123')
        self.client.force_authenticate(self.user)

    # 옵션이 지정되지 않으면 주문서 생성이 불가합니다.
    def test_not_create_without_option(self):
        payload = {
            "options": []
        }
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # 유저가 주문하는 금액의 합계가 20,000원이 넘으면 배송비가 0원으로 변경됩니다.
    def test_shipping_fee_is_zero_when_total_price_is_over_20000(self):
        call_command('mock_store')
        product = Product.objects.get(name='위처3')
        payload = {
            "options": [
                {
                    "product": product.id,
                    "name": "기본",
                    "quantity": 10
                },
                {
                    "product": product.id,
                    "name": "DLC 하츠 오브 스톤",
                    "quantity": 10
                }
            ]
        }
        res = self.client.post(ORDER_URL, payload, format='json')
        self.assertEqual(res.data['shipping_fee'], 0)

        return payload

    # 유저가 주문서를 생성 완료한 순간 옵션의 재고량에 반영이 되어야 합니다.
    def test_option_stock_is_changed_when_order_is_created(self):

        res = self.test_shipping_fee_is_zero_when_total_price_is_over_20000()
        options = Option.objects.filter(
            name__in=[option['name'] for option in res['options']],
        )

        for option in options:
            self.assertEqual(option.stock, 0)

    # 주문 내역에는 상품, 옵션, 구매 수량, 옵션별 총 주문 가격 정보들과  배송비가 표시되어야 합니다.
    def test_order_has_product_option_quantity_and_price_and_shipping_fee(self):
        # given
        call_command('mock_store')
        product = Product.objects.get(name='위처3')
        payload = {
            "options": [
                {
                    "product": product.id,
                    "name": "기본",
                    "quantity": 10
                },
                {
                    "product": product.id,
                    "name": "DLC 하츠 오브 스톤",
                    "quantity": 10
                }
            ]
        }
        res = self.client.post(ORDER_URL, payload, format='json')

        # when
        url = order_detail_url(res.data['id'])
        res = self.client.get(url)

        # then
        self.assertEqual(len(res.data['purchases']), 2)
        self.assertIn('quantity', res.data)
        self.assertIn('total_price', res.data)
        self.assertIn('shipping_fee', res.data)

        for purchase in res.data['purchases']:
            self.assertIn('product', purchase)
            self.assertIn('quantity', purchase)
            self.assertIn('total_price', purchase)
            self.assertIn('option', purchase)

    # 유저가 주문서를 생성 완료한 순간 옵션의 재고량이 0이 되면 옵션의 판매 여부가 품절로 변경됩니다.
    def test_option_is_sold_out_when_stock_is_zero(self):
        res = self.test_shipping_fee_is_zero_when_total_price_is_over_20000()

        for option in res['options']:
            option = Option.objects.get(name=option['name'], product=option['product'])
            self.assertTrue(option.is_sold_out, True)


class ProductAPITests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()

    # 비회원들은 상품 정보를 조회할 수 있습니다.
    def test_anonymous_user_can_search_order(self):
        call_command('mock_store')
        product_id = Product.objects.all().first().id

        request = self.factory.get(product_detail_url(product_id))
        request.user = AnonymousUser()

        res = ProductView.as_view()(request, pk=product_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class CartAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='userpassword123')
        self.client.force_authenticate(self.user)

    #장바구니에는 옵션을 설정한 상품을 담을 수 있습니다.
    def test_cart_has_option(self):
        call_command('mock_store')
        product = Product.objects.get(name='위처3')
        option = Option.objects.get(product=product, name='기본')

        payload = {
            'product': product.id,
            'option': option.id,
            'quantity': 1
        }

        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # 장바구니에서는 다수의 상품을 한 번에 구매(주문서 생성)할 수 있습니다.
    def test_cart_can_create_order(self):
        # given
        call_command('mock_store')
        last_option = Option.objects.all().last()
        first_option = Option.objects.all().first()

        payload1 = {
            'product': last_option.product.id,
            'option': last_option.id,
            'quantity': 10
        }
        payload2 = {
            'product': first_option.product.id,
            'option': first_option.id,
            'quantity': 1
        }
        res = self.client.post(CART_URL, payload1)
        res = self.client.post(CART_URL, payload2)

        # when  
        res = self.client.get(CART_URL)
        payload = {
            'options': [
                {
                    'product': res.data[0]['product']['id'],
                    'name': res.data[0]['option']['name'],
                    'quantity': res.data[0]['quantity']
                },
                {
                    'product': res.data[1]['product']['id'],
                    'name': res.data[1]['option']['name'],
                    'quantity': res.data[1]['quantity']
                }
            ]
        }

        # then
        res = self.client.post(ORDER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # 장바구니에 담긴 상품 옵션 중 재고량이 0인 상품이 포함되어 있다면, 구매가 불가능합니다.
    def test_cart_can_not_create_order_when_option_is_sold_out(self):
        pass

    # 장바구니에서는 담긴 상품을 선택하여 주문할 수 있습니다.
    def test_cart_can_create_order_with_selected_product(self):
        pass    

    # 유저는 바로 구매, 장바구니 구매와 상관없이 주문 내역 리스트를 조회할 수 있습니다.
    def test_user_can_search_order_list(self):
        pass
