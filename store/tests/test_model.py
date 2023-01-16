"""
Test Model
"""

from django.test import TestCase
from store.models import Product, Option

def createProduct(**params: dict) -> Product:
    """ Create and return a Product """
    return Product.objects.create(**params)

def createOption(**params: dict) -> Option:
    """ Create and return a Option """
    return Option.objects.create(**params)


class ProductTests(TestCase):
    """ Product model tests """

    def setUp(self) -> None:

        self.product = createProduct(
            name="상품1",
            price=10000,
        )

        self.option1 = createOption(
            product=self.product,
            name="옵션1",
            price=1000,
            stock=10,
        )

        self.option2 = createOption(
            product=self.product,
            name="옵션2",
            price=2000,
            stock=20,
        )

        return super().setUp()

    # 상품은 대표 이름, 기본 가격이 설정되어 있고, 하위 옵션으로 구성되어 있습니다.
    def test_product_has_name_and_price_and_options(self) -> None:
        """ Product has name, price and options """
        self.assertEqual(self.product.name, "상품1")
        self.assertEqual(self.product.price, 10000)
        self.assertEqual(self.product.options.count(), 2)