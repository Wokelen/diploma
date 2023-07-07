from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerializer, LoginSerializer, UserSerializer, UpdatePasswordSerializer


class UserCreateView(CreateAPIView):

    model = User
    serializer_class = UserCreateSerializer
    permission_classes: list = [AllowAny]


class LoginView(CreateAPIView):

    serializer_class = LoginSerializer
    permission_classes: list = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileView(RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:

        return self.request.user

    def delete(self, request, *args, **kwargs) -> Response:

        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):

        return self.request.user

