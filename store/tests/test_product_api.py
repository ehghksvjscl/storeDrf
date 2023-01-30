"""
Test Product API
"""

from django.test import TestCase, RequestFactory
from django.core.management import call_command
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from store.models import Product
from store.views.product import ProductDetailView


def product_detail_url(product_id):
    """Create and return a product detail URL."""
    return reverse("store:product-detail", args=[product_id])


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()

    # 비회원들은 상품 정보를 조회할 수 있습니다.
    def test_anonymous_user_can_search_order(self):
        call_command("mock_store")
        product_id = Product.objects.all().first().id

        request = self.factory.get(product_detail_url(product_id))
        request.user = AnonymousUser()

        res = ProductDetailView.as_view()(request, pk=product_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
