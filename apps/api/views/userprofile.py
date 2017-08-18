from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.permissions import IsAdminOrReadOnly
from apps.api.serializers.userprofile import UserSerializer
from apps.userprofile.models import User


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if request.data.get('is_blocked', None) == True:
            if instance.is_admin:
                raise ValidationError('Admin user cannot be blocked.')

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
