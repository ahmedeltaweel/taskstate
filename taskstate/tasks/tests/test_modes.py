from django.test import TestCase
from taskstate.tasks.models import Task
from taskstate.tasks.tests.factories import TaskFactory


class TestTasksMode(TestCase):
    def test_create_task(self):
        TaskFactory.create()
        self.assertEqual(Task.objects.count(), 1)

