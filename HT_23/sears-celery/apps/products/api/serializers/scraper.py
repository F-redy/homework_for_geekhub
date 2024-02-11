from rest_framework import serializers


class ProductScraperSerializer(serializers.Serializer):
    ids = serializers.CharField(min_length=5, required=True)
