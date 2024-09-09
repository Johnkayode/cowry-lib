from rest_framework import serializers
from api.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "uid",
            "first_name",
            "last_name",
            "email",
        )
        read_only_fields = ["uid"]

    def validate_email(self, email: str):
        email_exists: bool = User.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError(
                "A user with this email already exists", "invalid"
            )
        return email