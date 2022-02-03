from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, ActivationSerializer
from rest_framework.response import Response


class RegistrationView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            msg = ('Аккаунт успешно создан')
            return Response(msg, status=201)

class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Ваш аккаунт активирован!", status=status.HTTP_200_OK)



class ActivationView(APIView):

    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                "Аккаунт успешно активирован", status=200
            )

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogOutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            "Вы успешно вышли из своего аккаунта",
            status=200
        )
