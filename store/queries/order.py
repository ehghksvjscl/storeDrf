"""
Query for order
"""

from store.models import Order, Purchase, Option

def get_option(product, name):
    """Get option"""
    return Option.objects.filter(product=product,name=name) \
        .select_related('product').first()

def _total_option_price(option, quantity):
    """Total price"""
    return (option.product.price + option.price) * quantity

def create_purchase(user, quantity, order, option):
    """Create purchase"""

    result = Purchase.objects.create(
        user=user,
        product=option.product,
        option=option,
        order=order,
        quantity=quantity,
        total_price=_total_option_price(option, quantity)
    )

    return result

def _total_order_price(purchase):
    """Total price"""
    return purchase.total_price

def _shipping_fee(price, basePrice):
    """Shipping fee"""
    if price >= 20000:
        return 0
    
    return basePrice

def extend_order(order, user, options):
    """Create order"""
    total_price = 0

    for option in options:
        optionInstance = get_option(option['product'], option['name'])
        purchase = create_purchase(user, option['quantity'], order, optionInstance)
        total_price += _total_order_price(purchase)
        optionInstance.stock -= option['quantity']
        optionInstance.save()

    order.total_price = total_price
    order.shipping_fee = _shipping_fee(total_price, order.shipping_fee)
    order.save()

    return order

