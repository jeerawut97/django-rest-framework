from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

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

class Symptom(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, help_text='อุณหภูมิร่างกาย')
    o2sat = models.IntegerField(help_text='อ๊อกซิเจนในเลือด')
    systolic = models.IntegerField(help_text='ความดันตัวบน')
    diastolic = models.IntegerField(help_text='ความดันตัวล่าง')
    symptoms = models.ManyToManyField(Symptom, blank=True, help_text='อาการทีBพบ')

    @property
    def symptoms_display(self):
        return ', '.join(self.symptoms.values_list('name', flat=True))

    class Meta:
        ordering = ['-created']

