from rest_framework import serializers

from apps.userprofile.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']
