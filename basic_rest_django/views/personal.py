from rest_framework import status, permissions, authentication, exceptions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.db import transaction
from basic_rest_django.filter import PersonalFilter
from basic_rest_django.model_serializer import PersonalModelSerializer, UserModelSerializer
from basic_rest_django.models import *
from basic_rest_django.model_serializer import *
from django_filters import rest_framework
from rest_framework import filters


class Register(APIView):
    authentication_classes = []
    permission_classes = []
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        save_point = transaction.savepoint()
        try:
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            city = data.get('address')
            nick_name = data.get('nick_name')
            gender = data.get('gender')
            age = data.get('age')

            if not username:
                raise serializers.ValidationError({'username' : 'This field is required.'})
            if not password:
                raise serializers.ValidationError({'password' : 'This field is required.'})
            if not first_name:
                raise serializers.ValidationError({'first_name' : 'This field is required.'})
            if not last_name:
                raise serializers.ValidationError({'last_name' : 'This field is required.'})
            if not email:
                raise serializers.ValidationError({'email' : 'This field is required.'})
            if not city:
                raise serializers.ValidationError({'city' : 'This field is required.'})
            if not nick_name:
                raise serializers.ValidationError({'nick_name' : 'This field is required.'})
            if not gender:
                raise serializers.ValidationError({'gender' : 'This field is required.'})
            if not age:
                raise serializers.ValidationError({'age' : 'This field is required.'})

            data_user = {'username':username, 'password':password, 'email':email, 'first_name':first_name, 'last_name':last_name}
            user = UserModelSerializer().create(validated_data=data_user)
            if not user:
                raise Exception('error : user duplicate')
            data_addres = {'city':city}
            addres = AddressModelSerializer(data=data_addres)
            addres.is_valid(raise_exception=True)
            addres.save()
            data_personal = {'user':user.id, 'nick_name':nick_name, 'gender':gender, 'age':age, 'address':addres.data.get('id')}
            personal = PersonalModelSerializer(data=data_personal)
            personal.is_valid(raise_exception=True)
            personal.save()
            result = personal.data
            transaction.savepoint_commit(save_point)
        except Exception as error:
            transaction.savepoint_rollback(save_point)
            return Response(f'{error}', status=status.HTTP_404_NOT_FOUND)
        finally:
            transaction.clean_savepoints()
        return Response(result, status=status.HTTP_201_CREATED)

class PersonalList(generics.ListCreateAPIView):
    queryset = PersonalInformation.objects.all()
    serializer_class = PersonalModelSerializer
    filterset_class = PersonalFilter
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nick_name', 'gender', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'address__city']
    ordering_fields = ['user']
    ordering = ['-user']
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        save_point = transaction.savepoint()
        request = request.data
        try:
            data_user = {'username':request['username'], 'password':request['password'], 'email':request['email'], 'first_name':request['first_name'], 'last_name':request['last_name']}
            user = UserModelSerializer().create(validated_data=data_user)
            if not user:
                raise Exception('error : user duplicate')
            data_addres = {'city':request['city']}
            addres = AddressModelSerializer(data=data_addres)
            addres.is_valid(raise_exception=True)
            addres.save()
            data_personal = {'user':user.id, 'nick_name':request['nick_name'], 'gender':request['gender'], 'age':request['age'], 'address':addres.data.get('id')}
            personal = PersonalModelSerializer(data=data_personal)
            personal.is_valid(raise_exception=True)
            personal.save()
            result = personal.data
            transaction.savepoint_commit(save_point)
        except Exception as error:
            transaction.savepoint_rollback(save_point)
            return Response(f'{error}', status=status.HTTP_404_NOT_FOUND)
        finally:
            transaction.clean_savepoints()
        return Response(result, status=status.HTTP_201_CREATED)

    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # def get_queryset(self, lang='TH'):
    #     return super().get_queryset()

    # def get_serializer_class(self):
    #     return super().get_serializer_class()

    # def filter_queryset(self, queryset):
    #     return super().filter_queryset(queryset)

    # def get_object(self):
    #     return super().get_object()

class PersonalGet(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            personal = PersonalModelSerializer(PersonalInformation.objects.get(id=id))
        except PersonalInformation.DoesNotExist:
            return Response('error : personal not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(f'error : {error}', status=status.HTTP_404_NOT_FOUND)
        return Response(personal, status=status.HTTP_200_OK)

class PersonalUpdate(APIView):
    @transaction.atomic
    def put(self, request, id, *args, **kwargs):
        save_point = transaction.savepoint()
        try:
            result = {}
            data = request.data
            if not data:
                return Response('error : invalid param', status=status.HTTP_400_BAD_REQUEST)
            personal = PersonalInformation.objects.get(id=id)
            serializer = PersonalModelSerializer().update(personal, data)
            result = PersonalModelSerializer(personal).data
            transaction.savepoint_commit(save_point)
        except PersonalInformation.DoesNotExist:
            return Response('error : personal not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            transaction.savepoint_rollback(save_point)
            return Response(f'error : {error}', status=status.HTTP_404_NOT_FOUND)
        finally:
            transaction.clean_savepoints()
        return Response(result, status=status.HTTP_200_OK)