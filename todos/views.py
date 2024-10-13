from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers.todo_serializer import TodoCreatePostSerializer, TodoSerializer, TodoUpdatePostSerializer, \
    TodoRetrieveQsTodoSerializer, TodoListQsSerializer
from todos.services.todo_service import TodoService


class TodoViewSet(viewsets.GenericViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TodoCreatePostSerializer,
        responses={
            200: TodoRetrieveQsTodoSerializer,
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
        description="로그인된 사용자의 새로운 Todo 아이템 생성",
    )
    def create(self, request: Request):
        serializer = TodoCreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = TodoService(user=request.user)
        output_dto = service.create(data=serializer.validated_data)

        return Response(output_dto)

    @extend_schema(
        responses={
            200: TodoListQsSerializer(),
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
        description="로그인된 사용자의 Todo 목록 반환"
    )
    def list(self, request: Request):
        service = TodoService(user=request.user)
        output_dto = service.list(request)

        return Response(output_dto)

    @extend_schema(
        responses={
            200: TodoRetrieveQsTodoSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description="조회할 Todo 아이템의 ID",
                required=True,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='Authorization',
                location=OpenApiParameter.HEADER,
                description="JWT 인증 토큰",
                required=True,
                type=OpenApiTypes.STR
            ),
        ],
        description="ID로 지정한 Todo 항목 반환"
    )
    def retrieve(self, request: Request, pk):
        id = int(pk)
        service = TodoService(user=request.user)
        output_dto = service.retrieve(id=id)

        return Response(output_dto)

    @extend_schema(
        request=TodoUpdatePostSerializer,
        responses={
            200: TodoRetrieveQsTodoSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description="수정할 Todo 아이템의 ID",
                required=True,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='Authorization',
                location=OpenApiParameter.HEADER,
                description="JWT 인증 토큰",
                required=True,
                type=OpenApiTypes.STR
            ),
        ],
        description="ID로 지정한 Todo 항목 내용 업데이트"
    )
    def update(self, request: Request, pk):
        id = int(pk)
        serializer = TodoUpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = TodoService(user=request.user)
        output_dto = service.update(id=id, data=serializer.validated_data)

        return Response(output_dto)

    @extend_schema(
        responses={
            200: None,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description="삭제할 Todo 아이템의 ID",
                required=True,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='Authorization',
                location=OpenApiParameter.HEADER,
                description="JWT 인증 토큰",
                required=True,
                type=OpenApiTypes.STR
            ),
        ],
        description="ID로 지정한 Todo 항목 삭제"
    )
    def destroy(self, request: Request, pk):
        id = int(pk)
        service = TodoService(user=request.user)
        service.delete(id=id)

        return Response()
