from rest_framework import serializers
from django.contrib.auth import get_user_model
from basic_rest_django.models import *

User = get_user_model()

class AddressSerializer(serializers.Serializer):
    city = serializers.CharField()

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

class PersonalSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    nick_name = serializers.CharField()
    gender = serializers.CharField()
    age = serializers.IntegerField()
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    def create(self, validated_data):
        print(f'{validated_data = }')
        return PersonalInformation.objects.create(**validated_data)

class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        print(f'{validated_data = }')
        return Group.objects.create(**validated_data)

class MemberShipSerializer(serializers.Serializer):
    person = serializers.PrimaryKeyRelatedField(queryset=PersonalInformation.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    invite_reason = serializers.CharField()

    def create(self, validated_data):
        print(f'{validated_data = }')
        return Membership.objects.create(**validated_data)