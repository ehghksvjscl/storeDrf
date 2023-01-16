"""
Test Model
"""

from django.test import TestCase
from store.models import Product, Option

# 상품은 대표 이름, 기본 가격이 설정되어 있고, 하위 옵션으로 구성되어 있습니다.
class ProductTests(TestCase):

    # 상품은 대표 이름, 기본 가격이 설정되어 있고, 하위 옵션으로 구성되어 있습니다.
    def test_product_has_name_and_price_and_options(self):
        pass