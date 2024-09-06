from api.apps.users.models import User
from api.apps.users.serializers import UserSerializer
from rest_framework import generics, permissions as django_permissions


class EnrolUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = UserSerializer
    
