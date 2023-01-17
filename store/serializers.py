"""
Order Serializer
"""

from rest_framework import serializers
from store.models import Order, Purchase, Option

class OptionSerializer(serializers.ModelSerializer):
    """Serializer for Option"""

    class Meta:
        model = Option
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase"""

    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'order', 'product', 'quantity', 'options', 'created_at')

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'purchases', 'quantity', 'shipping_fee', 'shipping_address', 'total_price', 'is_cart', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at')

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    options = serializers.ListField()

    def validate_options(self, value):
        """Validate options"""
        if len(value) == 0:
            raise serializers.ValidationError('Options are required')
        return value

    class Meta:
        model = Order
        fields = ('id', 'user', 'quantity', 'shipping_fee', 'shipping_address', 'total_price', 'is_cart', 'created_at', 'updated_at', 'options')
        read_only_fields = ('id', 'user', 'created_at')