from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User
    """
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5} }
    
    def create(self, validated_data):
        """
        Creating user with validated_data and Returning user
        """
        return get_user_model().objects.create_user(**validated_data)

class TokenAuthSerializer(serializers.Serializer):
    """Serializer for token authentication."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    
    def validate(self, attrs):
        """auth validation and authenticate using email."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=email, password=password)
        if not user:
            raise serializers.ValidationError("Unable to authenticate with provided credentials.", code="authorization")

        attrs["user"] = user

        return attrs

