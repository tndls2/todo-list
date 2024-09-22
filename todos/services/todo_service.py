from accounts.models import User
from core.base_service import BaseService
from core.exceptions import NoPermission
from todos.models import Todo, TodoStatus
from todos.serializers.todo_serializer import TodoRetrieveQsTodoSerializer, TodoListQsTodoSerializer


class TodoService(BaseService):
    model = Todo

    def __init__(self, user=None):
        super(TodoService, self).__init__()
        self._user = user

    def create(self, data):
        user = self.user
        todo = Todo.objects.create(**data, user=user)
        serializer = TodoRetrieveQsTodoSerializer(todo)

        return serializer.data

    def list(self, request):
        user = self.user

        # 완료 상태별 분류
        # due_date 최신순 정렬
        not_yet_todos = Todo.objects.filter(
            user=user, status=TodoStatus.NOT_YET.value
        ).order_by('due_date')

        done_todos = Todo.objects.filter(
            user=user, status=TodoStatus.DONE.value
        ).order_by('due_date')

        not_yet_serializer = TodoListQsTodoSerializer(not_yet_todos, many=True)
        done_serializer = TodoListQsTodoSerializer(done_todos, many=True)

        response_data = {
            'not_yet_todos': not_yet_serializer.data,
            'done_todos': done_serializer.data
        }
        return response_data

    @property
    def user(self) -> User:
        if self._user is None or self._user.is_anonymous:
            raise NoPermission()
        return self._user
