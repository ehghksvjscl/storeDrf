"""
Order Serializer
"""

from rest_framework import serializers
from store.models import Order, Purchase, Option, Product, Cart
from store.queries.order import extend_order, get_option


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product"""

    class Meta:
        model = Product
        fields = ("id", "name")


class OptionSerializer(serializers.ModelSerializer):
    """Serializer for Option"""

    class Meta:
        model = Option
        fields = ("id", "name", "price", "stock")
        read_only_fields = ("id", "created_at")


class OrderOptionSerializer(serializers.ModelSerializer):
    """Serializer for OrderOption"""

    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = Option
        fields = ("id", "name", "product", "quantity")
        read_only_fields = ("id", "created_at")


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase"""

    option = OptionSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "order",
            "quantity",
            "shipping_fee",
            "option",
            "product",
            "total_price",
            "created_at",
        )


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "purchases",
            "quantity",
            "shipping_fee",
            "shipping_address",
            "total_price",
            "is_cart",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at")


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    options = serializers.ListField(write_only=True)

    # TODO : Refactor this

    def validate(self, data):
        """Validate options"""

        options = data.get("options")
        if len(options) == 0:
            raise serializers.ValidationError("Options is required")

        for option in options:
            option_instance = get_option(option["product"], option["name"])
            if option_instance is None:
                raise serializers.ValidationError(
                    f"Option {option['name']} is not available"
                )

            if option.get("quantity") is None:
                raise serializers.ValidationError(f"Quantity is required")
            elif option_instance.stock < option.get("quantity"):
                raise serializers.ValidationError(f"stock is not enough")
            elif option_instance.stock == 0:
                raise serializers.ValidationError(f"stock is not enough")

            if option.get("name") is None:
                raise serializers.ValidationError(f"Name is required")

            if option.get("product") is None:
                raise serializers.ValidationError(f"Product is required")

        return data

    def create(self, validated_data):
        """Create order"""
        user = self.context["request"].user
        options = validated_data.pop("options")
        order = Order.objects.create(user=user)
        order = extend_order(order, user, options)

        return order

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "quantity",
            "shipping_fee",
            "shipping_address",
            "total_price",
            "is_cart",
            "created_at",
            "options",
        )
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "total_price",
            "is_cart",
            "quantity",
            "shipping_fee",
            "shipping_address",
        )


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart"""

    option = OptionSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "quantity", "option", "product", "created_at")
        read_only_fields = ("id", "user", "created_at")


class CartCreateSerializer(serializers.Serializer):
    """Serializer for CartCreate"""

    option = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    # TODO : Refactor (순수함수로 만들기)

    def validate(self, data):
        """Validate option"""

        option = data.get("option")
        user = self.context["request"].user

        option_instance = Option.objects.filter(id=option).first()
        if option_instance is None:
            raise serializers.ValidationError(f"Option {option} is not available")

        if Cart.objects.filter(option=option_instance.id, user=user).exists():
            raise serializers.ValidationError(f"Option {option} is already in cart")

        return data

    # TODO : Refactor (어떻게 하면 좋을까?)
    def create(self, validated_data):
        """Create cart"""
        user = self.context["request"].user
        option = validated_data.pop("option")
        quantity = validated_data.pop("quantity")

        option_instence = (
            Option.objects.filter(id=option).select_related("product").first()
        )

        cart = Cart.objects.create(
            user=user,
            option=option_instence,
            product=option_instence.product,
            quantity=quantity,
        )

        return cart
