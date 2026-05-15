from rest_framework import serializers


def validate_photo_size(value):
    if value.size > 2 * 1024 * 1024:  # 2MB
        raise serializers.ValidationError("A imagem não pode ser maior que 2MB.")
    return value
