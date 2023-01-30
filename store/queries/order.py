"""
Query for order
"""

from .option import get_option, set_is_sold_out
from .purchase import create_purchase, total_order_price


def extend_order(order, user, options):
    """Create order"""
    total_price = 0
    total_quantity = 0
    total_shipping_fee = 0

    # TODO Refactor

    for option in options:
        option_instance = get_option(option["product"], option["name"])
        purchase = create_purchase(user, option, order, option_instance)
        total_price += total_order_price(purchase)
        total_quantity += option["quantity"]
        option_instance.stock -= option["quantity"]
        option_instance.is_sold_out = set_is_sold_out(
            option_instance, option["quantity"]
        )
        option_instance.save()

    order.total_price = total_price
    order.quantity = total_quantity
    order.shipping_fee = total_shipping_fee
    order.save()

    return order
