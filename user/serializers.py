from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import serializers

from user.models import Employee

User = get_user_model()


class AuthenticatedUserDetailSerializer(serializers.ModelSerializer):    # noqa
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser']


class EmployeeCreateSerializer(serializers.Serializer):    # noqa
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already exists.")
        return value

    def save(self, **kwargs):
        employee = Employee.objects.create_employee(**self.validated_data)
        return employee
