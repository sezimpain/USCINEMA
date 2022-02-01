from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .permissions import IsActivePermission
from .serializers import RegistrationSerializer, LoginSerializer, ActivationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            msg = ('Аккаунт успешно создан')
            return Response(msg, status=201)

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

class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            "Вы успешно вышли из своего аккаунта",
            status=200
        )

