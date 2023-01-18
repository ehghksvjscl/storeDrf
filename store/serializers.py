"""
Order Serializer
"""

from rest_framework import serializers
from store.models import Order, Purchase, Option, Product
from store.queries.order import extend_order, get_option

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product"""

    class Meta:
        model = Product
        fields = ('name', )

class OptionSerializer(serializers.ModelSerializer):
    """Serializer for Option"""

    class Meta:
        model = Option
        fields = ('id', 'name', 'price', 'stock')
        read_only_fields = ('id', 'created_at')


class OrderOptionSerializer(serializers.ModelSerializer):
    """Serializer for OrderOption"""
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = Option
        fields = ('id', 'name', 'product', 'quantity')
        read_only_fields = ('id', 'created_at')

class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase"""

    option = OptionSerializer(read_only=True)
    product = ProductSerializer(read_only=True) 


    class Meta:
        model = Purchase
        fields = ('id', 'order', 'quantity', 'shipping_fee', 'option', 'product', 'total_price', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'purchases', 'quantity', 'shipping_fee', 'shipping_address', 'total_price', 'is_cart', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    options = serializers.ListField(write_only=True)

    def validate(self, data):
        """Validate options"""

        options = data.get('options')
        if len(options) == 0:
            raise serializers.ValidationError('Options is required')

        for option in options:
            if get_option(option['product'], option['name']) is None:
                raise serializers.ValidationError(f"Option {option['name']} is not available")

            if option.get('quantity') is None:
                raise serializers.ValidationError(f"Quantity is required")

            if option.get('name') is None:
                raise serializers.ValidationError(f"Name is required")

            if option.get('product') is None:
                raise serializers.ValidationError(f"Product is required")

        return data

    def create(self, validated_data):
        """Create order"""
        user = self.context['request'].user
        options = validated_data.pop('options')
        order = Order.objects.create(user=user)
        order = extend_order(order, user, options)

        return order

    class Meta:
        model = Order
        fields = ('id', 'user', 'quantity', 'shipping_fee', 'shipping_address', 'total_price', 'is_cart', 'created_at', 'options')
        read_only_fields = ('id', 'user', 'created_at', 'total_price', 'is_cart', 'quantity', 'shipping_fee', 'shipping_address')