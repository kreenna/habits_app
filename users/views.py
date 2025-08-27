from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .permissions import IsOwner, IsModerator
from .serializers import UserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]

        return [permission() for permission in self.permission_classes]
