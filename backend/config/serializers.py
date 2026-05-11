from rest_framework import serializers


class DefaultErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
