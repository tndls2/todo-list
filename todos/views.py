from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers.todo_serializer import TodoCreatePostSerializer, TodoSerializer, TodoUpdatePostSerializer
from todos.services.todo_service import TodoService


class TodoViewSet(viewsets.GenericViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        serializer = TodoCreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = TodoService(user=request.user)
        output_dto = service.create(data=serializer.validated_data)

        return Response(output_dto)

    def list(self, request: Request):
        service = TodoService(user=request.user)
        output_dto = service.list(request)

        return Response(output_dto)

    def retrieve(self, request: Request, pk):
        id = int(pk)
        service = TodoService(user=request.user)
        output_dto = service.retrieve(id=id)

        return Response(output_dto)

    def update(self, request: Request, pk):
        id = int(pk)
        serializer = TodoUpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = TodoService(user=request.user)
        output_dto = service.update(id=id, data=serializer.validated_data)

        return Response(output_dto)

    def delete(self, request: Request, pk):
        id = int(pk)
        service = TodoService(user=request.user)
        service.delete(id=id)

        return Response()
