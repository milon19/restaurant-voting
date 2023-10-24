from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import UserEmailLoginSerializer


class UserEmailLoginView(TokenObtainPairView):
    serializer_class = UserEmailLoginSerializer
