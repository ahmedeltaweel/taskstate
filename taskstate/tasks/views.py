from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from taskstate.tasks.models import Task
from taskstate.tasks.serializers import TaskSerializer


class TasksViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
