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