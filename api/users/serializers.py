from typing import Optional, Type, Dict, Any, TypeVar

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenObtainSerializer, PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from django.utils.translation import gettext_lazy as _

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):

    # username = serializers.CharField(required=False)
    #password1 = serializers.CharField(write_only=True, label='Пароль')
    #password2 = serializers.CharField(write_only=True, label='Потверждение пароля')

    def create(self, validated_data):
        # if validated_data['password1'] != validated_data['password2']:
        #     raise ValidationError('Пароли не совпадают')
        # if not validated_data['email']:
        #     raise ValidationError('Введите E-mail.')

        # if get_user_model().objects.filter(email=validated_data['email']).exists():
        #     raise ValidationError('Пользователь с таким E-mail уже существует.')

        user = get_user_model().objects.create_user(
            username=None,
            email=validated_data['email'],
            # password=validated_data['password1'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = get_user_model()
        #fields = ('id', 'username', 'email', 'password1', 'password2')
        fields = ('id', 'email', 'password', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        #fields = ('id', 'username', 'email', 'password1', 'password2')
        fields = ('id', 'username', 'email', 'password', )


AuthUser = TypeVar("AuthUser", User, TokenUser)


class MyTokenObtainSerializer(serializers.Serializer):

    email_field = get_user_model().EMAIL_FIELD
    token_class: Optional[Type[Token]] = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields[self.email_field] = serializers.CharField(write_only=True)
        self.fields["password"] = PasswordField()
        print('****-*-**--*-', self.fields)

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.email_field: attrs[self.email_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        return {
            'email': self.user.email,
            'username': self.user.username,
            'token': self.user.token
        }

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return cls.token_class.for_user(user)  # type: ignore

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', )