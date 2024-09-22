from rest_framework import serializers

from core.exceptions import FieldRequiredException
from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'status', 'title', 'content', 'due_date', 'created_at', 'updated_at')


class TodoCreatePostSerializer(serializers.Serializer):
    status = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, data):
        status = data.get('status')
        title = data.get('title')
        due_date = data.get('due_date')

        if not status:
            raise FieldRequiredException("status")

        if not title:
            raise FieldRequiredException("title")

        if not due_date:
            raise FieldRequiredException("due_date")

        return data


class TodoRetrieveQsTodoSerializer(TodoSerializer):
    class Meta:
        model = Todo
        fields = (*TodoSerializer.Meta.fields,)


class TodoListQsTodoSerializer(TodoSerializer):
    class Meta:
        model = Todo
        fields = (*TodoSerializer.Meta.fields,)


class TodoUpdatePostSerializer(serializers.Serializer):
    pass

