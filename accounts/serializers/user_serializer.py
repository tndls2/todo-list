from rest_framework import serializers

from core.exceptions import FieldRequiredException


class UserSignUpPostSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        user_name = data.get('user_name')
        password = data.get('password')

        if not user_name:
            raise FieldRequiredException("user_name")

        if not password:
            raise FieldRequiredException("password")

        return data


class UserLogInPostSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        user_name = data.get('user_name')
        password = data.get('password')

        if not user_name:
            raise FieldRequiredException("user_name")

        if not password:
            raise FieldRequiredException("password")

        return data
