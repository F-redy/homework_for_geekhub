from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'is_staff']
