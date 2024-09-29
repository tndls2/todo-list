from accounts.models import User
from core.base_service import BaseService
from core.exceptions import NoPermission, TodoDoesNotExistException
from todos.models import Todo, TodoStatus, TodoLog, Action
from todos.serializers.todo_serializer import TodoRetrieveQsTodoSerializer, TodoListQsTodoSerializer


class TodoService(BaseService):
    model = Todo

    def __init__(self, user=None):
        super(TodoService, self).__init__()
        self._user = user

    def create(self, data):
        user = self.user
        todo = Todo.objects.create(**data, user=user)

        # 로그 생성
        self._create_log(action=Action.CREATE, todo=todo)

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

    def retrieve(self, id):
        # 인스턴스 가져오기
        todo = self._get_todo_with_permission(id)

        serializer = TodoRetrieveQsTodoSerializer(todo)
        return serializer.data

    def update(self, id, data):
        # 인스턴스 가져오기
        todo = self._get_todo_with_permission(id)

        # 필드 업데이트
        for field, value in data.items():
            setattr(todo, field, value)
        todo.save()

        # 로그 생성
        self._create_log(action=Action.UPDATE, todo=todo)

        serializer = TodoRetrieveQsTodoSerializer(todo)
        return serializer.data

    def delete(self, id):
        # 인스턴스 가져오기
        todo = self._get_todo_with_permission(id)

        if todo.user != self.user:
            raise NoPermission()

        # 로그 생성
        self._create_log(action=Action.DELETE, todo=todo)

        todo.delete()

    def _get_todo_with_permission(self, id):
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            raise TodoDoesNotExistException()

        if todo.user != self.user:
            raise NoPermission()

        return todo

    def _create_log(self, action, todo):
        TodoLog.objects.create(
            action=action,
            todo_id=todo.id,
            user_id=todo.user.id,
            status=todo.status,
            title=todo.title,
            content=todo.content,
            due_date=todo.due_date
        )

    @property
    def user(self) -> User:
        if self._user is None or self._user.is_anonymous:
            raise NoPermission()
        return self._user
