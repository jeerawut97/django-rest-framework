from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from basic_rest_django.models import *

User = get_user_model()

class BaseSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(auto_now_add=True) # create
    updated_at = serializers.DateTimeField(auto_now=True) # CUD

    class Meta:
        abstract = True

class AddressSerializer(serializers.Serializer):
    base = BaseSerializer(many=True)
    city = serializers.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.city}'