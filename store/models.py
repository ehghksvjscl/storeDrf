"""
Database Store models
"""
# built-in

from django.db import models


class Product(models.Model):
    """Product models"""
    name = models.CharField(max_length=255, verbose_name="대표이름")
    price = models.PositiveBigIntegerField(default=0, verbose_name="기본가격")


class Option(models.Model):
    """Option models"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=255, verbose_name="옵션명")
    price = models.PositiveBigIntegerField(default=0, verbose_name="옵션가격")
    stock = models.PositiveIntegerField(default=0, verbose_name="재고")


class Cart(models.Model):
    """Cart models"""
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="장바구니 담은 날짜")


class Order(models.Model):
    """Order models"""
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")
    shipping_fee = models.PositiveBigIntegerField(default=3000, verbose_name="배송비")
    shipping_address = models.CharField(max_length=255, default="", verbose_name="배송지")
    total_price = models.PositiveBigIntegerField(default=0, verbose_name="총가격")
    is_cart = models.BooleanField(default=False, verbose_name="장바구니 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="주문일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    
class Purchase(models.Model):
    """Purchase models"""
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="purchases")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchases")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="purchases")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="purchases")
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")
    total_price = models.PositiveBigIntegerField(default=0, verbose_name="옵션 총 가격")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="구매일")
