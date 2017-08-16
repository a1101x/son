from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.permissions import IsAdminOrReadOnly
from apps.api.serializers.userprofile import UserSerializer
from apps.userprofile.models import User


class UserViewSet(viewsets.ModelViewSet):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
