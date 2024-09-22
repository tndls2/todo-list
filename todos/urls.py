from django.urls import path, include
from rest_framework.routers import SimpleRouter

from todos.views import TodoViewSet

app_name = 'todos'

router = SimpleRouter()
router.register('', TodoViewSet, 'todo')

urlpatterns = [
    path('', include((router.urls, 'todo'))),
]
