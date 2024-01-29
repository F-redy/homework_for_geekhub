from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_staff = serializers.BooleanField()
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'is_staff']
        read_only_fields = ['id',]
