import json
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from taskstate.users.tests.factories import UserFactory
from taskstate.tasks.models import Task
from taskstate.tasks.tests.factories import TaskFactory


class TestTaskAPIs(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        token = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + token[0].key)

    def test_create_task(self):
        data = {
            'title': 'test_task_1',
            'description': 'test description'
        }
        response = self.client.post('/api/v1/tasks/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = response.json()
        self.assertEqual(response['title'], data['title'])
        self.assertEqual(response['description'], data['description'])
        self.assertEqual(response['state'], Task.STATES.NEW)

    def test_create_task_missing_title(self):
        data = {
            'description': 'test description'
        }
        response = self.client.post('/api/v1/tasks/', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['title'], ['This field is required.'])

    def test_update_task(self):
        data = {
            'title': 'new updated task',
            'description': 'test description'
        }
        task = TaskFactory.create(state=Task.STATES.NEW)
        response = self.client.put(
            '/api/v1/tasks/{}/'.format(task.pk),
            data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        task.refresh_from_db()
        self.assertEqual(response['title'], data['title'])
        self.assertEqual(response['description'], data['description'])
        self.assertEqual(response['state'], Task.STATES.NEW)

    def test_parital_update_task(self):
        data = {
            'description': 'test new description'
        }
        task = TaskFactory.create(state=Task.STATES.NEW)
        response = self.client.patch(
            '/api/v1/tasks/{}/'.format(task.pk),
            data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        task.refresh_from_db()
        self.assertEqual(response['description'], data['description'])
        self.assertEqual(response['state'], Task.STATES.NEW)

    def test_delete_task(self):
        task = TaskFactory.create()
        response = self.client.delete('/api/v1/tasks/{}/'.format(task.pk), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_set_task_in_progress(self):
        task = TaskFactory.create(state=Task.STATES.NEW)
        response = self.client.post(
            '/api/v1/tasks/{}/set-in-progress/'.format(task.pk),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.state, Task.STATES.IN_PROGRESS)
        response = response.json()
        self.assertEqual(response['state'], 'in progress')

    def test_set_task_in_progress_wrong_task_id(self):
        task = TaskFactory.create(state=Task.STATES.NEW)
        response = self.client.post(
            '/api/v1/tasks/{}/set-in-progress/'.format(task.pk + 10000),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertEqual(task.state, Task.STATES.NEW)

    def test_set_task_done(self):
        task = TaskFactory.create(state=Task.STATES.IN_PROGRESS)
        response = self.client.post(
            '/api/v1/tasks/{}/set-done/'.format(task.pk),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.state, Task.STATES.DONE)
        response = response.json()
        self.assertEqual(response['state'], 'done')

    def test_set_task_done_wrong_task_id(self):
        task = TaskFactory.create(state=Task.STATES.NEW)
        response = self.client.post(
            '/api/v1/tasks/{}/set-done/'.format(task.pk + 10000),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertEqual(task.state, Task.STATES.NEW)
