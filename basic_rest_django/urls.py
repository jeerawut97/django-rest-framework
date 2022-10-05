from django.urls import path
from basic_rest_django.views import personal

# import views

urlpatterns = [
    path("personal/register/", personal.Register.as_view(), name="personal_register"),
    path("personal/list/", personal.PersonalList.as_view(), name="personal_list"),
    path("personal/get/<int:id>/", personal.PersonalGet.as_view(), name="personal_get"),
    path("personal/update/<int:id>/", personal.PersonalUpdate.as_view(), name="personal_update"),
]