from rest_framework.serializers import ModelSerializer, CharField, ValidationError, EmailField, Serializer
from account.models import User
from .utils import send_activation_code
from django.contrib.auth import authenticate


class RegistrationSerializer(ModelSerializer):
    password = CharField(max_length=8)
    password_confirm = CharField(max_length=8)


    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'username')

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            msg = ('Пароли не совпадают')
            raise ValidationError(msg)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user

class ActivationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'code')

    email = EmailField(required=True)
    code = CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        code = data.get('activation_code')
        if not User.objects.filter(
            email=email, activation_code=code
        ).exists():
            raise ValidationError(
                "Пользователь не найден"
            )
        return data

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        # получение одной записи с бд
        user.is_active = True
        user.activation_code = ''
        user.save()




class LoginSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)
    username = CharField(required=True)

    def validated_email(self, email):
        user = User.objects.filter(email=email).exists()
        if not user:
            msg = ('Пользoватель не найден')
            raise ValidationError(msg)
        return email
    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        user = authenticate(
            request, email=email, password=password, username=username
        )
        if not user:
            msg = ('Данные не верны')
            raise ValidationError(msg)
        data['user'] = user
        return data

