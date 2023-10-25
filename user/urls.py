from django.urls import path

from user.views import (AuthenticatedUserDetail, CreateEmployee)

app_name = "user"

urlpatterns = [
    path('authenticated-user/', AuthenticatedUserDetail.as_view(), name='auth_user'),
    path('create-employee/', CreateEmployee.as_view(), name='create_employee'),
]

