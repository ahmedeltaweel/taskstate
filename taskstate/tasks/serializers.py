from rest_framework import serializers

from taskstate.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'state', 'created', 'modified']
