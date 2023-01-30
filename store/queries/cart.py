"""
Query for cart
"""

from store.models import Cart


def get_all_cart(**kwargs):
    """Get all cart"""
    return Cart.objects.all()


def get_cart_list(**kwargs):
    """Get cart list"""
    return Cart.objects.filter(**kwargs)


def create_cart(**kwargs):
    """Create cart"""
    return Cart.objects.create(**kwargs)
