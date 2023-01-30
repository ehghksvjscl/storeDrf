from store.models import Purchase

from .option import total_option_price


def _shipping_fee(price, basePrice=3000):
    """Shipping fee"""
    if price >= 20000:
        return 0

    return basePrice


def total_order_price(purchase):
    """Total price"""
    return purchase.total_price


def create_purchase(user, option_parms, order, option):
    """Create purchase"""
    total_price = total_option_price(option, option_parms["quantity"])

    result = Purchase.objects.create(
        user=user,
        product=option.product,
        option=option,
        order=order,
        quantity=option_parms["quantity"],
        total_price=total_price,
        shipping_fee=_shipping_fee(total_price),
    )

    return result
