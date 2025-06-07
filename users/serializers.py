from rest_framework import serializers
from django.core.exceptions import ValidationError

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'tg_chat_id')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        user = User.objects.create_user(
            username=validated_data['username'],
            email='',
            password=validated_data['password'],
            tg_chat_id=validated_data['tg_chat_id']
        )
        return user
