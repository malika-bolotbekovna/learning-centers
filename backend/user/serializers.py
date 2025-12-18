from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        validate_password(validated_data["password"], user)
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # если хочешь сразу вернуть юзера на фронт
    # можно добавить read-only поля
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True, allow_null=True, required=False)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise AuthenticationFailed("Укажите логин и пароль")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not user:
            # сюда попадаем, если логин/пароль неверные
            raise AuthenticationFailed("Неверный логин или пароль")

        if not user.is_active:
            raise AuthenticationFailed("Пользователь деактивирован")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            "id": user.id,
            "email": getattr(user, "email", None),
            "access": str(access),
            "refresh": str(refresh),
        }