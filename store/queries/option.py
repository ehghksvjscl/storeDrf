from store.models import Option


def get_option(product, name):
    """Get option"""
    return (
        Option.objects.filter(product=product, name=name)
        .select_related("product")
        .first()
    )


def total_option_price(option, quantity):
    """Total price"""
    return (option.product.price + option.price) * quantity


def set_is_sold_out(option, quantity):
    """Set is sold out"""
    if option.stock - quantity <= 0:
        return True

    return False
