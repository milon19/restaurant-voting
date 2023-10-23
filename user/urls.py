from django.urls import path

from user.views import AuthenticatedUserDetail

app_name = "user"

urlpatterns = [
    path('authenticated-user/', AuthenticatedUserDetail.as_view(), name='auth_user')
]

