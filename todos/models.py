from enum import Enum

from django.db import models

from core.utils.choice import get_choices
from core.utils.model import TimestampZone


class TodoStatus(Enum):
    DONE = 'done'
    NOT_YET = 'not_yet'


class Todo(TimestampZone):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    status = models.CharField(
        choices=get_choices(TodoStatus), default=TodoStatus.NOT_YET, max_length=10, help_text='완료 상태'
    )
    title = models.CharField(max_length=64, blank=False, null=False)
    content = models.TextField(blank=True)
    due_date = models.DateTimeField(null=False, help_text='마감 기한')

    def __str__(self):
        return self.title