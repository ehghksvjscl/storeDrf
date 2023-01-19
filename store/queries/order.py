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

def _shipping_fee(price, basePrice=3000):
    """Shipping fee"""
    if price >= 20000:
        return 0
    
    return basePrice

def create_purchase(user, option_parms, order, option):
    """Create purchase"""
    total_price = _total_option_price(option, option_parms['quantity'])

    result = Purchase.objects.create(
        user=user,
        product=option.product,
        option=option,
        order=order,
        quantity=option_parms['quantity'],
        total_price=total_price,
        shipping_fee = _shipping_fee(total_price)
    )

    return result

def _total_order_price(purchase):
    """Total price"""
    return purchase.total_price

def extend_order(order, user, options):
    """Create order"""
    total_price = 0
    total_quantity = 0
    total_shipping_fee = 0

    # TODO Refactor

    for option in options:
        option_instance = get_option(option['product'], option['name'])
        purchase = create_purchase(user, option, order, option_instance)
        total_price += _total_order_price(purchase)
        total_quantity += option['quantity']
        option_instance.stock -= option['quantity']
        option_instance.save()

    order.total_price = total_price
    order.quantity = total_quantity
    order.shipping_fee = total_shipping_fee
    order.save()

    return order

