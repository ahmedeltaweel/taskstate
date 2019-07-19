from rest_framework import serializers

from taskstate.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'state', 'linked_task', 'created', 'modified']
        extra_kwargs = {
            'state': {'read_only': True}
        }
