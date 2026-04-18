from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Task

class TaskAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        response = self.client.post('/api/tasks/', {
            "title": "Test Task",
            "description": "Test Desc",
            "status": "pending",
            "assigned_to": self.user.id
        })
        self.assertEqual(response.status_code, 201)

    def test_get_tasks(self):
        Task.objects.create(
            title="Task1",
            description="Desc",
            status="pending",
            assigned_to=self.user
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        task = Task.objects.create(
            title="Old",
            description="Desc",
            status="pending",
            assigned_to=self.user
        )
        response = self.client.put(f'/api/tasks/{task.id}/', {
            "title": "Updated",
            "description": "Desc",
            "status": "completed",
            "assigned_to": self.user.id
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        task = Task.objects.create(
            title="Delete",
            description="Desc",
            status="pending",
            assigned_to=self.user
        )
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, 204)

    def test_unauthorized_access(self):
        client = APIClient()
        response = client.get('/api/tasks/')
        self.assertEqual(response.status_code, 401)