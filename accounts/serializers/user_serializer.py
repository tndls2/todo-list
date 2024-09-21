from rest_framework import serializers


class UserSignUpPostSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField()


class UserLogInPostSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField()
