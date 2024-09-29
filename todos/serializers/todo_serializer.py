from rest_framework import serializers

from core.exceptions import FieldRequiredException
from todos.models import Todo, TodoStatus


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'status', 'title', 'content', 'due_date', 'created_at', 'updated_at')


class TodoCreatePostSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, data):
        status = data.get('status')
        title = data.get('title')
        due_date = data.get('due_date')

        if status is None:
            raise FieldRequiredException("status")

        if status not in TodoStatus.values:
            raise serializers.ValidationError({"detail": "유효하지 않은 상태 값입니다."})

        if title is None or title.strip() == "":
            raise FieldRequiredException("title")

        if due_date is None:
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


class TodoListQsSerializer(serializers.Serializer):
    not_yet_todos = TodoListQsTodoSerializer(many=True)
    done_todos = TodoListQsTodoSerializer(many=True)


class TodoUpdatePostSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, data):
        status = data.get('status')

        if status is not None and status not in TodoStatus.values:
            raise serializers.ValidationError({"detail": "유효하지 않은 상태 값입니다."})
