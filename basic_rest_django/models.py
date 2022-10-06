from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Address(BaseModel):
    city = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.city}'

class PersonalInformation(BaseModel):
    gender_type = (
        ('M', 'Men'),
        ('W', 'Women')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    nick_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=gender_type)
    age = models.IntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="personal_address", blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    def get_full_name(self):
            return self.user.first_name + " " + self.user.last_name

class Group(BaseModel):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(PersonalInformation, through='Membership')

    def __str__(self):
        return self.name

class Membership(BaseModel):
    person = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invite_reason = models.CharField(max_length=64)

