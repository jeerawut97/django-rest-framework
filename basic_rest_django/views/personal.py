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
from django_filters import rest_framework as djangoFilters
from rest_framework import filters


class Register(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]

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
            result = {
                'username' : f'{username}',
                'full_name' : f'{first_name} {last_name}',
                'first_name' : f'{first_name}',
                'last_name' : f'{last_name}',
                'nick_name' : f'{nick_name}',
                'gender' : personal.data.get('gender'),
                'age' : f'{age}',
                'address' : f'{city}'
            }

            transaction.savepoint_commit(save_point)
        except Exception as error:
            transaction.savepoint_rollback(save_point)
            return Response(f'{error}', status=status.HTTP_404_NOT_FOUND)
        finally:
            transaction.clean_savepoints()
        return Response(result, status=status.HTTP_201_CREATED)

class PersonalList(generics.ListAPIView):
    queryset = PersonalInformation.objects.all()
    serializer_class = PersonalModelSerializer
    filterset_class = PersonalFilter
    filter_backends = [djangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nick_name', 'gender', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'address__city']
    ordering_fields = ['user']
    ordering = ['-user']

class PersonalGet(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, id, *args, **kwargs):
        try:
            personal = PersonalModelSerializer(PersonalInformation.objects.get(id=id)).data
        except PersonalInformation.DoesNotExist:
            raise Exception('error : personal not found')
        except Exception as error:
            return Response(f'error : {error}', status=status.HTTP_404_NOT_FOUND)
        # result = {
        #     'full_name' : f'{personal.user.first_name} {personal.user.last_name}',
        #     'first_name' : personal.user.first_name,
        #     'last_name' : personal.user.last_name,
        #     'nick_name' : personal.nick_name,
        #     'gender' : personal.get_gender_display(),
        #     'age' : personal.age,
        #     'address' : personal.address.city
        # }
        return Response(personal, status=status.HTTP_200_OK)

class PersonalUpdate(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]
    def put(self, request, id, *args, **kwargs):
        try:
            result = {}
            data = request.data
            if not data:
                return Response('error : invalid param', status=status.HTTP_400_BAD_REQUEST)

            personal = PersonalInformation.objects.get(id=id)
            if 'first_name' in data:
                personal.user.first_name = data['first_name']
            if 'last_name' in data:
                personal.user.last_name = data['last_name']
            if 'nick_name' in data:
                personal.nick_name = data['nick_name']
            if 'gender' in data:
                personal.gender = personal.get_gender_display()
            if 'age' in data:
                personal.age = data['age']
            if 'address' in data:
                address = Address.objects.get(id=personal.address.id)
                address.city = data['address']
                address.save()
            personal.save()
            result['full_name'] =  f'{personal.user.first_name} {personal.user.last_name}'
            result['first_name'] = personal.user.first_name
            result['last_name'] = personal.user.last_name
            result['nick_name'] = personal.nick_name
            result['gender'] = personal.get_gender_display()
            result['age'] = f'{personal.age}'
            result['address'] = personal.address.city
        except PersonalInformation.DoesNotExist:
            return Response('error : personal not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(f'error : {error}', status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)