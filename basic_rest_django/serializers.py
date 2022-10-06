from rest_framework import serializers
from django.contrib.auth import get_user_model
from basic_rest_django.models import *

User = get_user_model()

class AddressSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

class PersonalSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    nick_name = serializers.CharField(max_length=30)
    gender = serializers.CharField()
    age = serializers.IntegerField(max_value=200, min_value=0)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    def create(self, validated_data):
        print(f'{validated_data = }')
        return PersonalInformation.objects.create(**validated_data)