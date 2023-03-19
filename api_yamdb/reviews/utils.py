from rest_framework import serializers
from django.utils import timezone

INVALID_NAME = ['me', 'Me', 'ME']


def validate_year(value):

    current_year = timezone.now().year
    if not 0 <= value <= current_year:
        raise serializers.ValidationError(
            'Укажите год создания произведения.'
        )
    return value


def validate_username(value):
    """Проверяем, пытается ли пользователь
        использовать "me" в качестве имени пользователя"""
    if value in INVALID_NAME:
        raise serializers.ValidationError("Недопустимое имя пользователя")
    return value
