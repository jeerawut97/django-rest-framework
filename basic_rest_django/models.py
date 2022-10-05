from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # create
    updated_at = models.DateTimeField(auto_now=True) # CUD

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
        return self.first_name + " " + self.last_name

