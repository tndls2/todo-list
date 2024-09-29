from enum import Enum

from django.db import models

from core.utils.choice import get_choices
from core.utils.model import TimestampZone


class TodoStatus(models.IntegerChoices):
    DONE = 0, 'done'
    NOT_YET = 1, 'not_yet'


class Todo(TimestampZone):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    status = models.IntegerField('완료 상태', choices=TodoStatus.choices)
    title = models.CharField(max_length=64, blank=False, null=False)
    content = models.TextField(blank=True)
    due_date = models.DateTimeField(null=False, help_text='마감 기한')

    def __str__(self):
        return self.title


class Action(models.IntegerChoices):
    CREATE = 0, 'Created'
    UPDATE = 1, 'Updated'
    DELETE = 2, 'Deleted'


class TodoLog(TimestampZone):
    id = models.AutoField(primary_key=True)
    action = models.IntegerField(choices=Action.choices)
    todo_id = models.IntegerField('해당 Todo의 ID')
    user_id = models.IntegerField('해당 Todo의 사용자')
    status = models.IntegerField('완료 상태', choices=TodoStatus.choices)
    title = models.CharField(max_length=64, blank=False, null=False)
    content = models.TextField(blank=True)
    due_date = models.DateTimeField(null=False, help_text='마감 기한')

    def __str__(self):
        return f'Todo Log for {self.title}'
