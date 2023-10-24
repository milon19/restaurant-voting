from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer


class UserEmailLoginSerializer(TokenObtainPairSerializer):  # noqa
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token
