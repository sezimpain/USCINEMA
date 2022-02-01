from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
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

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

