# ---------- Python's Libraries ---------------------------------------------------------------------------------------
from dataclasses import field
from datetime import timedelta
from random import choices

# ---------- Django Tools Rest Framework, Oauth 2 Tools ---------------------------------------------------------------
from django_filters import rest_framework as filters

# from django_filters import rest_framework as filters
from django.db.models import Q
from django.utils import timezone
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import CharField, F, DurationField, ExpressionWrapper, Value as V

# ---------- Created Tools --------------------------------------------------------------------------------------------
# from apis import utils
from basic_rest_django.models import *  

class PersonalFilter(filters.FilterSet):
    gender_type = (
        ('M', 'Men'),
        ('W', 'Women')
    )
    # user = filters.ModelChoiceFilter(field_name='user', queryset=User.objects.all())
    email = filters.CharFilter(field_name='user__email')
    firstname = filters.CharFilter(field_name='user__first_name')
    lastname = filters.CharFilter(field_name='user__last_name')
    nick_name = filters.CharFilter(field_name='nick_name')
    gender = filters.ChoiceFilter(field_name='gender', choices=gender_type)
    age = filters.NumberFilter(field_name='age')
    # address = filters.ModelChoiceFilter(field_name='address', queryset=Address.objects.all())
    city = filters.CharFilter(field_name='address__city')
    created_at = filters.DateTimeFromToRangeFilter(field_name='created_at')

    class Meta:
        model = PersonalInformation
        fields = '__all__'