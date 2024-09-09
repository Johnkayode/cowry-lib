from api.apps.users.models import User
from api.apps.users.serializers import UserSerializer
from rabbitmq import rabbitmq_client
from rest_framework import generics, permissions as django_permissions, response, status


class EnrolUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [django_permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        rabbitmq_client.publish("admin_updates", {"event_type": "user.enrolled", "data": serializer.data})
        headers = self.get_success_headers(serializer.data)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)