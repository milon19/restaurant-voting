from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class AuthenticatedUserDetailSerializer(serializers.ModelSerializer):    # noqa
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser']
