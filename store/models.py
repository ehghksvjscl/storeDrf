"""
Database Store models
"""

from django.db import models


class Product(models.Model):
    """Product models"""
    name = models.CharField(max_length=255, verbose_name="대표이름")
    price = models.PositiveBigIntegerField(default=0, verbose_name="기본가격")

    def __str__(self):
        return self.name

class Option(models.Model):
    """Option models"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=255, verbose_name="옵션명")
    price = models.PositiveBigIntegerField(default=0, verbose_name="옵션가격")
    stock = models.PositiveIntegerField(default=0, verbose_name="재고")

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Cart models"""
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="장바구니 담은 날짜")

    def __str__(self):
        return self.product + " " + self.option

class Order(models.Model):
    """Order models"""
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")
    shipping_price = models.PositiveBigIntegerField(default=3000, verbose_name="배송비")
    total_price = models.PositiveBigIntegerField(default=0, verbose_name="총가격")
    is_cart = models.BooleanField(default=False, verbose_name="장바구니 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="주문일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.user.email + " " + self.product.name + " " + self.option.name