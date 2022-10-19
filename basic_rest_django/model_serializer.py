from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from basic_rest_django.models import *

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # data['fullname'] = '{} {}'.format(data['first_name'], data['last_name'])
        data['fullname'] = f"{data['first_name']} {data['last_name']}"

        return data

    def validate(self, attrs):
        attrs = super().validate(attrs)
        username, password = attrs.get('username'), attrs.get('password')

        user = User.objects.get(username=username)
        if user:
            if user.check_password(password):
                return serializers.ValidationError()

        return attrs

    def create(self, validated_data):
        try:
            User.objects.get(username=validated_data['username'])
            return False
        except User.DoesNotExist:
            user = User(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city']

class PersonalModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            user = UserModelSerializer(User.objects.get(id=data['user'])).data
        except User.DoesNotExist:
            user = {}
        try:
            address = AddressModelSerializer(Address.objects.get(id=data['address'])).data
        except Address.DoesNotExist:
            address = {}

        data['gender'] = 'Men' if data['gender'] == 'M' else 'Women'
        data['user'] = user
        data['address'] =  address

        return data

    class Meta:
        model = PersonalInformation
        fields = '__all__'

class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'members']

class MemberShipModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['person', 'group', 'invite_reason']