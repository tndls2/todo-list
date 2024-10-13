from django.contrib.auth import logout
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.serializers.user_serializer import UserSignUpPostSerializer, UserLogInPostSerializer
from accounts.services.user_service import UserService
from core.permissions import IsNotAuthenticated


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserLogInPostSerializer

    @extend_schema(
        request=UserSignUpPostSerializer,
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
                        },
                    )
                ],
            ),
        },
        description="회원가입 후 access와 refresh 토큰 반환",
    )
    @action(methods=['POST'], detail=False, permission_classes=[IsNotAuthenticated])
    def signup(self, request: Request):
        serializer = UserSignUpPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = UserService()
        output_dto = service.signup(
            user_name=serializer.validated_data['user_name'],
            password=serializer.validated_data['password']
        )

        return Response(output_dto)

    @extend_schema(
        request=UserLogInPostSerializer,
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
                        },
                    )
                ],
            ),
        },
        description="사용자 로그인 처리 및 JWT 토큰 반환",
    )
    @action(methods=['POST'], detail=False, permission_classes=[IsNotAuthenticated])
    def login(self, request: Request):
        serializer = UserLogInPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = UserService()
        output_dto = service.login(
            user_name=serializer.validated_data['user_name'],
            password=serializer.validated_data['password']
        )

        return Response(output_dto)

    @extend_schema(
        responses={
            200: None,  # 로그아웃은 특별한 응답을 반환하지 않음
        },
        parameters=[
            OpenApiParameter(
                name='Authorization',
                location=OpenApiParameter.HEADER,
                description="JWT 인증 토큰",
                required=True,
                type=OpenApiTypes.STR
            )
        ],
        description="사용자 로그아웃 처리",
    )
    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request: Request):
        logout(request)
        return Response()
