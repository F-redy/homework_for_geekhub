from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField()
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_email_verified', 'is_staff')
        read_only_fields = ('id', )
