from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from basic_rest_django.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
import json

class Register(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = []
    parser_classes = [JSONParser]

    # create
    def post(self, request, *args, **kwargs):
        data = request.data
        if 'username' not in data:
            return Response('username params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in data:
            return Response('password params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'first_name' not in data:
            return Response('first_name params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'last_name' not in data:
            return Response('last_name params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'nick_name' not in data:
            return Response('nick_name params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'gender' not in data:
            return Response('gender params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'age' not in data:
            return Response('age params not found', status=status.HTTP_400_BAD_REQUEST)
        if 'address' not in data:
            return Response('address params not found', status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(data['username'], str):
            return Response('error type params : username', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['password'], str):
            return Response('error type params : password', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['first_name'], str):
            return Response('error type params : first_name', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['last_name'], str):
            return Response('error type params : last_name', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['nick_name'], str):
            return Response('error type params : nick_name', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['gender'], str):
            return Response('error type params : gender', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['age'], int):
            return Response('error type params : age', status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['address'], str):
            return Response('error type params : address', status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(username=data['username'])
            return Response('error : user duplicate', status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            user = User.objects.create(username=data['username'], first_name=data['first_name'], last_name=data['last_name'])
            user.set_password(data['password'])
            user.save()
            del data['username'], data['password'], data['first_name'], data['last_name']

        address = Address.objects.create(city=data['address'])
        personal_data = {**data, "user":user, "address": address}
        personal = PersonalInformation.objects.create(**personal_data)
        result = {
            'username' : f'{personal.user.username}',
            'full_name' : f'{personal.user.first_name} {personal.user.last_name}',
            'first_name' : f'{personal.user.first_name}',
            'last_name' : f'{personal.user.last_name}',
            'nick_name' : f'{personal.nick_name}',
            'gender' : f'{personal.get_gender_display()}',
            'age' : f'{personal.age}',
            'address' : f'{personal.address.city}'
        }
        return Response(result, status=status.HTTP_201_CREATED)

class Login(APIView):
    permission_classes = []
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            print(user)
            result = 'success'
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response('authenticated failed', status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        pass

class PersonalList(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []

    # list
    def get(self, request, format=None, *args, **kwargs):
        result = [{
            'full_name' : f'{personal_info.user.first_name} {personal_info.user.last_name}',
            'first_name' : personal_info.user.first_name,
            'last_name' : personal_info.user.last_name,
            'nick_name' : personal_info.nick_name,
            'gender' : personal_info.get_gender_display(),
            'age' : personal_info.age,
            'address' : personal_info.address.city
        } for personal_info in PersonalInformation.objects.all()]
        return Response(result, status=status.HTTP_200_OK)

class PersonalGet(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []

    # get
    def get(self, request, id, *args, **kwargs):
        try:
            personal = PersonalInformation.objects.get(id=id)
        except PersonalInformation.DoesNotExist:
            return Response('error : personal not found', status=status.HTTP_200_OK)
        except Exception as error:
            return Response(f'error : {error}')
        result = {
            'full_name' : f'{personal.user.first_name} {personal.user.last_name}',
            'first_name' : personal.user.first_name,
            'last_name' : personal.user.last_name,
            'nick_name' : personal.nick_name,
            'gender' : personal.get_gender_display(),
            'age' : personal.age,
            'address' : personal.address.city
        }
        return Response(result, status=status.HTTP_200_OK)

class PersonalUpdate(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    parser_classes = [JSONParser]

    # put
    def put(self, request, id, *args, **kwargs):
        try:
            result = {}
            data = request.data
            personal = PersonalInformation.objects.get(id=id)
            if 'first_name' in data:
                personal.user.first_name = data['first_name']
                result['first_name'] = personal.first_name
            if 'last_name' in data:
                personal.user.last_name = data['last_name']
                result['last_name'] = personal.last_name
            if 'nick_name' in data:
                personal.nick_name = data['nick_name']
                result['nick_name'] = personal.nick_name
            if 'gender' in data:
                personal.gender = personal.get_gender_display()
                result['gender'] = personal.gender
            if 'age' in data:
                personal.age = data['age']
                result['age'] = personal.age
            if 'address' in data:
                address = Address.objects.get(id=personal.address.id)
                address.city = data['address']
                result['address'] = address.city
                address.save()
            personal.save()
            result['full_name'] =  f'{personal.user.first_name} {personal.user.last_name}'
        except PersonalInformation.DoesNotExist:
            return Response('error : personal not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(f'error : {error}', status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)


