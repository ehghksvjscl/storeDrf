"""
User Serialisers
"""

from django.contrib.auth import authenticate

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            msg = "not authorization"
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
