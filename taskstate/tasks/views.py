from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.viewsets import ModelViewSet

from taskstate.tasks.models import Task
from taskstate.tasks.serializers import TaskSerializer


class TasksViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'], url_path='set-in-progress')
    def set_in_progress(self, request, pk=None):
        task = self.get_object()
        task.state = Task.STATES.IN_PROGRESS
        task.save()
        return Response({'state': 'in progress'})

    @action(detail=True, methods=['post'], url_path='set-done')
    def set_done(self, request, pk=None):
        task = self.get_object()
        task.state = Task.STATES.DONE
        task.save()
        return Response({'state': 'done'})

    @action(detail=True, methods=['post'], url_path='link-task')
    def link_task(self, request, pk=None):
        task = self.get_object()
        if task.state != Task.STATES.IN_PROGRESS:
            raise ValidationError(_('Only In progess tasks can be linked'))
        new_task = request.data.get('task')
        new_task = get_object_or_404(Task, pk=new_task)
        task.linked_task = new_task
        task.save()
        return Response({'state': 'done'})
