from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from user.serializers import (AuthenticatedUserDetailSerializer, EmployeeCreateSerializer)


class AuthenticatedUserDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthenticatedUserDetailSerializer

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CreateEmployee(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmployeeCreateSerializer

