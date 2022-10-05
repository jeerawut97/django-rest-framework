from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from basic_rest_django.models import *

User = get_user_model()

class MeasurementSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(default=timezone.now())
    temperature = serializers.DecimalField(max_digits=4, decimal_places=2)
    o2sat = serializers.IntegerField()
    systolic = serializers.IntegerField()
    diastolic = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        return Measurement.objects.create(**validated_data)