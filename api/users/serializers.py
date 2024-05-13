from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True, label='Пароль')
    password2 = serializers.CharField(write_only=True, label='Потверждение пароля')

    def create(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise ValidationError('Пароли не совпадают')

        if not validated_data['email']:
            raise ValidationError('Введите E-mail.')

        if get_user_model().objects.filter(email=validated_data['email']).exists():
            raise ValidationError('Пользователь с таким E-mail уже существует.')

        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )
        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password1', 'password2')