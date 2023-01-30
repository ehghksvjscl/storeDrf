"""
Query for product
"""
from django.shortcuts import get_object_or_404

from store.models import Product


def get_all_product(**kwargs):
    """Get all product"""
    return Product.objects.all()


def get_product_or_404(**kwargs):
    """Get product or 404"""
    return get_object_or_404(Product, **kwargs)
